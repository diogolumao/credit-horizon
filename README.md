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
* **Engenharia de Ponta a Ponta:** O projeto simula um ciclo real corporativo: ingestão de dados, engenharia de features, modelagem estatística, containerização (Docker) e deploy em nuvem.

---

## 🎯 O Problema de Negócio
Instituições financeiras enfrentam um dilema clássico de **assimetria de informação**: conceder crédito gera lucro, mas o risco de inadimplência (default) pode comprometer a solvência da operação. A análise manual de crédito é lenta, subjetiva e cara. Bancos tradicionais tendem a negar crédito para bons pagadores por falta de histórico convencional ou assumir riscos desnecessários.

**A Solução:** Uma aplicação capaz de analisar dezenas de variáveis simultaneamente e calcular a probabilidade matemática de calote em segundos, apoiando a decisão humana com dados estatísticos.

---

## 📊 Fonte de Dados e Insights (EDA)
Utilizamos o dataset **South German Credit Data**, referência global em análise de risco, extraído do *UCI Machine Learning Repository*. 
* **Privacidade:** Dados públicos e totalmente anonimizados (LGPD Compliant).
* **Automação:** Os dados são consumidos e pré-processados pelo script `ml_engine.py`.

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

## 📂 Estrutura do Projeto

```text
credit_horizon/
│
├── .streamlit/             # Configurações de tema da interface
├── assets/                 # Arquivos CSS e assets visuais
├── data/                   # Base de dados (german_credit_data.csv)
├── models/                 # Modelo treinado e encoders (credit_model.pkl)
├── utils/                  # Scripts auxiliares (ex: plots.py para gráficos)
├── app.py                  # Código principal da aplicação Web (Streamlit)
├── ml_engine.py            # Script de ingestão, EDA, treino e persistência do modelo
├── docker-compose.yml      # Orquestração de containers
├── Dockerfile              # Imagem da aplicação
├── requirements.txt        # Dependências do Python
└── README.md               # Documentação do projeto
🚀 Como Executar Localmente
Clone o repositório:

Bash
git clone [https://github.com/diogolumao/credit-horizon.git](https://github.com/diogolumao/credit-horizon.git)
cd credit-horizon
Crie um ambiente virtual e instale as dependências:

Bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
Treine o modelo (Gera os artefatos na pasta /models):

Bash
python ml_engine.py
Execute a aplicação:

Bash
streamlit run app.py
👨‍💻 Autor e Declaração
Diogo Alves

Portfólio: diogolumao.com.br

LinkedIn: in/diogoalves-dados

Eu, Diogo Alves, autorizo a cessão do meu projeto em favor da Semantix, bem como a divulgação do meu nome como autor responsável pelo projeto, uma vez que será possível incluir esse trabalho em meu portfólio. Autorizo também a divulgação dos meus contatos para a Semantix para fins exclusivos de contato profissional decorrente deste projeto.