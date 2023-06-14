import streamlit as st
import pandas as pd
from datetime import date 
import plotly.express as px

# ---------------------------------------------------------------------------------------------

st.write(
    '''
    **Top 50 Jogos Web App**
    '''
)

st.sidebar.header('Gráficos')

def get_data():
    path = '../2_bases_tratadas/base_tratada.csv'
    return pd.read_csv(path, sep=';') 

def get_data_from_db():
    tabela_jogos = 'DBJogos'
    db_path = 'sqlite:///bancojogos.db'
    return pd.read_sql_table(tabela_jogos, db_path) 

df = get_data_from_db() # <------------
df = df.set_index(df['titulo'].astype(str))

graph_type = ['[Visualizar base]', 'Barra', 'Linha', 'Boxplot', 'Scatter', 'Violino', 'Histrograma']

escolha_do_indicador = st.sidebar.selectbox("Escolha o tipo de gráfico que deseja vizualizar:", graph_type)

# ---------------------------------------------------------------------------------------------

if escolha_do_indicador=='[Visualizar base]':
    st.header('Base de dados')
    df

# ---------------------------------------------------------------------------------------------

elif escolha_do_indicador=='Barra':
    st.header('Gráfico: ' + escolha_do_indicador.upper())
    st.write('Vendas')
    st.bar_chart(data=df, x='titulo', y='vendas')

    # MARKDOWN
    '''
    Através do gráfico de barras, podemos notar alguns picos em meio aos valores de venda que se distoam
    dos demais. Temos aqui a visão geral que terá sua análise complementada no gráfico de histograma.
    '''

# ---------------------------------------------------------------------------------------------

elif escolha_do_indicador=='Linha':
    st.header('Gráfico: ' + escolha_do_indicador.upper())
    st.write('Vendas')
    st.line_chart(data=df, x='titulo', y='vendas')

    # MARKDOWN
    '''
    Conforme o gráfico de linhas nos mostra, a quantidade de vendas da maioria dos jogos listados
    segue um padrão linear, tendo grandes destaques apenas em alguns titulos específicos.
    '''

# ---------------------------------------------------------------------------------------------

elif escolha_do_indicador=='Boxplot':
    st.header('Gráfico: ' + escolha_do_indicador.upper())
    fig = px.box(df.vendas)
    st.plotly_chart(fig)

    # MARKDOWN
    '''
    É possivel observar através do boxplot valores de venda:\n
    Mínimos: 22.7 milhões\n
    Medianos: 29 milhões\n
    Máximos: 60 milhões\n

    Além deles, também é possível observar a existência de outliers, onde 5 titulos de jogos
    venderam uma quantidade considerável acima de todos os outros dentre a lista, assim se
    destacando.
    '''

# ---------------------------------------------------------------------------------------------

elif escolha_do_indicador=='Scatter':
    st.header('Gráfico: ' + escolha_do_indicador.upper())
    fig = px.scatter(df, x="titulo", y="vendas")
    st.plotly_chart(fig)

    # MARKDOWN
    '''
    O gráfico Scatter é organizado em ordem decrescente, assim tornando possível observarmos que dois dos pontos 
    outliers neste conjunto de dados não cresce exageradamente em relação ao resto do conjunto, enquanto que três 
    deles se destacam disparadamente.
    '''

# ---------------------------------------------------------------------------------------------

elif escolha_do_indicador=='Violino':
    st.header('Gráfico: ' + escolha_do_indicador.upper())
    fig = px.violin(df, y="vendas")
    st.plotly_chart(fig)

    # MARKDOWN
    '''
    É possível observar neste gráfico cuja forma assemelha-se a um violino, os outliers situados no range de valores.
    Assim como visto nos outros gráficos, é possível observar que há alguns valores maiores que outros.
    Um deles atinge o pico mais alto do violino, outro o meio, e mais dois próximos ao valor máximo calculado
    na mediana. 
    '''

# ---------------------------------------------------------------------------------------------

elif escolha_do_indicador=='Histrograma':
    st.header('Gráfico: ' + escolha_do_indicador.upper())
    fig = px.histogram(df, x="vendas")
    st.plotly_chart(fig)

    # MARKDOWN
    '''
    Conforme visto neste gráfico - e também com auxílio do gráfico de barras - é possível notar
    que este histograma trata-se do tipo multimodal, onde mais de um pico pode ser observado. 
    Portanto, conclui-se que os maiores valores observados neste conjunto de dados são exceções.
    '''