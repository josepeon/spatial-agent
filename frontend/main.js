


const webcamElement = document.getElementById("webcam");
const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");
const statusEl = document.getElementById("status");
const responseText = document.getElementById("responseText");
const audioPlayback = document.getElementById("audioPlayback");

let mediaRecorder;
let audioChunks = [];
let socket;

// Initialize webcam
navigator.mediaDevices.getUserMedia({ video: true, audio: true })
  .then(stream => {
    webcamElement.srcObject = stream;
  })
  .catch(err => {
    console.error("Failed to access media devices:", err);
  });

// Set up WebSocket
socket = new WebSocket("ws://localhost:8000/ws");

socket.onopen = () => {
  console.log("WebSocket connected");
};

socket.onmessage = (event) => {
  const data = JSON.parse(event.data);

  // Create and append message container
  const chatBox = document.getElementById("chatBox") || (() => {
    const box = document.createElement("div");
    box.id = "chatBox";
    document.body.appendChild(box);
    return box;
  })();

  const userMsg = document.createElement("div");
  userMsg.innerText = `You: [your question here]`; // Replace dynamically if needed
  userMsg.style.margin = "10px 0";

  const agentMsg = document.createElement("div");
  agentMsg.innerText = `Agent: ${data.text}`;
  agentMsg.style.margin = "10px 0";

  chatBox.appendChild(userMsg);
  chatBox.appendChild(agentMsg);

  const audioBlob = base64ToBlob(data.audio_base64, "audio/wav");
  audioPlayback.src = URL.createObjectURL(audioBlob);
  audioPlayback.play();
  statusEl.innerText = "Status: Response received";
};

startBtn.onclick = () => {
  audioChunks = [];
  statusEl.innerText = "Status: Recording...";
  startBtn.disabled = true;
  stopBtn.disabled = false;

  navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.start();

    mediaRecorder.ondataavailable = event => {
      audioChunks.push(event.data);
    };
  });
};

stopBtn.onclick = () => {
  statusEl.innerText = "Status: Sending audio...";
  startBtn.disabled = false;
  stopBtn.disabled = true;

  mediaRecorder.stop();
  mediaRecorder.onstop = () => {
    const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
    const reader = new FileReader();
    reader.onloadend = () => {
      const base64Audio = reader.result.split(",")[1];
      socket.send(JSON.stringify({ audio_base64: base64Audio }));
    };
    reader.readAsDataURL(audioBlob);
  };
};

function base64ToBlob(base64, mime) {
  const binary = atob(base64);
  const array = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) {
    array[i] = binary.charCodeAt(i);
  }
  return new Blob([array], { type: mime });
}