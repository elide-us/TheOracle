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
- WSGI entry point main:app uses FastAPI lifespan object for lifecycle management of both the FastAPI server and the Discord bot.
- Azure Web App needs startup command specified and the startup.sh needs to be present, this launches both the Docker container and the web app.
  - 'gunicorn -w 1 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 main:app'
  - Set the -w variable to the number of CPU in your system (e.g.: Azure App Service Basic 1 = 1 CPU)
- React frontend served from /static, packages built and deployed in CI/CD pipeline
- Build pipeline uses Vite for both development (npm start) and production (npm run build)
- Backend devstart.cmd will build React, copy, and serve the solution on FastAPI for backend testing
- Calls .env loader for local variables:
  - AZURE_BLOB_CONNECTION_STRING=""
  - AZURE_BLOB_CONTAINER_NAME=
  - DISCORD_CHANNEL=
  - DISCORD_SECRET=
  - LUMAAI_SECRET=
  - OPENAI_SECRET=

**Roadmap**:
- (Current) Working Prompt Builder POC with Frontend/Backend interactions - 80%
- Authentication (MSAL.js/MSAL) and bearer token system.
- PostgreSQL database for templates, prompts, user configuration, etc. - 5%
- Additional storage account management features.

# User Account Management:
- Users will be able to log in with various OAuth2 identity providers to access services via bearer tokens.
- Users will have their own workspace provisioned on the storage account.
- Storage Account custom domain should be implemented (elideus.net).
# Prompt Builder:
- Ability to save and recall template settings.
- User Suggestion: Ability to randomize settings.
- Front-end template data from backend API.
- Style tag system, style popup description.
- Template testing and customization.
# File Manager:
- Upload/Download/Link/Delete files from container.
- Separate containers per user.