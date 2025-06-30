import argparse

def adicionar_parenteses(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as fin, open(output_file, 'w', encoding='utf-8') as fout:
        for linha in fin:
            linha = linha.strip().rstrip(',')  # Remove espaços e vírgula final, se houver
            if linha:  # Evita linhas vazias
                nova_linha = f'({linha}),\n'
                fout.write(nova_linha)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Adiciona parênteses no início e final de cada linha.")
    parser.add_argument('input_file', help="Arquivo de entrada.")
    parser.add_argument('output_file', help="Arquivo de saída.")
    args = parser.parse_args()

    adicionar_parenteses(args.input_file, args.output_file)