# 🎓 Sistema de Boletim Escolar Digital

Este projeto automatiza a geração de boletins escolares a partir de arquivos "Mapão" do Excel (XLSX). Ele transforma dados brutos em uma interface web interativa, visual e pronta para impressão.

## 📁 Estrutura do Projeto

*   `index.html`: Interface principal para visualização dos boletins.
*   `📂 data/`: Contém os dados processados em formato JSON (`data.js`).
*   `📂 scripts/`: Scripts Python para extração e conversão de dados.
*   `📂 sources/`: Pasta destinada aos arquivos Excel originais (Mapão).
*   `📂 styles/`: Contém as folhas de estilo CSS (`style.css`).

## 🚀 Funcionalidades Principais

-   **Seletor de Alunos:** Dropdown para alternar instantaneamente entre os alunos da turma.
-   **Farol de Frequência:** Indicadores visuais coloridos para a frequência geral:
    -   🟢 **Verde:** ≥ 90%
    -   🟡 **Amarelo:** 85% a 89%
    -   🔴 **Vermelho:** < 85%
-   **Destaque de Notas:** Notas abaixo de 5,0 (ou menções EP/ED) são destacadas automaticamente em **vermelho**.
-   **Cálculo de Média:** O sistema gera uma prévia da nota final (5º conceito) baseada na média aritmética dos bimestres preenchidos.
-   **Status de Atividade:** Identificação visual para alunos inativos na turma (Transferidos, Baixa, etc.).
-   **Modo de Impressão:** Layout otimizado para gerar PDF ou imprimir o boletim individual sem os controles da web.

## 🛠️ Como Atualizar os Dados

Sempre que houver um novo arquivo de Mapão ou atualização de notas:

1. Coloque o arquivo `.xlsx` atualizado na pasta `sources/`.
2. Dê um duplo clique no arquivo `atualizar_boletim.bat` na raiz do projeto.
3. O script irá processar os dados em Python e enviar as atualizações automaticamente para o GitHub.

*(Nota: Caso queira fazer a extração manualmente sem enviar para o GitHub, você ainda pode rodar `python scripts/extract_data.py` no terminal).*

## 📋 Requisitos

-   **Navegador:** Qualquer navegador moderno (Chrome, Edge, Firefox).
-   **Extração de Dados:** Python 3.x com a biblioteca `pandas` e `openpyxl`.
