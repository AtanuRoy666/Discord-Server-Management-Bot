# Discord-Server-Management-Bot
This bot is made to manage the discord server of Robotics Club of Brac University(ROBU) with custom commands and member verification option. This application uses the discord.py api and pandas for connecting to the google sheets database.

## Member Verification
When a new member joins the discord server, this bot will send him/her a  direct-message to register usign their BRACU Student ID. The custom command for this and the others are mentioned below:  

## Custom Commands(For members): 
<ul>
  <li> <b>!reg<space><unique identifier>:</b> If you dm this command to the bot, it will check your membership status in the central database and if your ID is found there, your role will be updated according to your department. It will also save the discord_id of the sender to prevent multiple registration attempts. For our case the unique identifier was the bracu student id</li>
  <li> <b> !whoami<space><unique identifier>:</b> This will return your name and department to you. If the designation of the id is alumni then it will send a gratitude message.</li>
  
</ul>


## Custom Commands(For admins): 
These commands are for the server admins and need to be performed in a special text-channel named "for-bot"
<ul>
  <li> <b>!sendall<space><Any Message to broadcast>:</b> This command will broadcast a message to all of the server members</li>
  <li> <b>!remove<space><unique identifier>:</b> This will remove the server member with the mentioned unique identifier </li>
</ul>

##keep.py
This file was used to run the code indefinitely in repl server using the site: uptimerobot.com 
You can find the details in this video: https://www.youtube.com/watch?v=tMH16T74fWE
