# Seção 5 — Proposta de Pipeline Contínuo e Governança


### 1. Versionamento e Ciclo de Vida (Git)
* **Estratégia de Branching:** Uso de branches `main` (produção) e `develop` (testes de novas sequências).
* **Releases e Tags:** Cada atualização do banco será marcada com uma Tag (ex: `v1.0.1`), seguindo o Versionamento Semântico (SemVer).
* **Changelog:** Manutenção de um arquivo `CHANGELOG.md` detalhando quais táxons foram adicionados ou corrigidos em cada versão.

### 2. Rastreabilidade e Proveniência
* **Metadados de Origem:** Cada sequência no banco deve conter campos de proveniência: `source_db` (NCBI/SILVA), `accession_number` e `download_date`.
* **Integridade por Hash:** Geração de um hash SHA-256 para cada versão do banco, garantindo que o arquivo utilizado no pipeline de análise é exatamente o que foi homologado pela curadoria.

### 3. Validações Automáticas (CI/CD)
Proponho a implementação de **GitHub Actions** que disparem o script de validação (`validacao_db.py`) automaticamente a cada *Pull Request*:
* **Pre-commit Hooks:** Impedir o commit de arquivos TSV que contenham caracteres especiais inválidos ou duplicatas.
* **Teste de Cobertura:** Verificar se todos os 7 níveis taxonômicos (`k__` a `s__`) estão preenchidos antes de permitir o merge.

### 4. Critérios de Inclusão e Exclusão (Mensuráveis)
Para manter a alta performance do classificador, adotaremos:
* **Inclusão:** Apenas sequências 16S com comprimento > 1200bp (para bancos de referência) e taxonomia confirmada em pelo menos duas bases (ex: SILVA e Greengenes).
* **Exclusão:** Remoção automática de sequências com mais de 5 caracteres ambíguos (N) ou sequências identificadas como quimeras pelo algoritmo UCHIME.

### 5. Comunicação de Mudanças (Release Notes)
A cada nova versão, será gerado um **Diff de Taxonomia**:
* Um relatório automático comparando a versão anterior e a atual, listando:
    * Quantas espécies novas foram adicionadas.
    * Quais nomes foram atualizados por mudanças na nomenclatura botânica/zoológica.
    * Impacto esperado na acurácia da classificação.