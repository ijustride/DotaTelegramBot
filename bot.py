import os
from telegram.ext import Application, CommandHandler
from dotenv import load_dotenv
import dota

load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def start(update, context):
    await update.message.reply_text(
        "Send /hero <name> to get counters"
    )

async def hero(update, context):
    hero_name = " ".join(context.args).lower()

    if not hero_name:
        await update.message.reply_text("Usage: /hero Pudge")
        return

    hero_id = dota.name_to_id.get(hero_name)
    if not hero_id:
        await update.message.reply_text("Unknown hero")
        return

    matchups = dota.get_clean_matchups(hero_id)
    

    counters = sorted(matchups, key=lambda x: x["winrate"])[:5]
    

    text = f"*{dota.heroes_map[hero_id]}*\n\n"

    text += "*Counters*\n"
    for c in counters:
        text += f"• {dota.heroes_map[c['hero_id']]} ({100 - c['winrate'] * 100:.1f}%)\n"


    await update.message.reply_text(text, parse_mode="Markdown")

def main():
    dota.load_heroes()

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("hero", hero))
    app.run_polling()

if __name__ == "__main__":
    main()
