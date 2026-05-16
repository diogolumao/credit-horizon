# 💳 Credit Horizon | Semantix Case

![Python](https://img.shields.io/badge/Python-3.9-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit)
![Scikit-Learn](https://img.shields.io/badge/Scikit_Learn-Machine_Learning-F7931E?style=for-the-badge&logo=scikit-learn)
![Docker](https://img.shields.io/badge/Docker-Container-2496ED?style=for-the-badge&logo=docker)
![Status](https://img.shields.io/badge/Status-Concluído-success?style=for-the-badge)

> **Projeto final desenvolvido em parceria com a Semantix para o curso de Analista de Dados da EBAC.**

## 📌 Nota Técnica: A Escolha Tecnológica
*O escopo original deste projeto previa o uso do Looker Studio para visualização de dados. No entanto, visando entregar uma solução mais aderente às práticas de Engenharia de Machine Learning e Produtos de Dados (core business da Semantix), optou-se pelo desenvolvimento de uma Aplicação Web Full-Stack preditiva utilizando Python e Streamlit.*

* **De Descritivo para Preditivo:** Ferramentas de BI tradicionais olham para o passado. O uso do Python permitiu integrar um modelo de Inteligência Artificial em tempo real, transformando um dashboard estático em um **Simulador de Risco Ativo**.
* **Engenharia de Ponta a Ponta:** O projeto simula um ciclo real corporativo: ingestão de dados, engenharia de features, modelagem estatística, containerização (Docker) e deploy automatizado (CI/CD) em nuvem via GitHub Actions.

---

## 🎯 O Problema de Negócio
Instituições financeiras enfrentam um dilema clássico de **assimetria de informação**: conceder crédito gera lucro, mas o risco de inadimplência (default) pode comprometer a solvência da operação. A análise manual de crédito é lenta, subjetiva e cara. Bancos tradicionais tendem a negar crédito para bons pagadores por falta de histórico convencional ou assumir riscos desnecessários.

**A Solução:** Uma aplicação capaz de analisar dezenas de variáveis simultaneamente e calcular a probabilidade matemática de calote em segundos, apoiando a decisão humana com dados estatísticos.

---

## 📊 Fonte de Dados e Insights (EDA)
Utilizamos o dataset **South German Credit Data**, referência global em análise de risco, extraído do *UCI Machine Learning Repository*. 
* **Privacidade:** Dados públicos e totalmente anonimizados (LGPD Compliant).
* **Análise Exploratória:** Disponível e documentada no notebook `notebooks/01_eda_credit.ipynb`.

### Principais Insights Acionáveis:
1. **O Fator Tempo (Duração):** Empréstimos com prazos superiores a 48 meses apresentam taxa de inadimplência 40% maior. *Ação recomendada: Exigir garantias reais para aprovações longas.*
2. **A Finalidade do Recurso:** Créditos para "Educação" e "Negócios" têm inadimplência significativamente menor do que para "Veículo Novo". *Ação recomendada: Criar linhas subsidiadas para finalidades produtivas.*
3. **Bancarização e Saldo:** A ausência de conta corrente ou saldos negativos são os indicadores mais fortes de risco iminente. *Ação recomendada: Política de "Zero Crédito Desbancarizado" para novos clientes sem histórico.*

---

## 🧠 Modelagem de Machine Learning
O "cérebro" da aplicação é um modelo preditivo baseado em **Random Forest** (Floresta Aleatória).

Em vez de depender de uma única regra para aprovar ou negar crédito, o algoritmo cria centenas de "árvores de decisão" independentes (uma focada na idade, outra no histórico, outra no saldo, etc.). Ao receber um novo cliente, todas as árvores "votam" e a decisão final é baseada na maioria estatística ("Sabedoria das Multidões"). 
* **Acurácia do Modelo:** 74% (Validada em dados de teste desconhecidos, demonstrando robustez contra overfitting e alinhamento com benchmarks do setor financeiro).

---

## 📂 Arquitetura de Software e Estrutura de Pastas
O projeto foi modularizado seguindo as melhores práticas de Engenharia de Software e Ciência de Dados, separando as responsabilidades de modelagem, interface visual e infraestrutura:

```text
credit_horizon/
├── .github/workflows/      # Automação de CI/CD para deploy na VPS
├── .streamlit/             # Configurações de tema da interface
├── assets/                 # Arquivos CSS e assets visuais
├── data/                   
│   ├── raw/                # Base de dados bruta (imutável)
│   └── processed/          # Dados limpos e preparados
├── models/                 # Modelo treinado e encoders (credit_model.pkl)
├── notebooks/              # Ambiente de descoberta e experimentação
│   └── 01_eda_credit.ipynb # Análise Exploratória de Dados documentada
├── src/                    # Lógica Core (Backend ML)
│   ├── data_prep.py        # Pipelines de limpeza e encoding
│   ├── train.py            # Script para treinamento e validação do modelo
│   └── predict.py          # Lógica de inferência para consumo no frontend
├── utils/                  # Scripts auxiliares (ex: plots.py para gráficos Plotly)
├── app.py                  # Código principal da aplicação Web (Streamlit)
├── docker-compose.yml      # Orquestração do container (Produção VPS)
├── docker-compose.local.yml# Orquestração do container (Laboratório Local)
├── Dockerfile              # Imagem padrão do projeto
└── requirements.txt        # Dependências Python
```

🚀 Como Executar Localmente
Você pode executar a aplicação utilizando o Docker (recomendado) ou configurando um ambiente virtual Python manualmente.

Clone o repositório:

Bash
git clone [https://github.com/diogolumao/credit-horizon.git](https://github.com/diogolumao/credit-horizon.git)
cd credit-horizon
Opção 1: Via Docker (Recomendado)
Levante o contêiner utilizando a configuração de desenvolvimento local:

```Bash
docker compose -f docker-compose.local.yml up -d --build
```
Acesse a aplicação no navegador via: http://localhost:8530


Opção 2: Via Ambiente Virtual (Python)
Crie o ambiente, instale as dependências e rode a aplicação:

```Bash
python -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
(Opcional) Retreine o modelo gerando novos artefatos na pasta /models:

```Bash
python src/train.py
```
Suba o aplicativo Streamlit:

```Bash
streamlit run app.py
```

👨‍💻 Autor
Diogo Alves Analista de Dados & Analytics Engineer

Entre em contato:

Desenvolvido com 💙 e Python.

Eu, Diogo Alves, autorizo a cessão do meu projeto em favor da Semantix, bem como a divulgação do meu nome como autor responsável pelo projeto, uma vez que será possível incluir esse trabalho em meu portfólio. Autorizo também a divulgação dos meus contatos para a Semantix para fins exclusivos de contato profissional decorrente deste projeto.