import re
import sys

def extrair_itens(arquivo_entrada):
    with open(arquivo_entrada, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    itens = re.findall(r'- Item:\s*(\S+)', conteudo)
    return set(itens)

def buscar_blocos_por_item(itens, arquivos_referencia):
    blocos_unicos = {}

    for arquivo in arquivos_referencia:
        with open(arquivo, 'r', encoding='utf-8') as f:
            linhas = f.readlines()

        i = 0
        while i < len(linhas):
            linha = linhas[i]
            if linha.strip().startswith('- Id:'):
                inicio = i
                i += 1
                while i < len(linhas) and not linhas[i].strip().startswith('- Id:'):
                    i += 1
                bloco = linhas[inicio:i]
                for item in itens:
                    if any(l.strip() == f"AegisName: {item}" for l in bloco):
                        if item not in blocos_unicos:
                            blocos_unicos[item] = bloco
            else:
                i += 1
    return blocos_unicos.values()

def salvar_saida(blocos, arquivo_saida):
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        for bloco in blocos:
            f.writelines(bloco)
            f.write('\n')

def main():
    if len(sys.argv) != 3:
        print("Uso: python ITEMFINDER.py <arquivo_entrada> <arquivo_saida>")
        sys.exit(1)

    arquivo_entrada = sys.argv[1]
    arquivo_saida = sys.argv[2]

    arquivos_referencia = [
        r"C:\Users\mvrmo\OneDrive\Área de Trabalho\rathena-master\rathena-master\RAGNAFROST\illusion\item_db_equip.yml",
        r"C:\Users\mvrmo\OneDrive\Área de Trabalho\rathena-master\rathena-master\RAGNAFROST\illusion\item_db_etc.yml",
        r"C:\Users\mvrmo\OneDrive\Área de Trabalho\rathena-master\rathena-master\RAGNAFROST\illusion\item_db_usable.yml"
    ]

    itens = extrair_itens(arquivo_entrada)
    blocos = buscar_blocos_por_item(itens, arquivos_referencia)
    salvar_saida(blocos, arquivo_saida)
    print(f"Processamento concluído. {len(blocos)} blocos salvos em '{arquivo_saida}'.")

if __name__ == "__main__":
    main()
