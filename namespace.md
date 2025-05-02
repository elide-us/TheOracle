# --- GUILDS ---
## List all guilds the bot is in
GET    /rpc/discord/guilds/list

## Leave a specific guild
POST   /rpc/discord/guilds/leave/{guild_id}

# --- CHANNELS ---
## Send a message to a specific channel
POST   /rpc/discord/channels/send_message

## Upload a file to a channel
POST   /rpc/discord/channels/upload_file

## Queue a summary job for a specific channel
POST   /rpc/discord/channels/queue_summary

## Check the status of a summary job
GET    /rpc/discord/channels/summary_status/{job_id}

## List messages in a channel
GET    /rpc/discord/channels/list_messages

# --- USERS ---
## Send a direct message to the user who made the request
POST   /rpc/discord/users/send_message
