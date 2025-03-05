import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

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

