"""
validacao_db.py — Script de Validação de Banco de Referência 16S
Autor: Vinícius dos Santos Ribeiro
Descrição: Valida a integridade e consistência entre um arquivo FASTA
           e um arquivo de metadados taxonômicos (TSV) para uso em
           pipelines de classificação taxonômica (ex: QIIME 2).

Uso:
    python validacao_db.py <fasta_path> <tsv_path>

Exemplo:
    python validacao_db.py sequencias_curadas.fasta taxonomia_curada.tsv
"""

import sys
import os
import pandas as pd
from Bio import SeqIO


def validar_banco(fasta_path: str, tsv_path: str) -> None:
    """
    Valida a consistência entre um arquivo FASTA e um TSV de taxonomia.

    Parâmetros
    ----------
    fasta_path : str
        Caminho para o arquivo FASTA de sequências.
    tsv_path : str
        Caminho para o arquivo TSV de metadados taxonômicos.
    """
    print("\n" + "=" * 50)
    print("  VALIDAÇÃO TÉCNICA — BANCO DE REFERÊNCIA 16S")
    print("=" * 50)

    # --- Verificação de existência dos arquivos ---
    for path, label in [(fasta_path, "FASTA"), (tsv_path, "TSV")]:
        if not os.path.exists(path):
            print(f"\nERRO CRÍTICO: Arquivo {label} não encontrado: {path}")
            sys.exit(1)

    erros = 0
    relatorio = []

    # --- 1. Carregar e analisar o FASTA ---
    print("\n[1/4] Analisando sequências (FASTA)...")
    registros = list(SeqIO.parse(fasta_path, "fasta"))
    total_fasta = len(registros)
    print(f"  Total de sequências no FASTA : {total_fasta}")

    # IDs duplicados no FASTA
    fasta_ids = [r.id for r in registros]
    ids_dup_fasta = [i for i in set(fasta_ids) if fasta_ids.count(i) > 1]
    if ids_dup_fasta:
        msg = f"  ERRO: IDs duplicados no FASTA: {ids_dup_fasta}"
        print(msg); relatorio.append(msg); erros += 1
    else:
        print("  IDs duplicados no FASTA      : nenhum")

    # Sequências abaixo do limiar de comprimento
    LIMIAR_COMPRIMENTO = 200
    curtas = [r.id for r in registros if len(r.seq) < LIMIAR_COMPRIMENTO]
    if curtas:
        msg = f"  AVISO: Sequências abaixo de {LIMIAR_COMPRIMENTO}bp: {curtas}"
        print(msg); relatorio.append(msg)
    else:
        print(f"  Sequências < {LIMIAR_COMPRIMENTO}bp            : nenhuma")

    # --- 2. Carregar e analisar o TSV ---
    print("\n[2/4] Analisando metadados taxonômicos (TSV)...")
    df = pd.read_csv(tsv_path, sep='\t', header=None, names=['seq_id', 'taxonomy'])
    total_tsv = len(df)
    print(f"  Total de entradas no metadata: {total_tsv}")

    # IDs duplicados no TSV
    ids_dup_tsv = df[df.duplicated(subset='seq_id', keep=False)]['seq_id'].unique().tolist()
    if ids_dup_tsv:
        msg = f"  ERRO: IDs duplicados no TSV: {ids_dup_tsv}"
        print(msg); relatorio.append(msg); erros += 1
    else:
        print("  IDs duplicados no TSV        : nenhum")

    # Taxonomia incompleta (algum nível vazio ou ausente)
    NIVEIS_ESPERADOS = 7
    def contar_niveis(tax):
        return len([n for n in str(tax).split(';') if n.strip()])

    incompletas = df[df['taxonomy'].apply(contar_niveis) < NIVEIS_ESPERADOS]['seq_id'].tolist()
    if incompletas:
        msg = f"  AVISO: Taxonomia incompleta (< {NIVEIS_ESPERADOS} níveis): {incompletas}"
        print(msg); relatorio.append(msg)
    else:
        print(f"  Entradas com taxonomia incompleta: nenhuma")

    # Verificar formatação dos prefixos (k__, p__, etc.)
    invalidos_formato = df[~df['taxonomy'].str.contains('k__') |
                           ~df['taxonomy'].str.contains(';')]['seq_id'].tolist()
    if invalidos_formato:
        msg = f"  ERRO: Formatação inválida (sem prefixo k__ ou separador ;): {invalidos_formato}"
        print(msg); relatorio.append(msg); erros += 1
    else:
        print("  Formatação taxonômica (k__;...) : OK")

    # --- 3. Sincronização FASTA × TSV ---
    print("\n[3/4] Verificando integridade entre arquivos...")
    fasta_set = set(fasta_ids)
    tsv_set = set(df['seq_id'])

    apenas_fasta = sorted(fasta_set - tsv_set)
    apenas_tsv = sorted(tsv_set - fasta_set)

    if apenas_fasta:
        msg = f"  ERRO: IDs no FASTA sem entrada no TSV: {apenas_fasta}"
        print(msg); relatorio.append(msg); erros += 1
    else:
        print("  IDs no FASTA sem metadata    : nenhum")

    if apenas_tsv:
        msg = f"  ERRO: IDs no TSV sem sequência no FASTA: {apenas_tsv}"
        print(msg); relatorio.append(msg); erros += 1
    else:
        print("  IDs no TSV sem sequência     : nenhum")

    # --- 4. Resumo final ---
    print("\n[4/4] Gerando resumo...")
    print("\n" + "-" * 50)
    print(f"  Sequências no FASTA          : {total_fasta}")
    print(f"  Entradas no TSV              : {total_tsv}")
    print(f"  Erros críticos encontrados   : {erros}")
    print("-" * 50)

    if erros == 0:
        print("  RESULTADO FINAL: BANCO APROVADO ✓")
    else:
        print(f"  RESULTADO FINAL: BANCO REPROVADO — {erros} erro(s) crítico(s)")
    print("-" * 50 + "\n")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    fasta_input = sys.argv[1]
    tsv_input = sys.argv[2]
    validar_banco(fasta_input, tsv_input)
