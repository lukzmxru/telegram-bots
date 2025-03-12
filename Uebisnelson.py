from telegram import Update
from telegram.ext import Application, MessageHandler, filters
import openpyxl
import re
import asyncio
from datetime import datetime

# Configurações do bot
TOKEN = "7581699837:AAEymdXK6RF9hdXOFwjFiMB4Iv9XM5v-7x8"  # Token do Uelbis
PLANILHA_LOCAL = r"C:\Users\m7tb\Kemira Oyj\EXPEDICAO - IGF Almoxarifado/ESTOQUE ALMOX KEMIRA ORT.xlsx"  # Caminho da planilha local
GRUPO_DESTINO = -4783786888  # ID do grupo de skus 

# Atualiza a planilha com SKU, quantidade e data
def atualizar_planilha(sku, quantidade):
    try:
        # Abre a planilha
        workbook = openpyxl.load_workbook(PLANILHA_LOCAL)
        sheet = workbook.active
        
        # Procura o SKU na coluna A
        sku_encontrado = False
        for linha in sheet.iter_rows(min_row=2): #Ignora cabeçalho (linha 1)
            celula_sku = linha[0].value #Coluna A = SKU
            if celula_sku == sku:
                # Atualiza a quantidade na coluna N
                linha[13].value = quantidade
                
                # Atualiza a data na coluna L como objeto datetime
                linha[11].value = datetime.now()  
                
                # Formata a célula da data para "dd/mm/yyyy" e alinhamento à direita
                sheet.cell(row=linha[11].row, column=12).number_format = "dd/mm/yyyy"  
                sheet.cell(row=linha[11].row, column=12).alignment = openpyxl.styles.Alignment(horizontal='right')
                
                # Atualiza colunas K e Q
                linha[10].value = "SIM"
                linha[16].value = "Concluído"
                
                sku_encontrado = True
                break
        
        if not sku_encontrado:
            return f"❌ Eu não achei o sku {sku} na planilha."
        
        workbook.save(PLANILHA_LOCAL)
        return f"✅ SKU {sku} atualizado com sucesso! Nova quantidade: {quantidade}"
    
    except FileNotFoundError:
        return "❌ Planilha não encontrada. Verifique o caminho da planilha."

# Processa mensagens recebidas no grupo de destino
async def processar_mensagem(update: Update, context):
    try:
        # Verifica se é uma mensagem encaminhada do Wyvis (com legenda)
        if update.message.photo and update.message.caption:
            # Extrai SKU e Qtd da legenda
            caption = update.message.caption
            sku_match = re.search(r'SKU:\s*(\d+)', caption, re.IGNORECASE)
            qtd_match = re.search(r'Qtd:\s*(\d+)', caption, re.IGNORECASE)
            
            if sku_match and qtd_match:
                sku = sku_match.group(1)
                qtd = int(qtd_match.group(1))
                
                # Atualiza a planilha
                resultado = atualizar_planilha(sku, qtd)
                print(resultado)
                
                # Encaminha e remove a mensagem original
                await context.bot.forward_message(chat_id=GRUPO_DESTINO, from_chat_id=update.message.chat_id, message_id=update.message.message_id)
                await update.message.delete()
                
            else:
                print("Formato de legenda inválido.")
                
    except Exception as e:
        print(f"Erro: {str(e)}")

# Configuração do bot
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO & filters.CAPTION, processar_mensagem))
    
    print("Uebisnelson está observando o grupo...")
    app.run_polling()

if __name__ == "__main__":
   main()