import streamlit as st
import pandas as pd

# Configuração inicial da página do Streamlit
st.set_page_config(
    page_title="Guia de Engenharia Alternativa - Lada Niva",
    page_icon="🚜",
    layout="wide"
)

# Estilização customizada para seguir o padrão azul escuro/técnico
st.markdown("""
    <style>
    .main-title { font-size: 32px; font-weight: bold; color: #1F4E79; margin-bottom: 5px; }
    .subtitle { font-size: 16px; font-style: italic; color: #595959; margin-bottom: 25px; }
    .card-justificativa { background-color: #F2F2F2; padding: 12px; border-left: 5px solid #1F4E79; border-radius: 4px; margin-bottom: 10px; }
    .card-instalacao { background-color: #EEDBF7; padding: 12px; border-left: 5px solid #9B51E0; border-radius: 4px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🚜 Manual Técnico de Adaptações e Upgrades para Lada Niva</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Base de dados unificada com o acervo mecânico e projetos especiais do Grauçá 4x4</p>', unsafe_allow_html=True)

# 1. Banco de Dados Unificado (Dados das duas planilhas anteriores combinados)
@st.cache_data
def carregar_dados():
    banco_dados = [
        # --- LOTE 1: PEÇAS INTERCAMBIÁVEIS ---
        {
            "Sistema": "Suspensão Dianteira", "Componente Russo": "Pivô de Suspensão Superior",
            "Solucao": "Pivô de Suspensão com Flange Especial", "Codigo": "Pivô Superior S10 / Kit Geniva",
            "Origem": "Chevrolet S10", "Tipo": "Peça Intercambiável",
            "Justificativa": "O pivô original do Niva possui durabilidade limitada no uso severo fora de estrada e sua reposição no mercado nacional é escassa.",
            "Instalacao": "Requer o uso de uma flange adaptadora de aço desenvolvida pela Geniva. O pivô da S10 é fixado na balança superior, aumentando o curso e suportando pneus maiores.",
            "Link": "http://grauca4x4.blogspot.com/p/pecas-by-geniva_2.html"
        },
        {
            "Sistema": "Suspensão Dianteira", "Componente Russo": "Amortecedor Dianteiro",
            "Solucao": "Amortecedor Hidráulico Reforçado", "Codigo": "Cofap B47193 / Nakata HG 30548",
            "Origem": "GM Opala (6 cilindros)", "Tipo": "Peça Intercambiável",
            "Justificativa": "Amortecedores originais russos são muito macios, gerando instabilidade em terrenos acidentados ou oscilações excessivas na dianteira.",
            "Instalacao": "Instalação direta (Plug & Play) nos suportes originais. A carga para motores 6 cilindros estabiliza perfeitamente a dianteira pesada do Niva.",
            "Link": "http://grauca4x4.blogspot.com/p/pecas-by-geniva_2.html"
        },
        {
            "Sistema": "Suspensão Traseira", "Componente Russo": "Amortecedor Traseiro",
            "Solucao": "Amortecedor Pressurizado de Maior Curso", "Codigo": "Nakata HG 30549 / Monroe RS 5601",
            "Origem": "VW Kombi (Clipper) / Ford Pampa", "Tipo": "Peça Intercambiável",
            "Justificativa": "Limitação de curso de distensão original nas trilhas, impedindo que o pneu traseiro mantenha contato com o solo em valetas e erosões.",
            "Instalacao": "Encaixe direto nos olhais originais. Oferece maior curso útil de suspensão, ideal para quem utiliza molas traseiras levemente mais altas.",
            "Link": "http://grauca4x4.blogspot.com/p/pecas-by-geniva_2.html"
        },
        {
            "Sistema": "Suspensão Traseira", "Componente Russo": "Molas Helicoidais Traseiras",
            "Solucao": "Molas de Alta Carga Cortadas a Frio", "Codigo": "Molas Dianteiras (Versão c/ Ar)",
            "Origem": "Ford Corcel II / Del Rey / Pampa", "Tipo": "Peça Intercambiável",
            "Justificativa": "As molas traseiras originais do Niva cedem com facilidade quando o jipe é carregado com ferramentas, guinchos ou kit de gás GNV.",
            "Instalacao": "Necessário utilizar as molas dianteiras do Corcel II com ar-condicionado. Devem ser cortadas rigidamente a frio para ficarem com 8,5 ou 9 elos, ajustando a traseira na altura certa.",
            "Link": "http://grauca4x4.blogspot.com/p/pecas-by-geniva_2.html"
        },
        {
            "Sistema": "Transmissão / Eixos", "Componente Russo": "Carcaça do Diferencial Dianteiro",
            "Solucao": "Carcaça Substituta em Ferro Fundido", "Codigo": "Carcaça de Ferro Especial Geniva",
            "Origem": "Fabricação Sob Medida (Geniva)", "Tipo": "Modificação Estrutural",
            "Justificativa": "A carcaça original do diferencial dianteiro é feita de alumínio e fica fixada diretamente no bloco do motor. Sob forte estresse ou com motores modificados (como AP), ela trinca ou quebra os olhais de fixação.",
            "Instalacao": "Substituição estrutural completa. A carcaça de ferro fundido isola o diferencial do bloco do motor, sendo ancorada diretamente na suspensão/agregado, trazendo robustez extrema.",
            "Link": "http://grauca4x4.blogspot.com/p/pecas-by-geniva_2.html"
        },
        {
            "Sistema": "Sistema Elétrico", "Componente Russo": "Central de Fusíveis do Painel",
            "Solucao": "Caixa de Fusíveis Automotivos de Lâmina", "Codigo": "Adaptação Desenho André Milke",
            "Origem": "Painel Universal de Lâminas", "Tipo": "Modificação Estrutural",
            "Justificativa": "A caixa de fusíveis original do Niva utiliza fusíveis cilíndricos antigos (tipo baquelite) que sofrem oxidação severa, gerando mau contato crônico e perda de faróis.",
            "Instalacao": "Exige o mapeamento completo da fiação traseira original e fixação da nova central de fusíveis de lâmina modernos. Elimina permanentemente panes elétricas fantasmas.",
            "Link": "http://grauca4x4.blogspot.com/2015/04/caixa-de-fusiveis-by-andre-milke-post.html"
        },
        # --- LOTE 2: UPGRADES AVANÇADOS ---
        {
            "Sistema": "Alimentação / Motor", "Componente Russo": "Carcurador Original Weber Russo",
            "Solucao": "Carburador Weber Mini-Progressivo ou 2E", "Codigo": "Weber / Brosol",
            "Origem": "Fiat Uno 1.5 / VW Gol AP 1.6", "Tipo": "Upgrade de Performance",
            "Justificativa": "O carburador original possui regulagem complexa, giclagem difícil de calibrar para a nossa gasolina com etanol e desgaste acentuado nos eixos metálicos.",
            "Instalacao": "Exige a confecção ou compra de uma flange adaptadora de alumínio para a base do coletor de admissão original do Niva. Melhora o consumo e a marcha lenta.",
            "Link": "http://grauca4x4.blogspot.com/p/pecas-by-geniva_2.html"
        },
        {
            "Sistema": "Transmissão / Eixos", "Componente Russo": "Semieixos Traseiros Sem Flange",
            "Solucao": "Semieixo Traseiro com Flange Forjada Integrada", "Codigo": "Desenvolvimento Técnico Geniva",
            "Origem": "Aço Forjado Sob Medida", "Tipo": "Upgrade de Performance",
            "Justificativa": "O semieixo traseiro original utiliza um anel retentor sob pressão que, em caso de quebra do rolamento, deixa a roda traseira se soltar inteira para fora do jipe.",
            "Instalacao": "Substituição completa do semieixo por uma peça forjada em bloco único onde a flange da roda já faz parte da estrutura. Impede que a roda saia em quebras catastróficas.",
            "Link": "http://grauca4x4.blogspot.com/p/pecas-by-geniva_2.html"
        },
        {
            "Sistema": "Sistema de Direção", "Componente Russo": "Caixa de Direção Mecânica Pesada",
            "Solucao": "Adaptação de Caixa de Direção Hidráulica", "Codigo": "ZF / TRW Adaptada",
            "Origem": "Chevrolet Omega / Ford Santana", "Tipo": "Upgrade de Performance",
            "Justificativa": "A caixa mecânica original é extremamente pesada em manobras, folga com facilidade e causa grande cansaço físico ao condutor em terrenos acidentados.",
            "Instalacao": "Adaptação estrutural complexa na longarina dianteira esquerda para fixação da caixa hidráulica. Exige instalação de bomba hidráulica acionada por correia no motor.",
            "Link": "http://grauca4x4.blogspot.com/p/pecas-by-geniva_2.html"
        }
    ]
    return pd.DataFrame(banco_dados)

df = carregar_dados()

# 2. Barra Lateral (Filtros de Busca)
st.sidebar.header("🔍 Painel de Filtros")

# Filtro por Palavra-Chave
busca = st.sidebar.text_input("Buscar por componente ou carro base:", "").strip().lower()

# Filtro por Sistema Mecânico
sistemas_disponiveis = ["Todos"] + sorted(df["Sistema"].unique().tolist())
sistema_selecionado = st.sidebar.selectbox("Filtrar por Sistema Mecânico:", sistemas_disponiveis)

# Filtro por Tipo de Modificação
tipos_disponiveis = ["Todos"] + sorted(df["Tipo"].unique().tolist())
tipo_selecionado = st.sidebar.selectbox("Filtrar por Tipo de Solução:", tipos_disponiveis)

# 3. Aplicação dos Filtros no Dataframe
df_filtrado = df.copy()

if busca:
    df_filtrado = df_filtrado[
        df_filtrado["Componente Russo"].str.lower().str.contains(busca) |
        df_filtrado["Solucao"].str.lower().str.contains(busca) |
        df_filtrado["Origem"].str.lower().str.contains(busca) |
        df_filtrado["Codigo"].str.lower().str.contains(busca)
    ]

if sistema_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Sistema"] == sistema_selecionado]

if tipo_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Tipo"] == tipo_selecionado]

# 4. Exibição dos Resultados
st.subheader(f"🛠️ Soluções Mapeadas ({len(df_filtrado)} encontradas)")

if df_filtrado.empty:
    st.info("Nenhuma modificação encontrada para os filtros aplicados. Tente outro termo de busca!")
else:
    for idx, row in df_filtrado.iterrows():
        # Cria um acordeão expansível para cada componente mapeado
        with st.expander(f"⚙️ {row['Sistema']} -> **{row['Componente Russo']}** substituído por **{row['Origem']}**"):
            
            # Layout em colunas para os dados rápidos de balcão de autopeças
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**🔧 Solução Proposta:** {row['Solucao']}")
            with col2:
                st.write(f"**🏷️ Código/Fabricante:** {row['Codigo']}")
            with col3:
                st.write(f"**📌 Tipo de Upgrade:** {row['Tipo']}")
            
            st.write("---")
            
            # Detalhamento de Engenharia Mecânica
            st.markdown(f"**⚠️ O Problema Crônico (Por que adaptar?):**")
            st.markdown(f'<div class="card-justificativa">{row["Justificativa"]}</div>', unsafe_allow_html=True)
            
            st.markdown(f"**🛠️ Instruções Técnicas de Instalação:**")
            st.markdown(f'<div class="card-instalacao">{row["Instalacao"]}</div>', unsafe_allow_html=True)
            
            st.write("")
            st.write(f"🔗 [Clique aqui para abrir o post original com fotos no Blog Grauçá 4x4]({row['Link']})")

# Rodapé Informativo
st.sidebar.write("---")
st.sidebar.info("💡 **Dica de Garagem:** Mantenha este app aberto no celular enquanto faz as buscas em balcões de autopeças tradicionais ou ferros-velhos.")