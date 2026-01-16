import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime
import socket

st.title("Formulário de Pesquisa de Sellers")
st.write("""Em caso de dúvidas, entre em contato com: 📧 **caio.braga@shopee.com**"""
)
st.write("(*) Campo Obrigatório")

ARQUIVO_EXCEL = r"data\rms_table.xlsx"
FORM_ENTRIES = r'data\form_entries.xlsx'

# ---------- Funções auxiliares ----------
def get_hostname():
    return socket.gethostname()

def get_client_ip():
    try:
        return st.context.headers.get("X-Forwarded-For", "IP não disponível")
    except:
        return "IP não disponível"

# ---------- Base de referência ----------
df = pd.read_excel(r'data\rms_table.xlsx')
PLACEHOLDER = 'Selecione'

# ---------- Campos dinâmicos ----------
cluster = st.selectbox('Cluster*', [PLACEHOLDER] + df['cluster'].unique().tolist())

if cluster != PLACEHOLDER:
    mask = df['cluster'] == cluster
    rm_lead_choice = df[mask]['rm_lead'].unique().tolist()
    rm_lead = st.selectbox("Rm Lead*", [PLACEHOLDER] + rm_lead_choice)
else:
    rm_lead = PLACEHOLDER

if rm_lead != PLACEHOLDER:
    mask = mask & (df['rm_lead'].isin(rm_lead_choice))
    rm_choice = df[mask]['rm'].unique().tolist()
    rm = st.selectbox("RM*", [PLACEHOLDER] + rm_choice)
else:
    rm = PLACEHOLDER

if rm != PLACEHOLDER:
    mask = mask & (df['rm'] == rm)
    shop_name_choice = df[mask]['shop_name'].unique().tolist()
    shop_name = st.selectbox("Shop Name*", [PLACEHOLDER] + shop_name_choice)

    mask = mask & (df['shop_name'] == shop_name)
    shop_id_choice = df[mask]['shop_id'].unique().tolist()
    shop_id = st.selectbox("Shop ID*", [PLACEHOLDER] + shop_id_choice)
else:
    shop_name = PLACEHOLDER
    shop_id = PLACEHOLDER

# Registro de Vendas e Receita

# Mercado Livre
if shop_name != PLACEHOLDER:
    st.markdown("#### Mercado Livre")
    sem_vendas_meli = st.checkbox("Sem vendas meli")

    if sem_vendas_meli:
        unidades_vendidas_meli = np.nan
        receita_meli = np.nan
    else:
        unidades_vendidas_meli = st.number_input(
            "Unidades Vendidas Meli*",
            min_value=0,
            step=1
        )
        receita_meli = st.number_input(
            "Receita (R$) Meli*",
            min_value=0.0,
        )

# Amazon
if shop_name != PLACEHOLDER:
    st.markdown("#### Amazon")
    sem_vendas_amz = st.checkbox("Sem vendas Amazon")

    if sem_vendas_amz:
        unidades_vendidas_amz = np.nan
        receita_amz = np.nan
    else:
        unidades_vendidas_amz = st.number_input(
            "Unidades Vendidas Amazon*",
            min_value=0,
            step=1
        )
        receita_amz = st.number_input(
            "Receita (R$) Amazon*",
            min_value=0.0,
        )

# Shein
if shop_name != PLACEHOLDER:
    st.markdown("#### Shein")
    sem_vendas_shein = st.checkbox("Sem vendas Shein")

    if sem_vendas_shein:
        unidades_vendidas_shein = np.nan
        receita_shein = np.nan
    else:
        unidades_vendidas_shein = st.number_input(
            "Unidades Vendidas Shein*",
            min_value=0,
            step=1
        )
        receita_shein = st.number_input(
            "Receita (R$) Shein*",
            min_value=0.0,
        )

# Tik Tok
if shop_name != PLACEHOLDER:
    st.markdown("#### Tik Tok")
    sem_vendas_tts = st.checkbox("Sem vendas Tik Tok")

    if sem_vendas_tts:
        unidades_vendidas_tts = np.nan
        receita_tts = np.nan
    else:
        unidades_vendidas_tts = st.number_input(
            "Unidades Vendidas Tik Tok*",
            min_value=0,
            step=1
        )
        receita_tts = st.number_input(
            "Receita (R$) Tik Tok*",
            min_value=0.0,
        )

# ---------- Formulário ----------
with st.form("form_dinamico"):
    observacoes = st.text_area(
    "Observações",
    placeholder="Adicione aqui qualquer observação relevante sobre o seller, vendas ou contexto...",
    height=120
)
    submit = st.form_submit_button("Enviar")

# ---------- Validação ----------
campos_invalidos = (
    cluster == PLACEHOLDER or
    rm_lead == PLACEHOLDER or
    rm == PLACEHOLDER or
    shop_name == PLACEHOLDER or
    shop_id == PLACEHOLDER or
    (sem_vendas_meli == 1 and unidades_vendidas_meli == 0) or
    (sem_vendas_meli == 1 and receita_meli == 0) or
    (sem_vendas_meli == 0 and receita_meli == 0) or
    (sem_vendas_meli == 0 and unidades_vendidas_meli == 0) or
    (float(unidades_vendidas_meli) >= float(receita_meli)) or
    (sem_vendas_amz == 1 and unidades_vendidas_amz == 0) or
    (sem_vendas_amz == 1 and receita_amz == 0) or
    (sem_vendas_amz == 0 and receita_amz == 0) or
    (sem_vendas_amz == 0 and unidades_vendidas_amz == 0) or
    (float(unidades_vendidas_amz) >= float(receita_amz)) or
    (sem_vendas_shein == 1 and unidades_vendidas_shein == 0) or
    (sem_vendas_shein == 1 and receita_shein == 0) or
    (sem_vendas_shein == 0 and receita_shein == 0) or
    (sem_vendas_shein == 0 and unidades_vendidas_shein == 0) or
    (float(unidades_vendidas_shein) >= float(receita_shein)) or
    (sem_vendas_tts == 1 and unidades_vendidas_tts == 0) or
    (sem_vendas_tts == 1 and receita_tts == 0) or
    (sem_vendas_tts == 0 and receita_tts == 0) or
    (sem_vendas_tts == 0 and unidades_vendidas_tts == 0) or
    (float(unidades_vendidas_tts) >= float(receita_tts))
)

# ---------- Ao enviar ----------
if submit:
    if campos_invalidos:
        st.error("❌ Preencha todos os campos obrigatórios antes de enviar.")
    else:
        novo_registro = pd.DataFrame([{
            "timestamp": datetime.now(),
            "cluster": cluster,
            "rm_lead": rm_lead,
            "rm": rm,
            "shop_name": shop_name,
            "unidades_vendidas_meli": unidades_vendidas_meli,
            "receita_meli": receita_meli,
            "sem_vendas_meli": sem_vendas_meli,
            "unidades_vendidas_amz": unidades_vendidas_amz,
            "unidades_vendidas_shein": unidades_vendidas_shein,
            "receita_shein": receita_shein,
            "sem_vendas_shein": sem_vendas_shein,
            "receita_amz": receita_amz,
            "sem_vendas_amz": sem_vendas_amz,
            "unidades_vendidas_tts": unidades_vendidas_tts,
            "receita_tts": receita_tts,
            "sem_vendas_tts": sem_vendas_tts,
            "hostname": get_hostname(),
            'observacoes': observacoes
        }])

        if os.path.exists(FORM_ENTRIES):
            df_existente = pd.read_excel(FORM_ENTRIES)
            df_final = pd.concat([df_existente, novo_registro], ignore_index=True)
        else:
            df_final = novo_registro

        df_final.to_excel(FORM_ENTRIES, index=False)

        st.success("Registro salvo com sucesso!")
        st.dataframe(df_final.tail())
