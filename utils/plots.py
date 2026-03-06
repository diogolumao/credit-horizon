import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Definindo cores da Semantix/Horizonte
COLOR_GOOD = "#00CC96"  # Verde
COLOR_BAD = "#EF553B"  # Vermelho
COLOR_SEQ = ["#636EFA", "#EF553B", "#00CC96", "#AB63FA"]


def plot_distribuicao_risco(df):
    """Gráfico de Pizza: Bom vs Mau Pagador"""
    # Assumindo que na col credit_risk: 0=Mau, 1=Bom (ou vice-versa, o rótulo ajusta no app)
    fig = px.pie(
        df,
        names="credit_risk",
        title="Distribuição da Carteira (Risco)",
        color_discrete_sequence=[COLOR_BAD, COLOR_GOOD],
    )
    return fig


def plot_histograma_idade(df):
    """Histograma: Idade x Risco"""
    fig = px.histogram(
        df,
        x="age",
        color="credit_risk",
        nbins=30,
        title="Distribuição de Idade por Risco",
        color_discrete_sequence=[COLOR_BAD, COLOR_GOOD],
        opacity=0.7,
        barmode="overlay",
    )
    fig.update_layout(xaxis_title="Idade (Anos)", yaxis_title="Qtd. Clientes")
    return fig


def plot_dispersao_amount(df):
    """Dispersão: Valor x Duração"""
    fig = px.scatter(
        df,
        x="amount",
        y="duration",
        color="credit_risk",
        size="age",
        title="Valor do Crédito vs. Duração (Meses)",
        color_discrete_sequence=[COLOR_BAD, COLOR_GOOD],
        hover_data=["purpose"],
    )
    fig.update_layout(
        xaxis_title="Valor do Crédito (DM/€)", yaxis_title="Duração (Meses)"
    )
    return fig


def plot_boxplot_purpose(df):
    """Boxplot: Valor por Propósito"""
    fig = px.box(
        df,
        x="purpose",
        y="amount",
        color="credit_risk",
        title="Faixa de Valores por Finalidade do Empréstimo",
        color_discrete_sequence=[COLOR_BAD, COLOR_GOOD],
    )
    fig.update_layout(xaxis_title="Propósito", yaxis_title="Valor")
    return fig
