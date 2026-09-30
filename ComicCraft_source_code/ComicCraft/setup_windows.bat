@echo off
echo Creating ComicCraft virtual environment...
py -m venv .venv
call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
echo.
echo Setup complete.
echo Copy .env.example to .env, add your GEMINI_API_KEY, then run:
echo uvicorn app.main:app --reload
pause
