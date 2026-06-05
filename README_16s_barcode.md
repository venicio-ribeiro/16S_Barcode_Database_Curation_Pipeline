# 🧬 16S Barcode Database Curation Pipeline

> Curadoria, validação e preparação de banco de referência 16S para classificação taxonômica com QIIME 2.

---

## Visão Geral

Este repositório contém a solução completa para curadoria de banco de dados de sequências barcode 16S, incluindo scripts de automação, workflows de classificação e estratégias de governança para uso em produção.

O pipeline cobre todo o fluxo: desde a identificação e correção de inconsistências no banco bruto até o treinamento de um classificador Naive Bayes no QIIME 2, com validação automatizada entre cada etapa.

---

## Estrutura do Repositório

```
16s-barcode-curation-pipeline/
├── 1-curadoria/
│   ├── curar_banco.py              # Script principal de curadoria automatizada
│   ├── sequencias_curadas.fasta    # Banco FASTA após curadoria
│   ├── taxonomia_curada.tsv        # Metadados taxonômicos padronizados (7 níveis)
│   └── documentacao.md             # Decisões de curadoria documentadas
│
├── 2-classificacao/
│   └── workflow.md                 # Workflow QIIME 2 para treinamento do classificador
│
├── 3-diagnostico/
│   └── diagnostico.md              # Análise do output de classificação com problemas
│
├── 4-validacao/
│   ├── validacao_db.py             # Script de validação de integridade do banco
│   └── requirements.txt            # Dependências Python
│
├── 5-governanca/
│   └── pipeline_continuo.md        # Estratégia de curadoria contínua e CI/CD
│
└── README.md
```

---

## Funcionalidades

### 1. Curadoria Automatizada (`curar_banco.py`)
- Remoção de sequências duplicadas (por conteúdo de DNA)
- Filtragem de sequências abaixo do limiar de qualidade (< 200bp)
- Reconstrução e padronização de 7 níveis taxonômicos (`k__` → `s__`)
- Atualização de sinonímias (*Propionibacterium* → *Cutibacterium*)
- Sincronização 1:1 entre FASTA e metadados

### 2. Workflow de Classificação (`workflow.md`)
- Seleção e justificativa da região V3-V4 do gene 16S
- Primers 341F/805R com justificativa técnica para matrizes agrícolas
- Pipeline QIIME 2 completo: importação → PCR in silico → treinamento Naive Bayes

### 3. Diagnóstico de Problemas (`diagnostico.md`)
- Análise de padrões problemáticos no output do classificador
- Causa-raiz de sequências Unassigned e truncamentos taxonômicos
- Relação entre problemas de curadoria e erros de classificação

### 4. Script de Validação (`validacao_db.py`)
- Validação automatizada de integridade entre FASTA e TSV
- Detecção de IDs duplicados, sequências curtas e taxonomia incompleta
- Verificação de formatação de prefixos taxonômicos
- Relatório de resultado com saída clara no terminal

### 5. Governança e Curadoria Contínua (`pipeline_continuo.md`)
- Estratégia de versionamento semântico (SemVer) com Git
- Rastreabilidade por hash SHA-256 e metadados de proveniência
- CI/CD com GitHub Actions para validação automática a cada Pull Request
- Critérios mensuráveis de inclusão/exclusão de novas sequências

---

## Como Usar

### Pré-requisitos

```bash
pip install -r 4-validacao/requirements.txt
```

### Executar curadoria

```bash
python 1-curadoria/curar_banco.py
```

Gera `sequencias_curadas.fasta` e `taxonomia_curada.tsv` na pasta `1-curadoria/`.

### Validar banco curado

```bash
python 4-validacao/validacao_db.py \
  1-curadoria/sequencias_curadas.fasta \
  1-curadoria/taxonomia_curada.tsv
```

**Saída esperada:**
```
==================================================
  VALIDAÇÃO TÉCNICA — BANCO DE REFERÊNCIA 16S
==================================================

[1/4] Analisando sequências (FASTA)...
  Total de sequências no FASTA : 12
  IDs duplicados no FASTA      : nenhum
  Sequências < 200bp           : nenhuma

[2/4] Analisando metadados taxonômicos (TSV)...
  Total de entradas no metadata: 12
  IDs duplicados no TSV        : nenhum
  Entradas com taxonomia incompleta: nenhuma
  Formatação taxonômica (k__;...): OK

[3/4] Verificando integridade entre arquivos...
  IDs no FASTA sem metadata    : nenhum
  IDs no TSV sem sequência     : nenhum

[4/4] Gerando resumo...
--------------------------------------------------
  Sequências no FASTA          : 12
  Entradas no TSV              : 12
  Erros críticos encontrados   : 0
--------------------------------------------------
  RESULTADO FINAL: BANCO APROVADO ✓
--------------------------------------------------
```

### Treinar classificador (QIIME 2)

Siga o workflow detalhado em `2-classificacao/workflow.md`.

---

## Dependências

```
biopython>=1.81
pandas>=2.0.0
```

---

## Decisões Técnicas

| Decisão | Justificativa |
|---|---|
| Região V3-V4 (341F/805R) | Maior poder discriminatório em matrizes de solo/rizosfera; menor amplificação inespecífica de cloroplastos vs V1-V2 |
| Limiar de comprimento ≥ 200bp | Sequências muito curtas geram ruído estatístico no Naive Bayes |
| Reconstrução com 7 níveis | Compatibilidade com o formato esperado pelo `feature-classifier` do QIIME 2 |
| Atualização de sinonímias | Consistência com bases globais (SILVA, NCBI); *Propionibacterium* → *Cutibacterium* conforme reclassificação de 2016 |
| Docker (curadoria contínua) | Reprodutibilidade do ambiente de execução em produção |

---

## Autor

**Vinícius dos Santos Ribeiro**  
Analista de Bioinformática | Pipelines NGS · Genômica de Procariotos · Docker  
Mestrando em Biologia Celular e Molecular — UFRGS  

[GitHub](https://github.com/venicio-ribeiro) · [LinkedIn](https://linkedin.com/in/viníciusribeiro117-biotec) · vini.biotec@gmail.com
