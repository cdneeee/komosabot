import discord
import asyncio
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.voice_states = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

import discord
import asyncio
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.voice_states = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

TARGET_NICKNAMES = ["happyroma", "pegassi9404"]

@bot.event
async def on_ready():
    print(f"✅ Bot is ready — logged in as {bot.user}")

@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel is not None and after.self_mute:
        # Use nickname if available, otherwise username
        name_to_check = member.nick.lower() if member.nick else member.name.lower()

        if name_to_check in [n.lower() for n in TARGET_NICKNAMES]:
            print(f"⏳ {name_to_check} muted — waiting 15s...")
            await asyncio.sleep(15)

            updated_member = member.guild.get_member(member.id)
            if updated_member.voice and updated_member.voice.self_mute:
                try:
                    await updated_member.move_to(None)
                    print(f"🔨 Kicked {updated_member.name} from VC for still being muted.")
                except Exception as e:
                    print(f"❌ Failed to kick {updated_member.name}: {e}")
            else:
                print(f"✅ {member.name} unmuted before 15s passed — no action taken.")

bot.run(os.getenv("DISCORD_TOKEN"))
