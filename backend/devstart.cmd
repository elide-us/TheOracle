@echo on
cd ../frontend
call npm run build
IF ERRORLEVEL 1 (
    echo "npm run build failed. Exiting."
    exit /b 1
)
cd ..
robocopy frontend\dist backend\static /MIR
IF ERRORLEVEL 1 (
    echo "robocopy failed. Exiting."
    exit /b 1
)
cd backend
python -m uvicorn main:app --reload