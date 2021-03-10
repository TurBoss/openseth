import re
import discord

from yaml import load
from yaml import CLoader as Loader, CDumper as Dumper


class OpenSethClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.bot_ready = False
        
        self.message_id = 819329888695615528
        

    async def on_ready(self):
        self.bot_ready = True
        print('Logged in as {} id {}'.format(self.user.name, self.user.id))


    async def on_message(self, message):
        if not self.bot_ready:
            return
        
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith('!notify'):
            await message.reply('Would you like to notify about an event?\nPlease enter event from list:', mention_author=True)
            
        elif message.content.startswith('!create'):
            data = re.findall('"([^"]*)"', message.content)
            if len(data) == 3:
                await message.reply('New event created: {} on {} at {}'.format(data[0], data[1], data[2]), mention_author=True)
        
        elif message.content.startswith('!help'):
            await message.reply('Create a new event\nExample: "!create "World Event" "31/03/2021" "18:30"', mention_author=True)


    async def on_raw_reaction_add(self, payload):
        if not self.bot_ready:
            return
        
        message_id = payload.message_id
        member = payload.member
        user_id = payload.user_id
        
        if message_id != self.message_id:
            return
        
    async def on_raw_reaction_remove(self, payload):
        if not self.bot_ready:
            return
        
        message_id = payload.message_id
        member = payload.member
        user_id = payload.user_id
        
        if message_id != self.message_id:
            return
        
        s = self.user_table.select().where(
            and_(
                text("member_id == :user_id"),
                text("active == 1")
            )
        )
        
        print("Remove notification for user_id {}".format(user_id))


# This bot requires the members and reactions intents.
intents = discord.Intents.default()
intents.members = True

with open("config.yml") as f:
    config = load(f.read(), Loader=Loader)

token = config["bot"]["token"]

client = OpenSethClient(intents=intents)
client.run(token)
