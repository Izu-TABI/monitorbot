import discord
import os
from datetime import datetime, timedelta
from server import keep_alive

client=discord.Client(intents=discord.Intents.all())


LOG_CH_ID = int(os.environ['LOG_CHANNEL'])
GUILD_ID = int(os.environ['GUILD_ID'])


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$hello'):
    await message.channel.send('Hello')
  
@client.event
async def on_voice_state_update(member, before, after) :
  now = datetime.utcnow() + timedelta(hours=9)
  
  if member.guild.id == GUILD_ID and (before.channel != after.channel):
    if before.channel is None:
      msg = f'{now:%m/%d-%H:%M} **{member.name}**が<#{after.channel.id}>に参加しました。'
      await client.get_channel(LOG_CH_ID).send(msg)
      
    elif after.channel is None:
      msg = f'{now:%m/%d-%H:%M} **{member.name}**が<#{before.channel.id}>から退出しました。'
      await client.get_channel(LOG_CH_ID).send(msg)
    else:
      msg = f'{now:%m/%d-%H:%M} **{member.name}**が<#{before.channel.id}>から<#{after.channel.id}>へ移動しました。'
      await client.get_channel(LOG_CH_ID).send(msg)
    

@client.event
async def on_member_join(member):
  await client.get_channel(LOG_CH_ID).send(f'<@{member.id}>がサーバーに参加しました。自己紹介してください。')

keep_alive()
client.run(os.getenv('TOKEN'))
