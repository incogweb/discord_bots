import discord
import os
import patoolib
import zipfile

# Replace this with your bot token
TOKEN = "YOUR-DISCORD-BOT-TOKEN"

# Enable intents
intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    for attachment in message.attachments:
        if attachment.filename.endswith(".rar"):
            await message.channel.send("Processing your .rar file...")

            rar_path = f"downloads/{attachment.filename}"
            zip_path = rar_path.replace(".rar", ".zip")

            os.makedirs("downloads", exist_ok=True)
            await attachment.save(rar_path)

            extract_path = "extracted/"
            os.makedirs(extract_path, exist_ok=True)

            try:
                # Extract .rar file using patool
                patoolib.extract_archive(rar_path, outdir=extract_path)

                # Convert extracted files to .zip
                with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                    for root, _, files in os.walk(extract_path):
                        for file in files:
                            full_path = os.path.join(root, file)
                            rel_path = os.path.relpath(full_path, extract_path)
                            zf.write(full_path, rel_path)

                # Send the .zip file back
                await message.channel.send("Here is your converted .zip file:", file=discord.File(zip_path))

            except Exception as e:
                await message.channel.send(f"Error: {e}")

            # Cleanup files
            os.remove(rar_path)
            os.remove(zip_path)
            for root, _, files in os.walk(extract_path, topdown=False):
                for file in files:
                    os.remove(os.path.join(root, file))
                os.rmdir(root)

bot.run(TOKEN)
