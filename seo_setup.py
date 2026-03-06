import streamlit as st
import os
import shutil

# --- CONFIGURAÇÕES DO SEU SEO (ATUALIZADAS PARA O CREDIT HORIZON) ---
TITLE = "Credit Horizon | Simulador de Risco de Crédito AI"
DESCRIPTION = "Aplicação de Machine Learning (Random Forest) para análise preditiva e mitigação de risco de crédito. Desenvolvido em parceria com a Semantix."
KEYWORDS = "Machine Learning, Risco de Crédito, Random Forest, Python, Streamlit, Data Science, Semantix, EBAC"
AUTHOR = "Diogo Alves"
IMAGE_URL = "https://avatars.githubusercontent.com/u/30360463?v=4" # Pode manter sua foto ou colocar um print do dashboard
SITE_URL = "https://credit.diogolumao.com.br"

# --- SCRIPT DO MICROSOFT CLARITY ---
CLARITY_SCRIPT = """
<script type="text/javascript">
    (function(c,l,a,r,i,t,y){
        c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    })(window, document, "clarity", "script", "uu3omstqqc");
</script>
"""

def update_index_html():
    streamlit_path = os.path.dirname(st.__file__)
    index_path = os.path.join(streamlit_path, "static", "index.html")

    backup_path = index_path + ".backup"
    if not os.path.exists(backup_path):
        shutil.copy(index_path, backup_path)

    with open(index_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Ícone do Cartão de Crédito 💳 (Atualizado para combinar com o app.py)
    favicon_emoji = """
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>💳</text></svg>">
    """

    # Bloco completo de Meta Tags
    meta_tags = f"""
    {CLARITY_SCRIPT}
    <title>{TITLE}</title>
    <meta name="description" content="{DESCRIPTION}">
    <meta name="keywords" content="{KEYWORDS}">
    <meta name="author" content="{AUTHOR}">
    
    <meta property="og:title" content="{TITLE}">
    <meta property="og:description" content="{DESCRIPTION}">
    <meta property="og:image" content="{IMAGE_URL}">
    <meta property="og:url" content="{SITE_URL}">
    
    {favicon_emoji}
    """

    # --- REALIZANDO AS SUBSTITUIÇÕES ---

    # 1. Altera o Idioma de EN para pt-BR
    html_content = html_content.replace('<html lang="en">', '<html lang="pt-BR">')

    # 2. Injeta as Meta Tags e o Clarity no <head>
    html_content = html_content.replace("<title>Streamlit</title>", "")
    html_content = html_content.replace("<head>", f"<head>\n{meta_tags}")

    # 3. Altera a mensagem do Noscript
    html_content = html_content.replace(
        "You need to enable JavaScript to run this app.",
        f"Carregando {TITLE}...",
    )

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print("✅ Sucesso: Idioma alterado para pt-BR, Clarity e SEO injetados para o Credit Horizon!")

if __name__ == "__main__":
    update_index_html()