import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np

st.set_page_config(page_title = "Dasboard",
                   layout='wide')

st.sidebar.header('Sélectionnez les axes du graphe')
df = pd.read_excel('txETRl.xlsx', sheet_name='dim')
df.fillna(0, inplace=True)

regions = df["region"].unique()

selected_region = st.sidebar.selectbox("Selectionnez une Region:", regions)

df = df[df['region']== selected_region]
x_axis = st.sidebar.selectbox("choisir l'axe x", options = df.columns[2:], index=0)
y_axis = st.sidebar.selectbox("choisir l'axe y", options = df.columns[2:], index=1)
z_axis = st.sidebar.selectbox("choisir l'axe z", options = df.columns[2:], index=2)

fig = px.scatter_3d(df, x=x_axis,
                        y=y_axis,
                        z=z_axis,
                        color='country',
                        labels = {'xx':'yy'})
fig.update_layout(
    scene= dict(xaxis=dict(title=dict(text=x_axis, font=dict(size=30)), tickfont=dict(size=17)),
                yaxis=dict(title=dict(text=y_axis, font=dict(size=30)), tickfont=dict(size=17)),
                zaxis=dict(title=dict(text=z_axis, font=dict(size=30)), tickfont=dict(size=17)))) 

st.plotly_chart(fig)

st.markdown("---")

dfx = pd.read_excel('codiso2.xlsx', sheet_name='Feuil1')
dfa = pd.read_excel('slidmap2.xlsx', sheet_name='Feuil1')
dfa = dfa.fillna(0)
dfa['T3'] = dfa['T3'].astype(int)
dfa['T5'] = dfa['T5'].astype(int)

st.title("Pays dont les montants de T3 et de T5 consommés en 4 ans sont inférieurs/égaux aux montants des curseurs infra")

st.write("Fixer dans les deux sliders ci-dessous le montant total T3 et T5 consommés en 4 ans pour un pays")

selected_value_T3 = st.slider(
    label="Le montant de T3 (fonctionnement) consommé est au maximum de:",
    min_value=0,
    max_value=53630000,
    value=dfa['T3'].iloc[0],
    step=2500000
)

selected_value_T5 = st.slider(
    label="Le montant de T5 (investissement) consommé est au maximum de:",
    min_value=0,
    max_value=17000000,
    value=dfa['T5'].iloc[0],
    step=2500000
)

value_T3 = np.int32(selected_value_T3)+1
value_T5 = np.int32(selected_value_T5)+1

dmc_T3 = dfa.loc[dfa['T3']<value_T3]
dmc_T5 = dfa.loc[dfa['T5']<value_T5]
common = set(dmc_T3['country']).intersection(dmc_T5['country'])
dfy = pd.concat([dmc_T3[dmc_T3['country'].isin(common)],dmc_T5[dmc_T5['country'].isin(common)]])

dfy = dfy[['country', 'T3', 'T5']]
result = pd.merge(dfy, dfx, on = 'country', how='left')
result = result.fillna(0)
result['total T3+T5'] = result['T3'] + result['T5']

fig = px.choropleth(result, locations='iso', color='total T3+T5', hover_name='country', color_continuous_scale='viridis')
st.plotly_chart(fig)
