
from telegram import Update
from telegram.ext import Application, MessageHandler, filters
import os
import re
import requests

# Configurações básicas
TOKEN = "8013428342:AAFaIK_PNXktaIrCwz1kCEX289m1HBGJdjs"
DESTINO_ID = -1002383950901  # ID do grupo destino
PASTA_SKUS = r"C:\Users\m7tb\Pictures\SKUs para enviar"

async def processar_mensagem(update: Update, _):
    try:
        if update.message.photo and update.message.caption:
            # Regex só aceita exatamente 8 dígitos após "SKU:", sem letras ou caracteres extras
            sku_match = re.search(
                r'(?i)SKU:\s*(\d{8})(?:\D|$)',  # (?i) = case-insensitive, (?:\D|$) = bloqueia dígitos extras
                update.message.caption
            )
            
            if sku_match:
                sku = sku_match.group(1)
                
                # Baixa imagem
                foto = update.message.photo[-1]
                arquivo = await _.bot.get_file(foto.file_id)
                resposta = requests.get(arquivo.file_path)
                
                # Salva localmente
                os.makedirs(PASTA_SKUS, exist_ok=True)
                with open(os.path.join(PASTA_SKUS, f"{sku}.jpg"), 'wb') as f:
                    f.write(resposta.content)
                
                # Encaminha e remove mensagem original
                await _.bot.forward_message(DESTINO_ID, update.message.chat_id, update.message.message_id)
                await update.message.delete()
                
            else:
                await update.message.reply_text("❌ Arruma esse sku ai")
                
    except Exception as e:
        print(f"ERRO: {str(e)}")


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO & filters.CAPTION, processar_mensagem))
    
    print("Wyvisnelson ta na ativa ...")
    app.run_polling()

if __name__ == "__main__":
    main()