import discord
from discord.ext import commands
import math
import json
import asyncio
import os
from dotenv import load_dotenv


DEBUG = True

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
                embed = discord.Embed(title = '방송중인 스트리머', description = '현재 방송중인 스트리머 목록입니다. (%d/%d)'%(i+1, math.ceil(len(reader) / 25)), color = discord.Color.dark_green())
                for row in reader[i*25:(i+1)*25]:
                    platform, uid, name = row
                    address = ''
                    pname = ''
                    if platform == 'c' :
                        address = 'https://chzzk.naver.com/live/' + uid
                        pname = '치지직'
                    elif platform == 'a' :
                        address = 'https://play.afreecatv.com/' + uid
                        pname = '아프리카'
                    elif platform == 'y' :
                        address = 'https://www.youtube.com/channel/' + uid
                        pname = '유튜브'
                    else :
                        pass
                    embed.add_field(name = name, value = '[' + pname + '](' + address +')', inline = True)
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
            name = ' '.join(msg[2:-1])
            uid = msg[-1]
        except :
            await message.channel.send('이름과 uid를 다시 입력해주세요. 형식 : !멤버추가 [플랫폼] [이름] [uid]')
            return

        with open('./data/streamers.txt', 'r', encoding='utf-8') as f:
            reader = f.readlines()
            for row in reader:
                reader[reader.index(row)] = row.split(',')
            
            for row in reader:
                platform_, uid_, name_ = row
                if name_.strip() == name :
                    await message.channel.send('이미 추가된 스트리머입니다.')
                    return
        
        with open('./data/streamers.txt', 'a', encoding='utf-8') as f:
            f.write('%s,%s,%s\n' % (platform, uid, name))
            await message.channel.send('추가되었습니다. (%s, %s, %s)' % (platform, name, uid))

    if message.content.startswith('!안녕'):
        embed = discord.Embed(title = '안녕하세요!', description = '봇 응답 테스트', color = discord.Color.dark_green())
        await message.channel.send(embed = embed)

    if message.content.startswith('!방송인원') :
        chz = 0
        aff = 0
        etc = 0
        with open('./data/live_streamers.txt', 'r', encoding='utf-8') as f:
            reader = f.readlines()
            for row in reader:
                reader[reader.index(row)] = row.split(',')
            for i in range(len(reader)) :
                platform, uid, name = reader[i]
                if platform == 'c' :
                    chz = chz + 1
                elif platform == 'a' :
                    aff = aff + 1
                else :
                    etc = etc + 1
        embed = discord.Embed(title = '방송중인 스트리머 수', description = '전체 방송 수 : %d명'%(chz + aff + etc), color = discord.Color.dark_green())
        embed.add_field(name = '치지직', value = str(chz) + '명', inline = False)
        embed.add_field(name = '아프리카', value = str(aff) + '명', inline = False)
        embed.add_field(name = '기타', value = str(etc) + '명', inline = False)
        await message.channel.send(embed = embed)

    if message.content.startswith('!전체리스트') :
        nml = []
        with open('./data/streamers.txt', 'r', encoding='utf-8') as f:
            reader = f.readlines()
            for row in reader:
                reader[reader.index(row)] = row.split(',')

            for row in reader:
                platform, uid, name = row
                nml.append(name.strip())

        for i in range(1, math.ceil(len(nml)/30)+1) :
            embed = discord.Embed(title = '전체 스트리머', description = '전체 스트리머 목록입니다. (%d/%d)\n'%(i, math.ceil(len(nml)/30)) + ", ".join(nml[(i-1)*30:i*30]), color = discord.Color.dark_green())
            await message.channel.send(embed = embed)
            pass

    if message.content.startswith('!멤버검색') :
        msg = message.content.split(' ')
        nm = ' '.join(msg[1:])

        with open('./data/streamers.txt', 'r', encoding='utf-8') as f:
            reader = f.readlines()
            for row in reader:
                reader[reader.index(row)] = row.split(',')
            for row in reader:
                platform, uid, name = row
                if name.strip() == nm :
                    with open('./data/live_streamers.txt', 'r', encoding='utf-8') as t :
                        r = t.readlines()
                        for row in r:
                            r[r.index(row)] = row.split(',')
                        for row in r:
                            platform, uid, name = row
                            address = ''
                            if name.strip() == nm :
                                # is in the list, is live.
                                if platform == 'c' :
                                    address = 'https://chzzk.naver.com/live/' + uid
                                elif platform == 'a' :
                                    address = 'https://play.afreecatv.com/' + uid
                                elif platform == 'y' :
                                    address = 'https://www.youtube.com/channel/' + uid
                                else :
                                    pass
                                embed = discord.Embed(title = '%s 검색 결과'% nm.strip(), description = '스트리머가 리스트에 있으며 방송중입니다.\n%s'%address, color = discord.Color.dark_green())
                                await message.channel.send(embed = embed)
                                return
                        embed = discord.Embed(title = '%s 검색 결과'% nm.strip(), description = '스트리머가 리스트에 있으나 방송중이 아닙니다.', color = discord.Color.dark_green())
                        await message.channel.send(embed = embed)
                        return
            embed = discord.Embed(title = '%s 검색 결과'% nm.strip(), description = '스트리머가 리스트에 없습니다.', color = discord.Color.dark_green())
            await message.channel.send(embed = embed)

                            
                                        

                    


    if message.content.startswith('!도움') :
        embed = discord.Embed(title = '도움말', description = '사용 가능한 명령어 목록입니다.', color = discord.Color.dark_green())
        embed.add_field(name = '!안녕', value = '봇이 인사를 합니다.', inline = False)
        embed.add_field(name = '!전체리스트', value = '전체 스트리머 목록을 보여줍니다.', inline = False)
        embed.add_field(name = '!방송리스트', value = '방송중인 스트리머 목록을 보여줍니다.', inline = False)
        embed.add_field(name = '!멤버추가 [플랫폼] [이름] [uid]', value = '스트리머를 추가합니다.', inline = False)
        embed.add_field(name = '!멤버검색 [이름]', value = '스트리머를 검색합니다.', inline = False)
        embed.add_field(name = '!방송인원', value = '방송중인 스트리머 수를 보여줍니다.', inline = False)
        await message.channel.send(embed = embed)

async def update_streamers() :
    while True :
        with open('pipe.json', 'r') as file :
            content = json.load(file)
        while len(content['notification']) > 0 :
            CHL_ID = os.getenv('CHL_ID')
            #ERR_ID = os.getenv('ERR_ID')
            msg = content['notification'].pop(0)
            if '시작' in msg :
                embed = discord.Embed(title = '방송 시작', description = msg, color = discord.Color.blue())
                await client.get_channel(int(CHL_ID)).send(embed = embed)
            elif '종료' in msg :
                embed = discord.Embed(title = '방송 종료', description = msg, color = discord.Color.red())
                await client.get_channel(int(CHL_ID)).send(embed = embed)
            #elif '에러' in msg :
                #embed = discord.Embed(title = '에러 발생', description = msg, color = discord.Color.red())
                #await client.get_channel(int(ERR_ID)).send(embed = embed)
            else :
                pass
        with open('pipe.json', 'w') as file :
            json.dump(content, file)
        await asyncio.sleep(1)

#set status
@client.event
async def on_ready():
    if DEBUG :
        await client.change_presence(activity = discord.Game('[debug] 악놀2 중계 중...'))
    else :
        await client.change_presence(activity = discord.Game('악놀2 중계 중...'))

    client.loop.create_task(update_streamers())


load_dotenv(verbose=True)
cli_id = os.getenv('CLI_ID')
client.run(cli_id)