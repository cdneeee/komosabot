import discord
import asyncio
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.voice_states = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

TARGET_NICKNAMES = ["cdne", "pegassi9404","happyroma", "HappyKomosa"]

@bot.event
async def on_ready():
    print(f"✅ Bot is ready — logged in as {bot.user}")

@bot.event
async def on_voice_state_update(member, before, after):
    # 1. Prevent server mute/deafen for anyone
    if not before.mute and after.mute:
        try:
            await member.edit(mute=False)
            print(f"🔊 Auto-unmuted {member.name}")
        except Exception as e:
            print(f"❌ Failed to unmute {member.name}: {e}")

    if not before.deaf and after.deaf:
        try:
            await member.edit(deafen=False)
            print(f"🎧 Auto-undeafened {member.name}")
        except Exception as e:
            print(f"❌ Failed to undeafen {member.name}: {e}")

    # 2. Kick target users if they self-deafen
    name_to_check = member.nick.lower() if member.nick else member.name.lower()
    if name_to_check in [n.lower() for n in TARGET_NICKNAMES]:
        if after.channel and after.self_deaf:
            print(f"⏳ {member.name} self-deafened — waiting 15s...")
            await asyncio.sleep(15)

            updated = member.guild.get_member(member.id)
            if updated.voice and updated.voice.self_deaf:
                try:
                    await updated.move_to(None)
                    print(f"🔨 Kicked {updated.name} for still being self-deafened.")
                except Exception as e:
                    print(f"❌ Failed to kick {updated.name}: {e}")
            else:
                print(f"✅ {member.name} undeafened before 15s — no action taken.")
                
bot.run(os.getenv("DISCORD_TOKEN"))
