import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Importa as funções do nosso módulo de preparação
from src.data_prep import carregar_dados, processar_dados

MODEL_PATH = 'models/credit_model.pkl'

def treinar_modelo():
    df = carregar_dados()
    if df is None: return

    df_model, encoders, features_used = processar_dados(df)
    target = 'credit_risk'
    
    X = df_model.drop(target, axis=1)
    y = df_model[target]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    
    print("🧠 Treinando Random Forest...")
    model = RandomForestClassifier(n_estimators=200, random_state=42, max_depth=12)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    
    print("-" * 30)
    print(f"🏆 Acurácia do Modelo: {acc:.2%}")
    print("-" * 30)
    
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