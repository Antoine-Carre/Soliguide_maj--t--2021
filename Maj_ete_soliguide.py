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
st.sidebar.image("https://www.solinum.org/wp-content/uploads/2020/09/Soliguide_RVB_Inline_Original_Onwhite@4x-1-1024x319.png", use_column_width=True)
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
df_france = pd.read_csv('df_france.csv')
df_fiches_IDF = pd.read_csv('df_IDF.csv')
df_fiches_06 = pd.read_csv('df_fiches_06.csv')
df_fiches_33 = pd.read_csv('df_fiches_33.csv')
df_fiches_44 = pd.read_csv('df_fiches_44.csv')
df_fiches_67 = pd.read_csv('df_fiches_67.csv')
df_fiches_75 = pd.read_csv('df_fiches_75.csv')
df_fiches_77 = pd.read_csv('df_fiches_77.csv')
df_fiches_78 = pd.read_csv('df_fiches_78.csv')
df_fiches_91 = pd.read_csv('df_fiches_91.csv')
df_fiches_92 = pd.read_csv('df_fiches_92.csv')
df_fiches_93 = pd.read_csv('df_fiches_93.csv')
df_fiches_94 = pd.read_csv('df_fiches_94.csv')
df_fiches_95 = pd.read_csv('df_fiches_95.csv')


# Catégories de la base
categories = {
    0: "Unknowed",
    100: "Santé",
    101: "Addiction",
    102: "Dépistage",
    103: "Psychologie",
    104: "Soins enfants",
    105: "Généraliste",
    106: "Dentaire",
    107: "Suivi grossesse",
    109: "Vaccination",
    110: "Infirmerie",
    111: "Vétérinaire",

    200: "Formation et emploi",
    201: "Atelier numérique",
    202: "Formation français",
    203: "Accompagnement à l'emploi",
    204: "Pôle emploi",
    205: "Chantier d'insertion",
    206: "Soutien scolaire",

    300: "Hygiène et bien-être",
    301: "Douche",
    302: "Laverie",
    303: "Bien-être",
    304: "Toilettes",
    305: "Protections périodiques",
    306: "Masques",

    400: "Conseil",
    401: "Conseil logement",
    402: "Permanence juridique",
    403: "Domiciliation",
    404: "Accompagnement social",
    405: "Ecrivain public",
    406: "Conseil handicap",
    407: "Conseil administratif",

    500: "Technologie",
    501: "Ordinateur",
    502: "Wifi",
    503: "Prise",
    504: "Téléphones",
    505: "Numérisation de documents",

    600: "Alimentation",
    601: "Distribution alimentaire",
    602: "Restauration assise",
    603: "Colis Alimentaire",
    604: "Epicerie AideSociale",
    605: "Fontaine",

    700: "Accueil",
    701: "Accueil de jour",
    702: "Hébergement d'urgence",
    703: "Hébergement à long terme",
    704: "Logement bas prix",
    705: "Espaces de repos",
    706: "Halte de nuit",
    707: "Garde d'enfants",

    800: "Activités",
    801: "Sport",
    802: "Musée",
    803: "Bibliothèque",
    804: "Activités",
    805: "Animations et loisirs",

    900: "Matériel",
    901: "Bagagerie",
    902: "Magasin solidaire",
    903: "Vêtements",
    904: "Animaux",

    1100: "Spécialistes",
    1101: "Allergologie",
    1102: "Cardiologie",
    1103: "Dermatologie",
    1104: "Echographie",
    1105: "Endocrinologie",
    1106: "Gastro-entérologie",
    1107: "Gynécologie",
    1108: "Kinésithérapie",
    1109: "Mammographie",
    1110: "Ophtalmologie",
    1111: "Oto-rhino-laryngologie",
    1112: "Nutrition",
    1113: "Pédicure",
    1114: "Phlébologie",
    1115: "Pneumologie",
    1116: "Radiologie",
    1117: "Rhumatologie",
    1118: "Urologie",
    1119: "Orthophonie",
    1120: "Stomatologie",
    1121: "Osthéopathie",
    1122: "Accupuncture",
    }
categories_df = pd.DataFrame(categories.items(), columns=['categorie', 'name'])

###############
##  FRANCE   ##
###############

if categorie == 'France':
    st.title('Solinum - Mise à jour été 2021')
    st.subheader("100% de la base de données mise à jour pour l'été")

    html_string = "<br>"

    st.markdown(html_string, unsafe_allow_html=True)

    st.markdown(
        """

        Durant l'été 2021, sur les **_11678 structures_** accompagnées par Solinum, **_6 228 ont fermé_** et **_709 ont changé leurs horaires_**.

        """
    )

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

 ###############
##  ILE DE FRANCE   ##
###############

if categorie == 'Ile-De-France':
    st.title('Solinum - Mise à jour été 2021 - Ile-de-France')
    st.subheader("100% de la base de données mise à jour pour l'été")

    html_string = "<br>"

    st.markdown(html_string, unsafe_allow_html=True)

    st.markdown(
        """

        Durant l'été 2021, sur les **_8 727 structures_** accompagnées par Solinum, **_3 645 ont 
        fermé_** et **_486 ont changé leurs horaires_**.
        """
    )
   
 
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


  

#######################
##  ALPES MARITIMES  ##
#######################

if categorie == 'Alpes-Maritimes (06)':
    st.title('Solinum - Mise à jour été 2021 - Alpes-Maritimes')
    st.subheader("100% de la base de données mise à jour pour l'été")

    html_string = "<br>"

    st.markdown(html_string, unsafe_allow_html=True)

    st.markdown(
        """

        Durant l'été 2021, sur les **_8 727 structures_** accompagnées par Solinum, **_3 645 ont 
        fermé_** et **_486 ont changé leurs horaires_**.
        """
    )
    # Filtrage pour ne garder que les données de la région

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

    
    
###############
##  GIRONDE  ##
###############

if categorie == 'Gironde (33)':
    st.title('Solinum - Mise à jour été 2021 - Gironde')
    st.subheader("100% de la base de données mise à jour pour l'été")

    html_string = "<br>"

    st.markdown(html_string, unsafe_allow_html=True)

    st.markdown(
        """

        Durant l'été 2021, sur les **_972 structures_** accompagnées par Solinum, **_583 ont 
        fermé_** et **_104 ont changé leurs horaires_**.
        """
    )
   
 
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


########################
##  LOIRE ATLANTIQUE  ##
########################

if categorie == 'Loire-Atlantique (44)':
    st.title('Solinum - Mise à jour été 2021 - Loire-Atlantique')
    st.subheader("100% de la base de données mise à jour pour l'été")

    html_string = "<br>"

    st.markdown(html_string, unsafe_allow_html=True)

    st.markdown(
        """

        Durant l'été 2021, sur les **_982 structures_** accompagnées par Solinum, **_662 ont 
        fermé_** et **_78 ont changé leurs horaires_**.
        """
    )
   
 
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


################
##  BAS-RHIN  ##
################

if categorie == 'Bas-Rhin (67)':
    st.title('Solinum - Mise à jour été 2021 - Bas-Rhin')
    st.subheader("100% de la base de données mise à jour pour l'été")

    html_string = "<br>"

    st.markdown(html_string, unsafe_allow_html=True)

    st.markdown(
        """

        Durant l'été 2021, sur les **_421 structures_** accompagnées par Solinum, **_179 ont 
        fermé_** et **_39 ont changé leurs horaires_**.
        """
    )
   
 
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


################
##  PARIS  ##
################

if categorie == 'Paris (75)':
    st.title('Solinum - Mise à jour été 2021 - Paris')
    st.subheader("100% de la base de données mise à jour pour l'été")

    html_string = "<br>"

    st.markdown(html_string, unsafe_allow_html=True)

    st.markdown(
        """

        Durant l'été 2021, sur les **_2 624 structures_** accompagnées par Solinum, **_1 076 ont 
        fermé_** et **_74 ont changé leurs horaires_**.
        """
    )
   
 
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

######################
##  SEINE-ET-MARNE  ##
######################

if categorie == 'Seine-et-Marne (77)':
    st.title('Solinum - Mise à jour été 2021 - Seine-et-Marne ')
    st.subheader("100% de la base de données mise à jour pour l'été")

    html_string = "<br>"

    st.markdown(html_string, unsafe_allow_html=True)

    st.markdown(
        """

        Durant l'été 2021, sur les **_414 structures_** accompagnées par Solinum, **_29 ont 
        fermé_** et **_5 ont changé leurs horaires_**.
        """
    )
   
 
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

################
##  YVELINES  ##
################

if categorie == 'Yvelines (78)':
    st.title('Solinum - Mise à jour été 2021 - Yvelines ')
    st.subheader("100% de la base de données mise à jour pour l'été")

    html_string = "<br>"

    st.markdown(html_string, unsafe_allow_html=True)

    st.markdown(
        """

        Durant l'été 2021, sur les **_1008 structures_** accompagnées par Solinum, **_724 ont 
        fermé_** et **_42 ont changé leurs horaires_**.
        """
    )
   
 
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


################
##  ESSONNE  ##
################

if categorie == 'Essonne (91)':
    st.title('Solinum - Mise à jour été 2021 - Essonne')
    st.subheader("100% de la base de données mise à jour pour l'été")

    html_string = "<br>"

    st.markdown(html_string, unsafe_allow_html=True)

    st.markdown(
        """

        Durant l'été 2021, sur les **_482 structures_** accompagnées par Solinum, **_89 ont 
        fermé_** et **_24 ont changé leurs horaires_**.
        """
    )
   
 
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


######################
##  HAUTS-DE-SEINE  ##
######################

if categorie == 'Hauts-de-Seine (92)':
    st.title('Solinum - Mise à jour été 2021 - Hauts-de-Seine')
    st.subheader("100% de la base de données mise à jour pour l'été")

    html_string = "<br>"

    st.markdown(html_string, unsafe_allow_html=True)

    st.markdown(
        """

        Durant l'été 2021, sur les **_1 365 structures_** accompagnées par Solinum, **_883 ont 
        fermé_** et **_54 ont changé leurs horaires_**.
        """
    )
   
 
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


#########################
##  SEINE-SAINT-DENIS  ##
#########################

if categorie == 'Seine-Saint-Denis (93)':
    st.title('Solinum - Mise à jour été 2021 - Seine-Saint-Denis')
    st.subheader("100% de la base de données mise à jour pour l'été")

    html_string = "<br>"

    st.markdown(html_string, unsafe_allow_html=True)

    st.markdown(
        """

        Durant l'été 2021, sur les **_1 035 structures_** accompagnées par Solinum, **_645 ont 
        fermé_** et **_78 ont changé leurs horaires_**.
        """
    )
   
 
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



####################
##  VAL-DE-MARNE  ##
####################

if categorie == 'Val-de-Marne (94)':
    st.title('Solinum - Mise à jour été 2021 - Val-de-Marne')
    st.subheader("100% de la base de données mise à jour pour l'été")

    html_string = "<br>"

    st.markdown(html_string, unsafe_allow_html=True)

    st.markdown(
        """

        Durant l'été 2021, sur les **_599 structures_** accompagnées par Solinum, **_343 ont 
        fermé_** et **_18 ont changé leurs horaires_**.
        """
    )
   
 
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




####################
##  VAL-D'OISE  ##
####################

if categorie == 'Val-d\'Oise (95)':
    st.title('Solinum - Mise à jour été 2021 - Val-d\'Oise')
    st.subheader("100% de la base de données mise à jour pour l'été")

    html_string = "<br>"

    st.markdown(html_string, unsafe_allow_html=True)

    st.markdown(
        """

        Durant l'été 2021, sur les **_1 052 structures_** accompagnées par Solinum, **_676 ont 
        fermé_** et **_183 ont changé leurs horaires_**.
        """
    )
   
 
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

