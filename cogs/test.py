import discord
from discord import app_commands
from discord.ext import commands

class test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name='test',
        description='Test command',
    )
    async def test_command(self, interaction: discord.Interaction):
        await interaction.response.send_message('Test command executed successfully!')


async def setup(bot):
    await bot.add_cog(test(bot))