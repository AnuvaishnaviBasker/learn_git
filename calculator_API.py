from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Union
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="Calculator API",
    description="A simple calculator API that performs basic arithmetic operations built with FastAPI.",
    version="1.0.0"
)

class CalculationRequest(BaseModel):
    num1: float
    num2: float
    operation: str = Query(..., description="Choose: add, subtract, multiply, divide")

class CalculationResponse(BaseModel):
    num1: float
    num2: float
    operation: str
    result: float
    message: str = "Calculation Successful"

@app.get("/",response_class=HTMLResponse)
def home():
    return """
    <h1>Calculator API is running</h1>
    <p>Go to <a href="/docs">docs</a> to test the calculator interactively.</p>
    """

@app.post("/calculate", response_model=CalculationResponse)
def calculate(data: CalculationRequest):
    num1 = data.num1
    num2 = data.num2
    op = data.operation.lower()

    if op == "add":
        result = num1 + num2
        message = f"{num1} + {num2} = {result}"
    elif op == "subtract":
        result = num1 - num2
        message = f"{num1} - {num2} = {result}"
    elif op == "multiply":
        result = num1 * num2
        message = f"{num1} * {num2} = {result}"
    elif op == "divide":
        if num2 == 0:
            raise HTTPException(status_code=400, detail="Denominator cannot be zero")
        result = num1 / num2
        message = f"{num1} / {num2} = {result}"
    else:
        raise HTTPException(status_code=400, detail="Invalid operation")

    return CalculationResponse(
        num1=num1,
        num2=num2,
        operation=data.operation,
        result=result,
        message=message
    )

@app.get("/add")
def add(a:float, b:float):
    return {"result": a+b}

@app.get("/subtract")
def subtract(a:float, b:float):
    return {"result": a-b}

@app.get("/multiply")
def multiply(a:float, b:float):
    return {"result": a*b}

@app.get("/divide")
def divide(a:float, b:float):
    if b == 0:
        raise HTTPException(status_code=400, detail="Denominator cannot be zero")
    return {"result": a/b}

calculations_history = []

@app.post("/calculate")
def calculate_with_history(data: CalculationRequest):
    result = calculate(data)
    calculations_history.append(result.model_dump())
    return result

@app.get("/history")
def get_history():
    return {
        "total_calculations": len(calculations_history),
        "history":calculations_history[-10:]
    }