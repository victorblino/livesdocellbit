# Imports
import threading
from functions.twitterFunctions import connectTwitter
from functions.botFunctions import printEvent
from functions.twitchFunctions import connectEventSub, connectTwitch, verifyStreamIsOnline

# Global Variables
forever = threading.Event()

# Twitch Authentication
connectTwitch()

# # Twitter Authentication
# connectTwitter()

# Connect to EventSub
hook = connectEventSub()

# Verify stream and get infos
verifyStreamIsOnline()

# Run bot
try:
    printEvent(True, 'on_ready')
    forever.wait()
except KeyboardInterrupt:
    hook.stop()
finally:
    hook.stop()
    pass
