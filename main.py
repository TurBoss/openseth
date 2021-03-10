import re
import discord

from yaml import load
from yaml import CLoader as Loader, CDumper as Dumper

from sqlalchemy import create_engine, select, and_, text
from sqlalchemy import Table, Column, Boolean, Integer, String, MetaData, Date, Time


class TurBoEventClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.bot_ready = False
        
        self.meta = MetaData()

        self.event_table = Table('events', self.meta,
                                 Column('id', Integer, primary_key = True),
                                 Column('event', Integer),
                                 Column('name', String),
                                 Column('date', Date),
                                 Column('hour', Time)
                                 )

        self.user_table = Table('users', self.meta,
                                 Column('id', Integer, primary_key = True),
                                 Column('event', Integer),
                                 Column('name', String),
                                 Column('member_id', Integer),
                                 Column('active', Boolean)
                                 )
        
        self.engine = create_engine('sqlite:///events.db')
        self.meta.create_all(self.engine)
        
        self.conn = self.engine.connect()
        
        self.message_id = 813882134250389586
        

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
                ins = self.event_table.insert().values(event=int(message_id),
                                               name=data[0],
                                               date=data[1],
                                               hour=data[2],
                                               active=True)
                result = self.conn.execute(ins)
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
        
        s = self.user_table.select().where(
            and_(
                text("member_id == :user_id"),
                text("active == 1")
            )
        )
        
        result = self.conn.execute(s, user_id=payload.user_id).fetchall()
        
        print(result)
        
        if result:
            print("User {} already registered".format(member))
            return
        print("Register user {} for event {}".format(member, message_id))
        
        ins = self.user_table.insert().values(event=int(message_id),
                                               name=str(member),
                                               member_id=str(user_id),
                                               active=True)
        result = self.conn.execute(ins)

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
        
        result = self.conn.execute(s, user_id=user_id).fetchall()
        
        if not result:
            print("User {} not registered".format(member))
            return
        
        stmt = self.user_table.update().where(text("member_id == :user_id")).values(active=False)
        
        self.conn.execute(stmt, user_id=user_id)
        
        print("Remove notification for user_id {}".format(user_id))
        

        
# This bot requires the members and reactions intents.
intents = discord.Intents.default()
intents.members = True

with open("config.yml") as f:
    config = load(f.read(), Loader=Loader)

token = config["bot"]["token"]

client = TurBoEventClient(intents=intents)
client.run(token)
