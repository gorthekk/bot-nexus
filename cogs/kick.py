import discord
from discord import app_commands
from discord.ext import commands

class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name='kick',
        description='Kicks a user from the server'
    )
    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.checks.bot_has_permissions(kick_members=True)
    async def kick_command(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        # Check if the user can be kicked
        if member.top_role >= interaction.user.top_role:
            return await interaction.response.send_message(
                "You cannot kick someone with a higher or equal role.",
                ephemeral=True
            )

        if member.id == interaction.user.id:
            return await interaction.response.send_message(
                "You cannot kick yourself.",
                ephemeral=True
            )

        # Create kick confirmation embed
        embed = discord.Embed(
            title="Member Kicked",
            description=f"**Member:** {member.mention}\n**Reason:** {reason or 'No reason provided'}",
            color=discord.Color.red()
        )
        embed.set_footer(text=f"Kicked by {interaction.user}")

        try:
            await member.kick(reason=reason)
            await interaction.response.send_message(embed=embed)

            # Log the kick if log channel exists
            log_channel = discord.utils.get(interaction.guild.channels, name="staff-kick")
            if log_channel:
                await log_channel.send(embed=embed)

        except discord.Forbidden:
            await interaction.response.send_message(
                "I don't have permission to kick this member.",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"An error occurred: {str(e)}",
                ephemeral=True
            )

    @kick_command.error
    async def kick_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                "You don't have permission to kick members.",
                ephemeral=True
            )
        elif isinstance(error, app_commands.BotMissingPermissions):
            await interaction.response.send_message(
                "I don't have permission to kick members.",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"An error occurred: {str(error)}",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(Kick(bot))