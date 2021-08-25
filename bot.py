import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="/", description="Bot de Space Worlds")

@bot.event
async def on_ready():
    print("Le bot est en ligne.")
    await bot.change_presence(activity=discord.Game('SpaceWorlds.aternos.me'))


@bot.command()
async def ip(ctx):
    await ctx.send("SpaceWorlds.aternos.me")

@bot.command()
async def members(ctx):
    server = ctx.guild
    onlineplayer = server.member_count
    serverName = server.name
    await ctx.send(f"Il y a {onlineplayer} membres sur {serverName}")


@bot.command()
async def clear(ctx, number : int):
    msg = await ctx.channel.history(limit = number + 1).flatten()
    for message in msg:
        await message.delete()


async def createMutedRole(ctx):
    mutedRole = await ctx.guild.create_role(name="Muted", permissions=discord.Permissions(send_messages=False, speak=False), reason="Creation du role Muted pour mute des gens.")
    for channel in ctx.guild.channels:
        await channel.set_permissions(mutedRole, send_messages=False, speak=False)
    return mutedRole

async def getMutedRole(ctx):
    roles = ctx.guild.roles
    for role in roles:
        if role.name == "Muted":
            return role

    return await createMutedRole(ctx)

@bot.command()
async def mute(ctx, member: discord.Member, *, reason="Aucune raison"):
    mutedRole = await getMutedRole(ctx)
    await member.add_roles(mutedRole, reason=reason)
    embed = discord.Embed(title = "**Mute**", description = f"{member} a été mute.")
    embed.set_thumbnail(url = "https://ih1.redbubble.net/image.1819455167.1107/st,small,507x507-pad,600x600,f8f8f8.jpg")
    embed.add_field(name = "Membre mute :", value = member.name, inline = False)
    embed.add_field(name = "Raison :", value = reason, inline = False)


@bot.command()
async def unmute(ctx, member : discord.Member, *, reason = "Aucune raison"):
    mutedRole = await getMutedRole(ctx)
    await member.remove_roles(mutedRole, reason = reason)
    await ctx.send(f"{member.mention} a été unmute !")


@bot.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, user : discord.User, *reason):
    reason = " ".join(reason)
    server = ctx.guild
    serverName = server.name
    await ctx.guild.kick(user, reason = reason)
    embed = discord.Embed(title = "**Kick**", description = f"{user} a été kick !")
    embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
    embed.add_field(name = "Membre kick :", value = user.name, inline = False)
    embed.add_field(name = "Raison :", value = reason, inline = False)

@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, user : discord.User, *, reason = "Aucune raison"):
    reason = " ".join(reason)
    server = ctx.guild
    serverName = server.name
    await ctx.guild.ban(user, reason = reason)
    embed = discord.Embed(title = "**Ban**", description = f"{user} a été banni !")
    embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
    embed.set_thumbnail(url = "https://img2.freepng.fr/20180206/flq/kisspng-judge-auction-icon-auction-hammer-5a7a2fe2e7ac94.2811075015179570909489.jpg")
    embed.add_field(name = "Membre banni :", value = user.name, inline = False)
    embed.add_field(name = "Raison :", value = reason, inline = False)


@bot.command()
@commands.has_permissions(ban_members = True)
async def unban(ctx, user):
    username, userId = user.split("#")
    bannedUsers = await ctx.guild.bans()
    for i in bannedUsers:
        if i.user.name == username and i.user.discriminator == userId:
            await ctx.guild.unban(i.user)
            await ctx.send(f"{user} a été unban")
            return
    await ctx.send(f"{user} n'est pas ban, tu ne peux donc pas le deban")


@bot.command()
async def clown(ctx):
    await ctx.send("https://tenor.com/view/pennywise-hello-it-clown-gif-14167702")

@bot.command()
async def cmd(ctx):
    await ctx.send("**Voici la liste des commandes** :\n\n**/cmd** : liste des commandes du bot.\n**/ip** : ip du serveur Minecraft.\n**/members** : nombre de membres sur le discord.\n**/clear + nombre** : supprimer des messages.\n**/mute @user** : mute quelqu'un.\n**/unmute @user** : unmute quelqu'un.\n**/kick @user** : kick quelqu'un.\n**/ban @user** : ban quelqu'un.\n**/unban @user** : unban quelqu'un.")


bot.run("ODc0OTQ0MTIxMTkyNzE0MjUx.YROVNg.AwCAuRCCSAUKKjH-nzQC4BaSDPE")