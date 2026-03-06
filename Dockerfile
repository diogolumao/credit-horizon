FROM python:3.9-slim

WORKDIR /app

# Instala dependências básicas do sistema (Apenas o essencial e o curl para o Healthcheck)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala as dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# INJEÇÃO DE SEO: Roda o script para alterar o index.html do Streamlit dentro do container
RUN python seo_setup.py

# Expõe a porta do Streamlit
EXPOSE 8501

# Checagem de saúde do container
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Comando de inicialização
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]