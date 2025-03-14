import os
import openpyxl

PASTA_SKUS = r"C:\Users\m7tb\Pictures\SKUS enviados"
PLANILHA_LOCAL = r"C:\Users\m7tb\Kemira Oyj\EXPEDICAO - IGF Almoxarifado\ESTOQUE ALMOX KEMIRA ORT.xlsx"


def verificar_skus_pendentes():
    try:
        workbook = openpyxl.load_workbook(PLANILHA_LOCAL)
        sheet = workbook.active
        skus_pendentes = []

        for arquivo in os.listdir(PASTA_SKUS):
            if arquivo.endswith(".jpg") or arquivo.endswith(".png"):
                sku = os.path.splitext(arquivo)[0]

                sku_encontrado = False
                for linha in sheet.iter_rows(min_row=2):
                    celula_sku = linha[0].value
                    if celula_sku == sku:
                        sku_encontrado = True
                        status = linha[16].value

                        if status == "Pendente":
                            skus_pendentes.append(sku)
                            print(f"SKU {sku} não foi concluído.")
                        break

                if not sku_encontrado:
                    print(f"SKU {sku} não foi encontrado na planilha")
        if skus_pendentes:
            print("\nSKUS pendentes:")
            for sku in skus_pendentes:
                print(f" {sku}")
        else:
            print("Nenhum SKU pendente.")
    
    except FileNotFoundError:
        print("Erro: Planilha não encontrada. Verifique o caminho da planilha.")
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")


if __name__ == "__main__":
    verificar_skus_pendentes()