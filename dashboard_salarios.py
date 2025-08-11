import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# --- 1. Configurações Visuais Avançadas (TEMA AZUL) ---
COR_PRIMARIA_AZUL = "#4D94FF"
COR_SECUNDARIA_AZUL = "#F72585"
COR_TERCIARIA_AZUL = "#4ECDC4"
COR_QUATERNARIA_AZUL = "#FFD166"
PALETA_CORES_AZUL = ["#4D94FF", "#4ECDC4", "#F72585", "#FFD166", "#A855F7", "#06B6D4"]

pio.templates["premium_dark_blue"] = go.layout.Template(
    layout=go.Layout(
        font=dict(family="'Segoe UI', 'Helvetica Neue', Arial, sans-serif", size=12, color="#FFFFFF"),
        title_font=dict(family="'Segoe UI', 'Helvetica Neue', Arial, sans-serif", size=20, color=COR_PRIMARIA_AZUL),
        paper_bgcolor="rgba(15, 15, 15, 0.8)",
        plot_bgcolor="rgba(30, 30, 30, 0.8)",
        colorway=PALETA_CORES_AZUL,
        xaxis=dict(showgrid=True, gridcolor='rgba(64, 64, 64, 0.3)', linecolor='#666666', ticks='outside', tickcolor='#FFFFFF'),
        yaxis=dict(showgrid=True, gridcolor='rgba(64, 64, 64, 0.3)', linecolor='#666666', ticks='outside', tickcolor='#FFFFFF'),
        hoverlabel=dict(bgcolor="rgba(0, 0, 0, 0.8)", bordercolor=COR_PRIMARIA_AZUL, font=dict(color="white")),
    )
)
pio.templates.default = "premium_dark_blue"

st.set_page_config(
    page_title="Dashboard Executivo - Análise Salarial",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Premium com a nova paleta azul
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    .stApp {{
        background: linear-gradient(135deg, #0F0F0F 0%, #1A1A1A 50%, #0F0F0F 100%) !important;
        font-family: 'Inter', sans-serif !important;
        color: #FFFFFF !important;
    }}

    [data-testid="stAppViewContainer"] > .main {{
        background: transparent !important;
        backdrop-filter: blur(10px) !important;
    }}

    .main-header {{
        background: linear-gradient(90deg, {COR_PRIMARIA_AZUL}, {COR_TERCIARIA_AZUL}, {COR_SECUNDARIA_AZUL});
        background-size: 200% 200%;
        animation: gradientShift 4s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem !important;
        font-weight: 700 !important;
        text-align: center;
        margin-bottom: 1rem;
    }}

    @keyframes gradientShift {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}

    .subtitle {{
        color: #CCCCCC;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        text-shadow: 0 0 10px rgba(77, 148, 255, 0.3);
    }}

    [data-testid="stSidebar"] {{
        background: rgba(26, 26, 26, 0.7) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(77, 148, 255, 0.2) !important;
    }}

    div[data-testid="stMetric"] {{ 
        background: rgba(30, 30, 30, 0.6) !important;
        backdrop-filter: blur(15px) !important;
        border-radius: 15px !important;
        padding: 25px !important;
        border: 1px solid rgba(77, 148, 255, 0.2) !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
        transition: all 0.3s ease !important;
        position: relative !important;
        overflow: hidden !important;
    }}
    
    div[data-testid="stMetric"]:hover {{
        transform: translateY(-5px) !important;
        box-shadow: 0 15px 45px rgba(77, 148, 255, 0.2) !important;
        border: 1px solid rgba(77, 148, 255, 0.5) !important;
    }}

    div[data-testid="stMetric"]:before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(77, 148, 255, 0.1), transparent);
        transition: left 0.5s;
    }}

    div[data-testid="stMetric"]:hover:before {{
        left: 100%;
    }}

    .section-title {{
        font-size: 1.8rem !important;
        color: {COR_PRIMARIA_AZUL} !important;
        font-weight: 600 !important;
        margin: 3rem 0 1.5rem 0 !important;
        position: relative !important;
        padding-left: 20px !important;
    }}

    .section-title:before {{
        content: '';
        position: absolute;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        width: 4px;
        height: 30px;
        background: linear-gradient(180deg, {COR_PRIMARIA_AZUL}, {COR_TERCIARIA_AZUL});
        border-radius: 2px;
    }}

    /* CORREÇÃO DA COR DAS TAGS DO MULTISELECT */
    [data-baseweb="tag"] {{
        background-color: {COR_PRIMARIA_AZUL} !important;
        color: #000000 !important; /* Texto preto para melhor contraste com o azul claro */
        font-weight: 600;
    }}
    [data-baseweb="tag"] span[role="button"] {{
        color: #000000 !important;
    }}

    .stSpinner > div {{
        border-color: {COR_PRIMARIA_AZUL} !important;
        border-top-color: transparent !important;
    }}

    ::-webkit-scrollbar-thumb {{
        background: linear-gradient(180deg, {COR_PRIMARIA_AZUL}, {COR_TERCIARIA_AZUL});
        border-radius: 4px;
    }}

    ::-webkit-scrollbar-thumb:hover {{
        background: linear-gradient(180deg, {COR_TERCIARIA_AZUL}, {COR_PRIMARIA_AZUL});
    }}
</style>
""", unsafe_allow_html=True)


# --- 2. Funções de Carregamento e Análise (INTACTAS) ---
DATA_URL = "https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/refs/heads/main/dados-imersao-final.csv"

@st.cache_data(ttl=3600)
def load_data(url: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(url)
        df.columns = [c.strip().lower() for c in df.columns]
        df['usd'] = pd.to_numeric(df['usd'], errors='coerce')
        df.dropna(subset=['usd'], inplace=True)
        df['faixa_salarial'] = pd.cut(df['usd'], 
                                     bins=[0, 50000, 100000, 150000, 200000, float('inf')],
                                     labels=['Até 50k', '50k-100k', '100k-150k', '150k-200k', '200k+'])
        for col in ['cargo', 'senioridade', 'contrato', 'tamanho_empresa', 'remoto', 'residencia_iso3']:
            if col in df.columns:
                df[col] = df[col].astype(str)
        return df
    except Exception as e:
        st.error(f"❌ Erro ao carregar os dados: {e}")
        return pd.DataFrame()

@st.cache_data
def get_filtered_data(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    df_filtrado = df.copy()
    for column, values in filters.items():
        if values:
            df_filtrado = df_filtrado[df_filtrado[column].isin(values)]
    return df_filtrado

def generate_advanced_insights(df: pd.DataFrame) -> dict:
    if df.empty or len(df) < 10:
        return {"insights": ["⚠️ Amostra insuficiente para análises robustas"], "metrics": {}}
    
    insights = []
    metrics = {}
    
    if len(df['ano'].unique()) > 1:
        correlation = df['ano'].corr(df['usd'])
        slope = np.polyfit(df['ano'], df['usd'], 1)[0]
        trend = "crescente" if slope > 0 else "decrescente"
        insights.append(f"**Tendência de Mercado:** O mercado apresenta tendência {trend} com correlação de {correlation:.2f}")
    
    cv = df['usd'].std() / df['usd'].mean()
    dispersao = "alta" if cv > 0.5 else "moderada" if cv > 0.3 else "baixa"
    insights.append(f"**Dispersão Salarial:** {dispersao.title()} variabilidade (CV: {cv:.2f})")
    
    top_cargo = df.groupby('cargo')['usd'].mean().idxmax()
    top_salario = df.groupby('cargo')['usd'].mean().max()
    insights.append(f"**Top Cargo:** {top_cargo} - ${top_salario:,.0f}")
    
    Q1 = df['usd'].quantile(0.25)
    Q3 = df['usd'].quantile(0.75)
    IQR = Q3 - Q1
    outliers = df[(df['usd'] < Q1 - 1.5*IQR) | (df['usd'] > Q3 + 1.5*IQR)]
    outlier_percent = len(outliers) / len(df) * 100
    insights.append(f"**Outliers:** {outlier_percent:.1f}% dos salários são outliers estatísticos")
    
    metrics = {'mediana': df['usd'].median(), 'q3': Q3, 'cv': cv, 'skewness': df['usd'].skew()}
    
    return {"insights": insights, "metrics": metrics}

# --- 3. Visualizações Avançadas (COM NOVA PALETA) ---
def create_salary_trend_chart(df: pd.DataFrame):
    yearly_stats = df.groupby('ano').agg({'usd': ['mean', 'median', 'std', 'count']}).round(0)
    yearly_stats.columns = ['Média', 'Mediana', 'Desvio Padrão', 'Quantidade']
    yearly_stats = yearly_stats.reset_index()
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Evolução Salarial', 'Volume de Dados', 'Volatilidade', 'Comparativo Média vs Mediana'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    fig.add_trace(go.Scatter(x=yearly_stats['ano'], y=yearly_stats['Média'], 
                            name='Média', line=dict(color=COR_PRIMARIA_AZUL, width=3)), row=1, col=1)
    fig.add_trace(go.Scatter(x=yearly_stats['ano'], y=yearly_stats['Mediana'], 
                            name='Mediana', line=dict(color=COR_SECUNDARIA_AZUL, width=2)), row=1, col=1)
    fig.add_trace(go.Bar(x=yearly_stats['ano'], y=yearly_stats['Quantidade'], 
                        name='Volume', marker_color=COR_TERCIARIA_AZUL), row=1, col=2)
    fig.add_trace(go.Scatter(x=yearly_stats['ano'], y=yearly_stats['Desvio Padrão'], 
                            name='Volatilidade', line=dict(color=COR_QUATERNARIA_AZUL, width=2)), row=2, col=1)
    fig.add_trace(go.Bar(x=yearly_stats['ano'], y=yearly_stats['Média'] - yearly_stats['Mediana'], 
                        name='Diferença Média-Mediana', marker_color=PALETA_CORES_AZUL[4]), row=2, col=2)
    
    fig.update_layout(height=600, title_text="Análise Temporal Avançada", showlegend=False)
    return fig

def create_correlation_matrix(df: pd.DataFrame):
    df_numeric = df.select_dtypes(include=[np.number])
    if 'ano' in df.columns: df_numeric['ano'] = df['ano']
    corr_matrix = df_numeric.corr()
    fig = px.imshow(corr_matrix, text_auto=True, aspect="auto", title="Matriz de Correlação", color_continuous_scale="RdBu_r")
    fig.update_layout(height=500)
    return fig

def create_advanced_salary_analysis(df: pd.DataFrame):
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Distribuição por Senioridade', 'Box Plot por Tamanho Empresa', 
                       'Violino por Modalidade', 'Dispersão Salário vs Experiência')
    )
    
    for i, senioridade in enumerate(df['senioridade'].unique()):
        fig.add_trace(go.Box(y=df[df['senioridade'] == senioridade]['usd'], name=senioridade, 
                            marker_color=PALETA_CORES_AZUL[i % len(PALETA_CORES_AZUL)]), row=1, col=1)
    for i, tamanho in enumerate(df['tamanho_empresa'].unique()):
        fig.add_trace(go.Box(y=df[df['tamanho_empresa'] == tamanho]['usd'], name=f'Empresa {tamanho}', 
                            marker_color=PALETA_CORES_AZUL[i % len(PALETA_CORES_AZUL)]), row=1, col=2)
    for i, remoto in enumerate(df['remoto'].unique()):
        fig.add_trace(go.Violin(y=df[df['remoto'] == remoto]['usd'], name=remoto, 
                               line_color=PALETA_CORES_AZUL[i % len(PALETA_CORES_AZUL)]), row=2, col=1)
    if 'ano' in df.columns:
        fig.add_trace(go.Scatter(x=df['ano'], y=df['usd'], mode='markers',
                                marker=dict(color=df['usd'], colorscale='Cividis', size=5),
                                name='Salários'), row=2, col=2)
    
    fig.update_layout(height=800, title_text="Análise Salarial Multidimensional", showlegend=False)
    return fig

# --- 4. Dashboard Principal (COM AJUSTES FINAIS) ---
def main():
    st.markdown('<h1 class="main-header"> Dashboard Executivo </h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle"> Análise Avançada de Remuneração em Data Science & Analytics</p>', unsafe_allow_html=True)
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    status_text.text('⏳ Carregando dados...')
    progress_bar.progress(25)
    
    with st.spinner("🔄 Processando dados..."):
        df = load_data(DATA_URL)
    
    if df.empty:
        st.error("❌ Não foi possível carregar os dados")
        return
    
    progress_bar.progress(50)
    status_text.text('Configurando filtros...')
    
    with st.sidebar:
        # CORREÇÃO: Remoção da imagem quebrada
        # st.image("https://i.imgur.com/g2y8d2q.png", width=80) 
        st.markdown("## **Painel de Controle**")
        st.markdown("### **Período**")
        anos_disponiveis = sorted(df['ano'].unique(), reverse=True)
        selected_years = st.multiselect("Selecione os anos", anos_disponiveis, default=anos_disponiveis)
        st.markdown("### **Perfil Profissional**")
        selected_seniority = st.multiselect("Nível de Senioridade", sorted(df['senioridade'].unique()), default=sorted(df['senioridade'].unique()))
        st.markdown("### **Ambiente Corporativo**")
        selected_contract = st.multiselect("Tipo de Contrato", sorted(df['contrato'].unique()), default=sorted(df['contrato'].unique()))
        selected_company_size = st.multiselect("Porte da Empresa", sorted(df['tamanho_empresa'].unique()), default=sorted(df['tamanho_empresa'].unique()))
        st.markdown("### **Análise Geográfica**")
        cargos_unicos = sorted(df['cargo'].unique())
        selected_role_map = st.selectbox("Cargo para Mapeamento", cargos_unicos, index=cargos_unicos.index('Data Scientist') if 'Data Scientist' in cargos_unicos else 0)
        if st.button("🔄 Resetar Filtros", help="Limpa todos os filtros aplicados"):
            st.experimental_rerun()
    
    progress_bar.progress(75)
    status_text.text('🔍 Aplicando filtros...')
    
    filters = {'ano': selected_years, 'senioridade': selected_seniority, 'contrato': selected_contract, 'tamanho_empresa': selected_company_size}
    df_filtrado = get_filtered_data(df, filters)
    
    if df_filtrado.empty:
        st.warning("⚠️ Nenhum dado encontrado com os filtros aplicados")
        return
    
    progress_bar.progress(100)
    status_text.text('✅ Dados prontos!')
    progress_bar.empty()
    status_text.empty()
    
    st.markdown('<div class="section-title">Resumo Executivo</div>', unsafe_allow_html=True)
    
    salario_medio = df_filtrado['usd'].mean()
    salario_mediano = df_filtrado['usd'].median()
    salario_maximo = df_filtrado['usd'].max()
    total_registros = df_filtrado.shape[0]
    cargo_mais_frequente = df_filtrado["cargo"].mode().iloc[0] if not df_filtrado["cargo"].mode().empty else "N/A"
    
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)
    
    with col1:
        delta_medio = f"{(salario_medio - df['usd'].mean()) / df['usd'].mean() * 100:+.1f}%"
        st.metric("Salário Médio", f"${salario_medio:,.0f}", delta=delta_medio)
    with col2: st.metric("Salário Mediano", f"${salario_mediano:,.0f}")
    with col3: st.metric("Salário Máximo", f"${salario_maximo:,.0f}")
    with col4: st.metric("Total de Registros", f"{total_registros:,}")
    with col5: st.metric("Cargo Destaque", cargo_mais_frequente)
    with col6:
        variacao = df_filtrado['usd'].std() / df_filtrado['usd'].mean()
        st.metric("Coef. Variação", f"{variacao:.2f}")
    
    st.markdown('<div class="section-title">Insights Inteligentes</div>', unsafe_allow_html=True)
    
    insights_data = generate_advanced_insights(df_filtrado)
    col_insights1, col_insights2 = st.columns([2, 1])
    with col_insights1:
        with st.expander(" **Análises Automáticas** - Clique para expandir", expanded=True):
            for insight in insights_data["insights"]:
                st.markdown(f"• {insight}")
    with col_insights2:
        if insights_data["metrics"]:
            st.markdown("### Métricas Estatísticas")
            st.metric("Mediana", f"${insights_data['metrics']['mediana']:,.0f}")
            st.metric("Q3", f"${insights_data['metrics']['q3']:,.0f}")
            st.metric("Assimetria", f"{insights_data['metrics']['skewness']:.2f}")
    
    st.markdown('<div class="section-title">Análises Visuais Avançadas</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["Tendências", "Correlações", "Distribuições", "Geografia"])
    
    with tab1:
        if len(df_filtrado['ano'].unique()) > 1:
            st.plotly_chart(create_salary_trend_chart(df_filtrado), use_container_width=True)
        else:
            st.info("Selecione múltiplos anos para ver as tendências temporais")
    with tab2: st.plotly_chart(create_correlation_matrix(df_filtrado), use_container_width=True)
    with tab3: st.plotly_chart(create_advanced_salary_analysis(df_filtrado), use_container_width=True)
    with tab4:
        df_role = df_filtrado[df_filtrado['cargo'] == selected_role_map]
        if not df_role.empty:
            media_role_pais = df_role.groupby('residencia_iso3')['usd'].mean().reset_index()
            fig_map = px.choropleth(media_role_pais, locations='residencia_iso3', color='usd', color_continuous_scale='Cividis', title=f'Distribuição Salarial: {selected_role_map}', labels={'usd': 'Salário Médio (USD)'})
            fig_map.update_layout(height=500)
            st.plotly_chart(fig_map, use_container_width=True)
        else:
            st.warning(f"⚠️ Sem dados para o cargo '{selected_role_map}' com os filtros atuais")
    
    st.markdown('<div class="section-title">Exploração de Dados</div>', unsafe_allow_html=True)
    
    col_data1, col_data2 = st.columns([3, 1])
    with col_data2:
        st.markdown("### Opções de Visualização")
        show_raw = st.checkbox("Mostrar dados brutos", value=False)
        if st.button("📥 Download CSV", key="download_button", help="Baixar os dados filtrados em formato CSV"):
            csv = df_filtrado.to_csv(index=False)
            st.download_button(label="Clique para baixar", data=csv, file_name=f"dados_salarios_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv", mime="text/csv")
    with col_data1:
        if show_raw:
            st.dataframe(df_filtrado, use_container_width=True, height=400)
        else:
            st.markdown("### Resumo Estatístico")
            summary_stats = df_filtrado['usd'].describe().round(0)
            st.dataframe(summary_stats.to_frame('Estatísticas'), use_container_width=True)
    
    st.markdown("---")
    st.markdown("<div style='text-align: center; color: #666; padding: 20px;'><p> <strong>Dashboard </strong> | Desenvolvido para Imersão Alura em Análise de Dados</p><p> Insights baseados em análise estatística avançada e visualização interativa</p></div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
