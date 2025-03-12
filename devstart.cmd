@ECHO OFF
CD ./frontend
CALL npm ci
IF ERRORLEVEL 1 (
    ECHO "npm run build failed. Exiting."
    EXIT /b 1
)
CALL npm run lint
IF ERRORLEVEL 1 (
    ECHO "npm run build failed. Exiting."
    EXIT /b 1
)
CALL npm run build
IF ERRORLEVEL 1 (
    ECHO "npm run build failed. Exiting."
    EXIT /b 1
)
CD ..
robocopy frontend\dist backend\static /MIR
CD backend
python -m uvicorn main:app --reload
cd ..