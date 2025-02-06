import discord
from discord import app_commands
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # Store bot instance

    @app_commands.command(
        name='help',
        description='Shows all available commands !'
    )
    async def help_command(self, interaction: discord.Interaction):
        help_embed = discord.Embed(
            title='Nexus Developer Bot Commands',
            description='List of all available commands',
            color=discord.Color.random()
        )

        help_embed.add_field(
            name="General Commands", 
            value="`/help` - Shows this message\n`/ping` - Check bot latency", 
            inline=False
        )

        help_embed.add_field(
            name="Admin Commands",
            value="`/kick` - Kick a member\n`/ban` - Ban a member",
            inline=False
        )

        help_embed.set_footer(text=f"Requested by {interaction.user.name}")
        
        # Fix avatar URL property
        if self.bot.user.avatar:
            help_embed.set_thumbnail(url=self.bot.user.avatar.url)

        await interaction.response.send_message(embed=help_embed)

    @help_command.error
    async def help_command_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message(f"An error occurred: {str(error)}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Help(bot))