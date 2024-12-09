from commands.text_commands import handle_text_generate

async def get_dispatcher():
    return {
        "text":{
            "generate": handle_text_generate
        },
        "image":{
            # Future handlers
        },
        # Additional commands
    }

async def parse_and_dispatch(command: str, channel, dispatcher, openai_client):
  words = command.split()
  if len(words) < 2:
     await channel.send("Invalid command format. Must include <result> <action>.")
     return
  result, action = words[0], words[1]
  args = words[2:]
  if result not in dispatcher or action not in dispatcher[result]:
     await channel.send("Unknown command: {result} {action}")
     return
  return await dispatcher[result][action](args, channel, openai_client)