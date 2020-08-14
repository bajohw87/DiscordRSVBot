import discord
import pymongo
import datetime
import uuid
import os

#discord client
client = discord.Client()

#heroku mongodb
connection = pymongo.MongoClient('mongodb://%s:%s@cluster0-shard-00-00.hcdzj.mongodb.net:27017,cluster0-shard-00-01.hcdzj.mongodb.net:27017,cluster0-shard-00-02.hcdzj.mongodb.net:27017/MEMBER?ssl=true&replicaSet=atlas-5f3pgd-shard-0&authSource=admin&retryWrites=false&w=majority' % (os.environ["DB_USERNAME"], os.environ["DB_PASSWORD"]))
db = connection["MEMBER"]
fixCol = db["FIX_MEMBER"]
rCol = db["R_MEMBER"]
jobArr = ["전사","도적","법사","흑마","냥꾼","사제","술사","드루"]
roleArr = ["탱","딜","힐"]

#참고 DB query Result
#insert -> result.inserted_id or result.inserted_ids
#update -> result.matched_count or result.modified_count
#delete -> result.deleted_count

#로그
def findlog(id):
    return "https://ko.classic.warcraftlogs.com/character/kr/로크홀라/" + id

#장비
def findgear(id):
    return "https://wowgc.net/character/kr/로크홀라/" + id

#리셋
def findreset():
    return "http://wowreset.xyz/"

#고정 조회
def retrieveFixMember(message):
    msgArr = message.content.split(' ')
    if len(msgArr) > 2:
        if msgArr[1] == "":
            return "요일을 입력해주세요."
        if msgArr[2] == "상세":
            if fixCol.count_documents({"etc1": msgArr[1]}) == 0:
                return "등록된 명단이 없습니다."
            else:
                msg: str = ""
                for i in range(0, len(jobArr)):
                    mCnt = 0
                    mCursor = fixCol.find({"job": jobArr[i], "etc1": msgArr[1]}).sort("regdt", pymongo.ASCENDING)
                    mem: str = ""
                    for member in mCursor:
                        mCnt = mCnt+1
                        mem = mem + member["name"] + " (" + member["role"] + ")\n"
                    msg = msg + "-----" + jobArr[i] + "(" + "%d" % mCnt + ")-----\n" + mem
                msg = msg + "총 " + "%d" % (fixCol.count_documents({"etc1": msgArr[1]})) + " 명"
                for i in range(0, len(roleArr)):
                    if i == 0:
                        msg = msg + "  [ "
                    mCnt = 0
                    mCursor = fixCol.find({"role": roleArr[i], "etc1": msgArr[1]}).sort("regdt", pymongo.ASCENDING)
                    for member in mCursor:
                        mCnt = mCnt+1
                    msg = msg + roleArr[i] + "(" + "%d" % mCnt + ") "
                    if i == len(roleArr)-1:
                        msg = msg + "]"
                return msg

    if fixCol.count_documents({"etc1": msgArr[1]}) == 0:
        return "등록된 명단이 없습니다."
    else:
        mCursor = fixCol.find({"etc1": msgArr[1]}).sort("regdt", pymongo.ASCENDING)
        msg: str = ""
        for member in mCursor:
            msg = msg + member["name"] + "\n"
        msg = msg + "총 " + "%d" % (fixCol.count_documents({"etc1": msgArr[1]})) + " 명"
        return msg

#고정 등록
def registFixMember(message):
    msgArr = message.content.split(' ')
    if len(msgArr) == 5:
        if msgArr[1] == "":
            return "아이디를 입력해주세요."
        if msgArr[2] == "":
            return "직업을 입력해주세요."
        if msgArr[3] == "":
            return "역할을 입력해주세요."
        if msgArr[4] == "":
            return "요일을 입력해주세요."
        memObj = {
            "_id": uuid.uuid4(),
            "name": msgArr[1],
            "job": msgArr[2],
            "role": msgArr[3],
            "etc1": msgArr[4],
            "etc2": "",
            "regdt": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        fixCol.insert_one(memObj)
        return msgArr[1] + "님 " + msgArr[4] + "요일 고정 추가 완료"
    else:
        return "추가 실패!! 양식 확인 후 다시 추가하세요."

#고정 삭제
def deleteFixMember(message):
    msgArr = message.content.split(' ')
    if len(msgArr) == 3:
        if msgArr[1] == "":
            return "아이디를 입력해주세요."
        if msgArr[2] == "":
            return "요일을 입력해주세요."
        result = fixCol.delete_one({"name": msgArr[1], "etc1": msgArr[2]})
        if result.deleted_count > 0:
            return msgArr[1] + "님 " + msgArr[2] + "요일 고정 삭제 완료"
        else:
            return "삭제 실패!! 삭제 할 아이디가 명단에 없습니다."
    else:
        return "삭제 실패!! 양식 확인 후 다시 삭제하세요."

#예약 확인
def confirmReservationMember(message):
    msgArr = message.content.split(' ')
    if len(msgArr) == 3:
        if msgArr[1] == "":
            return "아이디를 입력해주세요."
        if msgArr[2] == "":
            return "요일을 입력해주세요."
        mCursor = rCol.find({"name": msgArr[1], "etc1": msgArr[2]}).sort("regdt", pymongo.ASCENDING)
        for member in mCursor:
            if msgArr[1].lower() == member["name"].lower():
                return msgArr[1] + "님 예약 되었습니다. 공초시간은 " + msgArr[2] + "요일 오후 10:30분 입니다!"
        return msgArr[1]+"님 예약확인 안되네요. 예약 글을 다시 남겨주세요"
    else:
        return "예약 확인 실패!! 양식 확인 후 다시 확인하세요."

#예약 조회
def retrieveReservationMember(message):
    msgArr = message.content.split(' ')
    if len(msgArr) > 2:
        if msgArr[1] == "":
            return "요일을 입력해주세요."
        if msgArr[2] == "상세":
            if rCol.count_documents({"etc1": msgArr[1]}) == 0:
                return "등록된 명단이 없습니다."
            else:
                msg: str = ""
                for i in range(0, len(jobArr)):
                    mCnt = 0
                    mCursor = rCol.find({"job": jobArr[i], "etc1": msgArr[1]}).sort("regdt", pymongo.ASCENDING)
                    mem: str = ""
                    for member in mCursor:
                        mCnt = mCnt + 1
                        mem = mem + member["name"] + " (" + member["role"] + ")\n"
                    msg = msg + "-----" + jobArr[i] + "(" + "%d" % mCnt + ")-----\n" + mem
                msg = msg + "총 " + "%d" % (rCol.count_documents({"etc1": msgArr[1]})) + " 명"
                for i in range(0, len(roleArr)):
                    if i == 0:
                        msg = msg + "  [ "
                    mCnt = 0
                    mCursor = rCol.find({"role": roleArr[i], "etc1": msgArr[1]}).sort("regdt", pymongo.ASCENDING)
                    for member in mCursor:
                        mCnt = mCnt + 1
                    msg = msg + roleArr[i] + "(" + "%d" % mCnt + ") "
                    if i == len(roleArr) - 1:
                        msg = msg + "]"
                return msg
    if rCol.count_documents({"etc1": msgArr[1]}) == 0:
        return "등록된 명단이 없습니다."
    else:
        mCursor = rCol.find({"etc1": msgArr[1]}).sort("regdt", pymongo.ASCENDING)
        msg: str = ""
        for member in mCursor:
            msg = msg + member["name"] + "\n"
        msg = msg + "총 " + "%d" % (rCol.count_documents({"etc1": msgArr[1]})) + " 명"
        return msg

#예약 등록
def registReservationMember(message):
    msgArr = message.content.split(' ')
    if len(msgArr) == 5:
        if msgArr[1] == "":
            return "아이디를 입력해주세요."
        if msgArr[2] == "":
            return "직업을 입력해주세요."
        if msgArr[3] == "":
            return "역할을 입력해주세요."
        if msgArr[4] == "":
            return "요일을 입력해주세요."
        memObj = {
            "_id": uuid.uuid4(),
            "name": msgArr[1],
            "job": msgArr[2],
            "role": msgArr[3],
            "etc1": msgArr[4],
            "etc2": "",
            "regdt": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        rCol.insert_one(memObj)
        return msgArr[1] + "님 " + msgArr[4] + "요일 예약 추가 완료"
    else:
        return "추가 실패!! 명령어 확인 후 다시 추가하세요."

#예약 삭제
def deleteReservationMember(message):
    msgArr = message.content.split(' ')
    if len(msgArr) == 3:
        if msgArr[1] == "":
            return "아이디를 입력해주세요."
        if msgArr[2] == "":
            return "요일을 입력해주세요."
        result = rCol.delete_one({"name": msgArr[1], "etc1": msgArr[2]})
        if result.deleted_count > 0:
            return msgArr[1] + "님 " + msgArr[2] + "요일 예약 삭제 완료"
        else:
            return "삭제 실패!! 삭제 할 아이디가 명단에 없습니다."
    else:
        return "예약 삭제 실패!! 양식 확인 후 다시 삭제하세요."

# 예약 초기화
def resetReservationMember(message):
    msgArr = message.content.split(' ')
    if len(msgArr) == 2:
        if msgArr[1] == "":
            return "요일을 입력해주세요."
        rCol.delete_many({"etc1": msgArr[1]})
        mCursor = fixCol.find({"etc1": msgArr[1]})
        for member in mCursor:
            memObj = {
                "_id": member["_id"],
                "name": member["name"],
                "job": member["job"],
                "role": member["role"],
                "etc1": member["etc1"],
                "etc2": member["etc2"],
                "regdt": member["regdt"]
            }
            rCol.insert_one(memObj)
        return "예약 초기화 완료. 고정 맴버 " + msgArr[1] + "요일 " + "%d" % (rCol.count_documents({"etc1": msgArr[1]})) + "  명 예약 자동 추가되었습니다."
    else:
        return "예약 삭제 실패!! 양식 확인 후 다시 삭제하세요."

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
            chkMessage = message.content.split(' ')
            if (len(chkMessage) != 2):
                return await message.channel.send("예약확인 실패!! 잘못된 명령어 입니다. 명령어 확인해주세요.")
            return await message.channel.send(confirmReservationMember(chkMessage[1]))
        if message.content.startswith("/로그"):
            chkMessage = message.content.split(' ')
            if (len(chkMessage) != 2):
                return await message.channel.send("로그조회 실패!! 잘못된 명령어 입니다. 명령어 확인해주세요.")
            return await message.channel.send(findlog(message.content[4:]))
        if message.content.startswith("/장비"):
            chkMessage = message.content.split(' ')
            if (len(chkMessage) != 2):
                return await message.channel.send("장비조회 실패!! 잘못된 명령어 입니다. 명령어 확인해주세요.")
            return await message.channel.send(findgear(message.content[4:]))
        if message.content.startswith("/리셋"):
            return await message.channel.send(findreset())
        if message.content.startswith("/봇"):
            channelid = str(message.channel.id)
            if channelid == os.environ["ADMIN_CHANNEL_ID"]:
                if message.author.id == 228518553882460171 or message.author.id == 525925078878388244:
                    return await message.channel.send("-----일반-----\n/예약확인 아이디 요일\n/로그 아이디\n/장비 아이디\n/리셋\n-----관리자봇전용 <= 채널에서만-----\n/고정추가 아이디 클래스 역할 요일\n/고정삭제 아이디 요일\n/고정명단 요일\n/고정명단 요일 상세\n/추가 아이디 클래스 역할 요일\n/삭제 아이디 요일\n/명단 요일\n/명단 요일 상세\n/초기화 요일")
            return await message.channel.send("----------\n/예약확인 아이디 요일\n/로그 아이디\n/장비 아이디\n/리셋")

        #관리자
        #print(message.author.id)
        #print(type(message.author.id)
        channelid = str(message.channel.id)
        if channelid == os.environ["ADMIN_CHANNEL_ID"]:
            if message.author.id == 228518553882460171 or message.author.id == 525925078878388244:
                chkMessage = message.content.split(' ')
                if message.content.startswith("/고정추가"):
                    if len(chkMessage) != 5:
                        return await message.channel.send("고정추가 실패!! 잘못된 명령어 입니다. 명령어 확인해주세요.")
                    return await message.channel.send(registFixMember(message))
                if message.content.startswith("/고정삭제"):
                    if len(chkMessage) != 3:
                        return await message.channel.send("고정삭제 실패!! 잘못된 명령어 입니다. 명령어 확인해주세요.")
                    return await message.channel.send(deleteFixMember(message))
                if message.content.startswith("/고정명단"):
                    if len(chkMessage) != 2:
                        if len(chkMessage) != 3:
                            return await message.channel.send("명단 조회 실패!! 잘못된 명령어 입니다. 명령어 확인해주세요.")
                    return await message.channel.send(retrieveFixMember(message))
                if message.content.startswith("/추가"):
                    if len(chkMessage) != 5:
                        return await message.channel.send("예약추가 실패!! 잘못된 명령어 입니다. 명령어 확인해주세요.")
                    return await message.channel.send(registReservationMember(message))
                if message.content.startswith("/삭제"):
                    if len(chkMessage) != 3:
                        return await message.channel.send("예약삭제 실패!! 잘못된 명령어 입니다. 명령어 확인해주세요.")
                    return await message.channel.send(deleteReservationMember(message))
                if message.content.startswith("/명단"):
                    if len(chkMessage) != 2:
                        if len(chkMessage) != 3:
                            return await message.channel.send("명단 조회 실패!! 잘못된 명령어 입니다. 명령어 확인해주세요.")
                    return await message.channel.send(retrieveReservationMember(message))
                if message.content.startswith("/초기화"):
                    if len(chkMessage) != 2:
                        return await message.channel.send("초기화 실패!! 잘못된 명령어 입니다. 명령어 확인해주세요.")
                    return await message.channel.send(resetReservationMember(message))
    except :
        return await message.channel.send("Bot Error")

client.run(os.environ["BOT_TOKEN"])
