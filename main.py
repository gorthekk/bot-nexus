import os
import discord
from discord.ext import commands
from discord import app_commands

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='!',  # Ensure prefix is set
            description='Nexus Developer Bot',
            intents=discord.Intents.all(),
            application_id='1333507452863516713',
        )
        self.initial_extensions = [f'cogs.{filename[:-3]}' for filename in os.listdir('./cogs') if filename.endswith('.py')]
        self.synced = False
        self.auto_sync = True

    async def setup_hook(self):
        print("🔄 Starting bot setup...")
        
        # Load extensions
        for ext in self.initial_extensions:
            try:
                await self.load_extension(ext)
                print(f'✓ Loaded extension: {ext}')
            except Exception as e:
                print(f'✗ Failed to load extension {ext}: {e}')

        try:
            # Register prefix commands
            for command in self.commands:
                print(f'✓ Registered prefix command: !{command.name}')

            # Sync slash commands
            synced = await self.tree.sync()
            print(f'✓ Synced {len(synced)} slash commands')
            self.synced = True

        except Exception as e:
            print(f'✗ Failed to sync commands: {e}')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f"Command not found. Use !help to see available commands.")

if __name__ == "__main__":
    bot = Bot()
    token = open('token.txt', 'r').read().strip()   
    bot.run(token)