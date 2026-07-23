# 📊 Dashboard de Gestão Escolar & Consolidação de Boletins (Mapão 2026)

Aplicação web estática e pipeline de dados em Python para extração, automação e visualização consolidada de notas e desempenhos acadêmicos por turma e bimestre.

---

## 🛠️ Tecnologias Utilizadas

- **Pipeline de Dados & Parsing:** Python 3 (openpyxl / pandas)
- **Frontend / Interface:** HTML5, CSS3 moderno (Flexbox/Grid), JavaScript Vanilla
- **Automação de Execução:** Windows Batch Script (`.bat`)
- **Desenvolvimento Assistido por IA:** Claude / ChatGPT / Gemini Agent Protocols (`.agents/AGENTS.md`)

---

## 💡 Desenvolvimento Assistido por Inteligência Artificial (AI Transparency)

Este projeto foi construído utilizando metodologias de **Engenharia de Software Assistida por IA (AI-Driven Development)**. O fluxo de trabalho combinou supervisão arquitetural humana rigorosa com aceleração do ciclo de código via Agentes de IA:

### 🤖 Papel da IA no Projeto:
1. **Geração e Refatoração de Scripts:** Auxílio na construção da lógica de parsing do script Python (`extract_data.py`) para leitura das planilhas de origem (`sources/*.xlsx`).
2. **Prototipagem de Interface:** Criação da estrutura base do frontend estático e estilização CSS responsiva.
3. **Documentação e Protocolos:** Estruturação das regras operacionais documentadas em `.agents/AGENTS.md`.

### 🧠 Papel Humano (Engenharia & Validação):
1. **Arquitetura & Requisitos:** Modelagem da estrutura de dados (`data.js`) e definição dos fluxos de atualização.
2. **Engenharia de Prompt & Raciocínio:** Direcionamento preciso das instruções, contexto pedagógico e restrições de integridade.
3. **Code Review & Troubleshooting:** Validação dos testes de extração, correção de bugs de layout e tratamento de exceções de planilhas.

---

## 📂 Estrutura do Repositório

```text
├── .agents/              # Instruções e diretrizes operacionais dos Agentes de IA
├── data/                 # Dados consolidados gerados em formato JavaScript/JSON (data.js)
├── scripts/              # Pipeline em Python (extract_data.py) para extração de planilhas
├── sources/              # Planilhas de origem em Excel (1º e 2º Bimestres)
├── styles/               # Folhas de estilo CSS
├── atualizar_boletim.bat # Script Batch para execução automatizada do pipeline no Windows
├── index.html            # Dashboard interativo do Mapão Escolar
└── README.md             # Documentação oficial do projeto

```

---

## 🚀 Como Executar o Projeto

### 1. Atualização dos Dados (Pipeline Python)

Caso haja novas planilhas na pasta `sources/`, execute o script Batch para reprocessar os dados:

```cmd
atualizar_boletim.bat

```

*(Ou rode manualmente o script Python: `python scripts/extract_data.py`)*

### 2. Visualização do Dashboard

Basta abrir o arquivo `index.html` em qualquer navegador web moderno (não requer servidor Node.js ou backend dinâmico).

```

