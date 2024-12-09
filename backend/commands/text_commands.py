from utils.messaging import send_to_discord

async def generate_text(prompt: str, client, channel) -> None:
    await channel.send("Sending text prompt to OpenAI.")
    completion = await client.chat.completions.create(
        model="chatgpt-4o-latest",
        max_completion_tokens=1000,
        messages=[
          {"role": "system", "content": "You are a helpful assistant."},
          {"role": "user", "content": prompt}
        ]
    )
    response_text = completion.choices[0].message.content
    await send_to_discord(channel, response_text)

async def handle_text_generate(args: str, channel, client):
    if len(args) < 1:
        await channel.send("Text generate requires a prompt.")
        return
    prompt = " ".join(args)
    return await generate_text(prompt, client, channel)
