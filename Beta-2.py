from pyrogram import Client, filters
from pytgcalls import PyTgCalls, idle
from pytgcalls.types import Update
from pytgcalls.types import AudioPiped
from pytgcalls.exceptions import GroupCallNotFound, AlreadyJoinedError, NoActiveGroupCall
import subprocess
from pytube import YouTube
from youtubesearchpython import VideosSearch
import asyncio
import os
from random import randint as randomNum


if not "Download" in os.listdir() :
	os.mkdir("Download")
if not "Output" in os.listdir():
	os.mkdir("Output")


api_id: int = int(25367618)
api_hash: str = str("7c434192dd12bfb05089ec2c424ff11c")
session_string: str = str("Your String Session Here")

bot = Client(name="my_account", api_id=api_id, api_hash=api_hash, session_string=session_string)

app = PyTgCalls(bot)

prefix = ""
uprefix = ["#"]

SudoUserId = [1796596300]
SUDOUSER = filters.user()
for user_id in SudoUserId :
	SUDOUSER.add(user_id)


MaxDuration = 60

def searchYt(query) :
	query = str(query)
	videosResult= VideosSearch(query, limit=1)
	Result = videosResult.result()
	title = Result["result"][0]["title"]
	duration = Result["result"][0]["duration"]
	link = Result["result"][0]["link"]
	return title, duration, link



async def autoLeave(time, chat_id):
	time = (float(time.replace(":", ".")) * 60) + 10
	await asyncio.sleep(time)
	try :
		await leave_stream(chat_id)
	except :
		pass

async def dnp(link):
	id = str(randomNum(1000, 100000))
	url = str(link)
	download_path = "Download/"
	video = YouTube(url).streams.first().download(download_path, filename='my_video')
	output_file = 'Output/song' + id + '.mp3'
	ffmpeg_command = (
	    'ffmpeg',
	    '-i', video,
	    '-vn',
	    '-c:a', 'libmp3lame',
	    '-b:a', '192k',
	    output_file
	)
	with open('/dev/null', 'w') as devnull:
	    subprocess.run(ffmpeg_command, stdout=devnull, stderr=devnull)
	os.system('rm Download/my_video && exit')
 
	return output_file



async def join_stream(chat_id, link):
	await app.join_group_call(
	   chat_id,
	   AudioPiped(
	       link,
	   )
	)
	
async def leave_stream(chat_id):
	await app.leave_group_call(
	chat_id,
	)

async def pause_stream(chat_id):
	await app.pause_stream(
	chat_id,
	)

async def resume_stream(chat_id):
	await app.resume_stream(
	chat_id,
	)
	
async def change_volume_call(chat_id, vol: int):
	await app.change_volume_call(
	chat_id,
	vol,
	)

@bot.on_message((filters.command("play", prefix) & filters.group) | (filters.command("play", uprefix)))
async def play(client, message):
	try :
		if message.text.lower().startswith("sudo") :
			text = message.text.split(" ", 3)
			chat_id = text[2]
			query = text[3]
		else :
			query = message.text.split(" ", 1)[1]
			chat_id = message.chat.id
		m = await message.reply_text("Processing Your Query...")
		title, duration, link = searchYt(query)
		if duration.count(":") > 1 :
			raise ZeroDivisionError
		await m.edit("Downloading Your Song...")
		output_file = await dnp(link)
		await m.delete()
		await join_stream(chat_id, output_file)
		os.system(f'rm {output_file} && exit')
		await message.reply_text(f"Playing Your Music\n\nTitle: {title}\n\nDuration: {duration}")
#		await autoLeave(duration, message.chat.id)
	except IndexError :
		await message.reply_text("Please Enter The Name Of Song Or Youtube Link.")
	except ZeroDivisionError :
		await m.delete()
		await message.reply_text("There is a limit of playing songs no more than length of 60 minutes")
	except GroupCallNotFound :
		await message.reply_text("Pahle vc to on karle 😂😂")
	except NoActiveGroupCall :
		await message.reply_text("Pahle vc to on karle 😂😂")
	except AlreadyJoinedError :
		await message.reply_text("Ek sath 50 gane sunega")
	except Exception as error:
		await message.reply_text(f"Error:  {error}")

@bot.on_message(filters.command("stop", prefix) & filters.group | (filters.command("stop", uprefix)))
async def stop(client, message):
	try :
		if message.text.lower().startswith("sudo") :
			chat_id = message.text.split(" ", 2)[2]
		else :
			chat_id = message.chat.id
		await leave_stream(chat_id)
		await message.reply_text("Stream Stopped 🥺🥺")
	except Exception as error :
		await message.reply_text(f"Error:  {error}")

@bot.on_message(filters.command(["pause", "mute"], prefix) & filters.group | (filters.command(["pause", "mute"], uprefix)))
async def pause(client, message):
	try :
		if message.text.lower().startswith("sudo") :
			chat_id = message.text.split(" ", 2)[2]
		else :
			chat_id = message.chat.id
		await pause_stream(chat_id)
		await message.reply_text("Stream Paused 🥺💔")
	except Exception as error :
		await message.reply_text(f"Error: {error}")


@bot.on_message(filters.command(["resume", "unmute"], prefix) & filters.group | (filters.command(["resume", "unmute"], uprefix)))
async def pause(client, message):
	try :
		if message.text.lower().startswith("sudo") :
			chat_id = message.text.split(" ", 2)[2]
		else :
			chat_id = message.chat.id
		await resume_stream(chat_id)
		await message.reply_text("Stream Resumed 😍❤️")
	except Exception as error :
		await message.reply_text(f"Error: {error}")


@bot.on_message(filters.command("volume", prefix) & filters.group | (filters.command("volume", uprefix)))
async def stop(client, message):
	try :
		if message.text.lower().startswith("sudo") :
			chat_id = message.text.split(" ", 2)[2]
			volume = int(message.text.split(" ", 3)[3])
		else :
			chat_id = message.chat.id
			volume = int(message.text.split(" ", 1)[1])
		await change_volume_call(chat_id, volume)
		await message.reply_text(f"Volume Changed To {volume}% 🎧")
	except (IndexError, ValueError) :
		await message.reply_text("Usages:- Volume (1-200)\nExample:- Volume 150")
	except NoActiveGroupCall :
		await message.send_text("How can I change my volume while I am not singing 🎤 a song 🤔")
	except Exception as error :
		await message.reply_text(f"Error:  {error}")

# 					PytgCalls Decorators 



@app.on_closed_voice_chat()
async def handler(client: PyTgCalls, chat_id: int):
	print(chat_id)

@app.on_group_call_invite()
async def handler(client: PyTgCalls, service_msg):
	print(service_msg)

@app.on_kicked()
async def handler(client: PyTgCalls, chat_id: int):
	print(chat_id)


@app.on_left()
async def handler(client: PyTgCalls, chat_id: int):
	print(chat_id)
	

@app.on_participants_change()
async def handler(client: PyTgCalls, update: Update):
	print(update)


@app.on_raw_update()
async def handler(client: PyTgCalls, update: Update):
	print(update)


@app.on_stream_end()
async def handler(client: PyTgCalls, update: Update):
	try :
		await leave_stream(update.chat_id)
	except :
		pass




if __name__ == "__main__" :
	app.start()
	os.system('clear && exit')
	print('\t\tBot Started')
	idle()
	print('Bot Stoped...\n')

