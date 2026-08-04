# Front End

This folder contains a Streamlit frontend for the Farmer Schemes RAG backend.

## Files

- `app.py`: Streamlit app that sends user questions to the backend at `http://localhost:8000/chat`.
- `requirements.txt`: Frontend dependency list.

## Setup

From the project root:

```bash
cd /Users/deepakmohanrajamohan/pyautogui/Farmassit_ai/front\ end
/Users/deepakmohanrajamohan/pyautogui/Farmassit_ai/.venv/bin/python -m pip install -r requirements.txt
```

## Run the backend

Start the FastAPI backend first from the project root:

```bash
cd /Users/deepakmohanrajamohan/pyautogui/Farmassit_ai
/Users/deepakmohanrajamohan/pyautogui/Farmassit_ai/.venv/bin/python -m uvicorn Backend.main:app --reload --port 8000
```

## Run the frontend

Then run:

```bash
streamlit run "front end/app.py"
```

## Notes

- The frontend expects the backend to be running on `http://localhost:8000`.
- If backend or API routes change, update `front end/app.py` accordingly.
