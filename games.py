import discord
from discord.ext import commands
import random
import economy_functions


class RollView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.roll_result = random.randint(1, 6)

    @discord.ui.button(label='1', style=discord.ButtonStyle.gray)
    async def button_1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.check_roll(interaction, 1)

    @discord.ui.button(label='2', style=discord.ButtonStyle.gray)
    async def button_2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.check_roll(interaction, 2)

    @discord.ui.button(label='3', style=discord.ButtonStyle.gray)
    async def button_3(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.check_roll(interaction, 3)

    @discord.ui.button(label='4', style=discord.ButtonStyle.gray)
    async def button_4(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.check_roll(interaction, 4)

    @discord.ui.button(label='5', style=discord.ButtonStyle.gray)
    async def button_5(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.check_roll(interaction, 5)

    @discord.ui.button(label='6', style=discord.ButtonStyle.gray)
    async def button_6(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.check_roll(interaction, 6)

    async def check_roll(self, interaction: discord.Interaction, guess: int):
        if guess == self.roll_result:
            await interaction.response.send_message("Correct!", ephemeral=True)
        else:
            await interaction.response.send_message(f"Incorrect! The correct number was {self.roll_result}.", ephemeral=True)


class RockPaperScissorsView(discord.ui.View):
    def __init__(self, player_id, amount):
        super().__init__()
        self.moves = ['rock', 'paper', 'scissors']
        self.player_id = player_id
        self.amount = amount

    @discord.ui.button(label='rock', style=discord.ButtonStyle.gray)
    async def button_rock(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.check_move(interaction, 'rock')

    @discord.ui.button(label='paper', style=discord.ButtonStyle.gray)
    async def button_paper(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.check_move(interaction, 'paper')

    @discord.ui.button(label='scissors', style=discord.ButtonStyle.gray)
    async def button_scissors(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.check_move(interaction, 'scissors')

    async def check_move(self, interaction: discord.Interaction, player_move: str):
        bot_move = random.choice(self.moves)
        user_data = economy_functions.load_data()
        if player_move == bot_move:
            await interaction.response.send_message(f"Draw! Both chose {bot_move}.", ephemeral=True)
        elif (player_move == "scissors" and bot_move == "rock") or \
                (player_move == "rock" and bot_move == "paper") or \
                (player_move == "paper" and bot_move == "scissors"):
            await interaction.response.send_message(f"You lose! {bot_move} beats {player_move}.", ephemeral=True)
        else:
            winnings = self.amount * 2
            user_data[str(self.player_id)]["gems"] += winnings
            economy_functions.save_data(user_data)
            await interaction.response.send_message(
                f"You win! {player_move} beats {bot_move}. You won {winnings} gems.", ephemeral=True)

class CoinFlipView(discord.ui.View):
    def __init__(self, player_id, amount):
        super().__init__()
        self.moves = ['head', 'tails']
        self.player_id = player_id
        self.amount = amount

    @discord.ui.button(label='head', style=discord.ButtonStyle.gray)
    async def button_head(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.check_move(interaction, 'head')

    @discord.ui.button(label='tails', style=discord.ButtonStyle.gray)
    async def button_tails(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.check_move(interaction, 'tails')

    async def check_move(self, interaction: discord.Interaction, player_move: str):
        coin_side = random.choice(self.moves)
        user_data = economy_functions.load_data()
        if player_move == coin_side:
            user_data[str(self.player_id)]["gems"] += self.amount * 2
            await interaction.response.send_message(f"You Win!, the coins flipped to be {player_move}", ephemeral=True)
            economy_functions.save_data(user_data)
        else:
            await interaction.response.send_message(f"You lose! {player_move} was not the side the coin flipped to be", ephemeral=True)
