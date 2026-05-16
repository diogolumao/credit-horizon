import pandas as pd
import os
from sklearn.preprocessing import LabelEncoder

def carregar_dados(data_path='data/raw/german_credit_data.csv'):
    """Carrega o dataset bruto da pasta raw."""
    print("🔄 Carregando dataset local...")
    if os.path.exists(data_path):
        try:
            df = pd.read_csv(data_path)
            print(f"✅ Dados carregados: {df.shape[0]} linhas e {df.shape[1]} colunas.")
            return df
        except Exception as e:
            print(f"❌ Erro ao ler CSV: {e}")
            return None
    else:
        print(f"❌ Arquivo '{data_path}' não encontrado.")
        return None

def processar_dados(df):
    """Limpa e aplica o encoding nas variáveis categóricas."""
    print("⚙️ Processando colunas...")
    target_col = 'credit_risk' 
    
    features = [
        'duration', 'amount', 'age',  
        'status', 'credit_history', 'purpose', 'savings', 
        'personal_status_sex', 'housing', 'job' 
    ]
    
    cols_to_use = [c for c in features if c in df.columns] + [target_col]
    df_clean = df[cols_to_use].copy()
    
    encoders = {}
    categorical_cols = [c for c in features if c in df_clean.columns and df_clean[c].dtype == 'O']
    
    for col in categorical_cols:
        le = LabelEncoder()
        df_clean[col] = le.fit_transform(df_clean[col].astype(str))
        encoders[col] = le
        print(f"   -> Coluna '{col}' codificada.")
        
    return df_clean, encoders, features