import os
import discord
import pandas as pd
from replit import db
from keep import keep_alive



sheet_id = str(os.environ['sh_id'])
intent=discord.Intents.default()
intent.members=True
client = discord.Client(intents=intent)


@client.event
async def on_ready():
	print("We have logged in as {0.user}".format(client))

@client.event
async def on_member_join(member):

	await member.send("Hello! Welcome to the oficial discord server of Robotics Club of Brac University(ROBU). I am your helping buddy. If you are a member of ROBU please send me your student id so that I can give you your roles. For example: If your ID is 21212121 then you simply write \n!reg 21212121 and press send. If you are here for the recruitment or for any other reason then you dont need to do anything.")

@client.event
async def on_message(message):
	if message.author.bot:
		return
	if message.content.startswith("!") or message.content.startswith("*"):
		df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")
		server_id = int(os.environ["server_id"])
		print(server_id)
		print(type(server_id))
		server = client.get_guild(server_id)
		server_ch=server.channels
		if message.channel not in server_ch:
			member = server.get_member(message.author.id)
			print(message.author.id)
			auth_id=str(message.author.id)
		
			msg = message.content[1:]
			# if msg.upper()=="DADS":
			# 	d=df[df["Designation"]=="Director"]
			# 	ad=df[df["Designation"]=="Assistant Director"]
			# 	s=df[df["Designation"]=="Secretary"]
			# 	frames=[d, ad, s]
			# 	dads=pd.concat(frames)
			# 	for i in range(dads.shape[0]):
			# 		name=dads.iloc[i][0]
			# 		designation=dads.iloc[i][2]
			# 		mail=dads.iloc[i][4]
			# 		line=name+", "+designation+"\nEmail: "+mail
			# 		await message.channel.send(line)
				
			if msg.upper().startswith("ALUMNI"):
				alum_name=msg[7:]
				if (df["Full Name"]==alum_name).any():
					nm = df[df["Full Name"]==alum_name]
					if auth_id not in db.keys():
						name=nm.iloc[0][0]
						print(name)
						designation=nm.iloc[0][2]
						role = discord.utils.get(server.roles, name=designation)

						try:
							await member.add_roles(role)
							await member.edit(nick=name)
							db[auth_id] = name
							print("Author ID", auth_id)
							greet="Hello "+name+"!\nYour nickname and role have been updated in the server!"
							await message.channel.send(greet)
							await message.channel.send("Now you can use the following commands\n!dads : To get the information about your Director, Assistant Directors and Secretaries and their email ids\n!update : To update your role after a promotion\n!whoami : To know your designation in the club")
						except:
							await message.channel.send("Error occured while registering. Please reach out to the moderators")
							print("Error occured while registering. Please reach out to the moderators")	
					else:
						await message.channel.send("Name already exists!")

		
			if msg.upper().startswith("REG"):
				idno=msg[4:].strip()
				print(idno)
				if (df["Student ID"]==int(idno)).any():
					i=df[df["Student ID"]==int(idno)]
					if auth_id not in db.keys():
						name=i.iloc[0][0]
						print(name)
						dept=i.iloc[0][2]
						role = discord.utils.get(server.roles, name=dept)
						dept_short=""
						if dept=="Event Management":
							dept_short="EM"
						elif dept=="Editorial & Publications":
							dept_short="E&P"
						elif dept=="Finance & Marketing":
							dept_short="F&M"
						elif dept == "Arts & Design":
							dept_short = "A&D"
						elif dept == "Strategic Planning":
							dept_short="SP"
						elif dept == "Human Resource":
							dept_short="HR"
						else: 
							dept_short=dept
					#await member.add_roles(role)
						try:
							old_role=member.top_role
							await member.remove_roles(old_role)
							
							await member.add_roles(role)
							new_nick=f"{name}[{dept_short}]"
							await member.edit(nick=new_nick)
							db[auth_id] = idno
							print("Author ID", auth_id)
							greet="Hello "+name+"!\nYour nickname and role have been updated in the server. Welcome to ROBU!"
							await message.channel.send(greet)
							await message.channel.send("Now you can use the following commands\n!whoami : To know your designation in the club")
						except:
							await message.channel.send("Error occured while registering. Please reach out to the moderators")
							print("Error occured while registering. Please reach out to the moderators")	
					else:
						await message.channel.send("ID already registered!")
				
				else:
					await message.channel.send("ID not found in the database")
				

			elif msg.upper().startswith("WHOAMI"):
				#print(df.head())
				if auth_id in db.keys():
					if int(db[auth_id]):
						val=int(db[auth_id])
						i=df[(df["Student ID"]==val)]
						name=i.iloc[0][0]
						dept=i.iloc[0][2]
						designation=i.iloc[0][3]
						if designation=="Alumni":
							greet=f"Hello {name}, our dearest alumni of ROBU. ROBU is forever indebted to you, as your leadership has hauled us to this position we are in right now, your guidance has led everyone to see the better part of themselves and helped every one of us realize our potentials and capabilities. You’re the best. We all hope that you would stay in touch with us through this discord and continue our beloved relationship.\nRegards,\nRobotics Club of Brac University"
						else:
							greet=f"Hello {name}!\nYour department is: {dept}"
						await message.channel.send(greet)
					else:
						nm = df[df["Designation"]=="Alumni"]
						val=db[auth_id]
						flag=False
						for i in range(nm.shape[0]):
							name=nm.iloc[i][0]
							if name==val:
								flag=True
						if flag:
							greet=f"Hello {name}, our dearest alumni of ROBU. ROBU is forever indebted to you, as your leadership has hauled us to this position we are in right now, your guidance has led everyone to see the better part of themselves and helped every one of us realize our potentials and capabilities. You’re the best. We all hope that you would stay in touch with us through this discord and continue our beloved relationship.\nRegards,\nRobotics Club of Brac University"
							
							await message.channel.send(greet)
						else:
							await message.channel.send("Name/ID not found in database. Please contact the moderators")

				
				else:
					await message.channel.send("ID not found in the database. Please contact the moderators")

			
			# elif msg.upper().startswith("UPDATE"):
			# 	if auth_id in db.keys():
			# 		val=int(db[auth_id])
			# 		print(val)
			# 		print(type(val))
			# 		i=df[(df["Student ID"]==val)]
			# 		dept=i.iloc[0][2]
			# 		new_role = discord.utils.get(server.roles, name=dept)
			# 		old_role=member.top_role
			# 		if str(old_role) != str(new_role):
			# 			try:
			# 				await member.remove_roles(old_role)
			# 				await member.add_roles(new_role)
			# 				await message.channel.send("Your role has been updated!")
			# 			except:
			# 				await message.channel.send("Error occured! Contact with the moderators")
			# 				print("Error occured! Contact with the moderators")
			# 		else:
			# 			await message.channel.send("Your promotion is yet to be updated in the database. Please be patient. Thanks!")
			# 	else:
			# 		await message.channel.send("ID not found in the database. Please Register.")
			
			
			# elif msg.upper().startswith("HELP"):
			# 	await message.channel.send("!reg<space>StudentID : This will register your ID, change your nickname in the server if it is not your registered name and give you appropriate roles\n!dads : To get the information about your Director, Assistant Directors and Secretaries and their email ids\n!update : To update your role after a promotion\n!whoami : To know your designation in the club")


			print(msg)
		elif str(message.channel)=="for-bot":
			member = server.get_member(message.author.id)
			print(message.author.id)
			auth_id=str(message.author.id)
			msg = message.content[1:]
			if msg.upper().startswith("SENDALL"):
				content=msg[8:]
				print(content)
				mem=server.members
				for m in mem:
					try:
						await m.send(content)
					except:
						print("sendall didnt work")
				print(content)
				await message.channel.send("Message sent!")
			
			if msg.upper().startswith("REMOVE"):
				rmv_id = msg[7:]
				print(rmv_id)
				keys = db.keys()
				for key in keys:
					if rmv_id == db[key]:
						print("key found")
						del db[key]
						print("key deleted")
						await message.channel.send(f"Member Removed! ID: {rmv_id}")
			
			#need to implement assign/update role for a group


@client.event
async def on_member_remove(member):
	print(member.id)
	try:
		del db[str(member.id)]
	except:
		print("deleted member was not registered")


keep_alive()


client.run(os.environ['token'])