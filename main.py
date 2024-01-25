import os
from pyrogram import Client, filters
from pytgcalls import PyTgCalls, StreamType

SUDO_USERS = [6352061770, 6734814441]
# Initialize the Client and PyTgCalls instances
app = Client("BADWZRoAg2oIR9qNjNjU4Osliq8irh2k3enJepRYKBBgtucM-8E30UN5NkJN8-CEIobWnKPb_OLS1UVtpiMVTSX2iFE96dvwYHqwbVcVALw3F8phZBA6YxN3EsEKZ8hao_vmVW2NW7K8BjUgoEfCwMllEonLgBr9kBaRvyiMtkmxTm306ig5bP1d1X5pD-yQsDjQwqQfAQYBnf7SS9c_4BqQBt8eizAW00CQWOs0SSN_fAVSR4p3UM_pCA_UQWn2Gei-k9B2YCUbCYg3ilVCuvAb58ilBRPh2Plmv21wQ7jkIgwfABILPFTBPeSMORoyuP13hFV_XE2aaaIVxURRjpj_YtO8aAAAAAGRbRzpAA")
callsmusic = PyTgCalls(app)

# Define a variable to track the playing state
playing = False

# Define a list to store the queue of songs
queue = []

# Define a function to play a song
async def play_song(query, user_id):
    # Search for the song using Yandex API (you can replace it with another search API)
    search_results = os.popen(f"yandex-music-search '{query}'").read().split("\n")

    # Extract the first search result
    song_url = search_results[0].split(" ")[-1]

    # Generate a file name for the song
    file_name = f"{query}.mp3"

    # Download the song using youtube-dl (you can replace it with another downloader)
    os.system(f"youtube-dl -x --audio-format mp3 {song_url} -o {file_name}")

    # Add the downloaded file to the queue
    queue.append((file_name, user_id))

    # If no song is playing, play the first song in the queue
    if not playing:
        await callsmusic.join_group_call(callsmusic.active_group, queue[0][0], stream_type=StreamType.PULSE_AUDIO, user_id=queue[0][1])
        playing = True

# Define a function to skip a song
async def skip_song():
    # Check if a song is playing
    if playing:
        # Skip the current song
        await callsmusic.skip_current_song(callsmusic.active_group)

        # If there's a next song in the queue, play it
        if len(queue) > 0:
            await callsmusic.join_group_call(callsmusic.active_group, queue[0][0], stream_type=StreamType.PULSE_AUDIO, user_id=queue[0][1])
            queue.pop(0)

# Define a function to pause a song
async def pause_song():
    # Check if a song is playing
    if playing:
        # Pause the current song
        await callsmusic.pause_current_song(callsmusic.active_group)

# Define a function to end a song
async def end_song():
    # Check if a song is playing
    if playing:
        # End the current song
        await callsmusic.stop_current_song(callsmusic.active_group)

        # Clear the queue
        queue.clear()

        # Set the playing state to False
        playing = False

# Define a command to play a song
@app.on_message(filters.command(["play"]))
async def play(_, message):
    # Get the user id of the user who sent the message
    user_id = message.from_user.id

    # Check if the user has the sudo permission
    if user_id in SUDO_USERS:
        # Get the query from the user's message
        query = message.text.split(" ")[1]

        # Play the song using the play_song function
        await play_song(query, user_id)
    else:
        # Send a message to the user if they don't have the sudo permission
        await message.reply("You don't have the sudo permission to play songs.")

# Define a command to skip a song
@app.on_message(filters.command(["skip"]))
async def skip(_, message):
    # Skip the current song using the skip_song function
    await skip_song()

# Define a command to pause a song
@app.on_message(filters.command(["pause"]))
async def pause(_, message):
    # Pause the current song using the pause_song function
    await pause_song()

# Define a command to end a song
@app.on_message(filters.command(["end"]))
async def end(_, message):
    # End the current song using the end_song function
    await end_song()
  
