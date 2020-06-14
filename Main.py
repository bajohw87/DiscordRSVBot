import discord
#import pymongo
#import datetime

#discord client
client = discord.Client()

#heroku mongodb
#connection = pymongo.MongoClient('mongodb://%s:%s@ds237735.mlab.com:37735/heroku_0fj18lf0?retryWrites=false' % (os.environ["DB_USERNAME"], os.environ["DB_PASSWORD"]))
#db = connection["heroku_0fj18lf0"]
#fixCol = db["FIX_MEMBERS"]
#rCol = db["R_MEMBERS"]
#jobArr = ["전사","도적","법사","흑마","냥꾼","사제","술사","드루"]
#roleArr = ["탱","딜","힐"]

#참고 DB query Result
#insert -> result.inserted_id or result.inserted_ids
#update -> result.matched_count or result.modified_count
#delete -> result.deleted_count
@client.event
async def on_ready():
    print(client.user.id)
    print("ready")

@client.event
async def on_message(message):
                  if message.content.startswith("/초기화"):
                    return await message.channel.send("하이")



client.run(os.environ["BOT_TOKEN"])
