import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from typing import Tuple, Dict

# Configuração inicial da página
st.set_page_config(
    page_title="Análise de Campanhas - iFood",
    page_icon="📈",
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
    .analysis-section {
        margin-top: 2rem;
        padding: 1.5rem;
        background-color: #F8F9FA;
        border-radius: 8px;
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
            usecols=['AcceptedCmpOverall', 'Age', 'education_Graduation'],
            dtype={
                'AcceptedCmpOverall': 'int8',
                'Age': 'int16',
                'education_Graduation': 'int8'
            }
        )
        return df.dropna()
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        return pd.DataFrame()

def process_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Processa os dados e calcula as taxas de aceitação
    """
    bins = [0, 30, 40, 50, 60, float('inf')]
    labels = ['≤30', '31-40', '41-50', '51-60', '>60']
    df['Faixa_Etaria'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)
    
    taxa_idade = df.groupby('Faixa_Etaria', observed=False)['AcceptedCmpOverall'].mean().reset_index()
    taxa_educacao = df.groupby('education_Graduation', observed=False)['AcceptedCmpOverall'].mean().reset_index()
    
    return taxa_idade, taxa_educacao

def create_bar_plot(df: pd.DataFrame, x_col: str, title: str) -> go.Figure:
    """
    Cria gráfico de barras interativo com paleta vermelha
    """
    fig = px.bar(
        df,
        x=x_col,
        y='AcceptedCmpOverall',
        title=title,
        color=x_col,
        color_discrete_sequence=px.colors.sequential.Reds,
        labels={'AcceptedCmpOverall': 'Taxa de Aceitação', x_col: ''}
    )
    fig.update_layout(
        showlegend=False,
        plot_bgcolor='white',
        xaxis_title=None,
        yaxis_tickformat=".0%",
        height=400
    )
    return fig

def display_key_metrics(taxa_idade: pd.DataFrame, taxa_educacao: pd.DataFrame) -> None:
    """
    Exibe métricas principais em cards estilizados
    """
    max_idade = taxa_idade.loc[taxa_idade['AcceptedCmpOverall'].idxmax()]
    max_educ = taxa_educacao.loc[taxa_educacao['AcceptedCmpOverall'].idxmax()]
    
    cols = st.columns(3)
    metrics = [
        ('👥 Melhor Faixa Etária', f"{max_idade['Faixa_Etaria']} ({max_idade['AcceptedCmpOverall']:.1%})", '#B22222'),
        ('🎓 Aceitação Graduados', f"{max_educ['AcceptedCmpOverall']:.1%}", '#CD5C5C'),
        ('📊 Diferença', f"{(max_idade['AcceptedCmpOverall'] - max_educ['AcceptedCmpOverall']):.1%}", '#DC143C')
    ]
    
    for col, (title, value, color) in zip(cols, metrics):
        with col:
            st.markdown(
                f'<div class="metric-card" style="border-color: {color}">'
                f'<h3 style="color: {color}">{title}</h3><h2>{value}</h2></div>', 
                unsafe_allow_html=True
            )

def generate_insights(taxa_idade: pd.DataFrame, taxa_educacao: pd.DataFrame) -> str:
    """
    Gera relatório textual formatado com insights
    """
    top_idade = taxa_idade.nlargest(1, 'AcceptedCmpOverall').iloc[0]
    top_educ = taxa_educacao.nlargest(1, 'AcceptedCmpOverall').iloc[0]
    
    insights = f"""
    ### 🔍 Insights Estratégicos

    **Performance por Faixa Etária:**
    - Faixa com maior aceitação: **{top_idade['Faixa_Etaria']}** ({top_idade['AcceptedCmpOverall']:.1%})
    - Variação entre faixas: **{(taxa_idade['AcceptedCmpOverall'].max() - taxa_idade['AcceptedCmpOverall'].min()):.1%}**

    **Análise Educacional:**
    - Clientes graduados: **{top_educ['AcceptedCmpOverall']:.1%}** de aceitação
    - Diferença educacional: **{(top_educ['AcceptedCmpOverall'] - taxa_educacao['AcceptedCmpOverall'].min()):.1%}**

    **Recomendações:**
    - Desenvolver campanhas personalizadas para faixa **{top_idade['Faixa_Etaria']}**
    - Criar conteúdo exclusivo para graduados
    - Implementar testes A/B entre diferentes grupos
    """
    return insights

def main():
    """Função principal do dashboard"""
    st.markdown('<h1 class="header-text">📈 Eficácia de Campanhas por Demografia</h1>', unsafe_allow_html=True)
    
    # Carregar dados
    df = load_data('../data/processed/ifood_df_atualizado.csv')
    
    if not df.empty:
        # Controles interativos
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                age_range = st.slider(
                    '🔢 Faixa Etária:',
                    min_value=int(df['Age'].min()),
                    max_value=int(df['Age'].max()),
                    value=(25, 55)
                )
            with col2:
                educ_filter = st.selectbox(
                    '🎓 Filtro por Educação:',
                    options=['Todos', 'Graduados', 'Não Graduados'],
                    index=0
                )

        # Aplicar filtros
        filtered_df = df[df['Age'].between(*age_range)]
        if educ_filter == 'Graduados':
            filtered_df = filtered_df[filtered_df['education_Graduation'] == 1]
        elif educ_filter == 'Não Graduados':
            filtered_df = filtered_df[filtered_df['education_Graduation'] == 0]

        # Processar dados
        taxa_idade, taxa_educacao = process_data(filtered_df)
        
        # Seção de Visualizações
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(
                    create_bar_plot(taxa_idade, 'Faixa_Etaria', 'Aceitação por Faixa Etária'),
                    use_container_width=True
                )
            with col2:
                st.plotly_chart(
                    create_bar_plot(taxa_educacao, 'education_Graduation', 'Aceitação por Educação'),
                    use_container_width=True
                )

        # Seção Analítica
        with st.container():
            st.markdown("---")
            st.markdown("### 📌 Análise Detalhada")
            
            # Métricas Principais
            display_key_metrics(taxa_idade, taxa_educacao)
            
            # Insights Expandíveis
            with st.expander("📄 Relatório Completo", expanded=True):
                st.markdown(
                    f'<div class="report-box">{generate_insights(taxa_idade, taxa_educacao)}</div>',
                    unsafe_allow_html=True
                )

if __name__ == "__main__":
    main()