import discord
from discord.ext import commands
import responses
import economy_functions
import games

# Specify the channel ID where commands are allowed
ALLOWED_CHANNEL_ID = 1255701186301136906  # Replace with your channel ID

async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        print(f"Response from handle_response: {response}")

        if response == "add_me":
            economy_functions.add_person(message.author.id)
            response = "You have been added to the economy system."
            print(f"Adding user {message.author.id} to the economy system")
        elif response == "help_me":
            response = "Redirect yourself to the help channel for a list of commands within the server"
        elif response == "beg":
            result = economy_functions.beg(message.author.id)
            response = result
        elif response == "roll":
            view = games.RollView()
            response = 'Guess the roll result:'
            if is_private:
                await message.author.send(response, view=view)
            else:
                await message.channel.send(response, view=view)
            return  # Return early to avoid sending response twice

        if response:
            if is_private:
                await message.author.send(response)
            else:
                await message.channel.send(response)
        else:
            print("No response generated for the message.")
    except Exception as e:
        print(f"Error sending message: {e}")

def run_discord_bot():
    TOKEN = 'ENTER_YOUR_BOT_TOKEN_HERE'

    intents = discord.Intents.default()
    intents.message_content = True
    client = commands.Bot(command_prefix='!', intents=intents)

    @client.event
    async def on_ready():
        print(f"{client.user} is now running")

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content.startswith(client.command_prefix):
            await client.process_commands(message)
            return  # Skip further processing if it's a command

        if message.channel.id != ALLOWED_CHANNEL_ID:
            return  # Ignore messages not in the allowed channel

        username = str(message.author.id)
        user_msg = str(message.content)
        print(f"{username} said: {user_msg} in channel {message.channel}")

        is_private = user_msg.startswith('/')
        user_message = user_msg[1:] if is_private else user_msg[1:]

        await send_message(message, user_message, is_private)

    @client.command()
    async def claim_daily_reward(ctx):
        try:
            user_id = ctx.author.id
            result = economy_functions.claim_daily_reward(user_id)
            await ctx.send(f"{ctx.author.mention}, {result}")
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send(f"An error occurred: {e}")

    @client.command()
    async def bet(ctx, game: str, amount: int):
        try:
            user_id = ctx.author.id
            game = game.lower()

            user_data = economy_functions.load_data()
            if str(user_id) not in user_data or user_data[str(user_id)]["gems"] < amount:
                await ctx.send(f"{ctx.author.mention}, you do not have enough gems to place this bet.")
                return

            if game == "roll":
                user_data[str(user_id)]["gems"] -= amount
                economy_functions.save_data(user_data)
                view = games.RollView()

                async def check_winner(interaction, guess):
                    if guess == view.roll_result:
                        winnings = amount * 2
                        user_data[str(user_id)]["gems"] += winnings
                        economy_functions.save_data(user_data)
                        await interaction.response.send_message(
                            f"{ctx.author.mention}, you won! You now have {user_data[str(user_id)]['gems']} gems.",
                            ephemeral=True)
                    else:
                        await interaction.response.send_message(
                            f"{ctx.author.mention}, you lost! The correct number was {view.roll_result}. You now have {user_data[str(user_id)]['gems']} gems.",
                            ephemeral=True)

                async def new_check_roll(interaction, button):
                    guess = int(button.label)
                    await check_winner(interaction, guess)

                for button in view.children:
                    button.callback = lambda i, b=button: new_check_roll(i, b)

                await ctx.send('Guess the roll result:', view=view)

            elif game == "rps":
                user_data[str(user_id)]["gems"] -= amount
                economy_functions.save_data(user_data)
                view = games.RockPaperScissorsView(ctx.author.id, amount)
                await ctx.send("Choose your move:", view=view)

            elif game == "coin_flip":
                user_data[str(user_id)]["gems"] -= amount
                economy_functions.save_data(user_data)
                view = games.CoinFlipView(ctx.author.id, amount)
                await ctx.send("Choose your move:", view=view)

            else:
                await ctx.send(f"{ctx.author.mention}, the game '{game}' is not recognized.")
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send(f"An error occurred: {e}")

    @client.command()
    async def beg(ctx):
        try:
            user_id = ctx.author.id
            result = economy_functions.beg(user_id)
            await ctx.send(f"{ctx.author.mention}, {result}")
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send(f"An error occurred: {e}")

    @client.command()
    async def add_me(ctx):
        try:
            economy_functions.add_person(ctx.author.id)
            await ctx.send(f"{ctx.author.mention}, you have been added to the economy system.")
        except Exception as e:
            print(f"Error: {e}")
            await ctx.send(f"An error occurred: {e}")

    client.run(TOKEN)
