import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import google.generativeai as genai

GOOGLE_API_KEY = "AQ.Ab8RNGK4zX59oVVe6-Vqf_252fIamKgigCOAX-6TEqTH9wcdbw"
genai.configure(api_key=GOOGLE_API_KEY)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
model = genai.GenerativeModel('gemini-1.5-flash')

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate", response_class=HTMLResponse)
async def generate(request: Request, topic: str = Form(...), qtype: str = Form(...)):
    prompt = f"Create a {qtype} question about {topic} for a student. Provide question and answer clearly."
    response = model.generate_content(prompt)
    return templates.TemplateResponse("index.html", {"request": request, "result": response.text, "topic": topic})
