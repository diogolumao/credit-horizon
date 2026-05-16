import pandas as pd

def calcular_risco(input_dict, pkg_modelo):
    """
    Recebe o dicionário com os inputs do usuário e o pacote do modelo.
    Retorna a probabilidade de risco de crédito.
    """
    model = pkg_modelo['model']
    encoders = pkg_modelo['encoders']
    features_order = pkg_modelo['features']

    # Cópia para não alterar o dicionário original
    dados_processados = input_dict.copy()

    # Transforma texto em número usando os encoders em loop dinâmico
    cols_categoricas = ['status', 'credit_history', 'purpose', 'savings', 'personal_status_sex', 'housing', 'job']
    for col in cols_categoricas:
        dados_processados[col] = encoders[col].transform([dados_processados[col]])[0]

    # Converte para DF e garante ordem das colunas exigida pelo modelo
    X_input = pd.DataFrame([dados_processados])
    X_input = X_input[features_order] 
    
    # Probabilidade da Classe 1 (Risco/Bad)
    proba = model.predict_proba(X_input)[0]
    risk_prob = proba[1] 
    
    return risk_prob