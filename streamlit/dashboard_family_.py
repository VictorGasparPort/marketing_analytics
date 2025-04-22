# app_ifood_dashboard.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------
# 1. CONFIGURAÇÃO DA PÁGINA
# ---------------------------
st.set_page_config(
    page_title="📊 Análise de Clientes Ifood - Família vs. Compras",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS customizado para manter a estética clean (preto e branco) e espaçamentos adequados
st.markdown("""
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            color: #000;
            background-color: #fff;
        }
        .report-box {
            background-color: #f9f9f9; 
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid #333;
            line-height: 1.6;
            font-size: 16px;
        }
        h1, h2, h3 {
            color: #000;
        }
    </style>
    """, unsafe_allow_html=True)

# ---------------------------
# 2. CARREGAMENTO DOS DADOS COM CACHE
# ---------------------------
@st.cache_data(show_spinner=True)
def load_data(path: str) -> pd.DataFrame:
    """
    Carrega o CSV com dados dos clientes do Ifood com otimização de memória.
    
    Parâmetros:
      - path (str): Caminho do arquivo CSV.
    
    Retorna:
      - df (pd.DataFrame): DataFrame carregado.
    """
    try:
        df = pd.read_csv(path)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
        return pd.DataFrame()

# ---------------------------
# 3. FUNÇÃO DE ANÁLISE
# ---------------------------
def analisar_familia_vs_comportamento_compra(dados: pd.DataFrame,
                                              colunas_filhos=['Kidhome', 'Teenhome'],
                                              colunas_gastos=['MntTotal', 'MntSweetProducts', 'MntGoldProds']):
    """
    Analisa como o número de filhos (crianças e adolescentes) afeta o gasto total e os gastos em produtos não essenciais.
    
    Parâmetros:
      - dados (pd.DataFrame): DataFrame contendo os dados dos clientes.
      - colunas_filhos (list): Lista com os nomes das colunas que representam o número de filhos.
      - colunas_gastos (list): Lista com os nomes das colunas de gastos a serem analisadas.
    
    Retorna:
      - gastos_medios (pd.DataFrame): DataFrame com a média dos gastos agrupados pelo total de filhos.
      - relatorio (str): Relatório textual com os principais insights da análise.
    """
    # Dicionário para descrição dos gastos (pode ser ajustado conforme a necessidade)
    colunas_descricao = {
        'MntTotal': "Gasto Total",
        'MntSweetProducts': "Gastos com Produtos Doces",
        'MntGoldProds': "Gastos com Produtos Premium"
    }

    # 1. Cálculo do número total de filhos (soma das colunas indicadas)
    dados['Total_Filhos'] = dados[colunas_filhos].sum(axis=1)

    # 2. Cálculo da média de gastos por número total de filhos
    try:
        gastos_medios = dados.groupby('Total_Filhos', observed=False)[colunas_gastos].mean().reset_index()
    except Exception as e:
        st.error(f"Erro durante o agrupamento: {e}")
        return None, None

    # 3. Geração do relatório textual com os resultados
    relatorio = "### Análise de Família vs. Comportamento de Compra\n\n"
    relatorio += "Média de gastos por número total de filhos:\n\n"
    for _, row in gastos_medios.iterrows():
        relatorio += f"**Número total de filhos: {int(row['Total_Filhos'])}**\n"
        for coluna in colunas_gastos:
            descricao = colunas_descricao.get(coluna, coluna)
            relatorio += f"- {descricao}: {row[coluna]:.2f}\n"
        relatorio += "\n"

    return gastos_medios, relatorio

# ---------------------------
# 4. FUNÇÃO PARA EXIBIR GRÁFICOS INTERATIVOS
# ---------------------------
def plot_gastos_interactive(gastos_medios: pd.DataFrame, gasto: str):
    """
    Plota um gráfico de barras interativo para o gasto selecionado.
    
    Parâmetros:
      - gastos_medios (pd.DataFrame): DataFrame com a média dos gastos por total de filhos.
      - gasto (str): Coluna de gastos a ser plotada.
    
    Retorna:
      - fig (plotly.graph_objects.Figure): Figura interativa.
    """
    descricao = {
        'MntTotal': "Gasto Total",
        'MntSweetProducts': "Gastos com Produtos Doces",
        'MntGoldProds': "Gastos com Produtos Premium"
    }
    
    fig = px.bar(gastos_medios, 
                 x='Total_Filhos', 
                 y=gasto, 
                 title=f"Média de {descricao.get(gasto, gasto)} por Número Total de Filhos",
                 labels={'Total_Filhos': 'Número Total de Filhos', gasto: descricao.get(gasto, gasto)},
                 color='Total_Filhos',
                 color_continuous_scale='Reds')
    fig.update_layout(template="simple_white", height=500)
    return fig

# ---------------------------
# 5. EXECUÇÃO DO DASHBOARD
# ---------------------------
def main():
    # Caminho dos dados
    data_path = '../data/processed/ifood_df_atualizado.csv'
    df = load_data(data_path)
    
    if df.empty:
        st.stop()

    # Cabeçalho principal
    st.markdown("<h1>📊 Dashboard - Análise de Clientes Ifood</h1>", unsafe_allow_html=True)
    st.markdown("### Análise de Família vs. Comportamento de Compra")
    st.markdown("---")

    # Aplicar a função de análise para gerar dados e relatório
    gastos_medios, relatorio = analisar_familia_vs_comportamento_compra(df)
    if gastos_medios is None:
        st.error("Não foi possível realizar a análise.")
        st.stop()

    # Widget: Slider para filtrar número total de filhos a serem exibidos (mínimo e máximo do agrupamento)
    min_filhos = int(gastos_medios['Total_Filhos'].min())
    max_filhos = int(gastos_medios['Total_Filhos'].max())
    filhos_range = st.slider("Filtrar Total de Filhos", min_value=min_filhos, max_value=max_filhos, value=(min_filhos, max_filhos), step=1)

    # Filtrar dados conforme o slider
    gastos_filtrados = gastos_medios[(gastos_medios['Total_Filhos'] >= filhos_range[0]) & 
                                     (gastos_medios['Total_Filhos'] <= filhos_range[1])]

    # Widget: Dropdown para selecionar o tipo de gasto a ser exibido
    opcoes_gastos = ['MntTotal', 'MntSweetProducts', 'MntGoldProds']
    gasto_selecionado = st.selectbox("Selecionar Tipo de Gasto", options=opcoes_gastos, format_func=lambda x: {
        'MntTotal': "Gasto Total",
        'MntSweetProducts': "Gastos com Produtos Doces",
        'MntGoldProds': "Gastos com Produtos Premium"
    }[x])

    # Exibir gráfico interativo do gasto selecionado
    fig = plot_gastos_interactive(gastos_filtrados, gasto_selecionado)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Exibir relatório textual estilizado com insights
    st.markdown("## 📝 Relatório Executivo")
    st.markdown(f"<div class='report-box'>{relatorio.replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)

# Executa a função principal com tratamento de erros
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"Ocorreu um erro inesperado: {e}")
