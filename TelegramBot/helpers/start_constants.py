from TelegramBot.version import __python_version__, __version__, __pyro_version__, __System_info__


COMMAND_TEXT = """🗒️ Documentation for commands available to user's 

• /start: To Get start message and help guide. 

• /alive: To check if bot is alive or not.

• /paste: paste text in katb.in website.

• /screenshot or /ss: Generates Screenshot from video file.

• /mediainfo or /m: Generates Mediainfo of file. 

• /sample or /trim: Generates Video sample file from a video.

• /spek or /sox: Generates audio Spectogram from Telegram audio files.


**Additional Flags for screenshot and mediainfo command** :-

```
--count=10 [ Number of screenshots. Default 10, Max 20 ]\n 
--fps=10 [ Difference between two consecutive screenshots in seconds. Default 5, Max 15 ]\n
--time=01:20:10 [ Time from where the screenshots should be taken in HH:MM:SS format ]\n
--hdr [ For HDR Videos.]\n
--r [ For raw Mediainfo in document format. ]
```

"""

ABOUT_CAPTION = f"""• Running On : {__System_info__}
• Python Version : {__python_version__}
• Bot Version : {__version__}
• Pyrogram  Version : {__pyro_version__}
• Bot Source : ||**On Sale**||
"""

START_ANIMATION = "https://telegra.ph/file/c0857672b427bec8542f6.mp4"

START_CAPTION = """ Hello There! I am a Telegram Bot which can generate screenshots from video files, trim sample video files, create mediainfo for Telegram files & Direct download links and Genarates info about Apple music Albums and Music Videos.\n\nPress commands button to know more about bot commands and its usage."""
