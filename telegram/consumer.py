import os
import ujson
import asyncio
import requests
from nats.aio.client import Client as NATS

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": text})

async def main():
    nc = NATS()
    await nc.connect("nats://nats:4222")

    async def message_handler(msg):
      try:
        data = ujson.loads(msg.data.decode())
        print(" [x] Recibido de NATS:", data)

        # Construir el mensaje a enviar a Telegram
        message = (
            f"📦 {data.get('product_name','(sin nombre)')}\n"
            f"💲 {data.get('price','?')} \n"
            f"📦 Stock: {data.get('stock','?')}\n"
            f"🔗 {data.get('url','')}\n"
            f"⏰ Actualizado: {data.get('updated','')}"
        )

        send_telegram(message)

      except Exception as e:
          print(" [!] Error procesando mensaje:", e)
          data = ujson.loads(msg.data.decode())
          print(" [x] Recibido de NATS:", data)
          send_telegram(data["text"])

    # Suscribirse al subject "tasks"
    await nc.subscribe("tasks", cb=message_handler)

    print(" [*] Esperando mensajes en NATS...")
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
