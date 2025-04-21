# Seu código Python para o Streamlit
import streamlit as st
import gspread
from gspread_dataframe import set_with_dataframe
import pandas as pd
from google.auth import default
from datetime import datetime

creds, _ = default()
gc = gspread.authorize(creds)

SPREADSHEET_NAME = 'Registros de Vendas'
try:
    sh = gc.open(SPREADSHEET_NAME)
except gspread.SpreadsheetNotFound:
    sh = gc.create(SPREADSHEET_NAME)

try:
    worksheet = sh.sheet1
except:
    worksheet = sh.add_worksheet(title='Dados', rows='1000', cols='20')

if not worksheet.row_values(1):
    worksheet.append_row(['Data', 'Quantidade de Itens', 'Valor', 'Forma de Pagamento'])

def carregar_dados():
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
    return df

st.title('Registro de Vendas')
data = st.date_input('Data', value=datetime.now().date())
quantidade = st.number_input('Quantidade de Itens', min_value=1, step=1)
valor = st.number_input('Valor', min_value=0.0, format="%.2f")
forma_pagamento = st.text_input('Forma de Pagamento')

if st.button('Adicionar Registro'):
    worksheet.append_row([str(data), int(quantidade), float(valor), forma_pagamento])
    st.success('Registro adicionado com sucesso!')

st.subheader('Registros atuais')
df = carregar_dados()
st.dataframe(df)
