# sudo apt update && sudo apt upgrade && sudo apt install ncdu ffmpeg tmux
# pip3 install ffmpeg-python telethon wget gevent requests validators
import asyncio, time, os, sys, random, shutil, requests,ffmpeg, re
import subprocess, ast, validators
from itertools import islice
import wget
from telethon import TelegramClient, events, Button, utils
from telethon.tl import types
from FastTelethon import download_file, upload_file

#from FastTelethonhelper import fast_download
#from FastTelethonhelper import fast_upload

from telethon import errors
from telethon.tl.types import ReplyInlineMarkup
from telethon.tl.types import InputBotInlineMessageText

import multiprocessing as mp

from telethon.tl.types import InputBotInlineMessageText

from enum import Enum, auto

import gevent
import hashlib
#from gevent import monkey; monkey.patch_all()

# We use a Python Enum for the state because it's a clean and easy way to do it
# Convasational
class State(Enum):
    WAIT_DIGITS = auto()
    WAIT_START = auto()
    WAIT_NAME = auto()
    WAIT_1 = auto()
    WAIT_2 = auto()

# The state in which different users are,
conversation_state = {}


# These example values won't work unless u get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
# and bot token
api_id = 6800960
api_hash = '868583386066479a0b4b801d3653dc0b'
bot_token = "5288596237:AAGyY9eUADmD-sn5uDNyVDMEjgi1HMhx1UI"


# ...code to create and setup client...
client = TelegramClient('billy', api_id, api_hash,proxy=None)
#client = TelegramClient('billy', api_id, api_hash,update_workers=2)



# Start_________________________________________________________________________________
@client.on(events.NewMessage(pattern="/start"))
async def handler(event):
    await event.respond("<i>Hi there!\nI can help you with file conversions!\nJust use /convert\nand watch me do my magick tricks.\nUse /help for more info\n!! I only support video files for Now , Don't send Anything apart from videos !!</i>.",parse_mode="html")



# Help__________________________________________________________________________________
@client.on(events.NewMessage(pattern="/help"))
async def handler(event):
    await event.respond("""<i>
Hi! I am a file converter bot.
I support 218 different file formats
and I know how to handle media of any kind
(audio files, documents, GIFs, photos, stickers, videos, voice notes, and video notes).

IMPORTANT: You can try me out for free.
If you need to convert only one file,
just go ahead and do it. However, this bot is a community project.
If you want to use this bot more often, please contribute by providing an API key:
see /contribute. This only takes A Min and it's dead simple.
You will be rewarded with 30 free extra-conversions every day.

It involves setting up an account. (Don't worry, it is free forever.) </i> """,parse_mode="html")



# Contribute____________________________________________________________________________
@client.on(events.NewMessage(pattern="/contribute"))
async def handler(event):
    await event.respond("""<i>

Welcome, future bot contributor!

By contributing to the bot, you can claim your own 30 free extra-conversions per day!
All you need to do
is to follow these three steps:

1) Create your own Billy Convert account here.
2) Visit the <a href='https://billyconvert.com'> dashboard</a> and copy the API key.
3) Get back to this chat and send /apikey. with the apikey e.g (/apikey U8EJIEIIEH82JEI ) .

Good job! Now every single operation of this bot will work based on your new
Cloud Convert account! Resetting the bot with /reset clears the API key from our
database. Once you send me your API key, I will tell you a secret /command as a thank-you gift!

</i>""",parse_mode="html")





# Location______________________________________________________________________________
@client.on(events.NewMessage(pattern="/location"))
async def call(event):
    await client.send_message(event.chat_id, 'Send Location', buttons=[
    Button.request_location('Send',resize=True, single_use=True),
    Button.request_phone('Send phone')
    ])



# Test______________________________________________________________________________
@client.on(events.NewMessage(pattern="/test"))
async def callb(event):
    await client.send_message(event.chat_id, 'Pick one from this', buttons=[
    [Button.inline('Boy',"kruz"), Button.inline('Girl',"katie")],
    [Button.url('Check this site!', 'https://lonamiwebs.github.io')]

    ])

    await client.send_message(event.chat_id, 'Welcome', buttons=[
    Button.text('Thanks!', resize=True, single_use=True) #,
#    Button.request_phone('Send phone')
    ])



# Bad words_____________________________________________________________________________
@client.on(events.NewMessage(pattern=r'(?i).*stupid'))
async def handler(event):
    h = await event.reply("<i>we don't use such word here</i>",parse_mode="html")
    await asyncio.sleep(2)
    await event.delete()
    await h.delete()


# Bad words_____________________________________________________________________________
@client.on(events.NewMessage(pattern=r'(?i).*foolish'))
async def handler(event):
    h = await event.reply("<i>we don't use such word here</i>",parse_mode="html")
    await asyncio.sleep(2)
    await event.delete()
    await h.delete()


# Bad words_____________________________________________________________________________
@client.on(events.NewMessage(pattern=r'(?i).*mad'))
async def handler(event):
    h = await event.reply("<i>we don't use such word here</i>",parse_mode="html")
    await asyncio.sleep(2)
    await event.delete()
    await h.delete()




# Get_______________________________________________________________________________
@client.on(events.NewMessage(pattern='/cancel'))
async def my_event_handler(event):
    who = event.sender_id
    state = conversation_state.get(who)
    sender = await event.get_sender()
    await event.delete()
    await event.reply(f"Process canceled by {sender.username}")
    del conversation_state[who]



# Get_______________________________________________________________________________
@client.on(events.NewMessage(pattern='/get'))
async def my_event_handler(event):
    sender = await event.get_sender()
    h = await client.download_profile_photo(sender)
    if h == None:
        return False
    else:
        if os.path.exists("profile"):
            shutil.move(str(h),"profile/" + str(h))
            await event.reply(f"i just Saved your photo {sender.username}")
            await event.respond(f"Username {sender.username} first nane {sender.first_name} Language {sender.lang_code} phone {sender.phone} Scam = {sender.scam}", file=f"profile/{h}")
            for i in os.listdir("profile/"):
                if "(1)" in i:
                    os.remove(i)
        else:
            os.mkdir("profile")





# Convert_______________________________________________________________________________
def convert(file, coder, quality):
    print(file, coder, quality)
    ran = random.randrange(1000,1500)
    global new_file
    new_file = "out" + file + ".mp4"
    def nn():
        pa = ffmpeg.input(file)
        stream = ffmpeg.output(pa,new_file,vcodec=coder,crf=quality, **{'b:v':'1000k'},acodec='mp3',preset='ultrafast')
        ffmpeg.run(stream)
        os.remove(file)
#        subprocess.Popen(f"ffmpeg -i {file} -vcodec {coder} -crf {quality} -b:v 1000k -acodec mp3 -preset ultrafast {new_file} -progress - -nostats > h ;",shell=True,stdout=subprocess.PIPE).stdout
    if __name__=='__main__':
        a1 = mp.Process(target=nn)
        a1.start()
        a1.join()


def is_downloadable(url):
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower() or 'html' in content_type.lower():
        return False
    return True



# /link______________________________________________________________________________
@client.on(events.NewMessage)
async def handler(event):
    who = event.sender_id
    state = conversation_state.get(who)
    if state is  None:
        if "/link" in event.text:
            lin = await event.respond("send me the link to the video")
            conversation_state[who] = State.WAIT_START

    if state == State.WAIT_START: # as @client.on(events.NewMessage)
        if validators.url(event.text):
            if is_downloadable(event.text) == True:
                nn = await event.respond(f"File from\n\n{event.text}\nis Downloadable âœ…")
                r = requests.get(event.text, allow_redirects=True)
                if event.text.find('/'):
                    dwn_file_name = event.text.rsplit('/', 1)[1]
                    def bar_progress(current, total, width=80):
                        global ii
                        #ii = "Downloading  %d%%" % (current / total * 100 )
                        ii = "Downloading: %d%% [%d / %d] bytes" % (current / total * 100, current, total)
                    wget.download(event.text, dwn_file_name, bar=bar_progress)
                    await nn.edit(ii)
                    await event.respond("Here is the Conveted File", file=dwn_file_name)
                    os.remove(dwn_file_name)
#_______________________________________________________________________________________
                    await event.reply(f"Download successful")
                    del conversation_state[who]
            else:
                await event.respond(f"File from\n\n{event.text}\nis not Downloadable")
                del conversation_state[who]
        else:
             await event.respond(f"This is not a correct url")
             del conversation_state[who]
        #del conversation_state[who]

class Timer:
    def __init__(self, time_between=2):
        self.start_time = time.time()
        self.time_between = time_between

    def can_send(self):
        if time.time() > (self.start_time + self.time_between):
            self.start_time = time.time()
            return True
        return False


# /Convert______________________________________________________________________________
@client.on(events.NewMessage)
async def handler(event):
    who = event.sender_id
    state = conversation_state.get(who)
    if state is  None:
        if "/convert" in event.text:
            await client.send_message(event.chat_id, 'Choose Encoder Type //', buttons=[
                Button.text('[1] > H264', resize=True, single_use=True),
                Button.text('[2] > libx265', resize=True, single_use=True),
                ])
            conversation_state[who] = State.WAIT_DIGITS
    ###################################################################################################################################################


    if state == State.WAIT_DIGITS: # as @client.on(events.NewMessage)
        if "H264" in event.text:
            digits = event.text
            global code
            code = digits
            await client.send_message(event.chat_id, f'{digits} selected\n\nEnter Quality Rate or Custom number:', buttons=[
                Button.text('18', resize=True, single_use=True),
                Button.text('28', resize=True, single_use=True),
                Button.text('38', resize=True, single_use=True)
                ])
            conversation_state[who] = State.WAIT_NAME


        if "libx265" in event.text:
            digits = event.text
            code = digits
            await client.send_message(event.chat_id, f'{digits} selected\n\nEnter Quality Rate or Custom number:', buttons=[
                Button.text('18', resize=True, single_use=True),
                Button.text('33', resize=True, single_use=True),
                Button.text('35', resize=True, single_use=True)
                ])
            #print(event.id,event.chat.id,message.chat.id)
            conversation_state[who] = State.WAIT_NAME
    ###################################################################################################################################################



    elif state == State.WAIT_NAME: # as @client.on(events.NewMessage)
        joe = event.text # quality num
        global qua
        qua = joe
        if event.text.isdigit():
            select = await client.send_message(event.chat_id, f'{joe} selected',buttons=Button.clear())
            await select.delete()
            global msg
            msg = await event.respond(f"Now send me the video file")
            conversation_state[who] = State.WAIT_1
        else:
            global nonsense
            nonsense = await event.reply(f"ðŸ¤¨    (  {event.text} )\n\nAnything other than numbers is not allowed")


    elif state == State.WAIT_1:
        try:
            await nonsense.delete()
        except NameError:
            pass

        # Printing download progress
        timer = Timer()
        async def callback(current, total):
            #ms = await event.reply(f"Downloading ")
            if timer.can_send():
                #print(f"Downloading => {file_name}\nIn {float.__floor__(current * 100 / total)}%")
                await ms.edit(f"Downloading => {file_name}\nIn {float.__floor__(current * 100 / total)}%")

        name = event.text
        sender = await event.get_sender()
        ran = random.randrange(1000,1500)
        ###################################################################################################################################################
        #h = await event.download_media(sender.username + str(ran),progress_callback=callback)
        ms = await msg.edit(f"Downloading ")
        extensions = [".mp4",".mpv",".webm",".avi",".mov",".m4v",".mpeg",".mpg",".mp2",".m4p",".ogg",".wmv",".flv",".mkv"]
        if event.file or event.document:
            print("event.file.name:  ", event.file.name)
            print("event.document:  ", event.document) # event.message.media
            file_name = None
            file_name = event.file.name if event.file.name else str(event.document.id)+'.mp4'
            print("update ", file_name)
            if file_name.lower().endswith(tuple(extensions)):

                if event.file.name == None: # using the document fuction to download (event.document.id)
                    file_name = str(event.document.id)+'.mp4'
                    with open(sender.username + file_name,'wb') as file:
                        await download_file(event.client, event.document, file, progress_callback=callback)
                    dd = await event.reply(f"Downloaded sucessfully 1")
                    await msg.delete()
                else:
                    try:                   # use normal video fuction to download  (event.file)
                        file_name = event.file.name
                        with open(sender.username + file_name, "wb") as out:
                            h = await download_file(event.client, event.document, out,progress_callback=callback)
                        dd = await event.reply(f"Downloaded sucessfully")
                        await msg.delete()
                    except errors.FloodWaitError as e: # telethon.errors.rpcerrorlist.FloodWaitError: time.sleep(900)
                        await event.respond(f"Sleeping for {e.seconds} seconds")
                        await asyncio.sleep(e.seconds)

                    global numbers_of_downloaded_file
                    numbers_of_downloaded_file = len(event.file.name.split('\n'))

                if "H264" in code:
                    await dd.edit("Converting File ...")
                    when_1 = await event.respond(f"Converting file {file_name}\nUsing H264 {qua} Encoder Please hold on ...")
                    gevent.spawn(convert(f"{sender.username}{file_name}", "h264", qua))


                   # Upload_____________________________________________________________
                    type_of = ""
                    msg = None
                    timer = Timer()
                    async def progress_bar(current, total):
                        if timer.can_send():
                            await when_1.edit(f"Uploading converted file => {float.__floor__(current * 100 / total)}%")

                    for new_file in os.listdir("."):
                        if sender.username in new_file:
                            with open(new_file, "rb") as out:
                                res = await upload_file(client, out, progress_callback=progress_bar)
                                attributes, mime_type = utils.get_attributes(
                                    new_file,
                                )
                                media = types.InputMediaUploadedDocument(
                                    file=res,
                                    mime_type=mime_type,
                                    attributes=attributes,
                                    force_file=False
                                )
                                await client.send_message(event.chat_id,file=media)

                                ff = await when_1.edit(f"Finished uploading")
                                #print(new_file[-8:]) # Last 8 str
                                os.rename(new_file,"wishfox.mp4")
                                def gofile(aa):
                                    files = {'upload_file': open("wishfox.mp4",'rb')}
                                    link = requests.post("https://store1.gofile.io/uploadFile",files=files)
                                    if link.status_code == 500:
                                        print("Gofile storage Full ", link.status_code)
                                        return False
                                    else:
                                        return link.json()
                                def anon(aa):
                                    files = {'upload_file': open("wishfox.mp4",'rb')}
                                    link = requests.post("https://api.anonfiles.com/upload",files=files)
                                    if link.status_code == 500:
                                        print("Anonfile storage Full", link.status_code)
                                        return False
                                    else:
                                        return link.json()

                                def sterea(aa):
                                    files = {'upload_file': open("wishfox.mp4",'rb')}
                                    link = requests.post("https://api.upvid.cc/upload",files=files)
                                    if link.status_code == 500:
                                        print("Anonfile storage Full", link.status_code)
                                        return False
                                    else:
                                        return link.json()
                                #def axfile(aa):
                                #    rec =  subprocess.Popen(f"curl -F file=@{aa} https://store1.gofile.io/uploadFile",shell=True, stdout=subprocess.PIPE).stdout
                                #    return ast.literal_eval(rec.read().decode())
                                #if  == False:
                                #    print("go next server")
                                #else:
                                #link = requests.post("https://store1.gofile.io/uploadFile",files=files).json()
                                #await ff.edit(f"Link <a href='{link['data']['downloadPage']}'>Link</a>",parse_mode="html")

                                #await ff.edit(f"Share <a href='{uplod('wishfox.mp4')['data']['downloadPage']}'>Link</a>",parse_mode="html")
                                os.remove("wishfox.mp4")
                                await dd.delete()
                                del conversation_state[who]


                if "libx265" in code:
                    await dd.edit("Converting File ...")
                    when_2 = await event.respond(f"Converting file {file_name}\nUsing Libx265 {qua} Encoder Please hold on ...")
                    gevent.spawn(convert(f"{sender.username}{file_name}", "libx265", qua))

                    # Upload_____________________________________________________________
                    type_of = ""
                    msg = None
                    timer = Timer()
                    async def progress_bar(current, total):
                        if timer.can_send():
                            await when_2.edit(f"Uploading converted file => {float.__floor__(current * 100 / total)}%")

                    for new_file in os.listdir("."):
                        if sender.username in new_file:
                            with open(new_file, "rb") as out:
                                res = await upload_file(client, out, progress_callback=progress_bar)
                                attributes, mime_type = utils.get_attributes(
                                    new_file,
                                )
                                media = types.InputMediaUploadedDocument(
                                    file=res,
                                    mime_type=mime_type,
                                    attributes=attributes,
                                    force_file=False
                                )
                                await client.send_message(event.chat_id,file=media)

                                ff = await when_2.edit(f"Finished uploading")
                                #print(new_file[-8:])
                                os.rename(new_file,"wishfox.mp4")

                                def gofile(aa):
                                    files = {'upload_file': open("wishfox.mp4",'rb')}
                                    link = requests.post("https://store1.gofile.io/uploadFile",files=files)
                                    if link.status_code == 500:
                                        print("Gofile storage Full ", link.status_code)
                                        return False
                                    else:
                                        return link.json()
                                def anon(aa):
                                    files = {'upload_file': open("wishfox.mp4",'rb')}
                                    link = requests.post("https://api.anonfiles.com/upload",files=files)
                                    if link.status_code == 500:
                                        print("Anonfile storage Full", link.status_code)
                                        return False
                                    else:
                                        return link.json()
                                def axfile(aa):
                                    rec =  subprocess.Popen(f"curl -F file=@{aa} https://store1.gofile.io/uploadFile",shell=True, stdout=subprocess.PIPE).stdout
                                    return ast.literal_eval(rec.read().decode())
                                #if  == False:
                                #    print("go next server")
                                #else:
                                #link = requests.post("https://store1.gofile.io/uploadFile",files=files).json()
                                #await ff.edit(f"Link <a href='{link['data']['downloadPage']}'>Link</a>",parse_mode="html")

                                #await ff.edit(f"Share <a href='{uplod('wishfox.mp4')['data']['downloadPage']}'>Link</a>",parse_mode="html")
                                os.remove("wishfox.mp4")
                                await dd.delete()
                                del conversation_state[who]

            else:
                await event.reply(f"{event.file.name}\nThis type of file is not accepted")

        else:
            await event.respond(f"No file Downloaded\nuse /convert and follow the steps carefully")
            del conversation_state[who]


 #       del conversation_state[who]



# Status________________________________________________________________________________
@client.on(events.NewMessage(pattern="/file_status"))
async def callback(event):
    sender = await event.get_sender()
    try:
        if sender.username in new_file:
            try:
                with open("h","r+") as fi:
                    for i in fi.readlines()[0:12][11:12]:
                        if i[9:] == "continue":
                            with open('h') as fin:
                                await event.respond(f"**{i}**",parse_mode="md")
                        else:
                            await event.respond(f"Finished Converting File")
                            os.remove("h")
            except FileNotFoundError:
                await event.respond(f"No on going process Use\n/convert to convert another file")
        else:
            await event.respond(f"No file found for user {sender.username}")
    except NameError:
        await event.respond(f"No file found for user <i>({sender.username})</i>",parse_mode="html")





# Check_________________________________________________________________________________
@client.on(events.NewMessage)
async def callback(event):
    if "/check" in event.text:
        sender = await event.get_sender()
#    if sender.username in numbers_of_downloaded_file:
        await event.respond(f"{sender.username} remaining convert is {10 - numbers_of_downloaded_file}")




# Note that if the download is too slow, you should consider installing cryptg
# (through pip install cryptg) so that decrypting the received data is done in C
# instead of Python (much faster).


client.start(bot_token=bot_token)
client.run_until_disconnected()
""" 
@client.on(events.NewMessage)
async def my_event_handler(event):
    start = "start"
    if start.lower() in event.raw_text:
        await event.respond('Hi! there')


#        await client.send_file('so.png')

client.start(bot_token=bot_token)
client.run_until_disconnected()

  messages = await client.get_messages('me')
  await messages[0].download_media()
"""
""" 
   print(client.download_profile_photo('me'))

   @client.on(events.NewMessage(pattern='(?i).*Hello'))
   async def handler(event):
      await event.reply('Hey!')
"""

# Message
""" 
async def handler(event):
    # Good
    chat = await event.get_chat()
    sender = await event.get_sender()
    chat_id = event.chat_id
    sender_id = event.sender_id

    # BAD. Don't do this
    chat = event.chat
    sender = event.sender
    chat_id = event.chat.id
    sender_id = event.sender.id
"""

# Upload
""" 
Sending media can be done with send_file:

client.send_file(chat, '/my/photos/me.jpg', caption="It's me!")
# or
client.send_message(chat, "It's me!", file='/my/photos/me.jpg')
You can send voice notes or round videos by setting the right arguments:

client.send_file(chat, '/my/songs/song.mp3', voice_note=True)
client.send_file(chat, '/my/videos/video.mp4', video_note=True)
You can set a JPG thumbnail for any document:

client.send_file(chat, '/my/documents/doc.txt', thumb='photo.jpg')
You can force sending images as documents:

client.send_file(chat, '/my/photos/photo.png', force_document=True)
You can send albums if you pass more than one file:

client.send_file(chat, [
    '/my/photos/holiday1.jpg',
    '/my/photos/holiday2.jpg',
    '/my/drawings/portrait.png'
])
The caption can also be a list to match the different photos.

Reusing Uploaded Files
All files you send are automatically cached, so if you do:

client.send_file(first_chat, 'document.txt')
client.send_file(second_chat, 'document.txt')
The 'document.txt' file will only be uploaded once. You can disable this behaviour
by settings allow_cache=False:

client.send_file(first_chat, 'document.txt', allow_cache=False)
client.send_file(second_chat, 'document.txt', allow_cache=False) Disabling cache
is the only way to send the same document with different attributes (for
example, you send an .ogg as a song but now you want it to show as a voice note;
you probably need to disable the cache). """
