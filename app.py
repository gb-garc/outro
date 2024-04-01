import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
# se precisar: pip install st-gsheets-connection

#url = "https://docs.google.com/spreadsheets/d/1JDy9md2VZPz4JbYtRPJLs81_3jUK47nx6GYQjgU8qNY/edit?usp=sharing"
#url = "https://docs.google.com/spreadsheets/d/1kB0oWRD6vOnNHzilJdofS6AF1u-hBTHYPP-ELi0GADo/edit#gid=258115823"
url = "https://docs.google.com/spreadsheets/d/1kB0oWRD6vOnNHzilJdofS6AF1u-hBTHYPP-ELi0GADo/edit?usp=sharing"
conn = st.experimental_connection("gsheets", type=GSheetsConnection)

df = conn.read(spreadsheet=url,worksheet="258115823") #,index_col=2)
#df = df.drop(df.columns[[1,10,11,12,13,14]], axis=1)
df = df.drop(df.columns[[1,11,12,13,14,15]], axis=1)
df.set_index(df.columns[1], inplace=True)
df = df.dropna(subset=['SOLICITANTE'])
df = df.sort_values(by='ORDEM', ascending=False)

st.divider()

#column_to_move = df.columns[2]
#df.insert(10, column_to_move, df.pop(column_to_move)) # Delete the column from its original position and insert it in the desired position
colunas = list(df.columns)
#df=df.index_col=2

url2="https://docs.google.com/forms/d/e/1FAIpQLSfJBAV_3q-3EN1R0qmIMYXrJHydjG2l0YzeZGn03qw5BsxojQ/viewform"
st.sidebar.link_button("Clique para preencher o formulário", url2)

col1, col2 = st.sidebar.columns(2)
col_filtro = col1.selectbox('Selecione a coluna', [c for c in colunas if c not in ['OBRA SOLICIT:']])
valor_filtro = col2.selectbox('Selecione o valor', list(df[col_filtro].unique()))

status_filtrar = col1.button('Filtrar')
status_limpar = col2.button('Limpar')
colunas_selecionadas = st.sidebar.multiselect('Selecione as colunas:', colunas, ['TIPO', 'SOLICITANTE', 'SOLICITADO EM:', 'SITUACAO', 'ORDEM'])

unique_index_values = df.index.unique().tolist()
col3, col4, col5 = st.columns(3)
valor_filtro2=col3.selectbox('Selecione uma solicitação para consultar os dados detalhados', unique_index_values)
status_filtrar2 = col4.button('Selecionar solicitação')
status_limpar2 = col5.button('Limpar pesquisa')
st.divider()

if status_filtrar2:
    texto1=valor_filtro2
    series= df.loc[texto1]
    df2=pd.DataFrame(series, index=colunas)
    st.dataframe(df2,height=500,width=800)

if status_limpar2:
    st.write("")
    
    
st.divider()
st.divider()
st.markdown('# Lista Completa de Solicitações')

if status_filtrar:
    st.dataframe(df.loc[df[col_filtro] == valor_filtro, colunas_selecionadas], height=800,width=800)
elif status_limpar:
    st.dataframe(df[colunas_selecionadas],height=800,width=800)
else:
    st.dataframe(df[colunas_selecionadas], height=800,width=800)



