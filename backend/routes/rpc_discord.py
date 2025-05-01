from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/rpc/discord", tags=["rpc", "discord"])

# --- payload models

class SendMessagePayload(BaseModel):
  channel_id: int
  content: str

class SummaryRequest(BaseModel):
  channel_id: int
  hours: str

# --- helpers
def get_discord_svc(request: Request):
  svc = request.app.state.discord_service
  if not svc:
    raise HTTPException(500, "Discord service not initialized")
  return svc

# --- endpoints

@router.get("/guilds")
async def list_guilds(request: Request):
  svc = get_discord_svc(request)
  return [
    {"id": g.id, "name": g.name, "member_count": g.member_count}
    for g in svc.bot.guilds
  ]

@router.post("/leave/{guild_id}")
async def leave_guild(guild_id: int, request: Request):
  svc = get_discord_svc(request)
  guild = svc.bot.get_guild(guild_id)
  if not guild:
    raise HTTPException)404, "Guild not found")
  await guild.leave()
  return {"status": "left", "guild_id": guild_id}

@router.post("/send_message")
async def send_message(payload: SendMessagePayload, request: Request):
  svc = get_discord_svc(request)
  channel = svc.bot.get_channel(payload.channel_id)
  if not channel:
    raise HTTPException(404, "Channel not found")
  await channel.send(payload.content)
  return {"status": "sent", "channel_id": payload.channel_id}

@router.post("/queue_summary")
async def queue_summary(req: SummaryRequest, request: Request):
  svc = get_discord_svc
  # the existing _summarize(ctx, channel, hours) is ctx-bound,
  # here we'll adapt it to the service - this is a stub:
  job = await svc.summary_queue.add(req.channel_id, req.hours)
  return {"status": "queued", "job_id": getattr(job, "id", None)}

@router.get("/summary_status/{job_id}")
async def summary_status(job_id: str, request: Request):
  svc = get_discord_svc(request)
  # stub: svc.summary_queue.status(job_id)
  status = svc.summary_queue.get_status(job_id)
  return {"job_id": job_id, "status": status}

