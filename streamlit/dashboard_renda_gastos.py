import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from typing import Tuple, Dict

# Configuração inicial da página
st.set_page_config(
    page_title="Análise Renda vs Gastos - iFood",
    page_icon="🍷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main { background-color: #FFFFFF; }
    .header-text { 
        color: #000000;
        font-family: 'Arial';
        border-bottom: 2px solid #B22222;
        padding-bottom: 10px;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #FFF5F5;
        border: 2px solid #B22222;
        border-radius: 8px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(178,34,34,0.1);
    }
    .report-box {
        border: 2px solid #B22222;
        border-radius: 8px;
        padding: 25px;
        margin: 15px 0;
        background-color: #FFF5F5;
    }
    .stSlider>div>div>div>div {
        background-color: #B22222 !important;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data(show_spinner="Carregando dados...")
def load_data(file_path: str) -> pd.DataFrame:
    """
    Carrega e otimiza os dados do arquivo CSV com tratamento de erros
    """
    try:
        df = pd.read_csv(
            file_path,
            usecols=['Income', 'MntWines', 'MntFruits', 'MntMeatProducts', 'Age'],
            dtype={
                'Income': 'float32',
                'MntWines': 'int32',
                'MntFruits': 'int16',
                'MntMeatProducts': 'int32',
                'Age': 'int16'
            }
        )
        return df.dropna()
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        return pd.DataFrame()

def calculate_analysis(df: pd.DataFrame, coluna_gastos: str) -> Tuple[float, pd.DataFrame]:
    """
    Realiza os cálculos principais da análise
    """
    bins = [0, 30000, 60000, 90000, float('inf')]
    labels = ['Baixa', 'Média', 'Alta', 'Muito Alta']
    df['Categoria_Renda'] = pd.cut(df['Income'], bins=bins, labels=labels)
    
    correlacao = df[['Income', coluna_gastos]].corr().iloc[0, 1]
    gastos_medios = df.groupby('Categoria_Renda', observed=False)[coluna_gastos].mean().reset_index()
    
    return correlacao, gastos_medios

def create_scatter_plot(df: pd.DataFrame, coluna_gastos: str) -> go.Figure:
    """Cria gráfico de dispersão interativo com paleta vermelha"""
    fig = px.scatter(
        df,
        x='Income',
        y=coluna_gastos,
        color='Categoria_Renda',
        color_discrete_sequence=px.colors.sequential.Reds,
        title='Renda vs. Gastos',
        labels={'Income': 'Renda (USD)', coluna_gastos: 'Gastos (USD)'}
    )
    fig.update_layout(
        legend_title_text='Categoria de Renda',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def create_bar_plot(gastos_medios: pd.DataFrame, coluna_gastos: str) -> go.Figure:
    """Cria gráfico de barras interativo com paleta vermelha"""
    fig = px.bar(
        gastos_medios,
        x='Categoria_Renda',
        y=coluna_gastos,
        title='Gastos Médios por Categoria de Renda',
        labels={'Categoria_Renda': 'Categoria', coluna_gastos: 'Gastos Médios (USD)'},
        color='Categoria_Renda',
        color_discrete_sequence=px.colors.sequential.Reds
    )
    fig.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def display_metrics(correlacao: float, gastos_medios: pd.DataFrame, coluna_gastos: str) -> None:
    """Exibe métricas principais em cards estilizados"""
    cols = st.columns(3)
    metrics = [
        ('📈 Correlação', f"{correlacao:.2f}", '#B22222'),
        ('💰 Máximo Gasto', f"USD {gastos_medios[coluna_gastos].max():.2f}", '#CD5C5C'),
        ('📉 Mínimo Gasto', f"USD {gastos_medios[coluna_gastos].min():.2f}", '#DC143C')
    ]
    
    for col, (title, value, color) in zip(cols, metrics):
        with col:
            st.markdown(
                f'<div class="metric-card" style="border-color: {color}; color: {color}">'
                f'<h3>{title}</h3><h2>{value}</h2></div>', 
                unsafe_allow_html=True
            )

def generate_report(correlacao: float, gastos_medios: pd.DataFrame, coluna_gastos: str) -> str:
    """Gera relatório textual formatado com insights"""
    produto = coluna_gastos.replace('Mnt', '').replace('Products', '')
    max_categoria = gastos_medios.loc[gastos_medios[coluna_gastos].idxmax()]
    
    report = f"""
    ### 🍷 Insights Estratégicos - {produto}

    **Padrões de Consumo:**
    - Categoria com maior gasto: **{max_categoria['Categoria_Renda']}** (USD {max_categoria[coluna_gastos]:.2f})
    - Correlação Renda-Gastos: **{correlacao:.2f}**
    
    **Gastos Médios por Categoria:**
    {''.join([f'\n- {row["Categoria_Renda"]}: USD {row[coluna_gastos]:.2f}' for _, row in gastos_medios.iterrows()])}

    **Recomendações:**
    - Desenvolver bundles premium para clientes de **alta renda**
    - Criar campanhas segmentadas para categoria **{max_categoria['Categoria_Renda']}**
    - Implementar programa de fidelidade com benefícios progressivos
    """
    return report

def main():
    """Função principal do dashboard"""
    st.markdown('<h1 class="header-text">🍷 Análise Renda vs Gastos</h1>', unsafe_allow_html=True)
    
    # Carregar dados
    df = load_data('../data/processed/ifood_df_atualizado.csv')
    
    if not df.empty:
        # Controles interativos
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                coluna_gastos = st.selectbox(
                    '🎯 Selecione o Produto:',
                    options=['MntWines', 'MntFruits', 'MntMeatProducts'],
                    format_func=lambda x: x.replace('Mnt', '').replace('Products', '')
                )
            with col2:
                income_range = st.slider(
                    '💰 Faixa de Renda (USD):',
                    min_value=int(df['Income'].min()),
                    max_value=int(df['Income'].max()),
                    value=(int(df['Income'].quantile(0.25)), int(df['Income'].quantile(0.75)))
                )

        # Processar dados
        filtered_df = df[df['Income'].between(*income_range)]
        correlacao, gastos_medios = calculate_analysis(filtered_df, coluna_gastos)
        
        # Gráficos
        with st.container():
            st.plotly_chart(create_scatter_plot(filtered_df, coluna_gastos), use_container_width=True)
            st.plotly_chart(create_bar_plot(gastos_medios, coluna_gastos), use_container_width=True)
        
        # Métricas e Relatório
        with st.container():
            st.markdown("### 📊 Métricas Principais")
            display_metrics(correlacao, gastos_medios, coluna_gastos)
            
            st.markdown("### 📄 Análise Detalhada")
            st.markdown(
                f'<div class="report-box">{generate_report(correlacao, gastos_medios, coluna_gastos)}</div>',
                unsafe_allow_html=True
            )

if __name__ == "__main__":
    main()