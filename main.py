from discord.ext import commands
import os
import discord


intents = discord.Intents.all()

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='!',
            intents=discord.Intents.all(),
            application_id='1333507452863516713'
        )
        self.initial_extensions = [f'cogs.{filename[:-3]}' for filename in os.listdir('./cogs') if filename.endswith('.py')]
        self.synced = False
        self.auto_sync = True



    async def setup_hook(self):
        
        # Load extensions
        for ext in self.initial_extensions:
            try:
                await self.load_extension(ext)
                print(f'✓ Loaded extension: {ext}')
            except Exception as e:
                print(f'✗ Failed to load extension {ext}: {e}')
        
        try:
            # Sync new commands
            commands = await self.tree.sync()
            print(f'✓ Synced {len(commands)} new commands globally')
            
            for guild in self.guilds:
                guild_commands = await self.tree.sync(guild=guild)
                print(f'✓ Synced {len(guild_commands)} new commands for {guild.name}')
            self.synced = True
            
        except Exception as e:
            print(f'✗ Failed to sync commands: {e}')

    async def on_guild_join(self, guild):
        """Auto-sync commands when bot joins new server"""
        if self.auto_sync:
            await self.tree.sync(guild=guild)
            print(f'✓ Auto-synced commands for new guild: {guild.name}')

    async def on_ready(self):
        print(f'✓ Logged in as {self.user.name} ({self.user.id})')
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="/help | Nexus Developer"
            ),
            status=discord.Status.online
        )
        if self.synced:
            print('✓ Bot is ready! Commands auto-synced')
        else:
            print('✗ Command sync failed - check permissions')

if __name__ == "__main__":
    bot = Bot()
    token = open('token.txt', 'r').read().strip()   
    bot.run(token)