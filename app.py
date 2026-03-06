import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
from utils import plots
import os

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(
    page_title="Credit Horizon | Semantix", 
    page_icon="💳", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS (Tenta carregar o estilo se existir)
try:
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except: pass

# --- 2. CARREGAMENTO ---
@st.cache_data
def load_data():
    if os.path.exists("data/german_credit_data.csv"):
        return pd.read_csv("data/german_credit_data.csv")
    return None

@st.cache_resource
def load_model():
    if os.path.exists("models/credit_model.pkl"):
        return joblib.load("models/credit_model.pkl")
    return None

df = load_data()
pkg = load_model()

if df is None or pkg is None:
    st.error("⚠️ Dados ou Modelo não encontrados. Rode o 'ml_engine.py' primeiro.")
    st.stop()

model = pkg['model']
encoders = pkg['encoders']
features_order = pkg['features']

# --- 3. BARRA LATERAL (Navegação) ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2822/2822582.png", width=60)
st.sidebar.title("Credit Horizon")
st.sidebar.markdown("**Powered by Semantix**")
st.sidebar.divider()

menu = st.sidebar.radio("Navegação", ["Dashboard (EDA)", "Simulador AI"])

# --- INFORMAÇÃO SOBRE O PROJETO ---
st.sidebar.info(
    """
    **Sobre o Projeto**
    
    Este app utiliza Machine Learning (Random Forest) para prever inadimplência em operações de crédito.
    
    *Desenvolvido por Diogo Alves*
    """
)

# --- 4. PÁGINAS DO APP ---

# === DASHBOARD ===
if menu == "Dashboard (EDA)":
    st.title("📊 Análise de Carteira de Crédito")
    st.markdown("Visão geral dos perfis de risco baseada no histórico bancário.")
    
    # KPIs
    c1, c2, c3 = st.columns(3)
    c1.metric("Total de Clientes", len(df))
    c2.metric("Ticket Médio", f"€ {df['amount'].mean():,.2f}")
    c3.metric("Idade Média", f"{int(df['age'].mean())} anos")
    
    st.divider()
    
    # Linha 1 de Gráficos
    g1, g2 = st.columns(2)
    with g1: 
        st.subheader("Distribuição de Idade")
        st.plotly_chart(plots.plot_histograma_idade(df), use_container_width=True)
    with g2: 
        st.subheader("Relação Valor x Prazo")
        st.plotly_chart(plots.plot_dispersao_amount(df), use_container_width=True)
    
    # Linha 2
    st.subheader("Análise por Finalidade")
    st.plotly_chart(plots.plot_boxplot_purpose(df), use_container_width=True)

# === SIMULADOR ===
elif menu == "Simulador AI":
    st.title("🤖 Simulador de Risco (Random Forest)")
    st.markdown("Preencha os dados abaixo para calcular o **Score de Crédito** em tempo real.")

    with st.form("simulador"):
        # Layout organizado em 3 colunas temáticas (como o anterior)
        c1, c2, c3 = st.columns(3)
        
        # Coluna 1: Dados Pessoais
        with c1:
            st.markdown("### 👤 Dados Pessoais")
            age = st.number_input("Idade", 18, 90, 30)
            
            # Pega opções do encoder mas usa label amigável
            opt_sex = list(encoders['personal_status_sex'].classes_)
            sex = st.selectbox("Estado Civil / Gênero", opt_sex)
            
            opt_housing = list(encoders['housing'].classes_)
            housing = st.selectbox("Tipo de Moradia", opt_housing)
            
            opt_job = list(encoders['job'].classes_)
            job = st.selectbox("Ocupação", opt_job)
            
        # Coluna 2: Situação Financeira
        with c2:
            st.markdown("### 💰 Financeiro")
            opt_stat = list(encoders['status'].classes_)
            status = st.selectbox("Status da Conta Corrente", opt_stat)
            
            opt_sav = list(encoders['savings'].classes_)
            savings = st.selectbox("Saldo em Poupança", opt_sav)
            
            opt_hist = list(encoders['credit_history'].classes_)
            history = st.selectbox("Histórico de Crédito", opt_hist)
        
        # Coluna 3: O Empréstimo
        with c3:
            st.markdown("### 🏦 O Empréstimo")
            amount = st.number_input("Valor Solicitado (€)", 100, 20000, 2500)
            duration = st.number_input("Prazo (Meses)", 4, 72, 24)
            
            opt_purp = list(encoders['purpose'].classes_)
            purpose = st.selectbox("Finalidade", opt_purp)

        # Botão de Ação Centralizado
        st.markdown("<br>", unsafe_allow_html=True)
        submit = st.form_submit_button("CALCULAR RISCO DE CRÉDITO", use_container_width=True)

        if submit:
            try:
                # Criar Dicionário de Input
                input_dict = {
                    'duration': duration,
                    'amount': amount,
                    'age': age,
                    # Transformar texto em número usando os encoders
                    'status': encoders['status'].transform([status])[0],
                    'credit_history': encoders['credit_history'].transform([history])[0],
                    'purpose': encoders['purpose'].transform([purpose])[0],
                    'savings': encoders['savings'].transform([savings])[0],
                    'personal_status_sex': encoders['personal_status_sex'].transform([sex])[0],
                    'housing': encoders['housing'].transform([housing])[0],
                    'job': encoders['job'].transform([job])[0]
                }
                
                # Converter para DF e garantir ordem das colunas
                X_input = pd.DataFrame([input_dict])
                X_input = X_input[features_order] 
                
                # Predição
                prediction = model.predict(X_input)[0]
                proba = model.predict_proba(X_input)[0]
                
                # Probabilidade da Classe "Bad" (Risco)
                # Assumindo que a classe 1 é 'bad' ou 'risk' no seu mapeamento
                risk_prob = proba[1] 
                
                st.divider()
                
                # Exibição do Resultado
                k1, k2 = st.columns([1,2])
                
                with k1:
                    if risk_prob > 0.5:
                        st.error("🚨 **ALTO RISCO**")
                        st.metric("Probabilidade de Default", f"{risk_prob*100:.1f}%")
                    else:
                        st.success("✅ **APROVADO**")
                        st.metric("Score de Segurança", f"{(1-risk_prob)*100:.1f}%")
                        
                with k2:
                    st.write("**Análise do Modelo:**")
                    st.progress(risk_prob)
                    if risk_prob > 0.5:
                        st.caption("O perfil apresenta características similares a clientes com histórico de inadimplência.")
                    else:
                        st.caption("O perfil é estatisticamente seguro baseando-se no histórico da carteira.")
            
            except Exception as e:
                st.error(f"Erro no cálculo: {e}")

# Footer
st.markdown('<div class="footer">Desenvolvido por Diogo Alves | Projeto Semantix</div>', unsafe_allow_html=True)