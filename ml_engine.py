import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

# --- CONFIGURAÇÃO ---
DATA_PATH = 'data/german_credit_data.csv'
MODEL_PATH = 'models/credit_model.pkl'

def carregar_dados():
    print("🔄 Carregando dataset local...")
    if os.path.exists(DATA_PATH):
        try:
            # O separador pode ser virgula ou ponto-virgula dependendo da sua fonte
            # Vamos tentar ler padrão, se der erro, ajustamos
            df = pd.read_csv(DATA_PATH)
            print(f"✅ Dados carregados: {df.shape[0]} linhas e {df.shape[1]} colunas.")
            return df
        except Exception as e:
            print(f"❌ Erro ao ler CSV: {e}")
            return None
    else:
        print("❌ Arquivo 'data/german_credit_data.csv' não encontrado.")
        return None

def processar_dados(df):
    print("⚙️ Processando colunas...")
    
    # Selecionamos as colunas mais relevantes para o simulador
    # Nomes baseados no seu cabeçalho enviado
    target_col = 'credit_risk' # 0 ou 1
    
    features = [
        'duration', 'amount', 'age',  # Numéricas
        'status', 'credit_history', 'purpose', 'savings', 
        'personal_status_sex', 'housing', 'job' # Categóricas
    ]
    
    # Filtrar apenas o que existe no DF (segurança)
    cols_to_use = [c for c in features if c in df.columns] + [target_col]
    df_clean = df[cols_to_use].copy()
    
    # Tratar Categóricas
    encoders = {}
    categorical_cols = [c for c in features if c in df_clean.columns and df_clean[c].dtype == 'O']
    
    for col in categorical_cols:
        le = LabelEncoder()
        # Converte para string para garantir e treina o encoder
        df_clean[col] = le.fit_transform(df_clean[col].astype(str))
        encoders[col] = le
        print(f"   -> Coluna '{col}' codificada.")
        
    return df_clean, encoders, features

def treinar_modelo():
    df = carregar_dados()
    if df is None: return

    df_model, encoders, features_used = processar_dados(df)
    
    target = 'credit_risk'
    
    # Separar X e y
    X = df_model.drop(target, axis=1)
    y = df_model[target]
    
    # Dividir Treino e Teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    
    print("🧠 Treinando Random Forest...")
    model = RandomForestClassifier(n_estimators=200, random_state=42, max_depth=12)
    model.fit(X_train, y_train)
    
    # Avaliar
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    
    print("-" * 30)
    print(f"🏆 Acurácia do Modelo: {acc:.2%}")
    print("Nota: Acima de 70% é excelente para risco de crédito.")
    print("-" * 30)
    
    # Salvar tudo que o App precisa
    pacote = {
        'model': model,
        'encoders': encoders,
        'features': X.columns.tolist(),
        'target_col': target
    }
    
    if not os.path.exists('models'):
        os.makedirs('models')
        
    joblib.dump(pacote, MODEL_PATH)
    print(f"💾 Modelo salvo em: {MODEL_PATH}")

if __name__ == "__main__":
    treinar_modelo()