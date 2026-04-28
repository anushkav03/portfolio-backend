from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500", "http://127.0.0.1:8000", "http://127.0.0.1:8000/static/lnsm.mp3"],
    allow_credentials=True,
    allow_methods=["*"], # allows POST, GET, OPTIONS, etc
    allow_headers=["*"], # allows HTMX-specific headers
)

# state
state = {
    "is_playing": False,
    "track": "lnsm"
}
tracks = {
    "lnsm": {"file": "lnsm.mp3"},
    "risingsun": {"file": "risingsun.mp3"}
}

# routes

# get opening scene; is this even necessary?
@app.get("/", response_class=HTMLResponse)
def load_scene():
    return

# play music
@app.post("/play")
async def play_music():
    state["is_playing"] = True
    trackURL = f"http://127.0.0.1:8000/static/{state['track']}.mp3"
    content = f"""
    <div id="bridge-audio" hx-swap-oob="true">
        <script>
            console.log("trying to play music")
            if (typeof playMusic == 'function') {{
                playMusic('{trackURL}')
            }} else {{
                console.error("playMusic function not found")
            }}
        </script>
    </div>
    """
    return HTMLResponse(content=content)

# pause music
@app.post("/pause")
async def pause_music():
    state["is_playing"] = False
    content = f"""
    <div id="bridge-audio" hx-swap-oob="true">
        <script>   
            pauseMusic()
        </script>
    </div>
    """
    return HTMLResponse(content=content)

# post bc state change
@app.post("/open-popup")
async def open_popup(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="popup.html",
        context={"tracks": tracks, "state": state}
    )

@app.get("/close-popup")
def close_popup():
    return

# change track
@app.post("/music/{track}")
def choose_track(track: str):
    state["track"] = track