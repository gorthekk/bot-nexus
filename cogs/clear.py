import discord
from discord.ext import commands
from discord import app_commands

class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("✓ Clear cog loaded")

    @app_commands.command(
        name="clear",
        description="Clear a specified number of messages"
    )
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, amount: int):
        try:
            if amount <= 0:
                await interaction.response.send_message("Please specify a positive number!", ephemeral=True)
                return

            # Defer the response since deletion might take time
            await interaction.response.defer(ephemeral=True)
            
            # Delete messages
            deleted = await interaction.channel.purge(limit=amount)
            
            # Send confirmation
            await interaction.followup.send(
                f"✅ Successfully deleted {len(deleted)} messages.",
                ephemeral=True
            )

        except discord.Forbidden:
            await interaction.followup.send("I don't have permission to delete messages!", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"An error occurred: {str(e)}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Clear(bot))