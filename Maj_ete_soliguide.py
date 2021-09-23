import streamlit as st 
from streamlit_folium import folium_static
import pandas as pd
import numpy as np
from numpy import nan
import re
import numpy as np
from datetime import timedelta
import datetime
import time
import plotly.express as px
from bson import ObjectId
import folium
from folium.plugins import MarkerCluster

@st.cache
def load_df(url):
    df = pd.read_csv(url)
    return df

# option
st.set_page_config(page_title="Soliguide 2021 - Mise à jour été",
                   page_icon="https://pbs.twimg.com/profile_images/1321098074765361153/F4UFTeix.png",
                   initial_sidebar_state="expanded")

#############
## sidebar ##
############# 
st.sidebar.image("https://s3.us-west-2.amazonaws.com/secure.notion-static.com/caeabe8c-f726-4dfe-ac9e-aaa9c4099e07/Soliguide_RVB_Original_PurpleOrange4x.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAT73L2G45O3KS52Y5%2F20210921%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20210921T140607Z&X-Amz-Expires=86400&X-Amz-Signature=3021703b71b396e5cf7dc4de84318ef5df3c46df80febb9ccea6d44d255bf447&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22Soliguide_RVB_Original_PurpleOrange4x.png%22", use_column_width=True)
st.sidebar.title('Soliguide 2021')
st.sidebar.subheader('Mise à jour été')

categorie = st.sidebar.selectbox("Choisissez votre territoire :", ("France",  "Ile-De-France", "Alpes-Maritimes (06)",
                                            "Gironde (33)",
                                            "Loire-Atlantique (44)", "Bas-Rhin (67)", 
                                            "Paris (75)", "Seine-et-Marne (77)","Yvelines (78)",
                                            "Essonne (91)", "Hauts-de-Seine (92)",
                                            "Seine-Saint-Denis (93)","Val-de-Marne (94)",
                                            "Val-d'Oise (95)"))

##########
## DATA ##
##########

# modifier selon la localisation de la BD
# Importation des fichier .csv en pandas

# Données pour cartes :
df_france = pd.read_csv('ressources/df_france.csv')
df_fiches_IDF = pd.read_csv('ressources/df_IDF.csv')
df_fiches_06 = pd.read_csv('ressources/df_fiches_06.csv')
df_fiches_33 = pd.read_csv('ressources/df_fiches_33.csv')
df_fiches_44 = pd.read_csv('ressources/df_fiches_44.csv')
df_fiches_67 = pd.read_csv('ressources/df_fiches_67.csv')
df_fiches_75 = pd.read_csv('ressources/df_fiches_75.csv')
df_fiches_77 = pd.read_csv('ressources/df_fiches_77.csv')
df_fiches_78 = pd.read_csv('ressources/df_fiches_78.csv')
df_fiches_91 = pd.read_csv('ressources/df_fiches_91.csv')
df_fiches_92 = pd.read_csv('ressources/df_fiches_92.csv')
df_fiches_93 = pd.read_csv('ressources/df_fiches_93.csv')
df_fiches_94 = pd.read_csv('ressources/df_fiches_94.csv')
df_fiches_95 = pd.read_csv('ressources/df_fiches_95.csv')


# Données pour le barchart horizontal:
df_comparaison_France = pd.read_csv('ressources/Fig2.csv')
df_comparaison_IDF = pd.read_csv('ressources/Fig2_IDF.csv')
df_comparaison_06 = pd.read_csv('ressources/Fig2_06.csv')
df_comparaison_33 = pd.read_csv('ressources/Fig2_33.csv')
df_comparaison_44 = pd.read_csv('ressources/Fig2_44.csv')
df_comparaison_67 = pd.read_csv('ressources/Fig2_67.csv')
df_comparaison_75 = pd.read_csv('ressources/Fig2_75.csv')
df_comparaison_77 = pd.read_csv('ressources/Fig2_77.csv')
df_comparaison_78 = pd.read_csv('ressources/Fig2_78.csv')
df_comparaison_91 = pd.read_csv('ressources/Fig2_91.csv')
df_comparaison_92 = pd.read_csv('ressources/Fig2_92.csv')
df_comparaison_93 = pd.read_csv('ressources/Fig2_93.csv')
df_comparaison_94 = pd.read_csv('ressources/Fig2_94.csv')
df_comparaison_95 = pd.read_csv('ressources/Fig2_95.csv')

# Données pour le stacked chart:
df_stacked_per_france = pd.read_csv('ressources/Fig3.csv')
df_stacked_per_IDF = pd.read_csv('ressources/Fig3_IDF.csv')
df_stacked_per_06 = pd.read_csv('ressources/Fig3_06.csv')
df_stacked_per_33 = pd.read_csv('ressources/Fig3_33.csv')
df_stacked_per_44 = pd.read_csv('ressources/Fig3_44.csv')
df_stacked_per_67 = pd.read_csv('ressources/Fig3_67.csv')
df_stacked_per_75 = pd.read_csv('ressources/Fig3_75.csv')
df_stacked_per_77 = pd.read_csv('ressources/Fig3_77.csv')
df_stacked_per_78 = pd.read_csv('ressources/Fig3_78.csv')
df_stacked_per_91 = pd.read_csv('ressources/Fig3_91.csv')
df_stacked_per_92 = pd.read_csv('ressources/Fig3_92.csv')
df_stacked_per_93 = pd.read_csv('ressources/Fig3_93.csv')
df_stacked_per_94 = pd.read_csv('ressources/Fig3_94.csv')
df_stacked_per_95 = pd.read_csv('ressources/Fig3_95.csv')

# Données pour le pie chart:
res_france = pd.read_csv('ressources/Fig4.csv')
res_IDF = pd.read_csv('ressources/Fig4_IDF.csv')
res_06 = pd.read_csv('ressources/Fig4_06.csv')
res_33 = pd.read_csv('ressources/Fig4_33.csv')
res_44 = pd.read_csv('ressources/Fig4_44.csv')
res_67 = pd.read_csv('ressources/Fig4_67.csv')
res_75 = pd.read_csv('ressources/Fig4_75.csv')
res_77 = pd.read_csv('ressources/Fig4_77.csv')
res_78 = pd.read_csv('ressources/Fig4_78.csv')
res_91 = pd.read_csv('ressources/Fig4_91.csv')
res_92 = pd.read_csv('ressources/Fig4_92.csv')
res_93 = pd.read_csv('ressources/Fig4_93.csv')
res_94 = pd.read_csv('ressources/Fig4_94.csv')
res_95 = pd.read_csv('ressources/Fig4_95.csv')

###############
##  FRANCE   ##
###############

if categorie == 'France':
    st.markdown("<h1 style='text-align: center; color: #3E3A71;'>Soliguide - Mise à jour été 2021</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #3E3A71;'>100% de la base de données mise à jour pour l'été</h2>", unsafe_allow_html=True)


    html_string = "<br>"

    st.markdown(html_string, unsafe_allow_html=True)

    html_string = "<center><font color='#3E3A71' face='Helvetica' size='6'>11 678 &emsp;&emsp;&emsp; 6 228 &emsp;&emsp;&emsp;&ensp; 709</font><br/><font size='2'>structures accompagnées cette été &emsp;&emsp;&emsp;&emsp; structures ont fermé &emsp;&emsp;&emsp;&emsp; structures ont changé d'horaire<br> <br></font>"

    st.markdown(html_string, unsafe_allow_html=True)

    # Création de la carte avec pour centre : le centre d ela France
    mappy = folium.Map(location=[46.227638, 2.213749],zoom_start=5.8)

    marker_cluster = MarkerCluster().add_to(mappy)

    # Ajout des différents markers :
    for en in range(len(df_france['colors'])):
        folium.CircleMarker([df_france.latitude[en], df_france.longitude[en]],
                            fill = True,
                            color = df_france['colors'][en],
                            radius = 5,
                            fill_color = df_france['colors'][en],
                            tooltip=df_france['Fermeture_Estivale'][en], 
                            popup=df_france['name'][en]
                            ).add_to( mappy )
    mappy.save('map.html')

    #Affichage de la carte
    folium_static(mappy)

    # Donnéés traitées pour construire graph 2
    df_comparaison_France['Part de service fermé'] = df_comparaison_France['Part de service fermé'].round(1)

    fig = px.bar(df_comparaison_France.head(10), y="catégorie", x=["ouvert", "Service fermé"],orientation='h', 
                 custom_data=['Part de service fermé'], color_discrete_sequence= [ '#7201a8', '#d8576b']) 

    fig.update_layout(title="<b>Quels sont les services qui ferment le plus pendant l'été</b>",
                          margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,
                            yaxis_title="",
                            xaxis_title="Nombre de services",
                            legend_title="Statut",)
    fig.update_traces(hovertemplate='Catégorie de service: %{y}<br> Nbre de service: %{x}  <br>Taux de fermeture :%{customdata}%') 
    st.plotly_chart(fig, use_container_width=True)

    
    # Donnéés traitées pour construire graph 3

    df_stacked_per_france = df_stacked_per_france.round()

    fig = px.bar(df_stacked_per_france, x="Categories", y=["Structure fermée", "Changement d'horaire", "Service fermé", "Ouvert"], 
                text='value', color_discrete_sequence= [ '#7201a8', '#bd3786', '#d8576b', '#ed7953'])
    fig.update_layout(title="<b>Quels impacts à l'été sur les services</b>",
                        margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,
                        legend_title="Services",                     
                        xaxis_title="",
                        yaxis_title="",)

    st.plotly_chart(fig, use_container_width=True)

    
    # Donnéés traitées pour construire graph 4
    
    res_france.rename(index={0: 'Soliguide', 1:'Acteurs'}, inplace=True)
    
    fig = px.pie(values=res_france.status, names=res_france.index, color_discrete_sequence=['palevioletred'])
    fig.update_traces(textinfo="percent+label")
    fig.update_layout(title="<b>Qui actualisent les données estivales ?</b>",
                      margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,)

    st.plotly_chart(fig, use_container_width=True)

    

    st.markdown("<h3 style='text-align: center; color: #3E3A71;'>La mise à jour été en quelques chiffres</h3>", unsafe_allow_html=True)


    html_string = "<br>"

    st.markdown(html_string, unsafe_allow_html=True)

    html_string = "<center><font color='#3E3A71' face='Helvetica' size='6'>6 000 &emsp;&emsp;&emsp; 840 &emsp;&emsp;&emsp;&ensp; 94 065</font><br/><font size='2'>e-mails et relances envoyées &emsp;&emsp;&emsp;&emsp; appels effectués &emsp;&emsp;&emsp;&emsp; recherchés réalisées sur Soliguide<br> <br></font>"

    st.markdown(html_string, unsafe_allow_html=True)



 ###############
##  ILE DE FRANCE   ##
###############

if categorie == 'Ile-De-France':
    st.markdown("<h1 style='text-align: center; color: #3E3A71;'>Soliguide - Mise à jour été 2021</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #3E3A71;'>100% de la base de données mise à jour pour l'été - Île-de-France</h2>", unsafe_allow_html=True)


    html_string = "<br>"

    st.markdown(html_string, unsafe_allow_html=True)

    html_string = "<center><font color='#3E3A71' face='Helvetica' size='6'>8 727 &emsp;&emsp;&emsp; 3 645 &emsp;&emsp;&emsp;&ensp; 486</font><br/><font size='2'>&emsp;structures accompagnées cette été &emsp;&emsp;&emsp; structures ont fermé &emsp;&emsp;&emsp;&emsp; structures ont changé d'horaire<br> <br></font>"

    st.markdown(html_string, unsafe_allow_html=True)
 
    # Création de la carte avec pour centre : le centre d ela France
    mappy = folium.Map(location=[df_fiches_IDF.latitude[0], df_fiches_IDF.longitude[0]],zoom_start=8.5)

    marker_cluster = MarkerCluster().add_to(mappy)

    # Ajout des différents markers :
    for en in range(len(df_fiches_IDF['colors'])):
        folium.CircleMarker([df_fiches_IDF.latitude[en], df_fiches_IDF.longitude[en]],
                            fill = True,
                            color = df_fiches_IDF['colors'][en],
                            radius = 5,
                            fill_color = df_fiches_IDF['colors'][en],
                            tooltip=df_fiches_IDF['Fermeture_Estivale'][en], 
                            popup=df_fiches_IDF['name'][en]
                            ).add_to( mappy )
    mappy.save('map.html')

    #Affichage de la carte
    folium_static(mappy)


    # Donnéés traitées pour construire graph 2
    df_comparaison_IDF['Part de service fermé'] = df_comparaison_IDF['Part de service fermé'].round(1)

    fig = px.bar(df_comparaison_IDF.head(10), y="catégorie", x=["ouvert", "Service fermé"],orientation='h', 
                 custom_data=['Part de service fermé'], color_discrete_sequence= [ '#7201a8', '#d8576b']) 

    fig.update_layout(title="<b>Quels sont les services qui ferment le plus pendant l'été</b>",
                          margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,
                            yaxis_title="",
                            xaxis_title="Nombre de services",
                            legend_title="Statut",)
    fig.update_traces(hovertemplate='Catégorie de service: %{y}<br> Nbre de service: %{x}  <br>Taux de fermeture :%{customdata}%') 
    st.plotly_chart(fig, use_container_width=True)
 

    html_string = "<h2>2 229 mails envoyés et au moins 840 appels réalisés</h2>"

    st.markdown(html_string, unsafe_allow_html=True)


    html_string = "<h2>94 065 recherches ont été effectuées sur soliguide cette été</h2>"

    st.markdown(html_string, unsafe_allow_html=True)

   # Donnéés traitées pour construire graph 3

    df_stacked_per_IDF = df_stacked_per_IDF.round()

    fig = px.bar(df_stacked_per_IDF, x="Categories", y=["Structure fermée", "Changement d'horaire", "Service fermé", "Ouvert"], 
                text='value', color_discrete_sequence= [ '#7201a8', '#bd3786', '#d8576b', '#ed7953'])
    fig.update_layout(title="<b>Quels impacts à l'été sur les services</b>",
                        margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,
                        legend_title="Services",                     
                        xaxis_title="",
                        yaxis_title="",)

    st.plotly_chart(fig, use_container_width=True)

    # Donnéés traitées pour construire graph 4
    
    res_IDF.rename(index={0: 'Soliguide', 1:'Acteurs'}, inplace=True)
    
    fig = px.pie(values=res_IDF.status, names=res_IDF.index, color_discrete_sequence=['palevioletred'])
    fig.update_traces(textinfo="percent+label")
    fig.update_layout(title="<b>Qui actualisent les données estivales ?</b>",
                      margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,)

    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<h3 style='text-align: center; color: #3E3A71;'>La mise à jour été en quelques chiffres</h3>", unsafe_allow_html=True)


    html_string = "<br>"

    st.markdown(html_string, unsafe_allow_html=True)

    html_string = "<center><font color='#3E3A71' face='Helvetica' size='6'>4 351 &emsp;&emsp;&emsp; 421 &emsp;&emsp;&emsp;&ensp; </font><br/><font size='2'>e-mails et relances envoyées &emsp;&emsp;&emsp;&emsp; appels effectués &emsp;&emsp;&emsp;&emsp; recherchés réalisées sur Soliguide<br> <br></font>"

    st.markdown(html_string, unsafe_allow_html=True)

#######################
##  ALPES MARITIMES  ##
#######################

if categorie == 'Alpes-Maritimes (06)':
    st.markdown("<h1 style='text-align: center; color: #3E3A71;'>Soliguide - Mise à jour été 2021</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #3E3A71;'>100% de la base de données mise à jour pour l'été - Alpes-Maritimes</h2>", unsafe_allow_html=True)


    html_string = "<br>"

    st.markdown(html_string, unsafe_allow_html=True)

    html_string = "<center><font color='#3E3A71' face='Helvetica' size='6'>576 &emsp;&emsp;&emsp;&ensp;&ensp; 208 &emsp;&emsp;&emsp;&emsp;&ensp; 2</font><br/><font size='2'>&emsp;structures accompagnées cette été &emsp;&emsp;&emsp; structures ont fermé &emsp;&emsp;&emsp;&emsp; structures ont changé d'horaire<br> <br></font>"

    st.markdown(html_string, unsafe_allow_html=True)

    # Création de la carte avec pour centre : le centre d ela France
    mappy = folium.Map(location=[df_fiches_06.latitude[0], df_fiches_06.longitude[0]],zoom_start=8.5)

    marker_cluster = MarkerCluster().add_to(mappy)

    # Ajout des différents markers :
    for en in range(len(df_fiches_06['colors'])):
        folium.CircleMarker([df_fiches_06.latitude[en], df_fiches_06.longitude[en]],
        fill = True,
        color = df_fiches_06['colors'][en],
        radius = 5,
        fill_color = df_fiches_06['colors'][en],
        tooltip=df_fiches_06['Fermeture_Estivale'][en], 
        popup=df_fiches_06['name'][en]
        ).add_to( mappy )
    mappy.save('map.html')

    #Affichage de la carte
    folium_static(mappy)

    # Donnéés traitées pour construire graph 2
    df_comparaison_06['Part de service fermé'] = df_comparaison_06['Part de service fermé'].round(1)

    fig = px.bar(df_comparaison_06.head(10), y="catégorie", x=["ouvert", "Service fermé"],orientation='h', 
                 custom_data=['Part de service fermé'], color_discrete_sequence= [ '#7201a8', '#d8576b']) 

    fig.update_layout(title="<b>Quels sont les services qui ferment le plus pendant l'été</b>",
                          margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,
                            yaxis_title="",
                            xaxis_title="Nombre de services",
                            legend_title="Statut",)
    fig.update_traces(hovertemplate='Catégorie de service: %{y}<br> Nbre de service: %{x}  <br>Taux de fermeture :%{customdata}%') 
    st.plotly_chart(fig, use_container_width=True)
 
  # Donnéés traitées pour construire graph 3

    df_stacked_per_06 = df_stacked_per_06.round()
    
    fig = px.bar(df_stacked_per_06, x="Categories", y=["Structure fermée", "Changement d'horaire", "Service fermé", "Ouvert"], 
                text='value', color_discrete_sequence= [ '#7201a8', '#bd3786', '#d8576b', '#ed7953'])
    fig.update_layout(title="<b>Quels impacts à l'été sur les services</b>",
                        margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,
                        legend_title="Services",                     
                        xaxis_title="",
                        yaxis_title="",)

    st.plotly_chart(fig, use_container_width=True)
    
    # Donnéés traitées pour construire graph 4
    
    res_06.rename(index={0: 'Soliguide', 1:'Acteurs'}, inplace=True)
    
    fig = px.pie(values=res_06.status, names=res_06.index, color_discrete_sequence=['palevioletred'])
    fig.update_traces(textinfo="percent+label")
    fig.update_layout(title="<b>Qui actualisent les données estivales ?</b>",
                      margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,)

    st.plotly_chart(fig, use_container_width=True)

    html_string = "<h2>2 229 mails envoyés et au moins 840 appels réalisés</h2>"

    st.markdown(html_string, unsafe_allow_html=True)

    html_string = "<h2>94 065 recherches ont été effectuées sur soliguide cette été</h2>"

    st.markdown(html_string, unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center; color: #3E3A71;'>La mise à jour été en quelques chiffres</h3>", unsafe_allow_html=True)


    html_string = "<br>"

    st.markdown(html_string, unsafe_allow_html=True)

    html_string = "<center><font color='#3E3A71' face='Helvetica' size='6'>418 &emsp;&emsp;&emsp;  &emsp;&emsp;&emsp;&ensp; 4120</font><br/><font size='2'>e-mails et relances envoyées &emsp;&emsp;&emsp;&emsp;  &emsp;&emsp;&emsp;&emsp; recherchés réalisées sur Soliguide<br> <br></font>"

    st.markdown(html_string, unsafe_allow_html=True)

    
###############
##  GIRONDE  ##
###############

if categorie == 'Gironde (33)':
    st.markdown("<h1 style='text-align: center; color: #3E3A71;'>Soliguide - Mise à jour été 2021</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #3E3A71;'>100% de la base de données mise à jour pour l'été - Gironde</h2>", unsafe_allow_html=True)


    html_string = "<br>"

    st.markdown(html_string, unsafe_allow_html=True)

    html_string = "<center><font color='#3E3A71' face='Helvetica' size='6'>972 &emsp;&emsp;&emsp;&emsp;&emsp; 583 &emsp;&emsp;&emsp;&emsp;&ensp; 104</font><br/><font size='2'>&emsp;structures accompagnées cette été &emsp;&emsp;&emsp; structures ont fermé &emsp;&emsp;&emsp;&emsp; structures ont changé d'horaire<br> <br></font>"

    st.markdown(html_string, unsafe_allow_html=True)
 
 
    # Création de la carte avec pour centre : le centre d ela France
    mappy = folium.Map(location=[df_fiches_33.latitude[0], df_fiches_33.longitude[0]],zoom_start=8.5)

    marker_cluster = MarkerCluster().add_to(mappy)

    # Ajout des différents markers :
    for en in range(len(df_fiches_33['colors'])):
        folium.CircleMarker([df_fiches_33.latitude[en], df_fiches_33.longitude[en]],
                            fill = True,
                            color = df_fiches_33['colors'][en],
                            radius = 5,
                            fill_color = df_fiches_33['colors'][en],
                            tooltip=df_fiches_33['Fermeture_Estivale'][en], 
                            popup=df_fiches_33['name'][en]
                            ).add_to( mappy )
    mappy.save('map.html')

    #Affichage de la carte
    folium_static(mappy)
    
    # Donnéés traitées pour construire graph 2
    df_comparaison_33['Part de service fermé'] = df_comparaison_33['Part de service fermé'].round(1)

    fig = px.bar(df_comparaison_33.head(10), y="catégorie", x=["ouvert", "Service fermé"],orientation='h', 
                 custom_data=['Part de service fermé'], color_discrete_sequence= [ '#7201a8', '#d8576b']) 

    fig.update_layout(title="<b>Quels sont les services qui ferment le plus pendant l'été</b>",
                          margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,
                            yaxis_title="",
                            xaxis_title="Nombre de services",
                            legend_title="Statut",)
    fig.update_traces(hovertemplate='Catégorie de service: %{y}<br> Nbre de service: %{x}  <br>Taux de fermeture :%{customdata}%') 
    st.plotly_chart(fig, use_container_width=True)
    
    
   # Donnéés traitées pour construire graph 3

    df_stacked_per_33 = df_stacked_per_33.round()

    fig = px.bar(df_stacked_per_33, x="Categories", y=["Structure fermée", "Changement d'horaire", "Service fermé", "Ouvert"], 
                text='value', color_discrete_sequence= [ '#7201a8', '#bd3786', '#d8576b', '#ed7953'])
    fig.update_layout(title="<b>Quels impacts à l'été sur les services</b>",
                        margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,
                        legend_title="Services",                     
                        xaxis_title="",
                        yaxis_title="",)

    st.plotly_chart(fig, use_container_width=True)
    
    # Donnéés traitées pour construire graph 4
    
    res_33.rename(index={0: 'Soliguide', 1:'Acteurs'}, inplace=True)
    
    fig = px.pie(values=res_33.status, names=res_33.index, color_discrete_sequence=['palevioletred'])
    fig.update_traces(textinfo="percent+label")
    fig.update_layout(title="<b>Qui actualisent les données estivales ?</b>",
                      margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,)

    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<h3 style='text-align: center; color: #3E3A71;'>La mise à jour été en quelques chiffres</h3>", unsafe_allow_html=True)

    html_string = "<br>"

    st.markdown(html_string, unsafe_allow_html=True)

    html_string = "<center><font color='#3E3A71' face='Helvetica' size='6'>597 &emsp;&emsp;&emsp; 268 &emsp;&emsp;&emsp;&ensp; 12 787</font><br/><font size='2'>e-mails et relances envoyées &emsp;&emsp;&emsp;&emsp; appels effectués &emsp;&emsp;&emsp;&emsp; recherchés réalisées sur Soliguide<br> <br></font>"

    st.markdown(html_string, unsafe_allow_html=True)

########################
##  LOIRE ATLANTIQUE  ##
########################

if categorie == 'Loire-Atlantique (44)':
    st.markdown("<h1 style='text-align: center; color: #3E3A71;'>Soliguide - Mise à jour été 2021</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #3E3A71;'>100% de la base de données mise à jour pour l'été - Loire-Atlantique</h2>", unsafe_allow_html=True)


    html_string = "<br>"

    st.markdown(html_string, unsafe_allow_html=True)

    html_string = "<center><font color='#3E3A71' face='Helvetica' size='6'>982 &emsp;&emsp;&emsp;&emsp; 662 &emsp;&emsp;&emsp;&emsp;&ensp; 78</font><br/><font size='2'>&emsp;structures accompagnées cette été &emsp;&emsp;&emsp; structures ont fermé &emsp;&emsp;&emsp;&emsp; structures ont changé d'horaire<br> <br></font>"

    st.markdown(html_string, unsafe_allow_html=True)
   
    # Création de la carte avec pour centre : le centre d ela France
    mappy = folium.Map(location=[df_fiches_44.latitude[0], df_fiches_44.longitude[0]],zoom_start=8.2)

    marker_cluster = MarkerCluster().add_to(mappy)

    # Ajout des différents markers :
    for en in range(len(df_fiches_33['colors'])):
        folium.CircleMarker([df_fiches_44.latitude[en], df_fiches_44.longitude[en]],
                            fill = True,
                            color = df_fiches_44['colors'][en],
                            radius = 5,
                            fill_color = df_fiches_44['colors'][en],
                            tooltip=df_fiches_44['Fermeture_Estivale'][en], 
                            popup=df_fiches_44['name'][en]
                            ).add_to( mappy )
    mappy.save('map.html')

    #Affichage de la carte
    folium_static(mappy)
    
    # Donnéés traitées pour construire graph 2
    df_comparaison_44['Part de service fermé'] = df_comparaison_44['Part de service fermé'].round(1)

    fig = px.bar(df_comparaison_44.head(10), y="catégorie", x=["ouvert", "Service fermé"],orientation='h', 
                 custom_data=['Part de service fermé'], color_discrete_sequence= [ '#7201a8', '#d8576b']) 

    fig.update_layout(title="<b>Quels sont les services qui ferment le plus pendant l'été</b>",
                          margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,
                            yaxis_title="",
                            xaxis_title="Nombre de services",
                            legend_title="Statut",)
    fig.update_traces(hovertemplate='Catégorie de service: %{y}<br> Nbre de service: %{x}  <br>Taux de fermeture :%{customdata}%') 
    st.plotly_chart(fig, use_container_width=True)

   # Donnéés traitées pour construire graph 3

    df_stacked_per_44 = df_stacked_per_44.round()

    fig = px.bar(df_stacked_per_44, x="Categories", y=["Structure fermée", "Changement d'horaire", "Service fermé", "Ouvert"], 
                text='value', color_discrete_sequence= [ '#7201a8', '#bd3786', '#d8576b', '#ed7953'])
    fig.update_layout(title="<b>Quels impacts à l'été sur les services</b>",
                        margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,
                        legend_title="Services",                     
                        xaxis_title="",
                        yaxis_title="",)

    st.plotly_chart(fig, use_container_width=True)

    # Donnéés traitées pour construire graph 4
    
    res_44.rename(index={0: 'Soliguide', 1:'Acteurs'}, inplace=True)
    
    fig = px.pie(values=res_44.status, names=res_44.index, color_discrete_sequence=['palevioletred'])
    fig.update_traces(textinfo="percent+label")
    fig.update_layout(title="<b>Qui actualisent les données estivales ?</b>",
                      margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,)

    st.plotly_chart(fig, use_container_width=True)
    
    
    st.markdown("<h3 style='text-align: center; color: #3E3A71;'>La mise à jour été en quelques chiffres</h3>", unsafe_allow_html=True)


    html_string = "<br>"

    st.markdown(html_string, unsafe_allow_html=True)

    html_string = "<center><font color='#3E3A71' face='Helvetica' size='6'>767 &emsp;&emsp;&emsp; 95 &emsp;&emsp;&emsp;&ensp; 8 899</font><br/><font size='2'>e-mails et relances envoyées &emsp;&emsp;&emsp;&emsp; appels effectués &emsp;&emsp;&emsp;&emsp; recherchés réalisées sur Soliguide<br> <br></font>"

    st.markdown(html_string, unsafe_allow_html=True)

################
##  BAS-RHIN  ##
################

if categorie == 'Bas-Rhin (67)':
    st.markdown("<h1 style='text-align: center; color: #3E3A71;'>Soliguide - Mise à jour été 2021</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #3E3A71;'>100% de la base de données mise à jour pour l'été - Bas-Rhin</h2>", unsafe_allow_html=True)


    html_string = "<br>"

    st.markdown(html_string, unsafe_allow_html=True)

    html_string = "<center><font color='#3E3A71' face='Helvetica' size='6'>421 &emsp;&emsp;&emsp;&emsp; 179 &emsp;&emsp;&emsp;&emsp;&ensp; 39</font><br/><font size='2'>&emsp;structures accompagnées cette été &emsp;&emsp;&emsp; structures ont fermé &emsp;&emsp;&emsp;&emsp; structures ont changé d'horaire<br> <br></font>"

    st.markdown(html_string, unsafe_allow_html=True)
 
    # Création de la carte avec pour centre : le centre d ela France
    mappy = folium.Map(location=[df_fiches_67.latitude[0], df_fiches_67.longitude[0]],zoom_start=8.5)

    marker_cluster = MarkerCluster().add_to(mappy)

    # Ajout des différents markers :
    for en in range(len(df_fiches_67['colors'])):
        folium.CircleMarker([df_fiches_67.latitude[en], df_fiches_67.longitude[en]],
                            fill = True,
                            color = df_fiches_67['colors'][en],
                            radius = 5,
                            fill_color = df_fiches_67['colors'][en],
                            tooltip=df_fiches_67['Fermeture_Estivale'][en], 
                            popup=df_fiches_67['name'][en]
                            ).add_to( mappy )
    mappy.save('map.html')

    #Affichage de la carte
    folium_static(mappy)

     # Donnéés traitées pour construire graph 2
    df_comparaison_67['Part de service fermé'] = df_comparaison_67['Part de service fermé'].round(1)

    fig = px.bar(df_comparaison_67.head(10), y="catégorie", x=["ouvert", "Service fermé"],orientation='h', 
                 custom_data=['Part de service fermé'], color_discrete_sequence= [ '#7201a8', '#d8576b']) 

    fig.update_layout(title="<b>Quels sont les services qui ferment le plus pendant l'été</b>",
                          margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,
                            yaxis_title="",
                            xaxis_title="Nombre de services",
                            legend_title="Statut",)
    fig.update_traces(hovertemplate='Catégorie de service: %{y}<br> Nbre de service: %{x}  <br>Taux de fermeture :%{customdata}%') 
    st.plotly_chart(fig, use_container_width=True)


   # Donnéés traitées pour construire graph 3

    df_stacked_per_67 = df_stacked_per_67.round()
    
    fig = px.bar(df_stacked_per_67, x="Categories", y=["Structure fermée", "Changement d'horaire", "Service fermé", "Ouvert"], 
                text='value', color_discrete_sequence= [ '#7201a8', '#bd3786', '#d8576b', '#ed7953'])
    fig.update_layout(title="<b>Quels impacts à l'été sur les services</b>",
                        margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,
                        legend_title="Services",                     
                        xaxis_title="",
                        yaxis_title="",)

    st.plotly_chart(fig, use_container_width=True)

    # Donnéés traitées pour construire graph 4
    
    res_67.rename(index={0: 'Soliguide', 1:'Acteurs'}, inplace=True)
    
    fig = px.pie(values=res_67.status, names=res_67.index, color_discrete_sequence=['palevioletred'])
    fig.update_traces(textinfo="percent+label")
    fig.update_layout(title="<b>Qui actualisent les données estivales ?</b>",
                      margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,)

    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<h3 style='text-align: center; color: #3E3A71;'>La mise à jour été en quelques chiffres</h3>", unsafe_allow_html=True)


    html_string = "<br>"

    st.markdown(html_string, unsafe_allow_html=True)

    html_string = "<center><font color='#3E3A71' face='Helvetica' size='6'>245 &emsp;&emsp;&emsp; 56 &emsp;&emsp;&emsp;&ensp; 11 501</font><br/><font size='2'>e-mails et relances envoyées &emsp;&emsp;&emsp;&emsp; appels effectués &emsp;&emsp;&emsp;&emsp; recherchés réalisées sur Soliguide<br> <br></font>"

    st.markdown(html_string, unsafe_allow_html=True)
    
################
##  PARIS  ##
################

if categorie == 'Paris (75)':
    st.markdown("<h1 style='text-align: center; color: #3E3A71;'>Soliguide - Mise à jour été 2021</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #3E3A71;'>100% de la base de données mise à jour pour l'été - Paris</h2>", unsafe_allow_html=True)


    html_string = "<br>"

    st.markdown(html_string, unsafe_allow_html=True)

    html_string = "<center><font color='#3E3A71' face='Helvetica' size='6'>2 624 &emsp;&emsp;&emsp; 1 076 &emsp;&emsp;&emsp;&ensp;&ensp;  74</font><br/><font size='2'>&emsp;structures accompagnées cette été &emsp;&emsp;&emsp; structures ont fermé &emsp;&emsp;&emsp;&emsp; structures ont changé d'horaire<br> <br></font>"

    st.markdown(html_string, unsafe_allow_html=True)
  
    # Création de la carte avec pour centre : le centre d ela France
    mappy = folium.Map(location=[48.856614, 2.3522219],zoom_start=12.1)

    marker_cluster = MarkerCluster().add_to(mappy)

    # Ajout des différents markers :
    for en in range(len(df_fiches_75['colors'])):
        folium.CircleMarker([df_fiches_75.latitude[en], df_fiches_75.longitude[en]],
                            fill = True,
                            color = df_fiches_75['colors'][en],
                            radius = 5,
                            fill_color = df_fiches_75['colors'][en],
                            tooltip=df_fiches_75['Fermeture_Estivale'][en], 
                            popup=df_fiches_75['name'][en]
                            ).add_to( mappy )
    mappy.save('map.html')

    #Affichage de la carte
    folium_static(mappy)

     # Donnéés traitées pour construire graph 2
    df_comparaison_75['Part de service fermé'] = df_comparaison_75['Part de service fermé'].round(1)

    fig = px.bar(df_comparaison_75.head(10), y="catégorie", x=["ouvert", "Service fermé"],orientation='h', 
                 custom_data=['Part de service fermé'], color_discrete_sequence= [ '#7201a8', '#d8576b']) 

    fig.update_layout(title="<b>Quels sont les services qui ferment le plus pendant l'été</b>",
                          margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,
                            yaxis_title="",
                            xaxis_title="Nombre de services",
                            legend_title="Statut",)
    fig.update_traces(hovertemplate='Catégorie de service: %{y}<br> Nbre de service: %{x}  <br>Taux de fermeture :%{customdata}%') 
    st.plotly_chart(fig, use_container_width=True)


   # Donnéés traitées pour construire graph 3

    df_stacked_per_75 = df_stacked_per_75.round()

    fig = px.bar(df_stacked_per_75, x="Categories", y=["Structure fermée", "Changement d'horaire", "Service fermé", "Ouvert"], 
                text='value', color_discrete_sequence= [ '#7201a8', '#bd3786', '#d8576b', '#ed7953'])
    fig.update_layout(title="<b>Quels impacts à l'été sur les services</b>",
                        margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,
                        legend_title="Services",                     
                        xaxis_title="",
                        yaxis_title="",)

    st.plotly_chart(fig, use_container_width=True)

    
    # Donnéés traitées pour construire graph 4
    
    res_75.rename(index={0: 'Soliguide', 1:'Acteurs'}, inplace=True)
    
    fig = px.pie(values=res_75.status, names=res_75.index, color_discrete_sequence=['palevioletred'])
    fig.update_traces(textinfo="percent+label")
    fig.update_layout(title="<b>Qui actualisent les données estivales ?</b>",
                      margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,)

    st.plotly_chart(fig, use_container_width=True)


######################
##  SEINE-ET-MARNE  ##
######################

if categorie == 'Seine-et-Marne (77)':
    st.markdown("<h1 style='text-align: center; color: #3E3A71;'>Soliguide - Mise à jour été 2021</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #3E3A71;'>100% de la base de données mise à jour pour l'été - Seine-et-Marne</h2>", unsafe_allow_html=True)


    html_string = "<br>"

    st.markdown(html_string, unsafe_allow_html=True)

    html_string = "<center><font color='#3E3A71' face='Helvetica' size='6'>414 &emsp;&emsp;&emsp;&emsp; 29 &emsp;&emsp;&emsp;&emsp;&emsp;  5</font><br/><font size='2'>&emsp;structures accompagnées cette été &emsp;&emsp;&emsp; structures ont fermé &emsp;&emsp;&emsp;&emsp; structures ont changé d'horaire<br> <br></font>"

    st.markdown(html_string, unsafe_allow_html=True)
   
    # Création de la carte avec pour centre : le centre d ela France
    mappy = folium.Map(location=[df_fiches_77.latitude[0], df_fiches_77.longitude[0]],zoom_start=8.2)

    marker_cluster = MarkerCluster().add_to(mappy)

    # Ajout des différents markers :
    for en in range(len(df_fiches_77['colors'])):
        folium.CircleMarker([df_fiches_77.latitude[en], df_fiches_77.longitude[en]],
                            fill = True,
                            color = df_fiches_77['colors'][en],
                            radius = 5,
                            fill_color = df_fiches_77['colors'][en],
                            tooltip=df_fiches_77['Fermeture_Estivale'][en], 
                            popup=df_fiches_77['name'][en]
                            ).add_to( mappy )
    mappy.save('map.html')

    #Affichage de la carte
    folium_static(mappy)

     # Donnéés traitées pour construire graph 2
    df_comparaison_77['Part de service fermé'] = df_comparaison_77['Part de service fermé'].round(1)

    fig = px.bar(df_comparaison_77.head(10), y="catégorie", x=["ouvert", "Service fermé"],orientation='h', 
                 custom_data=['Part de service fermé'], color_discrete_sequence= [ '#7201a8', '#d8576b']) 

    fig.update_layout(title="<b>Quels sont les services qui ferment le plus pendant l'été</b>",
                          margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,
                            yaxis_title="",
                            xaxis_title="Nombre de services",
                            legend_title="Statut",)
    fig.update_traces(hovertemplate='Catégorie de service: %{y}<br> Nbre de service: %{x}  <br>Taux de fermeture :%{customdata}%') 
    st.plotly_chart(fig, use_container_width=True)


   # Donnéés traitées pour construire graph 3

    df_stacked_per_77 = df_stacked_per_77.round()

    fig = px.bar(df_stacked_per_77, x="Categories", y=["Structure fermée", "Changement d'horaire", "Service fermé", "Ouvert"], 
                text='value', color_discrete_sequence= [ '#7201a8', '#bd3786', '#d8576b', '#ed7953'])
    fig.update_layout(title="<b>Quels impacts à l'été sur les services</b>",
                        margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,
                        legend_title="Services",                     
                        xaxis_title="",
                        yaxis_title="",)

    st.plotly_chart(fig, use_container_width=True)

       
    # Donnéés traitées pour construire graph 3
    res_77.rename(index={0: 'Soliguide', 1:'Acteurs'}, inplace=True)
    
    fig = px.pie(values=res_77.status, names=res_77.index, color_discrete_sequence=['palevioletred'])
    fig.update_traces(textinfo="percent+label")
    fig.update_layout(title="<b>Qui actualisent les données estivales ?</b>",
                      margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,)

    st.plotly_chart(fig, use_container_width=True)

################
##  YVELINES  ##
################

if categorie == 'Yvelines (78)':
    st.markdown("<h1 style='text-align: center; color: #3E3A71;'>Soliguide - Mise à jour été 2021</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #3E3A71;'>100% de la base de données mise à jour pour l'été - Yvelines</h2>", unsafe_allow_html=True)


    html_string = "<br>"

    st.markdown(html_string, unsafe_allow_html=True)

    html_string = "<center><font color='#3E3A71' face='Helvetica' size='6'>1 008 &emsp;&emsp;&emsp;&emsp; 724 &emsp;&emsp;&emsp;&emsp;&ensp;  42</font><br/><font size='2'>&emsp;structures accompagnées cette été &emsp;&emsp;&emsp; structures ont fermé &emsp;&emsp;&emsp;&emsp; structures ont changé d'horaire<br> <br></font>"

    st.markdown(html_string, unsafe_allow_html=True)
 
    # Création de la carte avec pour centre : le centre d ela France
    mappy = folium.Map(location=[df_fiches_78.latitude[0], df_fiches_78.longitude[0]],zoom_start=8.5)

    marker_cluster = MarkerCluster().add_to(mappy)

    # Ajout des différents markers :
    for en in range(len(df_fiches_78['colors'])):
        folium.CircleMarker([df_fiches_78.latitude[en], df_fiches_78.longitude[en]],
                            fill = True,
                            color = df_fiches_78['colors'][en],
                            radius = 5,
                            fill_color = df_fiches_78['colors'][en],
                            tooltip=df_fiches_78['Fermeture_Estivale'][en], 
                            popup=df_fiches_78['name'][en]
                            ).add_to( mappy )
    mappy.save('map.html')

    #Affichage de la carte
    folium_static(mappy)


     # Donnéés traitées pour construire graph 2
    df_comparaison_78['Part de service fermé'] = df_comparaison_78['Part de service fermé'].round(1)

    fig = px.bar(df_comparaison_78.head(10), y="catégorie", x=["ouvert", "Service fermé"],orientation='h', 
                 custom_data=['Part de service fermé'], color_discrete_sequence= [ '#7201a8', '#d8576b']) 

    fig.update_layout(title="<b>Quels sont les services qui ferment le plus pendant l'été</b>",
                          margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,
                            yaxis_title="",
                            xaxis_title="Nombre de services",
                            legend_title="Statut",)
    fig.update_traces(hovertemplate='Catégorie de service: %{y}<br> Nbre de service: %{x}  <br>Taux de fermeture :%{customdata}%') 
    st.plotly_chart(fig, use_container_width=True)


   # Donnéés traitées pour construire graph 3

    df_stacked_per_78 = df_stacked_per_78.round()

    fig = px.bar(df_stacked_per_78, x="Categories", y=["Structure fermée", "Changement d'horaire", "Service fermé", "Ouvert"], 
                text='value', color_discrete_sequence= [ '#7201a8', '#bd3786', '#d8576b', '#ed7953'])
    fig.update_layout(title="<b>Quels impacts à l'été sur les services</b>",
                        margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,
                        legend_title="Services",                     
                        xaxis_title="",
                        yaxis_title="",)

    st.plotly_chart(fig, use_container_width=True)
       
    # Donnéés traitées pour construire graph 4
    res_78.rename(index={0: 'Soliguide', 1:'Acteurs'}, inplace=True)
    
    fig = px.pie(values=res_78.status, names=res_78.index, color_discrete_sequence=['palevioletred'])
    fig.update_traces(textinfo="percent+label")
    fig.update_layout(title="<b>Qui actualisent les données estivales ?</b>",
                      margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,)

    st.plotly_chart(fig, use_container_width=True)


################
##  ESSONNE  ##
################

if categorie == 'Essonne (91)':
    st.markdown("<h1 style='text-align: center; color: #3E3A71;'>Soliguide - Mise à jour été 2021</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #3E3A71;'>100% de la base de données mise à jour pour l'été - Essonne</h2>", unsafe_allow_html=True)


    html_string = "<br>"

    st.markdown(html_string, unsafe_allow_html=True)

    html_string = "<center><font color='#3E3A71' face='Helvetica' size='6'>482 &emsp;&emsp;&emsp;&emsp;&ensp; 89 &emsp;&emsp;&emsp;&emsp;&emsp; 24</font><br/><font size='2'>&emsp;structures accompagnées cette été &emsp;&emsp;&emsp; structures ont fermé &emsp;&emsp;&emsp;&emsp; structures ont changé d'horaire<br> <br></font>"

    st.markdown(html_string, unsafe_allow_html=True)
 
    # Création de la carte avec pour centre : le centre d ela France
    mappy = folium.Map(location=[df_fiches_91.latitude[0], df_fiches_91.longitude[0]],zoom_start=9.5)

    marker_cluster = MarkerCluster().add_to(mappy)

    # Ajout des différents markers :
    for en in range(len(df_fiches_91['colors'])):
        folium.CircleMarker([df_fiches_91.latitude[en], df_fiches_91.longitude[en]],
                            fill = True,
                            color = df_fiches_91['colors'][en],
                            radius = 5,
                            fill_color = df_fiches_91['colors'][en],
                            tooltip=df_fiches_91['Fermeture_Estivale'][en], 
                            popup=df_fiches_91['name'][en]
                            ).add_to( mappy )
    mappy.save('map.html')

    #Affichage de la carte
    folium_static(mappy)

     # Donnéés traitées pour construire graph 2
    df_comparaison_91['Part de service fermé'] = df_comparaison_91['Part de service fermé'].round(1)

    fig = px.bar(df_comparaison_91.head(10), y="catégorie", x=["ouvert", "Service fermé"],orientation='h', 
                 custom_data=['Part de service fermé'], color_discrete_sequence= [ '#7201a8', '#d8576b']) 

    fig.update_layout(title="<b>Quels sont les services qui ferment le plus pendant l'été</b>",
                          margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,
                            yaxis_title="",
                            xaxis_title="Nombre de services",
                            legend_title="Statut",)
    fig.update_traces(hovertemplate='Catégorie de service: %{y}<br> Nbre de service: %{x}  <br>Taux de fermeture :%{customdata}%') 
    st.plotly_chart(fig, use_container_width=True)


   # Donnéés traitées pour construire graph 3

    df_stacked_per_91 = df_stacked_per_91.round()

    fig = px.bar(df_stacked_per_91, x="Categories", y=["Structure fermée", "Changement d'horaire", "Service fermé", "Ouvert"], 
                text='value', color_discrete_sequence= [ '#7201a8', '#bd3786', '#d8576b', '#ed7953'])
    fig.update_layout(title="<b>Quels impacts à l'été sur les services</b>",
                        margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,
                        legend_title="Services",                     
                        xaxis_title="",
                        yaxis_title="",)

    st.plotly_chart(fig, use_container_width=True)

       
    # Donnéés traitées pour construire graph 4
    res_91.rename(index={0: 'Soliguide', 1:'Acteurs'}, inplace=True)
    
    fig = px.pie(values=res_91.status, names=res_91.index, color_discrete_sequence=['palevioletred'])
    fig.update_traces(textinfo="percent+label")
    fig.update_layout(title="<b>Qui actualisent les données estivales ?</b>",
                      margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,)

    st.plotly_chart(fig, use_container_width=True)

######################
##  HAUTS-DE-SEINE  ##
######################

if categorie == 'Hauts-de-Seine (92)':
    st.markdown("<h1 style='text-align: center; color: #3E3A71;'>Soliguide - Mise à jour été 2021</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #3E3A71;'>100% de la base de données mise à jour pour l'été - Hauts-de-Seine</h2>", unsafe_allow_html=True)


    html_string = "<br>"

    st.markdown(html_string, unsafe_allow_html=True)

    html_string = "<center><font color='#3E3A71' face='Helvetica' size='6'>1 365 &emsp;&emsp;&emsp;&emsp; 883 &emsp;&emsp;&emsp;&emsp;  54</font><br/><font size='2'>&emsp;structures accompagnées cette été &emsp;&emsp;&emsp; structures ont fermé &emsp;&emsp;&emsp;&emsp; structures ont changé d'horaire<br> <br></font>"

    st.markdown(html_string, unsafe_allow_html=True)
   
    # Création de la carte avec pour centre : le centre d ela France
    mappy = folium.Map(location=[48.828508, 2.2188068],zoom_start=11)

    marker_cluster = MarkerCluster().add_to(mappy)
 
    # Création de la carte avec pour centre : le centre d ela France
    mappy = folium.Map(location=[48.828508, 2.2188068],zoom_start=11)

    marker_cluster = MarkerCluster().add_to(mappy)

    # Ajout des différents markers :
    for en in range(len(df_fiches_92['colors'])):
        folium.CircleMarker([df_fiches_92.latitude[en], df_fiches_92.longitude[en]],
                            fill = True,
                            color = df_fiches_92['colors'][en],
                            radius = 5,
                            fill_color = df_fiches_92['colors'][en],
                            tooltip=df_fiches_92['Fermeture_Estivale'][en], 
                            popup=df_fiches_92['name'][en]
                            ).add_to( mappy )
    mappy.save('map.html')

    #Affichage de la carte
    folium_static(mappy)

     # Donnéés traitées pour construire graph 2
    df_comparaison_92['Part de service fermé'] = df_comparaison_92['Part de service fermé'].round(1)

    fig = px.bar(df_comparaison_92.head(10), y="catégorie", x=["ouvert", "Service fermé"],orientation='h', 
                 custom_data=['Part de service fermé'], color_discrete_sequence= [ '#7201a8', '#d8576b']) 

    fig.update_layout(title="<b>Quels sont les services qui ferment le plus pendant l'été</b>",
                          margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,
                            yaxis_title="",
                            xaxis_title="Nombre de services",
                            legend_title="Statut",)
    fig.update_traces(hovertemplate='Catégorie de service: %{y}<br> Nbre de service: %{x}  <br>Taux de fermeture :%{customdata}%') 
    st.plotly_chart(fig, use_container_width=True)


   # Donnéés traitées pour construire graph 3

    df_stacked_per_92 = df_stacked_per_92.round()

    fig = px.bar(df_stacked_per_92, x="Categories", y=["Structure fermée", "Changement d'horaire", "Service fermé", "Ouvert"], 
                text='value', color_discrete_sequence= [ '#7201a8', '#bd3786', '#d8576b', '#ed7953'])
    fig.update_layout(title="<b>Quels impacts à l'été sur les services</b>",
                        margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,
                        legend_title="Services",                     
                        xaxis_title="",
                        yaxis_title="",)

    st.plotly_chart(fig, use_container_width=True)

    # Donnéés traitées pour construire graph 4
    res_92.rename(index={0: 'Soliguide', 1:'Acteurs'}, inplace=True)
    
    fig = px.pie(values=res_92.status, names=res_92.index, color_discrete_sequence=['palevioletred'])
    fig.update_traces(textinfo="percent+label")
    fig.update_layout(title="<b>Qui actualisent les données estivales ?</b>",
                      margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,)

    st.plotly_chart(fig, use_container_width=True)

#########################
##  SEINE-SAINT-DENIS  ##
#########################

if categorie == 'Seine-Saint-Denis (93)':
    st.markdown("<h1 style='text-align: center; color: #3E3A71;'>Soliguide - Mise à jour été 2021</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #3E3A71;'>100% de la base de données mise à jour pour l'été - Seine-Saint-Denis</h2>", unsafe_allow_html=True)


    html_string = "<br>"

    st.markdown(html_string, unsafe_allow_html=True)

    html_string = "<center><font color='#3E3A71' face='Helvetica' size='6'>1 035 &emsp;&emsp;&emsp;&emsp; 645 &emsp;&emsp;&emsp;&emsp;  78</font><br/><font size='2'>&emsp;structures accompagnées cette été &emsp;&emsp;&emsp; structures ont fermé &emsp;&emsp;&emsp;&emsp; structures ont changé d'horaire<br> <br></font>"

    st.markdown(html_string, unsafe_allow_html=True)

    # Création de la carte avec pour centre : le centre d ela France
    mappy = folium.Map(location=[df_fiches_93.latitude[0], df_fiches_93.longitude[0]],zoom_start=11)

    marker_cluster = MarkerCluster().add_to(mappy)

    # Ajout des différents markers :
    for en in range(len(df_fiches_93['colors'])):
        folium.CircleMarker([df_fiches_93.latitude[en], df_fiches_93.longitude[en]],
                            fill = True,
                            color = df_fiches_93['colors'][en],
                            radius = 5,
                            fill_color = df_fiches_93['colors'][en],
                            tooltip=df_fiches_93['Fermeture_Estivale'][en], 
                            popup=df_fiches_93['name'][en]
                            ).add_to( mappy )
    mappy.save('map.html')

    #Affichage de la carte
    folium_static(mappy)

     # Donnéés traitées pour construire graph 2
    df_comparaison_93['Part de service fermé'] = df_comparaison_93['Part de service fermé'].round(1)

    fig = px.bar(df_comparaison_93.head(10), y="catégorie", x=["ouvert", "Service fermé"],orientation='h', 
                 custom_data=['Part de service fermé'], color_discrete_sequence= [ '#7201a8', '#d8576b']) 

    fig.update_layout(title="<b>Quels sont les services qui ferment le plus pendant l'été</b>",
                          margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,
                            yaxis_title="",
                            xaxis_title="Nombre de services",
                            legend_title="Statut",)
    fig.update_traces(hovertemplate='Catégorie de service: %{y}<br> Nbre de service: %{x}  <br>Taux de fermeture :%{customdata}%') 
    st.plotly_chart(fig, use_container_width=True)


   # Donnéés traitées pour construire graph 3

    df_stacked_per_93 = df_stacked_per_93.round()

    fig = px.bar(df_stacked_per_93, x="Categories", y=["Structure fermée", "Changement d'horaire", "Service fermé", "Ouvert"], 
                text='value', color_discrete_sequence= [ '#7201a8', '#bd3786', '#d8576b', '#ed7953'])
    fig.update_layout(title="<b>Quels impacts à l'été sur les services</b>",
                        margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,
                        legend_title="Services",                     
                        xaxis_title="",
                        yaxis_title="",)

    st.plotly_chart(fig, use_container_width=True)

    # Donnéés traitées pour construire graph 4
    res_93.rename(index={0: 'Soliguide', 1:'Acteurs'}, inplace=True)
    
    fig = px.pie(values=res_93.status, names=res_93.index, color_discrete_sequence=['palevioletred'])
    fig.update_traces(textinfo="percent+label")
    fig.update_layout(title="<b>Qui actualisent les données estivales ?</b>",
                      margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,)

    st.plotly_chart(fig, use_container_width=True)


####################
##  VAL-DE-MARNE  ##
####################

if categorie == 'Val-de-Marne (94)':
    st.markdown("<h1 style='text-align: center; color: #3E3A71;'>Soliguide - Mise à jour été 2021</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #3E3A71;'>100% de la base de données mise à jour pour l'été - Val-de-Marne</h2>", unsafe_allow_html=True)


    html_string = "<br>"

    st.markdown(html_string, unsafe_allow_html=True)

    html_string = "<center><font color='#3E3A71' face='Helvetica' size='6'>599 &emsp;&emsp;&emsp;&emsp; 343 &emsp;&emsp;&emsp;&emsp;&ensp; 18</font><br/><font size='2'>&emsp;structures accompagnées cette été &emsp;&emsp;&emsp; structures ont fermé &emsp;&emsp;&emsp;&emsp; structures ont changé d'horaire<br> <br></font>"

    st.markdown(html_string, unsafe_allow_html=True)
   
    # Création de la carte avec pour centre : le centre d ela France
    mappy = folium.Map(location=[df_fiches_94.latitude[0], df_fiches_94.longitude[0]],zoom_start=11)

    marker_cluster = MarkerCluster().add_to(mappy)

    # Ajout des différents markers :
    for en in range(len(df_fiches_94['colors'])):
        folium.CircleMarker([df_fiches_94.latitude[en], df_fiches_94.longitude[en]],
                            fill = True,
                            color = df_fiches_94['colors'][en],
                            radius = 5,
                            fill_color = df_fiches_94['colors'][en],
                            tooltip=df_fiches_94['Fermeture_Estivale'][en], 
                            popup=df_fiches_94['name'][en]
                            ).add_to( mappy )
    mappy.save('map.html')

    #Affichage de la carte
    folium_static(mappy)

     # Donnéés traitées pour construire graph 2
    df_comparaison_94['Part de service fermé'] = df_comparaison_94['Part de service fermé'].round(1)

    fig = px.bar(df_comparaison_94.head(10), y="catégorie", x=["ouvert", "Service fermé"],orientation='h', 
                 custom_data=['Part de service fermé'], color_discrete_sequence= [ '#7201a8', '#d8576b']) 

    fig.update_layout(title="<b>Quels sont les services qui ferment le plus pendant l'été</b>",
                          margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,
                            yaxis_title="",
                            xaxis_title="Nombre de services",
                            legend_title="Statut",)
    fig.update_traces(hovertemplate='Catégorie de service: %{y}<br> Nbre de service: %{x}  <br>Taux de fermeture :%{customdata}%') 
    st.plotly_chart(fig, use_container_width=True)


   # Donnéés traitées pour construire graph 3

    df_stacked_per_94 = df_stacked_per_94.round()

    fig = px.bar(df_stacked_per_94, x="Categories", y=["Structure fermée", "Changement d'horaire", "Service fermé", "Ouvert"], 
                text='value', color_discrete_sequence= [ '#7201a8', '#bd3786', '#d8576b', '#ed7953'])
    fig.update_layout(title="<b>Quels impacts à l'été sur les services</b>",
                        margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,
                        legend_title="Services",                     
                        xaxis_title="",
                        yaxis_title="",)

    st.plotly_chart(fig, use_container_width=True)

    # Donnéés traitées pour construire graph 4
    res_94.rename(index={0: 'Soliguide', 1:'Acteurs'}, inplace=True)
    
    fig = px.pie(values=res_94.status, names=res_94.index, color_discrete_sequence=['palevioletred'])
    fig.update_traces(textinfo="percent+label")
    fig.update_layout(title="<b>Qui actualisent les données estivales ?</b>",
                      margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,)

    st.plotly_chart(fig, use_container_width=True)

####################
##  VAL-D'OISE  ##
####################

if categorie == 'Val-d\'Oise (95)':
    st.markdown("<h1 style='text-align: center; color: #3E3A71;'>Soliguide - Mise à jour été 2021</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #3E3A71;'>100% de la base de données mise à jour pour l'été - Val-d'Oise</h2>", unsafe_allow_html=True)


    html_string = "<br>"

    st.markdown(html_string, unsafe_allow_html=True)

    html_string = "<center><font color='#3E3A71' face='Helvetica' size='6'>1 052 &emsp;&emsp;&emsp;&emsp; 676 &emsp;&emsp;&emsp;&ensp;&ensp;  183</font><br/><font size='2'>&emsp;structures accompagnées cette été &emsp;&emsp;&emsp; structures ont fermé &emsp;&emsp;&emsp;&emsp; structures ont changé d'horaire<br> <br></font>"

    st.markdown(html_string, unsafe_allow_html=True)

    # Création de la carte avec pour centre 
    mappy = folium.Map(location=[df_fiches_95.latitude[0], df_fiches_95.longitude[0]],zoom_start=9.5)

    marker_cluster = MarkerCluster().add_to(mappy)

    # Ajout des différents markers :
    for en in range(len(df_fiches_95['colors'])):
        folium.CircleMarker([df_fiches_95.latitude[en], df_fiches_95.longitude[en]],
                            fill = True,
                            color = df_fiches_95['colors'][en],
                            radius = 5,
                            fill_color = df_fiches_95['colors'][en],
                            tooltip=df_fiches_95['Fermeture_Estivale'][en], 
                            popup=df_fiches_95['name'][en]
                            ).add_to( mappy )
    mappy.save('map.html')

    #Affichage de la carte
    folium_static(mappy)

    
     # Donnéés traitées pour construire graph 2
    df_comparaison_95['Part de service fermé'] = df_comparaison_95['Part de service fermé'].round(1)

    fig = px.bar(df_comparaison_95.head(10), y="catégorie", x=["ouvert", "Service fermé"],orientation='h', 
                 custom_data=['Part de service fermé'], color_discrete_sequence= [ '#7201a8', '#d8576b']) 

    fig.update_layout(title="<b>Quels sont les services qui ferment le plus pendant l'été</b>",
                          margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,
                            yaxis_title="",
                            xaxis_title="Nombre de services",
                            legend_title="Statut",)
    fig.update_traces(hovertemplate='Catégorie de service: %{y}<br> Nbre de service: %{x}  <br>Taux de fermeture :%{customdata}%') 
    st.plotly_chart(fig, use_container_width=True)


   # Donnéés traitées pour construire graph 3

    df_stacked_per_95 = df_stacked_per_95.round()

    fig = px.bar(df_stacked_per_95, x="Categories", y=["Structure fermée", "Changement d'horaire", "Service fermé", "Ouvert"], 
                text='value', color_discrete_sequence= [ '#7201a8', '#bd3786', '#d8576b', '#ed7953'])
    fig.update_layout(title="<b>Quels impacts à l'été sur les services</b>",
                        margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,
                        legend_title="Services",                     
                        xaxis_title="",
                        yaxis_title="",)

    st.plotly_chart(fig, use_container_width=True)


    # Donnéés traitées pour construire graph 4
    res_95.rename(index={0: 'Soliguide', 1:'Acteurs'}, inplace=True)
    
    fig = px.pie(values=res_95.status, names=res_95.index, color_discrete_sequence=['palevioletred'])
    fig.update_traces(textinfo="percent+label")
    fig.update_layout(title="<b>Qui actualisent les données estivales ?</b>",
                      margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,)

    st.plotly_chart(fig, use_container_width=True)
    
