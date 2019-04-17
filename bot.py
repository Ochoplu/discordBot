import discord
from discord.ext import commands
import asyncio
from itertools import cycle
import youtube_dl
import traceback
import sys
import translate




TOKEN = "NTYzNzIyOTQ2MjU0OTk1NDY5.XKibpQ.oC0tnWs_c8oavrrAb-2aMiDpXAQ"

command_prefix = "/"

client = commands.Bot(command_prefix = "/")
status = ["/ajuda per veure totes les comandes", "CREADOR: @Dani G.", "VERSIÓ 0.1"]
players={}
client.remove_command("repite")
queues={}

@client.event

async def on_command_error(error, ctx):

		if hasattr(ctx.command, 'on_error'):
			return
		ignored = (commands.CommandNotFound)
		error = getattr(error, 'original', error)
		if isinstance(error, ignored):
			channel=ctx.message.channel
			return await client.send_message(channel, "Aquesta comanda no existeix :x:, /ayuda per veure totes les comandes.")
		elif isinstance(error, discord.errors.ClientException):
			channel=ctx.message.channel
			return await client.send_message(channel, "Ja estic reproduint una cançó, escriu /llista <url> per afegir-la a la cua.")

		elif isinstance(error, commands.NoPrivateMessage):
			try:
				return await ctx.author.send('Este comando no se puede usar en mensajes privados')
			except:
				pass

		elif isinstance(error, commands.BadArgument):
			if ctx.command.qualified_name == 'tag list':
				return await ctx.send('No puedo encontrar ese miembro, intenta de nuevo.')

		elif isinstance(error, discord.errors.Forbidden):
			channel=ctx.message.channel
			return await client.send_message(channel, "No tengo permisos para ejecutar este comando, dame permisos de administrador :robot:")

		elif isinstance(error, commands.MissingRequiredArgument):
				channel=ctx.message.channel
				return await client.send_message(channel, "Selecciona una quantitat per a eliminar :x:")


		print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
		traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

@commands.command(name='repeat', aliases=['mimic', 'copy'])
async def do_repeat(ctx, *, inp: str):
		await ctx.send(inp)

@do_repeat.error
async def do_repeat_handler(error, ctx):
		if isinstance(error, commands.MissingRequiredArgument):
				if error.param.name == 'inp':
						await ctx.send("You forgot to give me input to repeat!")



#-------------------------------------INICIADO----------------------------------------------------------------

def check_queue(id):
	if queues[id] != []:
			player = queues[id].pop(0)
			players[id] = player
			player.start()


@client.command
async def mencionar(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    for user in message.mentions:
        msg = 'PONG {}'.format(user.mention)
        await client.send_message(message.channel, msg)

@client.event
async def on_member_join(member):           #funcion con parametro miembro
	rol = discord.utils.get(member.server.roles, name="ESTUDIANT")         #obtiene bits de info sobre el rol
	await client.add_roles(member, rol)
 # asigna al parametro miembro el parametro rol

@client.event
async def on_ready():
	print('Logeado como:')
	print(client.user.name)
	print(client.user.id)
	print('------')
	print("El bot está listoooh, vamoh a darle")


async def change_status():
	await client.wait_until_ready()        #espera que el bot se inicie
	msgs=cycle(status)                     #variable que loopea la lista stauts (mas arriba del codigo)

	while not client.is_closed:           #mientras el cliente no este cerrado
			current_status=next(msgs)         #crea variable que va pasando la lista status
			await client.change_presence(game=discord.Game(name=current_status))              #el bot juega a esa variable
			await asyncio.sleep(5)                 #el programa duerme cada 5 segundos
#----------------------------------------------SUGERENCIAS--------------------------------------------------------------

@client.command(pass_context=True)
async def sugerencia(ctx, *, output):
	channel=563720387133833216
	embedSug=discord.Embed(
	title="**Sugerencia**",
	description = "Enviada per un usuari",
	colour=0x008000,
	)

	embedSug.set_image(url="https://cdn.discordapp.com/attachments/530732415107465216/531165137013571587/x_lineverds.gif")
	embedSug.set_thumbnail(url="https://cdn.discordapp.com/attachments/564066011121319977/564066057392881704/conveni_lesheures.png")
	embedSug.set_author(name="Les Heures", icon_url="https://cdn.discordapp.com/attachments/564066011121319977/564066057392881704/conveni_lesheures.png")
	embedSug.add_field(name="Sugerencia:", value=output)

	await client.say("Sugerencia enviada :white_check_mark:")
	await client.send_message(discord.Object(id=channel),embed=embedSug)
#-------------------------------------------------HORARI-----------------------------------------------------------
@client.command(pass_context=True)
async def horari():
	await client.say("https://cdn.discordapp.com/attachments/564066011121319977/564075843350167572/unknown.png")

#--------------------------------------------TRADUCCIÓ---------------------------------
@client.command(pass_context=True)
async def translate(self, language, *text):
        """Translates text from English to specified language

        **Use double quotes for each option**

        **Dependencies**: pip install translate
                          (https://github.com/terryyin/google-translate-python)

        Keyword arguments:
        language -- Two-letter code for the languate to translate to
        text -- Text to translate.

        """
        text_to_string = ''.join(text)
        translator = Translator(to_lang=language)
        translation = translator.translate(text_to_string)

        await self.bot.say(translation)
#----------------------------------------------repite lo que pongas----------------------------------------
@client.command()
async def repiteix(*args):
	output=""                #crea variable que  contiene un texto vacio
	for word in args:   #bucle, por cada word en el parametro args:
			output+=word    #output incrementa en palabra
			output+=" "     #si hay espacios, lo mismo
	await client.say(output)      #envia output



#---------------------------------------------------eliminar mensajes-----------------------------------
@client.command(pass_context=True)
async def elimina(ctx, amount=500):

	channel=ctx.message.channel
	messages=[]                     #crea lista vacia
	async for message in client.logs_from(channel, limit=20 + 1):      #por cada mensage en .... (canal y limite es 20+1)
			messages.append(message)                                       #añade a la lista el mensaje

	await client.delete_messages(messages)                                                          #elimina los mensajes de la lista
	await client.say("Missatges eliminats")
#-----------------------------------------------embedDevs--------------------------------------------------
@client.command(pass_context=True)

async def devs(ctx):
	author=ctx.message.channel
	embedPrueba=discord.Embed(
			title="Creador",
			description="Gràcies per crear-me!",
			colour = 0x008000,
			)

	embedPrueba.set_image(url="https://cdn.discordapp.com/attachments/530732415107465216/531165137013571587/x_lineverds.gif")
	embedPrueba.set_thumbnail(url="https://cdn.discordapp.com/attachments/564066011121319977/564066057392881704/conveni_lesheures.png")
	embedPrueba.set_author(name="Les Heures", icon_url="https://cdn.discordapp.com/attachments/564066011121319977/564066057392881704/conveni_lesheures.png")
	embedPrueba.add_field(name="Creador", value="```@Dani G.```", inline=False)


	await client.send_message(author, embed=embedPrueba)

#---------------------------------------------embedAJudaMusica----------------------------------------
@client.command(pass_context=True)

async def musica(ctx):
		channel = ctx.message.channel
		embedMusica = discord.Embed(

		title="Menú d'ajuda de la música",
		colour = 0xb30000,
		)

		embedMusica.set_image(url="https://cdn.discordapp.com/attachments/530732415107465216/531165137013571587/x_lineverds.gif")
		embedMusica.set_thumbnail(url="https://cdn.discordapp.com/attachments/564066011121319977/564066057392881704/conveni_lesheures.png")
		embedMusica.set_author(name="Les Heures", icon_url="https://cdn.discordapp.com/attachments/564066011121319977/564066057392881704/conveni_lesheures.png")
		embedMusica.add_field(name="Totes les comandes", value="**/uneix**-----s'uneix al canal de veu actual'\n** /cançó <url>**-----reprodueix una cançó\n**/pausa**-----pausa la cançó\n**/resumeix**-----resumeix la cançó\n**/para**-----para la cançón\n**/llista <url>**-----afegeix a la llista la cançó\n**?seguent**-----reprodueix la següent cançó de la llista.")

		await client.send_message(channel, embed=embedMusica)
#--------------------------------------------------------embedAyuda--------------------------------------
@client.command(pass_context=True)

async def ajuda(ctx):
		channel = ctx.message.channel
		embedAyuda = discord.Embed(
		title="Menú d'ajuda",
		colour = 0xb30000,
		description="Totes les comandes"
		)

		embedAyuda.set_image(url="https://cdn.discordapp.com/attachments/530732415107465216/531165137013571587/x_lineverds.gif")
		embedAyuda.set_thumbnail(url="https://cdn.discordapp.com/attachments/564066011121319977/564066057392881704/conveni_lesheures.png")
		embedAyuda.set_author(name="Les Heures", icon_url="https://cdn.discordapp.com/attachments/564066011121319977/564066057392881704/conveni_lesheures.png")
		embedAyuda.add_field(name="ADMIN :tickets:", value="```/admin```", inline=True)
		embedAyuda.add_field(name="MÚSICA :musical_note: ", value="```/musica```", inline=True)
		await client.send_message(channel, embed=embedAyuda)
#---------------------------------------------embedINFO----------------------------------------------------------

@client.command(pass_context=True)

async def info(ctx, user : discord.Member):
	channel = ctx.message.channel

	embedInfo = discord.Embed(
	title = "**Informació de: {}**".format(user.display_name),
	colour = 0xb30000,
	)
	embedInfo.set_image(url="https://cdn.discordapp.com/attachments/530732415107465216/531165137013571587/x_lineverds.gif")
	embedInfo.set_thumbnail(url="https://cdn.discordapp.com/attachments/564066011121319977/564066057392881704/conveni_lesheures.png")
	embedInfo.set_author(name="Les Heures", icon_url="https://cdn.discordapp.com/attachments/564066011121319977/564066057392881704/conveni_lesheures.png")
	embedInfo.add_field(name="**Nom de l'usuari:**", value="```{}```".format(user.display_name), inline=True)
	embedInfo.add_field(name="**S'ha unit el:**", value="```{}```".format(user.joined_at), inline=True)
	embedInfo.add_field(name="Gràcies per unirte!", value ="{}".format(user.mention), inline=True)



	await client.send_message(channel, embed=embedInfo)


#---------------------------------------------------------------------------------------------MÚSICA---------------------------------------------------------------------------------------
@client.command(pass_context=True)

async def uneix(ctx):
	channel=ctx.message.author.voice.voice_channel
	await client.join_voice_channel(channel)
	await client.say("Afegit amb èxit! :white_check_mark:")

@client.command(pass_context=True)

async def para(ctx):
	server=ctx.message.server
	voice_client=client.voice_client_in(server)
	await voice_client.disconnect()
	await client.say("Desconectat amb èxit!  :white_check_mark:")



@client.command(pass_context=True)
async def cançó(ctx, url):
	server = ctx.message.server
	channel=ctx.message.author.voice.voice_channel
	await client.join_voice_channel(channel)
	player = await client.voice_client_in(server).create_ytdl_player(url, after = lambda: check_queue(server.id))
	players[server.id] = player
	player.start()

	await client.say("**Buscant cançó...**")
	await client.say("**Reproduïnt cançó! :robot:**")

@client.command(pass_context=True)
async def pausa(ctx):
	id = ctx.message.server.id
	players[id].pause()
	await client.say("**Pausant cançó... :robot:**")

@client.command(pass_context=True)
async def seguent(ctx):
	id = ctx.message.server.id
	players[id].stop()
	await client.say("**Seguent cançó... :robot:**")
@client.command(pass_context=True)
async def resumeix(ctx):
	id = ctx.message.server.id
	players[id].resume()
	await client.say("**Resumint cançó... :robot:**")



@client.command(pass_context=True)

async def lista(ctx, url):
	server = ctx.message.server
	voice_client = client.voice_client_in(server)
	player = await voice_client.create_ytdl_player(url, after = lambda: check_queue(server.id))
	if server.id in queues:
			queues[server.id].append(player)
	else:
			queues[server.id] = [player]

	await client.say("**Vídeo afegit a la llista** :white_check_mark: :robot: ")


#----------------------------------INICIAR BOT---------------------------------
client.loop.create_task(change_status())
client.run(TOKEN)
