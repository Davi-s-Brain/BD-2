import ast
import re
import argparse
import sys

def parse_tuple_line(line):
    """
    Extrai um tuple Python de uma linha:
    - Substitui 'true'/'false' por 'True'/'False' para ast.literal_eval.
    - Busca do primeiro '(' até o último ')'.
    Retorna a tupla se for válida, ou None caso não seja uma linha de tupla.
    """
    stripped = line.strip()
    # Deve começar com '('
    if not stripped.startswith('('):
        return None
    # Encontrar posição do último ')'
    last = stripped.rfind(')')
    if last == -1:
        return None
    content = stripped[:last+1]
    # Substituir booleans estilo SQL por estilo Python
    content = re.sub(r'\btrue\b', 'True', content, flags=re.IGNORECASE)
    content = re.sub(r'\bfalse\b', 'False', content, flags=re.IGNORECASE)
    try:
        val = ast.literal_eval(content)
        if isinstance(val, tuple):
            return val
    except Exception as e:
        # Debug: exiba no stderr a linha que falhou, se quiser investigar
        print(f"[DEBUG] literal_eval falhou para linha: {repr(stripped)} -> {e}", file=sys.stderr)
        return None

def format_sql_tuple_with_id(id_value, tup):
    """
    Formata a tupla pré-existente adicionando id_value no início.
    Strings escapam apóstrofos; bool vira TRUE/FALSE; None vira NULL; números sem aspas.
    Retorna algo como "(id, 'texto', 123, TRUE),"
    """
    parts = []
    for v in (id_value,) + tup:
        if isinstance(v, str):
            esc = v.replace("'", "''")
            parts.append(f"'{esc}'")
        elif isinstance(v, bool):
            parts.append('TRUE' if v else 'FALSE')
        elif v is None:
            parts.append('NULL')
        else:
            parts.append(str(v))
    return '(' + ', '.join(parts) + '),'

def process_file(input_path, output_path, start_id):
    current_id = start_id
    with open(input_path, 'r', encoding='utf-8') as fin, open(output_path, 'w', encoding='utf-8') as fout:
        for lineno, line in enumerate(fin, start=1):
            tup = parse_tuple_line(line)
            if tup is not None:
                new_line = format_sql_tuple_with_id(current_id, tup) + '\n'
                fout.write(new_line)
                current_id += 1
            else:
                fout.write(line)
    print(f"Processado. Próximo ID após conclusão será {current_id}.")

def main():
    parser = argparse.ArgumentParser(description="Inserir IDs sequenciais em tuplas existentes no arquivo.")
    parser.add_argument('input_file', help="Arquivo de entrada contendo linhas de tuplas (sem ID).")
    parser.add_argument('output_file', help="Arquivo de saída com IDs inseridos.")
    parser.add_argument('--start-id', type=int, required=True, help="ID inicial para a primeira tupla encontrada.")
    args = parser.parse_args()

    try:
        process_file(args.input_file, args.output_file, args.start_id)
    except Exception as e:
        print(f"Erro: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()