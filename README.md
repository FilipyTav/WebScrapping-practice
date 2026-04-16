# WebScrapping - Jogos Steam

Um script em Python para realizar web scraping de informações sobre jogos (preço, desenvolvedores, gêneros, metascore, etc.) da Steam.

## Estrutura do Projeto

| Diretório / Arquivo | Descrição |
| :--- | :--- |
| `src/main.py` | Ponto de entrada da aplicação. |
| `src/utils.py` | Módulo de Persistência e Auxiliares: Gerencia operações de entrada/saída (I/O) de arquivos e manipulação de dados locais. |
| `src/search.py` | Motor de Scraping / Integração: Responsável pelas requisições HTTP, parsing de HTML e comunicação com fontes externas. |
| **src/cache/** | **Repositório para armazenamento de dados temporários e resultados processados.** |
| ├─ `cache_metadata.json` | Controle de Sincronização: Armazena metadados e timestamps para validar a integridade e o ciclo de expiração do cache (TTL). |
| ├─ `game_data.json` | Base de Conhecimento Histórica: Repositório JSON contendo o índice completo de jogos consultados anteriormente para otimização de buscas. |
| └─ `game_info.md` | Snapshot de Consulta: Documento formatado contendo os detalhes detalhados da última pesquisa realizada, pronto para leitura humana. |

## Como Executar

### 1. Pré-requisitos
* **Python 3.10** ou superior.

### 2. Instalação
1. Clone o repositório para sua máquina:
```bash
git clone https://github.com/FilipyTav/WebScrapping-practice.git
cd WebScrapping-practice
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
```

- Windows:
```bash
venv\Scripts\activate
```

- Linux:
```bash
source venv/bin/activate
```

3. Instale as dependências necessárias:
```bash
pip install -r requirements.txt
```

### 3. Execução
Execute o arquivo principal:
```bash
python src/main.py
```
