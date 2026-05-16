import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
from utils import plots
import os

# Importa a função de inferência da nossa nova estrutura
from src.predict import calcular_risco

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(
    page_title="Credit Horizon | Semantix", 
    page_icon="💳", 
    layout="wide",
    initial_sidebar_state="expanded"
)

try:
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except: pass

# --- 2. CARREGAMENTO ---
@st.cache_data
def load_data():
    if os.path.exists("data/raw/german_credit_data.csv"):
        return pd.read_csv("data/raw/german_credit_data.csv")
    return None

@st.cache_resource
def load_model():
    if os.path.exists("models/credit_model.pkl"):
        return joblib.load("models/credit_model.pkl")
    return None

df = load_data()
pkg = load_model()

if df is None or pkg is None:
    st.error("⚠️ Dados ou Modelo não encontrados. Execute 'python src/train.py' primeiro.")
    st.stop()

encoders = pkg['encoders']

# --- 3. BARRA LATERAL ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2822/2822582.png", width=60)
st.sidebar.title("Credit Horizon")
st.sidebar.markdown("**Powered by Semantix**")
st.sidebar.divider()
menu = st.sidebar.radio("Navegação", ["Dashboard (EDA)", "Simulador AI"])

st.sidebar.info("**Sobre o Projeto**\n\nEste app utiliza Machine Learning (Random Forest) para prever inadimplência.\n\n*Desenvolvido por Diogo Alves*")

# --- 4. PÁGINAS DO APP ---
if menu == "Dashboard (EDA)":
    st.title("📊 Análise de Carteira de Crédito")
    st.markdown("Visão geral dos perfis de risco baseada no histórico bancário.")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Total de Clientes", len(df))
    c2.metric("Ticket Médio", f"€ {df['amount'].mean():,.2f}")
    c3.metric("Idade Média", f"{int(df['age'].mean())} anos")
    
    st.divider()
    
    g1, g2 = st.columns(2)
    with g1: 
        st.subheader("Distribuição de Idade")
        st.plotly_chart(plots.plot_histograma_idade(df), use_container_width=True)
    with g2: 
        st.subheader("Relação Valor x Prazo")
        st.plotly_chart(plots.plot_dispersao_amount(df), use_container_width=True)
    
    st.subheader("Análise por Finalidade")
    st.plotly_chart(plots.plot_boxplot_purpose(df), use_container_width=True)

elif menu == "Simulador AI":
    st.title("🤖 Simulador de Risco (Random Forest)")
    st.markdown("Preencha os dados abaixo para calcular o **Score de Crédito** em tempo real.")

    with st.form("simulador"):
        c1, c2, c3 = st.columns(3)
        
        with c1:
            st.markdown("### 👤 Dados Pessoais")
            age = st.number_input("Idade", 18, 90, 30)
            sex = st.selectbox("Estado Civil / Gênero", list(encoders['personal_status_sex'].classes_))
            housing = st.selectbox("Tipo de Moradia", list(encoders['housing'].classes_))
            job = st.selectbox("Ocupação", list(encoders['job'].classes_))
            
        with c2:
            st.markdown("### 💰 Financeiro")
            status = st.selectbox("Status da Conta Corrente", list(encoders['status'].classes_))
            savings = st.selectbox("Saldo em Poupança", list(encoders['savings'].classes_))
            history = st.selectbox("Histórico de Crédito", list(encoders['credit_history'].classes_))
        
        with c3:
            st.markdown("### 🏦 O Empréstimo")
            amount = st.number_input("Valor Solicitado (€)", 100, 20000, 2500)
            duration = st.number_input("Prazo (Meses)", 4, 72, 24)
            purpose = st.selectbox("Finalidade", list(encoders['purpose'].classes_))

        st.markdown("<br>", unsafe_allow_html=True)
        submit = st.form_submit_button("CALCULAR RISCO DE CRÉDITO", use_container_width=True)

        if submit:
            try:
                # 1. Agrupamos as respostas da tela
                input_dict = {
                    'duration': duration, 'amount': amount, 'age': age,
                    'status': status, 'credit_history': history, 'purpose': purpose,
                    'savings': savings, 'personal_status_sex': sex, 'housing': housing, 'job': job
                }
                
                # 2. Invocamos a regra de negócio limpa da camada 'src'
                risk_prob = calcular_risco(input_dict, pkg)
                
                # 3. Exibição Visual
                st.divider()
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

st.markdown('<div class="footer">Desenvolvido por Diogo Alves | Projeto Semantix</div>', unsafe_allow_html=True)