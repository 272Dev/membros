import discord
import threading
import base64
import os
from flask import Flask, jsonify
from flask_cors import CORS

# ---- config ----
_t = base64.b64decode("TVRRNU9Ea3dOalV4TlRNeE56TXlOVGswTlEuRzlVUm5FLmpnblZkNF9zQmZnNjRwZDdMV2d2ek9yT3hvVmZDc19lQTBoR0p3").decode()
GUILD_ID = 1444145999349153865
PORT = int(os.environ.get("PORT", 5000))
# ----------------

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)
app = Flask(__name__)
CORS(app)

@app.route("/members")
def members():
    guild = client.get_guild(GUILD_ID)
    if guild is None:
        return jsonify({"error": "Servidor não encontrado", "count": 0}), 404
    return jsonify({
        "count": guild.member_count,
        "name": guild.name,
        "online": sum(1 for m in guild.members if m.status != discord.Status.offline and not m.bot)
    })

@app.route("/")
def index():
    return jsonify({"status": "online", "bot": "272 Member Counter"})

@client.event
async def on_ready():
    print(f"Bot conectado: {client.user}")
    guild = client.get_guild(GUILD_ID)
    if guild:
        print(f"Servidor: {guild.name} — {guild.member_count} membros")

def run_flask():
    app.run(host="0.0.0.0", port=PORT)

threading.Thread(target=run_flask, daemon=True).start()
client.run(_t)
