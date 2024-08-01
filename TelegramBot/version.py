from sys import version_info
from pyrogram import __version__ as __pyro_version__
from platform import system, release
__major__ = 0
__minor__ = 1
__micro__ = 0


def get_version() -> str:
    return f"{__major__}.{__minor__}.{__micro__}"

__System_info__ = f"{system()} {release()}"
__python_version__ = f"{version_info[0]}.{version_info[1]}.{version_info[2]}"
__version__ = get_version()
__pyrogram_version__ = __pyro_version__
