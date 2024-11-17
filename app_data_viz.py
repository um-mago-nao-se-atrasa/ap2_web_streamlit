# \script\maquina\Scripts>activate
# \script>streamlit run app_data_viz.py
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.title('Micro Dados Presentes Enem 2023')
st.sidebar.header('Filtros')

@st.cache_data
def carregar_dados():
    enem = pd.read_csv('amostra_presentes_enem_bruto1.csv')
    return enem
dados = carregar_dados()

# EXPANSÃO 1
caixa1 = st.expander('DADOS GERAIS DOS CANDIDATOS PRESENTES')
with caixa1:
    col1, col2, col3 =st.columns(3)

    cand_F = dados['TP_SEXO'] == 'F'
    contagemF = dados[cand_F]
    contagemF = contagemF['TP_SEXO'].count()
    cand_M = dados['TP_SEXO'] == 'M'
    contagemM = dados[cand_M]
    contagemM = contagemM['TP_SEXO'].count()
    
    col1.metric('Total de candidatos', dados['TP_SEXO'].count())
    col2.metric("Média de notas de redação", round(dados.NU_NOTA_REDACAO.mean(), 2))
    col3.metric('Média de Notas Matemática', round(dados.NU_NOTA_MT.mean(), 2))

    # Gráfico de Pizza da qnt de alunos por sexo
    st.write('  ')
    st.write('GRÁFICO DE SETOR: QUANTIDADE POR SEXO')
    sexo_contagem = dados['TP_SEXO'].value_counts().reset_index().rename(columns={'TP_SEXO': 'SEXO', 'count': 'Quantidade'})
    figTorta = px.pie(sexo_contagem, values='Quantidade', names='SEXO', title = 'Quantidades de alunos por sexo')
    st.plotly_chart(figTorta)

    # Boxplot Notas de Redação   
    box_notas = dados['NU_NOTA_REDACAO'].reset_index().drop('index', axis=1).rename(columns={'NU_NOTA_REDACAO': 'NOTA_REDACAO'})
    figBOX = px.box(box_notas, x='NOTA_REDACAO', title='BoxPlot Notas de Redação')
    st.plotly_chart(figBOX)
    st.write(f'Média das notas de Redação: {dados['NU_NOTA_REDACAO'].mean().round(2)}')

    # Boxplot Notas de Matematica  
    box_notas_mat = dados['NU_NOTA_MT'].reset_index().drop('index', axis=1).rename(columns={'NU_NOTA_MT': 'NOTA_MATEMATICA'})
    figBOXmat = px.box(box_notas_mat, x='NOTA_MATEMATICA', title='BoxPlot Notas de Matematica')
    st.plotly_chart(figBOXmat)
    st.write(f'Média das notas de Matemática: {dados['NU_NOTA_MT'].mean().round(2)}')

    


##################SideBar Filtro de Sexo#################
sidesexo = dados['TP_SEXO'].drop_duplicates()
opc1 = st.sidebar.selectbox('Sexo do Candidato',sidesexo)
sexo_escolha = dados.loc[dados['TP_SEXO'] == opc1] # dF da Escolha de Gênero

##################### Expansão 2#####################
caixa2 = st.expander(f'Filtro por sexo : {opc1}')
with caixa2:
    #Informações Gerais da escolha
    col1, col2, col3 =st.columns(3)
    col1.metric(f'Quantidade de candidatos {opc1}:', sexo_escolha['TP_SEXO'].count())
    col2.metric(f'Média das notas de Redação:', round(sexo_escolha['NU_NOTA_REDACAO'].mean(), 2))
    col3.metric(f'Media das notas de Matemática', round(sexo_escolha['NU_NOTA_MT'].mean(), 2))

    # Histograma das notas de Redação
    notas_reda = sexo_escolha['NU_NOTA_REDACAO'].reset_index().rename(columns={'NU_NOTA_REDACAO': 'NOTA DE REDACAO'})
    fig_red = px.histogram(notas_reda, x='NOTA DE REDACAO', title='Histograma Notas Redação')
    st.plotly_chart(fig_red)

    # Histograma das notas de Matemática
    notas_mat = sexo_escolha['NU_NOTA_MT'].reset_index().rename(columns={'NU_NOTA_MT': 'NOTA DE MATEMATICA'})
    fig_mat = px.histogram(notas_mat, x='NOTA DE MATEMATICA', title='Histograma Notas Matemática', nbins = 40)
    st.plotly_chart(fig_mat)

    

###################### SideBar Filtro de Tipo de Escola####################
escola = dados['R_TP_ESCOLA'].drop_duplicates()
opc2 = st.sidebar.selectbox('Tipo de Escola', escola)
escolha_escola = dados.loc[dados['R_TP_ESCOLA'] == opc2] # dF da Escolha do tipo de Escola


#################### Expansão 3 ########################
caixa3 = st.expander(f' Filtro "tipo de escola": {opc2}')
with caixa3:
    #Informações Gerais da escolha
    col1, col2, col3 =st.columns(3)
    contagem_opc2 = escolha_escola['TP_SEXO'].count()
    col1.metric('Quantidade de alunos', contagem_opc2)
    col2.metric('Média das Notas de Redação', round(escolha_escola.NU_NOTA_REDACAO.mean(),2))
    
    # Gráfico de qnt de escolas por Estado
    st.write(f'Quantidades de Escolas {opc2} por Estado')
    agrupado_estado = escolha_escola.groupby('SG_UF_ESC')[['R_TP_ESCOLA']].count().rename(columns={'SG_UF_ESC': 'Estado', 'R_TP_ESCOLA': 'Quantidade'})
    st.bar_chart(agrupado_estado, x_label = 'Estados', y_label = f'Quantidade de escola {opc2}')

    # Filtro de Genero
    genero = dados['TP_SEXO'].drop_duplicates()
    g_escolha = st.selectbox('Escolha o gênero', genero)
    escolha_genero = escolha_escola[escolha_escola['TP_SEXO'] == g_escolha] # dF do genero escolhido
    st.write(f'Média de notas do gênero {g_escolha} dê escolas "{opc2}": {round(escolha_genero.NU_NOTA_REDACAO.mean(), 2)}')
    st.write(f'Quantidade do gênero {g_escolha} dê escolas "{opc2}": {escolha_genero.TP_SEXO.count()}')   
    # Gráfico BoxPlot 
    notas_reda = escolha_genero['NU_NOTA_REDACAO'].reset_index().drop('index', axis=1).rename(columns={'NU_NOTA_REDACAO': 'NOTA_REDACAO'})
    fig1 = px.box(notas_reda, x='NOTA_REDACAO', title='BoxPlot Notas de Redação')
    st.plotly_chart(fig1)
    

    #Filtro de renda familiar.
    st.write('Média de notas de Redação pela renda declarada')
    agrupado_renda = escolha_escola.groupby('R_Q006')[['NU_NOTA_REDACAO']].mean().rename(columns={'R_Q006': 'Renda:', 'NU_NOTA_REDACAO': 'Media'}).round(2)
    st.bar_chart(agrupado_renda, x_label = 'Rendas', y_label = 'Media Notas de Redação')

    #Filtro de Escolaridade da Mãe
    st.write('Média de notas de Redação pela escolaridade da mãe')
    agrupado_escolaridade = escolha_escola.groupby('R_Q002')[['NU_NOTA_REDACAO']].mean().rename(columns={'R_Q002': 'Escolaridade da Mãe', 'NU_NOTA_REDACAO': 'Nota'}).round(2)
    st.bar_chart(agrupado_escolaridade, x_label = 'Escolaridade da Mãe', y_label = 'Media Notas de Redação')



###################### SideBar Filtro Estado ###################
estado = dados['SG_UF_ESC'].drop_duplicates()
opc4 = st.sidebar.selectbox('Estado', estado)
estado_escolha = dados.loc[dados['SG_UF_ESC'] == opc4] # dF da Escolha do Estado

#################### Expansão 4 ########################
caixa4 = st.expander(f'Filtro por Estado: {opc4}')
with caixa4:
     #Informações Gerais da escolha
     col1, col2, col3 = st.columns(3)
     col1.metric('Quantidade de candidatos: ', estado_escolha['TP_SEXO'].count())
     feminino = estado_escolha[estado_escolha['TP_SEXO'] == 'F']
     masculino = estado_escolha[estado_escolha['TP_SEXO'] == 'M']
     feminino = feminino['TP_SEXO'].count()
     masculino = masculino['TP_SEXO'].count()
     col2.metric('Candidatos Femininos ', feminino)
     col3.metric('Candidatos Masculinos ', masculino)
     col1.metric('Média de notas Redação', round(estado_escolha['NU_NOTA_REDACAO'].mean(),2))
     col2.metric('Média de notas Matemática', round(estado_escolha['NU_NOTA_MT'].mean(),2))

     #### Gráfico de Pizza de Quantidades de alunos por tipo de escola
     escola_contagem = estado_escolha['R_TP_ESCOLA'].value_counts().reset_index().rename(columns={'R_TP_ESCOLA': 'Tipo de Escola', 'count': 'Quantidade'})
     figTorta2 = px.pie(escola_contagem, values='Quantidade', names='Tipo de Escola', title = 'Quantidades de alunos por Tipo de Escola')
     st.plotly_chart(figTorta2)



     ###### Gráfico de Barras Média de notas de Redação por Escolaridade da Mãe ########
     st.write('Média de notas de Redação pela Escolaridade da Mãe')
     agrupado_escolaridade_mae = estado_escolha.groupby('R_Q002')[['NU_NOTA_REDACAO']].mean().rename(columns={'R_Q002': 'Escolaridade da Mãe', 'NU_NOTA_REDACAO': 'Nota'}).round(2)
     st.bar_chart(agrupado_escolaridade_mae, x_label = 'Escolaridade da Mãe', y_label = 'Media Notas de Redação')

     ###### Gráfico de Barras Média de notas de Redação por Renda Familiar ########
     st.write('Média de notas de Redação pela renda Familiar declarada')
     agrupado_escolaridade_mae = estado_escolha.groupby('R_Q006')[['NU_NOTA_REDACAO']].mean().rename(columns={'R_Q006': 'Renda Familiar', 'NU_NOTA_REDACAO': 'Nota'}).round(2)
     st.bar_chart(agrupado_escolaridade_mae, x_label = 'Renda Familiar', y_label = 'Media Notas de Redação')

     



   
