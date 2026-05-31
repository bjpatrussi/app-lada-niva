import streamlit as st
import pandas as pd
import os

# Configuração inicial da página do Streamlit
st.set_page_config(
    page_title="Guia de Engenharia Alternativa - Lada Niva",
    page_icon="🚜",
    layout="wide"
)

# Estilização técnica (Azul Corporativo)
st.markdown("""
    <style>
    .main-title { font-size: 32px; font-weight: bold; color: #1F4E79; margin-bottom: 5px; }
    .subtitle { font-size: 16px; font-style: italic; color: #595959; margin-bottom: 25px; }
    .card-justificativa { background-color: #F2F2F2; padding: 12px; border-left: 5px solid #1F4E79; border-radius: 4px; margin-bottom: 10px; }
    .card-instalacao { background-color: #EEDBF7; padding: 12px; border-left: 5px solid #9B51E0; border-radius: 4px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🚜 Manual Técnico de Adaptações e Upgrades para Lada Niva</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Base de dados dinâmica lida a partir do compilado oficial de peças alternativas</p>', unsafe_allow_html=True)

# NOME DA SUA PLANILHA NO GITHUB
NOME_PLANILHA = "pecas_niva_v3.xlsx"

# 1. Função Inteligente para Carregar os dados do arquivo Excel
@st.cache_data
def carregar_dados_do_excel():
    # Verifica se o arquivo Excel está na pasta
    if not os.path.exists(NOME_PLANILHA):
        st.error(f"Erro Crítico: O arquivo '{NOME_PLANILHA}' não foi encontrado na pasta do projeto!")
        return pd.DataFrame()
    
    try:
        # Lê a planilha preenchendo células vazias com texto em branco
        dados_excel = pd.read_excel(NOME_PLANILHA)
        dados_excel = dados_excel.fillna("")
        return dados_excel
    except Exception as e:
        st.error(f"Erro ao ler a planilha: {e}")
        return pd.DataFrame()

df = carregar_dados_do_excel()

# Se a planilha foi lida com sucesso, monta os filtros e a interface
if not df.empty:
    # 2. Barra Lateral (Painel de Filtros Dinâmicos)
    st.sidebar.header("🔍 Painel de Filtros")

    # Filtro por Palavra-Chave
    busca = st.sidebar.text_input("Buscar por componente ou carro base:", "").strip().lower()

    # Filtro por Sistema Mecânico (Lido automaticamente da planilha)
    sistemas_disponiveis = ["Todos"] + sorted([str(s) for s in df["Sistema"].unique() if s])
    sistema_selecionado = st.sidebar.selectbox("Filtrar por Sistema Mecânico:", sistemas_disponiveis)

    # Filtro por Tipo de Modificação (Lido automaticamente da planilha)
    tipos_disponiveis = ["Todos"] + sorted([str(t) for t in df["Tipo"].unique() if t])
    tipo_selecionado = st.sidebar.selectbox("Filtrar por Tipo de Solução:", tipos_disponiveis)

    # 3. Aplicação dos Filtros no Painel
    df_filtrado = df.copy()

    if busca:
        df_filtrado = df_filtrado[
            df_filtrado["Componente Russo"].astype(str).str.lower().str.contains(busca) |
            df_filtrado["Solucao"].astype(str).str.lower().str.contains(busca) |
            df_filtrado["Origem"].astype(str).str.lower().str.contains(busca) |
            df_filtrado["Codigo"].astype(str).str.lower().str.contains(busca)
        ]

    if sistema_selecionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Sistema"] == sistema_selecionado]

    if tipo_selecionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Tipo"] == tipo_selecionado]

    # 4. Exibição dos Cartões de Peças na Tela
    st.subheader(f"🛠️ Soluções Mapeadas ({len(df_filtrado)} encontradas)")

    if df_filtrado.empty:
        st.info("Nenhuma modificação encontrada para essa busca.")
    else:
        for idx, row in df_filtrado.iterrows():
            with st.expander(f"⚙️ {row['Sistema']} -> **{row['Componente Russo']}** compatível com **{row['Origem']}**"):
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**🔧 Peça Nacional Substituta:** {row['Solucao']}")
                with col2:
                    st.write(f"**🏷️ Código Comercial/Fabricante:** {row['Codigo']}")
                with col3:
                    st.write(f"**📌 Classificação:** {row['Tipo']}")
                
                st.write("---")
                
                if row['Justificativa']:
                    st.markdown(f"**⚠️ Motivo da Adaptação / Problema Crônico:**")
                    st.markdown(f'<div class="card-justificativa">{row["Justificativa"]}</div>', unsafe_allow_html=True)
                
                if row['Instalacao']:
                    st.markdown(f"**🛠️ Notas Técnicas de Instalação/Adaptação:**")
                    st.markdown(f'<div class="card-instalacao">{row["Instalacao"]}</div>', unsafe_allow_html=True)
                
                if row['Link']:
                    st.write("")
                    st.write(f"🔗 [Abrir Post Original no Blog Grauçá 4x4]({row['Link']})")

    # Rodapé Técnico Lateral
    st.sidebar.write("---")
    st.sidebar.success(f"📈 Total de registros carregados da planilha V3.0: {len(df)}")