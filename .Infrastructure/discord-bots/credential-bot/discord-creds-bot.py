#!/usr/bin/python3

#|##############################|#
#| Chronos Security             |#
#| https://chronossec.site      |#
#| https://github.com/ChronosPK |#
#|##############################|#

import discord
import datetime

# Define the welcome message
welcome_message = """
Welcome to our CTF server, {user}!

Here are your credentials:
||`{creds}`||

Please keep them safe and do not share them with anyone.

Enjoy your stay!
"""

# Set up the intents for the bot
intents = discord.Intents.default()
intents.members = True

# Set up the client with the intents
client = discord.Client(intents=intents)

# Define the list of credentials
creds = []
with open('credentials.txt', 'r') as file:
    creds = file.readlines()

# Define the list of used credentials
used_lines = []
with open('used_credentials.txt', 'r') as file:
    used_lines = file.read().splitlines()

# Define the index of the next set of credentials to be used
next_creds_index = 0

# Define the function that handles new member join events
@client.event
async def on_member_join(member):
    global next_creds_index

    # Check if the member has already been assigned credentials (see below)
    if str(member.id) in used_lines:
        return
 
    # Get the next set of credentials from the list
    if next_creds_index < len(creds):
        creds_line = creds[next_creds_index].strip()
        await member.send(welcome_message.format(user=member.mention, creds=creds_line))
        next_creds_index += 1
    else:
        await member.send("Sorry, no more credentials available.")

    # Add the user's ID to the list of used credentials
    used_lines.append(str(member.id))
    with open('used_credentials.txt', 'a') as file:
        file.write(str(member.id) + '\n')

    # log when each user has joined the server
    with open('joined_users.txt', 'a') as file:
        timestamp = datetime.datetime.now().strftime('%d.%m.%Y [%H:%M:%S]')
        file.write(f'{timestamp} : {member.name}\n')
        #file.write(str(member.display_name) + '\n')


# Define the function that handles errors
@client.event
async def on_error(event, *args, **kwargs):
    with open('error.log', 'a') as file:
        if event == 'on_message':
            file.write(f'Unhandled message: {args[0]}\n')
        else:
            file.write(f'Unhandled event: {event}\n')



# Run the bot
client.run('4MTA4MDU2MjI1NjUwMjMzNzYyNg.Gs__-Q.4n5Z8R4aMARP7Fx-K14Y6Nd4kKk7uSYZtS1Ac')
