import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from flask import Flask
from threading import Thread
import logging

logging.basicConfig(level=logging.INFO)
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

app = Flask('')

@app.route('/')
def home():
    return "✅ Bot is running."

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"<a:Verify:1382696460696555630> Logged in as {bot.user}")

@bot.command(name="clear")
@commands.has_permissions(manage_messages=True)
async def clear_messages(ctx, amount: int):
    if amount <= 0:
        await ctx.send("❌ Please provide a positive number.")
        return
    deleted = await ctx.channel.purge(limit=amount + 1)
    confirm = await ctx.send(f"<a:Verify:1382696460696555630> Deleted {len(deleted)-1} messages.")
    await confirm.delete(delay=5)

@bot.command(name="copyrole")
@commands.has_permissions(manage_roles=True)
async def copy_role(ctx, role_id: int):
    role = ctx.guild.get_role(role_id)
    if not role:
        await ctx.send("❌ Role not found in this server.")
        return
    try:
        new_role = await ctx.guild.create_role(
            name=f"{role.name} (copy)",
            permissions=role.permissions,
            colour=role.colour,
            hoist=role.hoist,
            mentionable=role.mentionable
        )
        await ctx.send(f"<a:Verify:1382696460696555630> Role copied: {new_role.mention}")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

# ثوابت الرتب
OLD_ROLE_ID = 1382389547664539740

# === أمر التحقق للذكور ===
@bot.command(name="vb")
@commands.has_permissions(manage_roles=True)
async def verify_boy(ctx, member_id: int):
    member = ctx.guild.get_member(member_id)
    if not member:
        await ctx.send("<a:11pm_exclamation:1044561523282026566> Member not found.")
        return

    role = ctx.guild.get_role(1382389524524564521)
    if not role:
        await ctx.send("<a:11pm_exclamation:1044561523282026566> 'Verified' role not found.")
        return

    old_role = ctx.guild.get_role(OLD_ROLE_ID)

    try:
        if old_role in member.roles:
            await member.remove_roles(old_role)
    except discord.Forbidden:
        await ctx.send("⚠️ I don't have permission to remove the old role.")
        return

    try:
        await member.add_roles(role)
    except discord.Forbidden:
        await ctx.send("<a:11pm_exclamation:1044561523282026566> I don't have permission to assign that role.")
        return

    try:
        dm_embed = discord.Embed(
            title="<a:Verify:1382696460696555630> You have been verified!",
            description=f"You've been verified in **{ctx.guild.name}**. Welcome!",
            color=0xa365c2
        )
        await member.send(embed=dm_embed)
    except discord.HTTPException as e:
        if e.code == 40003:
            await ctx.send("⚠️ I’m sending DMs too quickly. Please wait a moment.")
        else:
            await ctx.send("⚠️ I couldn't send a DM to this user.")

    logs_channel = bot.get_channel(1382389657878134878)
    if logs_channel:
        log_embed = discord.Embed(
            title="🔍 Verification Log (Boy)",
            description=(f"<:verificator:1382693841395781693> **Verifier:** {ctx.author.mention}\n"
                         f"<a:verify:1382693444425879554> **Verified Member:** {member.mention}"),
            color=0xa365c2
        )
        await logs_channel.send(embed=log_embed)

    await ctx.send(f"<a:Verify:1382696460696555630> {member.mention} has been verified and given the role.")

# === أمر التحقق للإناث ===
@bot.command(name="vg")
@commands.has_permissions(manage_roles=True)
async def verify_girl(ctx, member_id: int):
    member = ctx.guild.get_member(member_id)
    if not member:
        await ctx.send("<a:11pm_exclamation:1044561523282026566> Member not found.")
        return

    role = ctx.guild.get_role(1382389520661614614)
    if not role:
        await ctx.send("<a:11pm_exclamation:1044561523282026566> 'Verified Female' role not found.")
        return

    old_role = ctx.guild.get_role(OLD_ROLE_ID)

    try:
        if old_role in member.roles:
            await member.remove_roles(old_role)
    except discord.Forbidden:
        await ctx.send("⚠️ I don't have permission to remove the old role.")
        return

    try:
        await member.add_roles(role)
    except discord.Forbidden:
        await ctx.send("<a:11pm_exclamation:1044561523282026566> I don't have permission to assign that role.")
        return

    try:
        dm_embed = discord.Embed(
            title="<a:Verify:1382696460696555630> You have been verified (Female)!",
            description=f"You've been verified in **{ctx.guild.name}** as a female member. Welcome!",
            color=0xff69b4
        )
        await member.send(embed=dm_embed)
    except discord.HTTPException as e:
        if e.code == 40003:
            await ctx.send("⚠️ I’m sending DMs too quickly. Please wait a moment.")
        else:
            await ctx.send("⚠️ I couldn't send a DM to this user.")

    logs_channel = bot.get_channel(1382389657878134878)
    if logs_channel:
        log_embed = discord.Embed(
            title="🔍 Verification Log (Girl)",
            description=(f"<:verificator:1382693841395781693> **Verifier:** {ctx.author.mention}\n"
                         f"<a:verifiedfemale:1382693498784059452> **Verified Member:** {member.mention}"),
            color=0xff69b4
        )
        await logs_channel.send(embed=log_embed)

    await ctx.send(f"<a:Verify:1382696460696555630> {member.mention} has been verified as female and given the role.")

if __name__ == "__main__":
    keep_alive()
    try:
        bot.run(os.getenv("BOT_TOKEN"))
    except Exception as e:
        print(f"❌ Bot failed to run: {e}")

