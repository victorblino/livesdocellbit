import asyncio
from functions.botFunctions import printEvent
from functions.twitchFunctions import connectEventSub, connectTwitch, verifyStreamIsOnline

async def main():
    await connectTwitch()
    hook = await connectEventSub()
    await verifyStreamIsOnline()

    printEvent(True, 'on_ready')
    try:
        await asyncio.Event().wait()
    finally:
        await hook.stop()

asyncio.run(main())
