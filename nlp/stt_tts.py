import asyncio
from lmnt.api import Speech
from openai import AsyncOpenAI

DEFAULT_PROMPT = 'Read me the text of a short sci-fi story in the public domain.'
VOICE_ID = 'lily'
LMNT_API_KEY = '2b4e75c1e1b34aa287a78152394e316e'  # Replace with your actual LMNT API key
OPENAI_API_KEY = 'x'

async def main():
  async with Speech(LMNT_API_KEY) as speech:
    connection = await speech.synthesize_streaming(VOICE_ID)
    t1 = asyncio.create_task(reader_task(connection))
    t2 = asyncio.create_task(writer_task(connection))
    await asyncio.gather(t1, t2)


async def reader_task(connection):
  """Streams audio data from LMNT and writes it to `output.mp3`."""
  with open('output.mp3', 'wb') as f:
    async for message in connection:
      f.write(message['audio'])


async def writer_task(connection):
    """Streams text from ChatGPT to LMNT."""
    client = AsyncOpenAI(api_key=OPENAI_API_KEY)
    response = await client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': DEFAULT_PROMPT}],
        stream=True)

    async for chunk in response:
        if (not chunk.choices[0] or
            not chunk.choices[0].delta or
            not chunk.choices[0].delta.content):
          continue
        content = chunk.choices[0].delta.content
        await connection.append_text(content)
        print(content, end='', flush=True)

    # After `finish` is called, the server will close the connection
    # when it has finished synthesizing.
    await connection.finish()


asyncio.run(main())
