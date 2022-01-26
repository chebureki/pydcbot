import os
from aiohttp import client
import discord
import time
import random
from random import randint
import re
from discord import Guild
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.environ['TOKEN']
prefix = "!"


class MyClient(discord.Client):
    async def on_ready(self):
        botchannel = client.get_channel(930845203273764975)
        print("{} online!".format(self.user))
        #await botchannel.send("{} online!".format(self.user))

    async def on_message(self, message):
        if message.content == prefix + "help":
            await message.channel.send(
                "Hier sind alle Befehle: ``` !help\n !zensur\n !purge\n !roulette\n !info (@user / Leer lassen für selbst)\n !exit\n !val (Anzahl der Spieler)```"
            )

        elif message.content == prefix + "zensur":
            await message.delete()
            await message.channel.send("Sowas gibt es hier nicht!")

        elif message.content == "Sowas gibt es hier nicht!" and message.author == client.user: # will propably not work
            time.sleep(5)
            await message.delete()

        elif message.content.startswith(prefix + "purge"):
            anzahl = message.content.split(" ")
            await message.channel.purge(limit=int(anzahl[1])+1)

        elif message.content == prefix + "roulette":
            rnd = randint(1, 6)
            if rnd == 6:
                await message.channel.send("Du bist tot!\nViel Spaß in der Hölle")
                rollen = message.author.roles
                await message.author.remove_roles(rollen, 1)
                print("rollen entfernt")
                await message.author.add_roles(rollen, 1)

            else:
                await message.channel.send("Du lebst!\nGlück gehabt!")

        elif message.content.startswith(prefix + "val"):
            befehl = message.content.split(" ")
            if int(befehl) < 6:
                for i in range(0, int(befehl[1])):
                    weapon = [
                        "Classic",
                        "Shorty",
                        "Frenzy",
                        "Ghost",
                        "Sheriff",
                        "Stinger",
                        "Spectre",
                        "Bucky",
                        "Judge",
                        "Bulldog",
                        "Guardian",
                        "Phantom",
                        "Vandal",
                        "Marshal",
                        "Operator",
                        "Ares",
                        "Odin",
                    ]
                    shield = ["Heavy", "Light", "None"]
                    x = random.randint(0, 16)
                    y = random.randint(0, 2)
                    await message.channel.send(weapon[x] + " und " + shield[y])
                    time.sleep(1)

        elif message.content == prefix + "stop" or message.content == prefix + "exit":
            botchannel = client.get_channel(930845203273764975)
            await botchannel.send("{} offline!".format(self.user))
            exit()

        elif message.content.startswith(prefix + "info"):
            try:
                if len(message.content.split(" ")) == 1:
                    date = message.author.created_at
                    date = date.strftime('%d.%m.%Y')
                    joindate = message.author.joined_at
                    joindate = joindate.strftime('%d.%m.%Y')
                    await message.channel.send("Name: {}\nErstellt am: {}\nServermitglied seit: {}\n{}".format(message.author.name, date, joindate, message.author.avatar_url))

                else:
                    person = int(
                        re.search("<@!(\d*)>", message.content).groups()[0])
                    user = await Guild.fetch_member(message.guild, person)
                    date = user.created_at
                    date = date.strftime('%d.%m.%Y')
                    joindate = user.joined_at
                    joindate = joindate.strftime('%d.%m.%Y')
                    await message.channel.send("Name: {}\nErstellt am: {}\nServermitglied seit: {}\n{}".format(user.name, date, joindate, user.avatar_url))

            except:
                user = await client.fetch_user(person)
                date = user.created_at
                date = date.strftime('%d.%m.%Y')
                await message.channel.send("Name: {}\nErstellt am: {}\n{}".format(user.name, date, user.avatar_url))

        elif message.content[0] == prefix:
            await message.channel.send("Das war kein gültiger Befehl")


client = MyClient()
client.run(TOKEN)
