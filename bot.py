import discord
from discord.ext import commands
import math
import json
import asyncio
import os
from dotenv import load_dotenv

#sets prefix and loads intents
client = commands.Bot(command_prefix = "!", intents = discord.Intents.all())


#on ready message log in terminal
@client.event
async def on_ready():
    print('bot online')    


#hello command which btw is the only one that works rn
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('!중계만들기') :
        pass

    if message.content.startswith('!방송리스트'):
        with open('./data/live_streamers.txt', 'r', encoding='utf-8') as f:
            #await message.channel.send(f.read())
            reader = f.readlines()
            for row in reader:
                reader[reader.index(row)] = row.split(',')
            for i in range(0, math.ceil(len(reader) / 25)) :
                embed = discord.Embed(title = '방송중인 스트리머', description = '현재 방송중인 스트리머 목록입니다. (%d/%d)'%(i+1, math.ceil(len(reader) / 25)), color = discord.Color.red())
                for row in reader[i*25:(i+1)*25]:
                    platform, uid, name = row
                    address = ''
                    if platform == 'c' :
                        address = 'https://chzzk.naver.com/live/' + uid
                    elif platform == 'a' :
                        address = 'https://play.afreecatv.com/' + uid
                    elif platform == 'y' :
                        address = 'https://www.youtube.com/channel/' + uid
                    else :
                        pass
                    embed.add_field(name = name, value = address, inline = False)
                    #await message.channel.send(row)

                await message.channel.send(embed = embed)
            

    if message.content.startswith('!멤버추가') :
        msg = message.content.split(' ')
        try :
            if msg[1] == '치지직' or msg[1] == 'c' or msg[1] == 'ㅊ' :
                platform = 'c'
            elif msg[1] == '아프리카' or msg[1] == 'a' or msg[1] == 'ㅇ' :
                platform = 'a'
            elif msg[1] == '유튜브' or msg[1] == 'y' or msg[1] == '유' :
                platform = 'y'
            else :
                await message.channel.send('플랫폼을 다시 입력해주세요. 형식 : !멤버추가 [플랫폼] [이름] [uid]')
                return
        except :
            await message.channel.send('플랫폼을 다시 입력해주세요. 형식 : !멤버추가 [플랫폼] [이름] [uid]')
            return
        try :
            name = msg[2]
            uid = msg[3]
        except :
            await message.channel.send('이름과 uid를 다시 입력해주세요. 형식 : !멤버추가 [플랫폼] [이름] [uid]')
            return


        with open('./data/streamers.txt', 'a', encoding='utf-8') as f:
            f.write('%s,%s,%s\n' % (platform, uid, name))
            await message.channel.send('추가되었습니다. (%s, %s ,%s)' % (platform, name, uid))

    if message.content.startswith('!안녕'):
        await message.channel.send('안녕하세요!')


async def update_streamers() :
    while True :
        with open('pipe.json', 'r') as file :
            content = json.load(file)
        while len(content['notification']) > 0 :
            CHL_ID = os.getenv('CHANNEL_ID')
            await client.get_channel(int(CHL_ID)).send(content['notification'].pop(0))
        with open('pipe.json', 'w') as file :
            json.dump(content, file)
        await asyncio.sleep(1)

#set status
@client.event
async def on_ready():
    await client.change_presence(activity = discord.Game('being useless'))
    client.loop.create_task(update_streamers())


load_dotenv(verbose=True)
cli_id = os.getenv('CLIENT_ID')
client.run(cli_id)