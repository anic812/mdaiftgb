import re
import m3u8
import httpx
from pyrogram import Client, filters
from pyrogram.types import Message
from TelegramBot.helpers.pasting_services import katbin_paste

apple_rx = re.compile(r"apple\.com\/(\w\w)\/album\/.+\/(\d+|pl\..+)")
applemv_rx = re.compile(r"https://music\.apple\.com/(\w+)/music-video/.+\/(\d+)")


headers = {
    'origin': 'https://music.apple.com',
    'Authorization': 'Bearer eyJhbGciOiJFUzI1NiIsInR5',
}

params = {
    'extend': 'extendedAssetUrls',
}

apple_url_filter = filters.create(lambda _, __, message: bool(apple_rx.search(message.text) or applemv_rx.search(message.text)))

@Client.on_message(filters.text & filters.private & apple_url_filter)
async def apple_music_handler(client: Client, message: Message):
    if apple_rx.search(message.text):
        msgd = await message.reply_text("Processing Apple Muisc Album",quote=True)
        await amInfo(message)
        return await msgd.delete()
    elif applemv_rx.search(message.text):
        msgd = await message.reply_text("Processing Apple Muisc Video",quote=True)
        await amvInfo(message)
        return await msgd.delete()
    else:
       return await message.reply_text("`Invalid Apple Music URL provided!`",quote=True)
    

async def updateToken():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://music.apple.com/us/album/positions-deluxe-edition/1553944254")
        jspath = re.search(r"crossorigin src=\"(/assets/index.+?\.js)\"", response.text).group(1)
        my = await client.get("https://music.apple.com" + jspath)
        tkn = re.search(r"(eyJhbGc.+?)\"", my.text).group(1)
        headers['Authorization'] = f'Bearer {tkn}'

def format_duration(duration_in_millis):
    duration_in_seconds = duration_in_millis / 1000
    minutes = int(duration_in_seconds // 60)
    seconds = int(duration_in_seconds % 60)
    return f"{minutes}:{seconds:02}"


async def amInfo(message: Message):
    result = apple_rx.search(message.text)
    if not result:
        message.reply("`Improper Apple Music album URL!`")
        return
    message.reply("`Processing Apple Music Album`")
    region, id_ = result.groups()

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f'https://amp-api.music.apple.com/v1/catalog/{region}/albums/{id_}/',
            params=params,
            headers=headers
        )

        if response.status_code == 401:
            print("Updating token!")
            await updateToken()
            response = await client.get(
                f'https://amp-api.music.apple.com/v1/catalog/{region}/albums/{id_}/',
                params=params,
                headers=headers
            )

    info = response.json()['data'][0]
    release_date = info['attributes']['releaseDate']
    adm = 'True' if info['attributes']['isMasteredForItunes'] else 'False'
    url = info['attributes']['url']
    abn = info['attributes']['name']
    artist = info['attributes']['artistName']
    traits = info['attributes']['audioTraits']
    photo = info['attributes']['artwork']['url']
    w = str(info['attributes']['artwork']['width'])
    h = str(info['attributes']['artwork']['height'])
    artwork = info['attributes']['artwork']['url'].format(w=3000, h=3000)
    barcode = info['attributes']['upc']
    copyright_ = info['attributes']['copyright']  # Changed variable name to avoid using a keyword
    hls = info['relationships']['tracks']['data'][0]['attributes']['extendedAssetUrls']['enhancedHls']

    playlist = m3u8.parse(m3u8.load(hls).dumps())
    alacs = []
    for stream in playlist['playlists']:
        if stream['stream_info']['codecs'] == 'alac':
            temp = stream['stream_info']['audio'].split('-')
            sr = int(temp[-2]) / 1000
            depth = int(temp[-1])
            alacs.append((sr, depth))
    alacs.sort()

    codecs = ["Lossy AAC"]
    if 'atmos' in traits:
        codecs.append("Dolby Atmos")
    if 'lossless' in traits:
        for i, j in alacs:
            codecs.append(f"ALAC {j}-{i}")

    formatted_lines = []
    for track in response.json()['data'][0]['relationships']['tracks']['data']:
        name = track['attributes']['name']
        duration = format_duration(track['attributes']['durationInMillis'])
        formatted_line = f"{track['attributes']['trackNumber']} {name} {duration}"
        formatted_lines.append(formatted_line)
    formatted_code = "\n".join([line for line in formatted_lines])
    trkplst = katbin_paste(formatted_code)
    print(trkplst, 'ok')
    text = f"""Album : **[{abn}]({url}) | [3000x3000]({artwork})**
Artist : **{artist}**
Release Date : **{release_date}**
Codecs : **{' | '.join(codecs)}**
Barcode : **{barcode}**
Mastered for iTunes: **{adm}**
             **[Tracklist]({trkplst})**\n

{copyright_}
"""
    message.reply_photo(photo=photo.format(w=w, h=h), caption=text)


async def amvInfo(message: Message):
    result = applemv_rx.search(message.text)
    if not result:
        message.reply("`Improper Apple Music album URL!`")
        return
    message.reply("`Processing Apple Music Video`")
    region, id_ = result.groups()

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f'https://amp-api.music.apple.com/v1/catalog/{region}/music-videos/{id_}/',
            params=params,
            headers=headers
        )

        if response.status_code == 401:
            print("Updating token!")
            await updateToken()
            response = await client.get(
                f'https://amp-api.music.apple.com/v1/catalog/{region}/music-videos/{id_}/',
                headers=headers
            )

    info = response.json()['data'][0]['attributes']
    mv = info['name']
    url = info['url']
    dura = info['durationInMillis']
    fdura = f"{dura // 60000}:{dura // 1000 % 60:02}"
    photo = info['artwork']['url']
    w = str(info['artwork']['width'])
    h = str(info['artwork']['height'])
    artist = info['artistName']
    artwork = info['artwork']['url'].format(w=3000, h=3000)

    genre = ', '.join(info['genreNames'])
    hires = '🟢' if info['has4K'] else '🔴'
    hdr = '🟢' if info['hasHDR'] else '🔴'
    isrc = info['isrc']
    date = info['releaseDate']
    maxres = f"{info['previews'][0]['artwork']['width']}x{info['previews'][0]['artwork']['height']}"
    format_ = f"4K:{hires} | HDR:{hdr}"  # Changed variable name to avoid using a keyword

    text = f"""Music Video : **[{mv}]({url}) | [3000x3000]({artwork})**
Duration    : **{fdura} min**
Artist      : **{artist}**
Genre       : **{genre}**
Release Date: **{date}**
ISRC        : {isrc}
Formats     : **{format_}**
Max Resolution: **{maxres}**
"""
    message.reply_photo(photo=photo.format(w=w, h=h), caption=text)