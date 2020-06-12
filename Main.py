import discord
import os

client = discord.Client()

fixMemberStr: str = os.environ["FIX_MEMBERS"]
fixMembers = []
rMembers = []

#예약초기화
def resetreserve():
    if not fixMemberStr:
        return "예약 초기화 실패!! 고정맴버를 확인하세요."
    else:
        del rMembers[:]
        fixMembers = fixMemberStr.split("|")
        for fixMember in fixMembers:
            rMembers.append(fixMember)
        return "예약 초기화 완료!! 고정맴버만 예약 명단에 추가 되엇습니다"

#로그
def findlog(id):
    return "https://ko.classic.warcraftlogs.com/character/kr/로크홀라/" + id

#장비
def findgear(id):
    return "https://wowgc.net/character/kr/로크홀라/" + id

#리셋
def findreset():
    return "http://wowreset.xyz/"

@client.event
async def on_ready():
    print(client.user.id)
    print("ready")

@client.event
async def on_message(message):
    try:
        #사용자
        #print(message.content[6:])
        #print(message.content[10:])
        if message.content.startswith("/예약확인"):
            rYn = False
            for rMember in rMembers:
                if rMember == message.content[6:]:
                    chkMessage = message.content.split(' ')
                    if (len(chkMessage) != 2):
                        return await message.channel.send("예약확인 실패!! 잘못된 명령어 입니다. 띄어쓰기 확인해주세요.")
                    await message.channel.send(message.content[6:] + " 님 예약 되었습니다. 공초시간은 월요일 오후 10:30분 입니다!")
                    rYn = True
                    break
            if not rYn:
                await message.channel.send(message.content[6:] + " 님 예약확인 안되네요. 예약 글을 다시 남겨주세요")
        if message.content.startswith("/로그"):
            chkMessage = message.content.split(' ')
            if (len(chkMessage) != 2):
                return await message.channel.send("로그조회 실패!! 잘못된 명령어 입니다. 띄어쓰기 확인해주세요.")
            await message.channel.send(findlog(message.content[4:]))
        if message.content.startswith("/장비"):
            chkMessage = message.content.split(' ')
            if (len(chkMessage) != 2):
                return await message.channel.send("장비조회 실패!! 잘못된 명령어 입니다. 띄어쓰기 확인해주세요.")
            await message.channel.send(findgear(message.content[4:]))
        if message.content.startswith("/리셋"):
            await message.channel.send(findreset())
        if message.content.startswith("/봇"):
            if message.channel.id == 698931662553350205:
                if message.author.id == 228518553882460171 or message.author.id == 525925078878388244:
                    return await message.channel.send("-----일반-----\n/예약확인 아이디\n/로그 아이디\n/장비 아이디\n/리셋\n-----관리자 <= 채널에서만-----\n/추가 아이디\n/삭제 아이디\n/명단\n/초기화")
            await message.channel.send("----------\n/예약확인 아이디\n/로그 아이디\n/장비 아이디\n/리셋")

        #관리자
        #print(message.author.id)
        #print(type(message.author.id))
        if message.channel.id == 698931662553350205:
            if message.author.id == 228518553882460171 or message.author.id == 525925078878388244:
                if message.content.startswith("/추가"):
                    chkMessage = message.content.split(' ')
                    if(len(chkMessage) != 2):
                        return await message.channel.send("예약추가 실패!! 잘못된 명령어 입니다. 띄어쓰기 확인해주세요.")
                    rMembers.append(message.content[4:])
                    await message.channel.send(message.content[4:] + " 님 명단 추가 완료")
                if message.content.startswith("/삭제"):
                    chkMessage = message.content.split(' ')
                    if (len(chkMessage) != 2):
                        return await message.channel.send("예약취소 실패!! 잘못된 명령어 입니다. 띄어쓰기 확인해주세요.")
                    rMembers.remove(message.content[4:])
                    await message.channel.send(message.content[4:] + " 님 명단 삭제 완료")
                if message.content.startswith("/명단"):
                    if len(rMembers) > 0:
                        msg: str = ""
                        for i in range(0,len(rMembers)):
                            msg = msg+rMembers[i]
                            if i < len(rMembers):
                                msg = msg+"\n"
                        await message.channel.send(msg)
                    await message.channel.send("총 " + "%d" % (len(rMembers)) + " 명 예약확인")
                if message.content.startswith("/초기화"):
                    await message.channel.send(resetreserve())
    except :
        await message.channel.send("Bot Error")

        
client.run(os.environ["BOT_TOKEN"])
