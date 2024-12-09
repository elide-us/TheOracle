import asyncio

async def send_to_discord(channel, text: str, max_message_size: int = 250, max_line_length: int = 80, delay: float = 1.0):
  start = 0
  while start < len(text):
    end = min(start + max_message_size, len(text))
    if end < len(text) and text[end] != ' ':
      end = text.rfind(' ', start, end)
      if end == -1:
        end = start + max_message_size
    
    chunk = text[start:end].strip()

    lines = []
    while len(chunk) > max_line_length:
      line_end = chunk.rfind(' ', 0, max_line_length)
      if line_end == -1:
        line_end = max_line_length
      lines.append(chunk[:line_end].strip())
      chunk = chunk[line_end:].strip()
    lines.append(chunk)

    for line in lines:
      if line:
        await channel.send(chunk)
        await asyncio.sleep(delay)
    
    start = end