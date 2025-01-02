@echo on
cd ../frontend
call npm run lint
IF ERRORLEVEL 1 (
    echo "npm run build failed. Exiting."
    exit /b 1
)
call npm run build
IF ERRORLEVEL 1 (
    echo "npm run build failed. Exiting."
    exit /b 1
)
cd ..
robocopy frontend\dist backend\static /MIR
cd backend
python -m uvicorn main:app --reload
