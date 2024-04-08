import logging
import aiohttp
from aiohttp import ClientTimeout
import asyncio  

async def test_timeout():
    try:
        async with aiohttp.ClientSession(timeout=ClientTimeout(total=5)) as session:
            async with session.get("https://www.example.com") as response:
                print(response.status)  # Should print 200 if successful
    except aiohttp.ClientTimeoutError:
        print("Timeout Occurred")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

asyncio.run(test_timeout())