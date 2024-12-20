from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from google import genai  

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Use Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Initialize Gemini client
api_key = "AIzaSyDjC5DNEpyJtCxziKK8_IwfifXsyD1qTlk"
client = genai.Client(api_key=api_key)

@app.get("/", response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/video-stream")
async def video_stream(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket connection accepted for video stream.")
    
    try:
        while True:
            # Receive video frame from the WebSocket
            data = await websocket.receive_bytes()

            # Process the frame using Gemini API (pseudo-code)
            response = client.models.generate_content(
                model="gemini-2.0-flash-exp", 
                contents="Process this video frame"
            )
            print("Gemini Response:", response.text)

            await websocket.send_text(response.text)

    except Exception as e:
        print("WebSocket error:", e)
    finally:
        await websocket.close()
