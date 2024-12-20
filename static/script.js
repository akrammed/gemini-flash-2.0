const video = document.getElementById("video");
const startButton = document.getElementById("start");
const responseElement = document.getElementById("response");

// Access the webcam and display video
navigator.mediaDevices
  .getUserMedia({ video: true })
  .then((stream) => {
    video.srcObject = stream;
  })
  .catch((error) => {
    console.error("Error accessing webcam:", error);
  });

// WebSocket connection
let socket;

startButton.addEventListener("click", () => {
  socket = new WebSocket("ws://localhost:8000/video-stream");

  socket.onopen = () => {
    console.log("WebSocket connected!");
    startSendingFrames();
  };

  socket.onmessage = (event) => {
    responseElement.textContent = `Gemini Response: ${event.data}`;
  };

  socket.onerror = (error) => {
    console.error("WebSocket error:", error);
  };

  socket.onclose = () => {
    console.log("WebSocket closed.");
  };
});

// Send video frames to the WebSocket server
function startSendingFrames() {
  const canvas = document.createElement("canvas");
  const context = canvas.getContext("2d");

  setInterval(() => {
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    canvas.toBlob((blob) => {
      if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(blob);
      }
    });
  }, 100);
}
