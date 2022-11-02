import discord
from discord import app_commands, ui
from dotenv import load_dotenv
from os import getenv

load_dotenv()
token = getenv("TOKEN")

intents = discord.Intents.default()
intents.members = True

GUILD = discord.Object(id=978803693820452874)


class Client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild=GUILD)
            self.synced = True


class AdminRequest(ui.Modal, title="Admin Request"):
    server = ui.TextInput(
        label="Server #",
        style=discord.TextStyle.short,
        placeholder="1",
        required=True,
        max_length=1
    )
    team = ui.TextInput(
        label="Team issue is located on",
        style=discord.TextStyle.short,
        placeholder="German",
        required=True,
        max_length=10,
    )
    user = ui.TextInput(
        label="User causing the problem (if applicable)",
        style=discord.TextStyle.short,
        placeholder="Jimbob",
        default="N/A",
        required=False,
    )
    detail = ui.TextInput(
        label="Details about the incident",
        style=discord.TextStyle.long,
        placeholder="Please provide as much detailed information as possible about the issue that is going on.",
        required=True,
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(
            title=self.title,
            color=discord.Color.blue()
        )
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        embed.add_field(name="Server #", value=self.server)
        embed.add_field(name="Team", value=self.team)
        embed.add_field(name="Player Name", value=self.user)
        embed.add_field(name="Details", value=self.detail)
        await interaction.response.send_message(embed=embed)


client = Client()
tree = app_commands.CommandTree(client)


@tree.command(
    name="admin_request",
    description="Make an Admin Request",
    guild=GUILD,
)
async def admin_request(interaction: discord.Interaction):
    await interaction.response.send_modal(AdminRequest())


def get_vc_members(voice_channel):
    member_list = []
    for member in voice_channel.members:
        member_list.append(member.name)
    if len(member_list) <= 0:
        return "Channel is empty"
    member_per_line = '\n'.join(member_list)
    return member_per_line


def embed_message(vc_members, channel):
    embed = discord.Embed(
        title=f"{channel}",
        color=discord.Color.green()
    )
    embed.add_field(name="Members", value='>>> {}'.format(vc_members))
    return embed


client.run(token)
