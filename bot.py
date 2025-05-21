import discord
from discord.ext import commands
import sqlite3
from config import DATABASE
from config import TOKEN

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# Prefix perintah
bot = commands.Bot(command_prefix='!', intents=intents)

# Event yang terpicu ketika bot siap
@bot.event
async def on_ready():
    print(f'Bot {bot.user.name} siap bekerja!')

# Event yang terpicu ketika anggota baru bergabung
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name='umum')
    if channel:
        await channel.send(f'Selamat datang di server, {member.mention}!')

# Respon sederhana untuk perintah !ping
@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

# Perintah !hello yang merespon dengan mention pengguna
@bot.command()
async def hello(ctx):
    await ctx.send(f'Hey, {ctx.author.mention}! aku adalah bot mengenai informasi status orang dewasa!')

# Perintah !echo yang mengulangi pesan pengguna
@bot.command()
async def echo(ctx, *, message: str):
    await ctx.send(message)

# Penanganan kesalahan perintah
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Harap tentukan semua argumen yang diperlukan.')
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send('Perintah tidak ditemukan.')
    else:
        await ctx.send('Terjadi kesalahan saat menjalankan perintah.')

@bot.command()
async def info_random(ctx):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('SELECT * FROM adults ORDER BY RANDOM() LIMIT 1')
    row = cur.fetchone()
    await ctx.send(f'Usia: {row[0]}, Pekerjaan: {row[1]}, Pendidikan: {row[3]}, Penghasilan: {row[-1]}')

@bot.command()
async def cari_usia(ctx, umur: int):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('SELECT age, workclass, education, income FROM adults WHERE age = ?', (umur,))
    rows = cur.fetchall()
    if rows:
        msg = "\n".join([f'👤 {r[0]}thn, {r[1]}, {r[2]}, {r[3]}' for r in rows[:5]])  # batasi 5 dulu
        await ctx.send(f'Ditemukan:\n{msg}')
    else:
        await ctx.send('Tidak ada data dengan usia tersebut.')

@bot.command()
async def top_pendidikan(ctx):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('SELECT education, COUNT(*) FROM adults GROUP BY education ORDER BY COUNT(*) DESC LIMIT 5')
    rows = cur.fetchall()
    msg = "\n".join([f'{r[0]}: {r[1]}' for r in rows])
    await ctx.send(f'Top 5 Pendidikan:\n{msg}')

# Jalankan bot
bot.run(TOKEN)