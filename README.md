# TheOracleGPT

  An AI-powered Discord Gateway API Bot. Simple, straight-forward configuration. Accessible code-base, industry standard best-practice implementation. Robust async architecture.

**Configuration**:

- Azure Web App (Python/Linux) B1+
- GitHub Actions CI/CD Integration
- Direct Code-to-Production Pipeline
- Web App Configuration:
  - Set Always On
  - Set Startup Command
  - Configure CI/CD
  - Set Environment Variables (API tokens)
- FastAPI async Framework
- OpenAI, LumaAI, Discord, more!

**Costs**:
- B1 Azure App Service Plan (1 CPU, Always On), < $15/mo
- OpenAI API: Cost per call varies
- LumaAI APi: ~$0.30 per 5 seconds of video generation

**Technical Details**:
- WSGI entry point app:app uses FastAPI lifespan object for lifecycle management of both the FastAPI server and the Discord bot.
- Azure Web App needs startup command specified and the startup.sh needs to be present, this launches both the Docker container and the web app.
  - 'gunicorn -w 1 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 app:app'
  - Set the -w variable to the number of CPU in your system (e.g.: Azure App Service Basic 1 = 1 CPU)