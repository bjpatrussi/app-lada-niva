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

# Função Inteligente para identificar a origem do link e dar o nome correto ao botão
def obter_nome_do_link(url):
    url_lower = str(url).lower()
    if "grauca4x4" in url_lower:
        return "🔗 Abrir Matéria Original no Blog Grauçá 4x4"
    elif "sertaooffroad" in url_lower or ".pdf" in url_lower:
        return "📄 Baixar Catálogo/Manual Técnico (PDF)"
    elif "scribd" in url_lower:
        return "📚 Visualizar Documento de Engenharia no Scribd"
    elif "drive.google" in url_lower:
        return "📁 Abrir Arquivo Compartilhado no Google Drive"
    else:
        return "🌐 Abrir Fonte Externa de Consulta"

# 1. Carregar os dados do arquivo Excel
@st.cache_data
def carregar_dados_do_excel():
    if not os.path.exists(NOME_PLANILHA):
        st.error(f"Erro Crítico: O arquivo '{NOME_PLANILHA}' não foi encontrado!")
        return pd.DataFrame()
    
    try:
        dados_excel = pd.read_excel(NOME_PLANILHA)
        dados_excel = dados_excel.fillna("")
        return dados_excel
    except Exception as e:
        st.error(f"Erro ao ler a planilha: {e}")
        return pd.DataFrame()

df = carregar_dados_do_excel()

if not df.empty:
    # 2. Barra Lateral (Painel de Filtros Dinâmicos)
    st.sidebar.header("🔍 Painel de Filtros")

    busca = st.sidebar.text_input("Buscar por componente ou carro base:", "").strip().lower()

    sistemas_disponiveis = ["Todos"] + sorted([str(s) for s in df["Sistema"].unique() if s])
    sistema_selecionado = st.sidebar.selectbox("Filtrar por Sistema Mecânico:", sistemas_disponiveis)

    tipos_disponiveis = ["Todos"] + sorted([str(t) for t in df["Tipo"].unique() if t])
    tipo_selecionado = st.sidebar.selectbox("Filtrar por Tipo de Solução:", tipos_disponiveis)

    # 3. Aplicação dos Filtros
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

    # 4. Exibição dos Resultados
    st.subheader(f"🛠️ Soluções Mapeadas ({len(df_filtrado)} encontradas)")

    if df_filtrado.empty:
        st.info("Nenhuma modificação encontrada.")
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
                
                # CORREÇÃO AQUI: O link agora passa pela função para ganhar o nome correto de forma dinâmica
                if row['Link'] and str(row['Link']).strip() != "":
                    texto_botao = obter_nome_do_link(row['Link'])
                    st.write("")
                    st.markdown(f"[{texto_botao}]({row['Link']})")

    st.sidebar.write("---")
    st.sidebar.success(f"📈 Total de registros carregados: {len(df)}")