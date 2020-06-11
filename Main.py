import discord
import os

client = discord.Client()

fixMemberStr = ""
fixMembers = []
rmembers = []

@client.event
async def on_ready():
    print(client.user.id)
    print("ready")

@client.event
async def on_message(message):
    print(message.content[6:])
    print(message.content[10:])

    if message.content.startswith("/예약확인"):
        rYn = False
        for rmember in rmembers:
            if rmember == message.content[6:]:
                chkMessage = message.content.split(' ')
                if (len(chkMessage) != 2):
                    return await message.channel.send("예약추가 실패!! 잘못된 명령어 입니다. 띄어쓰기 확인해주세요.")
                await message.channel.send(message.content[6:] + " 님 예약 되었습니다. 공초시간은 월요일 오후 10:30분 입니다!")
                rYn = True
                break
        if not rYn:
            await message.channel.send(message.content[6:] + " 님 예약확인 안되네요. 다시 예약 글 남겨주세요")

    print(message.author.id)
    print(type(message.author.id))
    if message.author.id == 228518553882460171 or message.author.id == 525925078878388244:
        if message.content.startswith("/1005관리자"):
            await message.channel.send("----일반 명령어----\n/예약확인 아이디")
            await message.channel.send("----관리자 명령어----\n/1005예약추가 아이디\n/1005예약취소 아이디\n/1005예약확인")
        if message.content.startswith("/1005예약추가"):
            chkMessage = message.content.split(' ')
            if(len(chkMessage) != 2):
                return await message.channel.send("예약추가 실패!! 잘못된 명령어 입니다. 띄어쓰기 확인해주세요.")
            rmembers.append(message.content[10:])
            await message.channel.send(message.content[10:] + " 님 명단 추가 완료")
        if message.content.startswith("/1005예약취소"):
            chkMessage = message.content.split(' ')
            if (len(chkMessage) != 2):
                return await message.channel.send("예약취소 실패!! 잘못된 명령어 입니다. 띄어쓰기 확인해주세요.")
            rmembers.remove(message.content[10:])
            await message.channel.send(message.content[10:] + " 님 명단 삭제 완료")
        if message.content.startswith("/1005예약확인"):
            cnt = len(rmembers)
            await message.channel.send(rmembers)
            await message.channel.send("총 " + "%d" % (len(rmembers)) + " 명 예약확인")


access_token = os.environ("BOT_TOKEN")
client.run(access_token)
