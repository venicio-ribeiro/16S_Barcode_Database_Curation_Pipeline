import pandas as pd
from Bio import SeqIO
import os

def curar_dados(fasta_input, tsv_input):
    print("--- Iniciando Processo de Curadoria ---")
    
    # 1. CARREGAR METADADOS
    df = pd.read_csv(tsv_input, sep='\t')
    
    # 2. PADRONIZAÇÃO TAXONÔMICA (Reconstrução Total de 7 Níveis)
    def higienizar_taxonomia(tax):
        tax = str(tax).strip().replace(',', ';')
        
        # Prefixo padrão para os 7 níveis
        niveis = ['k__', 'p__', 'c__', 'o__', 'f__', 'g__', 's__']
        
        # Limpa os nomes originais tirando qualquer prefixo que já exista
        pedacos = []
        for p in tax.split(';'):
            p_limpo = p.strip()
            if '__' in p_limpo:
                p_limpo = p_limpo.split('__')[-1]
            if p_limpo:
                pedacos.append(p_limpo)
        
        # Reconstrói garantindo EXATAMENTE 7 níveis
        tax_final = []
        for i in range(len(niveis)):
            if i < len(pedacos):
                tax_final.append(f"{niveis[i]}{pedacos[i]}")
            else:
                # Se faltar nível (ex: parou em Gênero), completa com 'unidentified'
                tax_final.append(f"{niveis[i]}unidentified")
        
        return ";".join(tax_final)

    df['taxonomy'] = df['taxonomy'].apply(higienizar_taxonomia)
    
    # Ajuste de sinonímia
    df['taxonomy'] = df['taxonomy'].str.replace('Propionibacterium', 'Cutibacterium')

    # 3. FILTRAGEM DE SEQUÊNCIAS
    valid_records = []
    seen_sequences = set()
    
    for record in SeqIO.parse(fasta_input, "fasta"):
        seq_str = str(record.seq).upper()
        if len(seq_str) >= 200 and seq_str not in seen_sequences:
            seen_sequences.add(seq_str)
            valid_records.append(record)

    # 4. SINCRONIZAÇÃO
    ids_finais = [r.id for r in valid_records]
    df_curado = df[df['seq_id'].isin(ids_finais)].drop_duplicates(subset=['seq_id'])
    
    # 5. SALVAMENTO (Garante que salva na mesma pasta dos originais)
    diretorio = os.path.dirname(os.path.abspath(fasta_input))
    
    SeqIO.write(valid_records, os.path.join(diretorio, "sequencias_curadas.fasta"), "fasta")
    df_curado[['seq_id', 'taxonomy']].to_csv(
        os.path.join(diretorio, "taxonomia_curada.tsv"), 
        sep='\t', index=False, header=False
    )
    
    print(f"Sucesso! {len(valid_records)} sequências curadas e padronizadas.")

if __name__ == "__main__":
    import os
    try:
        path = os.path.dirname(os.path.abspath(__file__))
    except:
        path = os.getcwd()
    
    f_in = os.path.join(path, "sequencias.fasta")
    t_in = os.path.join(path, "metadata.tsv")
    
    if os.path.exists(f_in):
        curar_dados(f_in, t_in)