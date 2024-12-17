import asyncio

async def send_to_discord(channel, text: str, max_message_size: int = 250, delay: float = 1.0):
    start = 0
    while start < len(text):
        # Find the end of the current chunk without breaking words
        end = min(start + max_message_size, len(text))
        if end < len(text) and text[end] != ' ':
            end = text.rfind(' ', start, end)  # Adjust to the last space
            if end == -1:  # If no spaces are found, force cut at max length
                end = start + max_message_size
        
        chunk = text[start:end].strip()
        if chunk:
            await channel.send(chunk)
            await asyncio.sleep(delay)
        
        start = end