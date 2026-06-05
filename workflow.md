#Seção 2 — Estratégia de Classificação Taxonômica
#1. Definição do Alvo Molecular
#A região V3-V4 do gene 16S rRNA foi selecionada para o treinamento do classificador Naive Bayes.

#Justificativa Técnica:
#A escolha baseia-se na necessidade de equilíbrio entre o comprimento do amplicon (~460 bp) e o poder de discriminação taxonômica. Em matrizes complexas de interesse agrícola (solo e rizosfera), as regiões V3-V4 apresentam maior robustez para a identificação de gêneros fixadores de nitrogênio e promotores de crescimento vegetal, além de apresentarem menor taxa de amplificação inespecífica de DNA de cloroplastos quando comparadas às regiões V1-V2.

#2.# Seleção de Primers
#341F: 5'-CCTACGGGNGGCWGCAG-3'
#
#805R: 5'-GACTACHVGGGTATCTAATCC-3'

#A utilização do set de primers 341F/805R justifica-se pela sua ampla adoção em protocolos de metabarcoding (ex: Illumina MiSeq 2x300bp), garantindo que o banco de referência curado seja compatível com os dados de sequenciamento gerados rotineiramente no laboratório.

#3. Pipeline de Treinamento (QIIME 2
#O workflow de treinamento utiliza a implementação Naive Bayes do plugin feature-classifier. O processo é sumarizado nos comandos abaixo:
# 1. Conversão dos dados curados (Seção 1) para artefatos .qza
qiime tools import \
  --type 'FeatureData[Sequence]' \
  --input-path 1-curadoria/sequencias_curadas.fasta \
  --output-path reference_seqs.qza

qiime tools import \
  --type 'FeatureData[Taxonomy]' \
  --input-format HeaderlessTSVTaxonomyFormat \
  --input-path 1-curadoria/taxonomia_curada.tsv \
  --output-path reference_taxonomy.qza

# 2. In silico PCR (Trimming)
# Recorte do banco de dados para a região delimitada pelos primers 341F/805R
qiime feature-classifier extract-reads \
  --i-sequences reference_seqs.qza \
  --p-f-primer CCTACGGGNGGCWGCAG \
  --p-r-primer GACTACHVGGGTATCTAATCC \
  --p-min-length 400 \
  --p-max-length 500 \
  --o-reads v3v4_ref_seqs.qza

# 3. Fit do Modelo
qiime feature-classifier fit-classifier-naive-bayes \
  --i-reference-reads v3v4_ref_seqs.qza \
  --i-reference-taxonomy reference_taxonomy.qza \
  --o-classifier agro_intecso_v3v4_classifier.qza
  
  