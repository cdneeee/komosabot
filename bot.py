import discord
import asyncio
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.voice_states = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
active_deaf_timers = {}

@bot.event
async def on_ready():
    print(f"✅ Bot is ready — logged in as {bot.user}")

@bot.event
async def on_voice_state_update(member, before, after):
    user_id = member.id

    # 1. Auto-unmute/deafen if server did it
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

    # 2. If user self-deafens, start or restart timer
    if after.channel and after.self_mute and not before.self_mute:
        # If already has a timer, cancel it first
        if user_id in active_deaf_timers:
            active_deaf_timers[user_id].cancel()

        print(f"⏳ {member.name} self-deafened — starting 20 min timer")
        task = asyncio.create_task(handle_self_deafen(member))
        active_deaf_timers[user_id] = task

    # 3. If user undeafens early, cancel the timer
    if before.self_mute and not after.self_mute:
        if user_id in active_deaf_timers:
            active_deaf_timers[user_id].cancel()
            del active_deaf_timers[user_id]
            print(f"✅ {member.name} unmuted early — timer canceled")

async def handle_self_deafen(member):
    try:
        await asyncio.sleep(20 * 60)  # 20 minutes
        updated = member.guild.get_member(member.id)

        if updated.voice and updated.voice.self_mute:
            try:
                await updated.move_to(None)
                print(f"🔨 Kicked {updated.name} from VC for staying self-muted.")
            except Exception as e:
                print(f"❌ Could not kick {updated.name}: {e}")
        else:
            print(f"✅ {updated.name} unmuted before 20 mins — no action")

    except asyncio.CancelledError:
        # Task was cancelled (undeafened or re-triggered)
        print(f"⚠️ Timer cancelled for {member.name}")
    finally:
        # Cleanup
        active_deaf_timers.pop(member.id, None)

bot.run(os.getenv("DISCORD_TOKEN"))
