from fastapi import FastAPI, UploadFile, Form
from models import problem1_logic, problem2_logic, problem3_logic, problem4_logic, problem5_logic

app = FastAPI()

@app.post("/problem1")
def run_problem1(data: dict):
    return problem1_logic(data)

@app.post("/problem2")
def run_problem2(file: UploadFile, param: str = Form(...)):
    file_bytes = file.file.read()
    return problem2_logic(file_bytes, param)

@app.post("/problem3")
def run_problem3(text: str = Form(...), k: int = Form(...)):
    return problem3_logic(text, k)

@app.post("/problem4")
def run_problem4(data: dict):
    return problem4_logic(data)

@app.post("/problem5")
def run_problem5(file: UploadFile = None, text: str = Form("")):
    file_bytes = file.file.read() if file else None
    return problem5_logic(file_bytes, text)
