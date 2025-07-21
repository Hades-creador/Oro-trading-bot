
import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

API_KEY = os.getenv("API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ENTRY_MARGIN = float(os.getenv("ENTRY_MARGIN", 0.001))
TP_MARGIN = float(os.getenv("TP_MARGIN", 0.008))
SL_MARGIN = float(os.getenv("SL_MARGIN", 0.006))

def get_gold_price():
    url = f"https://www.alphavantage.co/query?function=COMMODITY_EXCHANGE_RATE&from_symbol=XAU&to_symbol=USD&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    try:
        return float(data["Realtime Commodity Exchange Rate"]["5. Exchange Rate"])
    except:
        return None

async def oro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price = get_gold_price()
    if price:
        entry = price * (1 - ENTRY_MARGIN)
        tp = price * (1 + TP_MARGIN)
        sl = price * (1 - SL_MARGIN)
        trend = "📈 Alcista" if TP_MARGIN > SL_MARGIN else "📉 Bajista"

        message = f"""📈 Predicción del Oro

💰 Precio actual: ${price:.2f}
📥 Entrada sugerida: ${entry:.2f}
📤 Salida (TP): ${tp:.2f}
🛑 Stop Loss: ${sl:.2f}

Tendencia: {trend}"""
    else:
        message = "No se pudo obtener el precio del oro. Intenta más tarde."

    await update.message.reply_text(message)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("oro", oro))
    app.run_polling()
