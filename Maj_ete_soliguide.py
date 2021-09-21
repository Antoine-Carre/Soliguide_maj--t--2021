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
df_IDF = pd.read_csv('df_IDF.csv')
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



df_fiches = pd.read_csv('df_fiches.csv')
df_history = pd.read_csv('df_history.csv')
df_mails = pd.read_csv('df_mails.csv')
df_search = pd.read_csv('search.csv')
df_appel = pd.read_csv('Organisme_allDep_appel.csv')
df_fiches_IDF = pd.read_csv('df_fiches_IDF.csv')
df_fiches_06 = pd.read_csv('df_fiches_06.csv')



# Modification du fichier fiches pour ne garder que les zones concernée par la màj été
df_fiches = df_fiches[(df_fiches['region']=='Île-de-France') |(df_fiches['departement']=='Gironde') 
                     |(df_fiches['departement']== 'Alpes-Maritimes') |(df_fiches['departement']=='Bas-Rhin')
                     |(df_fiches['departement']=='Loire-Atlantique') ]
df_fiches.reset_index(inplace=True)

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


    # Donnéés traitées pour construire graph 2
    from numpy import nan
    df_fiches['services'] = df_fiches.services_all.astype(str).apply(lambda x:eval(x))
    df_close_4 =pd.json_normalize(df_fiches['services'])
    df_fiche_closed_4 = pd.concat([df_fiches, df_close_4], axis=1)

    data_you_need=pd.DataFrame()
    for n in range(25):
        test = pd.merge(df_fiche_closed_2['Fermeture_Estivale'], pd.json_normalize(df_close_4[n]), how='left', left_index=True, right_index=True)
        test = test[['Fermeture_Estivale','categorie','name', 'close.actif','close.dateDebut','close.dateFin']]
        data_you_need=data_you_need.append(test,ignore_index=True)
    
    df_categories_closed = pd.merge(data_you_need, categories_df, how='left', left_on='categorie', right_on='categorie')
    df_categories_closed['Counts']=1

    # Nbre de services
    df2=df_categories_closed.groupby(['name_y'], as_index=False).agg({'categorie':'count'})

    df2b=df_categories_closed.groupby(['Fermeture_Estivale','close.actif', 'name_y'], as_index=False).agg({'categorie':'count'})
    test = df2b[(df2b['close.actif']==True) | (df2b['Fermeture_Estivale']=='Fermé') ]
    df3=test.groupby(['name_y'], as_index=False).agg({'categorie':'sum'})
    
    df_comparaison = pd.merge(df2,df3, how='left', left_on='name_y', right_on='name_y')

    df_comparaison['percent'] = (df_comparaison['categorie_y'] / df_comparaison['categorie_x']) * 100
    df_comparaison_sorted = df_comparaison.sort_values(by='percent', ascending=False)

    df_comparaison_sorted['ouvert'] = df_comparaison_sorted.categorie_x - df_comparaison_sorted.categorie_y
    df_comparaison_sorted.rename(columns={'categorie_y':'fermé','name_y':'catégorie','categorie_x':'Nbre_de_services'}, inplace=True)
    
    fig = px.bar(df_comparaison_sorted, x="catégorie", y="Nbre_de_services", color="percent",
                hover_data=['fermé'])
    fig.update_xaxes(range=(-.5, 35))
    fig.update_layout(title="<b>Quels sont les services qui ferment le plus pendant l'été</b>",
                      margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,
                        xaxis_title="",
                        yaxis_title="Nombre de services",)


    st.plotly_chart(fig, use_container_width=True)


    # Donnéés traitées pour construire graph 3
    df_stacked_services = df_categories_closed[['name_y','categorie','Fermeture_Estivale','close.actif']]
    df_stacked_services.rename(columns={"name_y":"catégories", "categorie":"categorie_code","close.actif":"service_fermé"}, inplace=True)

    df_stacked_services = pd.merge(df_stacked_services, pd.get_dummies(df_stacked_services.Fermeture_Estivale), left_index=True, right_index=True)

    df_stacked_services = pd.merge(df_stacked_services, pd.get_dummies(df_stacked_services.service_fermé), left_index=True, right_index=True)

    df_stacked_services.drop(columns=['Fermeture_Estivale','service_fermé'], inplace=True)

    df_stacked_services['Categories'] = df_stacked_services['categorie_code'].astype(str)
    df_stacked_services['Categories'] = df_stacked_services['Categories'].str.replace(r'^10\d', 'Santé')
    df_stacked_services['Categories'] = df_stacked_services['Categories'].str.replace(r'^11\d{1,}', 'Santé')
    df_stacked_services['Categories'] = df_stacked_services['Categories'].str.replace(r'^20\d', 'Formation')
    df_stacked_services['Categories'] = df_stacked_services['Categories'].str.replace(r'^30\d', 'Hygiène')
    df_stacked_services['Categories'] = df_stacked_services['Categories'].str.replace(r'^40\d', 'Conseil')
    df_stacked_services['Categories'] = df_stacked_services['Categories'].str.replace(r'^50\d', 'Technologie')
    df_stacked_services['Categories'] = df_stacked_services['Categories'].str.replace(r'^60\d', 'Alimentation')
    df_stacked_services['Categories'] = df_stacked_services['Categories'].str.replace(r'^70\d', 'Accueil')
    df_stacked_services['Categories'] = df_stacked_services['Categories'].str.replace(r'^80\d', 'Activités')
    df_stacked_services['Categories'] = df_stacked_services['Categories'].str.replace(r'^90\d', 'Matériel')
    df_stacked_services['Categories'] = df_stacked_services['Categories'].apply(lambda x: x[:-2])

    df_stacked_services[True] = df_stacked_services[True] + df_stacked_services['Fermé']
    df_stacked_services[True].replace(2, 0)

    df_stacked_services = df_stacked_services[['Categories','catégories','Fermé','Modification',True]]

    df_stacked = df_stacked_services.groupby('Categories')[['Fermé', 'Modification',True]].sum().reset_index()
    df_stacked = df_stacked.rename(columns={'Fermé':'Structure fermée','Modification':'Changement d\'horaire',True:'Service fermé'})
    df_stacked = df_stacked[df_stacked.Categories !='n']

    df_stacked_per = df_stacked.copy()

    df_stacked_per.iloc[:, 1:] = df_stacked_per.iloc[:, 1:].apply(lambda x: x.div(x.sum()).mul(100), axis=1).astype(float)
    df_stacked_per = df_stacked_per.round(2)

    fig2 = px.bar(df_stacked_per, x="Categories", y=["Structure fermée", "Changement d'horaire", "Service fermé"], 
             color_discrete_sequence= [ '#7201a8', '#bd3786', '#d8576b'],
             text = 'value',)

    fig2.update_traces(
        hovertemplate="<br>".join([
            "Categories: %{x}",
            "Poucentage: %{y}%"
            ])
    )
    fig2.update_layout(title="<b>Quels impacts à l'été sur les services</b>",
                      margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,
                        xaxis_title="",
                        yaxis_title="Nombre de services",)

    fig2.update_layout(
        legend=dict(title = "Types d'impact" ))
        
        
    st.plotly_chart(fig2, use_container_width=True)

    # Recuperation des données concernant les mise à jours
    df_history['userDatas'] = df_history.userDatas.astype(str).apply(lambda x:eval(x))
    df_history_bis =pd.json_normalize(df_history['userDatas'])
    df_history_bis_2 = pd.concat([df_history, df_history_bis], axis=1)

    # Extraction des données nécessaire au pie chart
    df_history_2 = df_history_bis_2[['_id','created_at','status']]

    # Mise en forme de la date pour permettre le filtrage sur les donné concernant la MàJ été 2021
    df_history_2.created_at = pd.to_datetime(df_history_2['created_at']).dt.strftime('%Y-%m-%d')

    # Filtrage des données sur la période estival 2021  
    df_history_2 = df_history_2.loc[(df_history_2['created_at']>"2021-05-31") & (df_history_2['created_at']>"2021-09-01")]

    # Après vérification, on a constater que certain compte pro ont été créés comme Simple_User, rectification pour le graph
    df_history_2.status.replace({'SIMPLE_USER': 'PRO'}, inplace=True)

    # Changement des noms pour une meilleure libilité du graph
    df_history_2.status.replace({'PRO': 'Acteurs', 'ADMIN_SOLIGUIDE': 'Soliguide'}, inplace=True)

    # Comptage des modification par type de profile
    res = pd.DataFrame(df_history_2.status.value_counts())

    fig = px.pie(values=res.status, names=res.index, color_discrete_sequence=['palevioletred'])
    fig.update_traces(textinfo="percent+label")
    fig.update_layout(title="<b>Qui actualisent les données estivales ?</b>",
                      margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,)

    st.plotly_chart(fig, use_container_width=True)


    html_string = "<h2>2 229 mails envoyés et au moins 840 appels réalisés</h2>"

    st.markdown(html_string, unsafe_allow_html=True)


    html_string = "<h2>94 065 recherches ont été effectuées sur soliguide cette été</h2>"

    st.markdown(html_string, unsafe_allow_html=True)


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


    # Donnéés traitées pour construire graph 2
    from numpy import nan
    df_fiches_IDF['services'] = df_fiches_IDF.services_all.astype(str).apply(lambda x:eval(x))
    df_fiches_IDF_close_3 =pd.json_normalize(df_fiches_IDF['services'])
    df_fiches_IDF_fiche_closed_3 = pd.concat([df_fiches_IDF, df_fiches_IDF_close_3], axis=1)

    data_you_need_idf=pd.DataFrame()
    for n in range(25):
        test = pd.merge(df_fiches_IDF['Fermeture_Estivale'], pd.json_normalize(df_fiches_IDF_close_3[n]), how='left', left_index=True, right_index=True)
        test = test[['Fermeture_Estivale','categorie','name', 'close.actif','close.dateDebut','close.dateFin']]
        data_you_need_idf=data_you_need_idf.append(test,ignore_index=True)
    
    df_categories_closed_idf = pd.merge(data_you_need_idf, categories_df, how='left', left_on='categorie', right_on='categorie')
    df_categories_closed_idf['Counts']=1

    # Nbre de services
    df2_idf=df_categories_closed_idf.groupby(['name_y'], as_index=False).agg({'categorie':'count'})

    dbf2_idf=df_categories_closed_idf.groupby(['Fermeture_Estivale','close.actif', 'name_y'], as_index=False).agg({'categorie':'count'})
    test = dbf2_idf[(dbf2_idf['close.actif']==True) | (dbf2_idf['Fermeture_Estivale']=='Fermé') ]
    df3_idf=test.groupby(['name_y'], as_index=False).agg({'categorie':'sum'})
    
    df_comparaison_idf = pd.merge(dbf2_idf,df3_idf, how='left', left_on='name_y', right_on='name_y')

    df_comparaison_idf['percent'] = (df_comparaison_idf['categorie_y'] / df_comparaison_idf['categorie_x']) * 100
    df_comparaison_sorted_idf = df_comparaison_idf.sort_values(by='percent', ascending=False)

    df_comparaison_sorted_idf['ouvert'] = df_comparaison_sorted_idf.categorie_x - df_comparaison_sorted_idf.categorie_y
    df_comparaison_sorted_idf.rename(columns={'categorie_y':'fermé','name_y':'catégorie','categorie_x':'Nbre_de_services'}, inplace=True)
    
    fig = px.bar(df_comparaison_sorted_idf, x="catégorie", y="Nbre_de_services", color="percent",
                hover_data=['fermé'])
    fig.update_xaxes(range=(-.5, 35))
    fig.update_layout(title="<b>Quels sont les services qui ferment le plus pendant l'été</b>",
                      margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,
                        xaxis_title="",
                        yaxis_title="Nombre de services",)


    st.plotly_chart(fig, use_container_width=True)


    # Donnéés traitées pour construire graph 3
    df_stacked_services_idf = df_categories_closed_idf[['name_y','categorie','Fermeture_Estivale','close.actif']]
    df_stacked_services_idf.rename(columns={"name_y":"catégories", "categorie":"categorie_code","close.actif":"service_fermé"}, inplace=True)

    df_stacked_services_idf = pd.merge(df_stacked_services_idf, pd.get_dummies(df_stacked_services_idf.Fermeture_Estivale), left_index=True, right_index=True)

    df_stacked_services_idf = pd.merge(df_stacked_services_idf, pd.get_dummies(df_stacked_services_idf.service_fermé), left_index=True, right_index=True)

    df_stacked_services_idf.drop(columns=['Fermeture_Estivale','service_fermé'], inplace=True)

    df_stacked_services_idf['Categories'] = df_stacked_services_idf['categorie_code'].astype(str)
    df_stacked_services_idf['Categories'] = df_stacked_services_idf['Categories'].str.replace(r'^10\d', 'Santé')
    df_stacked_services_idf['Categories'] = df_stacked_services_idf['Categories'].str.replace(r'^11\d{1,}', 'Santé')
    df_stacked_services_idf['Categories'] = df_stacked_services_idf['Categories'].str.replace(r'^20\d', 'Formation')
    df_stacked_services_idf['Categories'] = df_stacked_services_idf['Categories'].str.replace(r'^30\d', 'Hygiène')
    df_stacked_services_idf['Categories'] = df_stacked_services_idf['Categories'].str.replace(r'^40\d', 'Conseil')
    df_stacked_services_idf['Categories'] = df_stacked_services_idf['Categories'].str.replace(r'^50\d', 'Technologie')
    df_stacked_services_idf['Categories'] = df_stacked_services_idf['Categories'].str.replace(r'^60\d', 'Alimentation')
    df_stacked_services_idf['Categories'] = df_stacked_services_idf['Categories'].str.replace(r'^70\d', 'Accueil')
    df_stacked_services_idf['Categories'] = df_stacked_services_idf['Categories'].str.replace(r'^80\d', 'Activités')
    df_stacked_services_idf['Categories'] = df_stacked_services_idf['Categories'].str.replace(r'^90\d', 'Matériel')
    df_stacked_services_idf['Categories'] = df_stacked_services_idf['Categories'].apply(lambda x: x[:-2])

    df_stacked_services_idf[True] = df_stacked_services_idf[True] + df_stacked_services_idf['Fermé']
    df_stacked_services_idf[True].replace(2, 0)

    df_stacked_services_idf = df_stacked_services_idf[['Categories','catégories','Fermé','Modification',True]]

    df_stacked_idf = df_stacked_services_idf.groupby('Categories')[['Fermé', 'Modification',True]].sum().reset_index()
    df_stacked_idf = df_stacked_idf.rename(columns={'Fermé':'Structure fermée','Modification':'Changement d\'horaire',True:'Service fermé'})
    df_stacked_idf = df_stacked_idf[df_stacked_idf.Categories !='n']

    df_stacked_per_idf = df_stacked_idf.copy()

    df_stacked_per_idf.iloc[:, 1:] = df_stacked_per_idf.iloc[:, 1:].apply(lambda x: x.div(x.sum()).mul(100), axis=1).astype(float)
    df_stacked_per_idf = df_stacked_per_idf.round(2)

    fig = px.bar(df_stacked_per_idf, x="Categories", y=["Structure fermée", "Changement d'horaire", "Service fermé"], 
             color_discrete_sequence= [ '#7201a8', '#bd3786', '#d8576b'],
             text = 'value',)

    fig.update_traces(
        hovertemplate="<br>".join([
            "Categories: %{x}",
            "Poucentage: %{y}%"
            ])
    )
    fig.update_layout(title="<b>Quels impacts à l'été sur les services</b>",
                      margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,
                        xaxis_title="",
                        yaxis_title="Nombre de services",)

    fig.update_layout(
        legend=dict(
            title = "Types d'impact",
            ),
        
        )
        
        
    st.plotly_chart(fig, use_container_width=True)

    # Recuperation des données concernant les mise à jours
    df_history['userDatas'] = df_history.userDatas.astype(str).apply(lambda x:eval(x))
    df_history_bis =pd.json_normalize(df_history['userDatas'])
    df_history_bis_2 = pd.concat([df_history, df_history_bis], axis=1)

    # Extraction des données nécessaire au pie chart
    df_history_2 = df_history_bis_2[['_id','created_at','status']]

    # Mise en forme de la date pour permettre le filtrage sur les donné concernant la MàJ été 2021
    df_history_2.created_at = pd.to_datetime(df_history_2['created_at']).dt.strftime('%Y-%m-%d')

    # Filtrage des données sur la période estival 2021  
    df_history_2 = df_history_2.loc[(df_history_2['created_at']>"2021-05-31") & (df_history_2['created_at']>"2021-09-01")]

    # Après vérification, on a constater que certain compte pro ont été créés comme Simple_User, rectification pour le graph
    df_history_2.status.replace({'SIMPLE_USER': 'PRO'}, inplace=True)

    # Changement des noms pour une meilleure libilité du graph
    df_history_2.status.replace({'PRO': 'Acteurs', 'ADMIN_SOLIGUIDE': 'Soliguide'}, inplace=True)

    # Comptage des modification par type de profile
    res = pd.DataFrame(df_history_2.status.value_counts())

    fig = px.pie(values=res.status, names=res.index, color_discrete_sequence=['palevioletred'])
    fig.update_traces(textinfo="percent+label")
    fig.update_layout(title="<b>Qui actualisent les données estivales ?</b>",
                      margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,)

    st.plotly_chart(fig, use_container_width=True)


    html_string = "<h2>2 229 mails envoyés et au moins 840 appels réalisés</h2>"

    st.markdown(html_string, unsafe_allow_html=True)


    html_string = "<h2>94 065 recherches ont été effectuées sur soliguide cette été</h2>"

    st.markdown(html_string, unsafe_allow_html=True)

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

    # Donnéés traitées pour construire graph 2
    df_fiches_06['services'] = df_fiches_06.services_all.astype(str).apply(lambda x:eval(x))
    df_fiches_06_close_3 =pd.json_normalize(df_fiches_06['services'])
    df_fiches_06_fiche_closed_3 = pd.concat([df_fiches_06, df_fiches_06_close_3], axis=1)

    data_you_need_06=pd.DataFrame()
    for n in range(25):
        test = pd.merge(df_fiches_06['Fermeture_Estivale'], pd.json_normalize(df_fiches_06_close_3[n]), how='left', left_index=True, right_index=True)
        test = test[['Fermeture_Estivale','categorie','name', 'close.actif','close.dateDebut','close.dateFin']]
        data_you_need_06=data_you_need_06.append(test,ignore_index=True)
    
    df_categories_closed_06 = pd.merge(data_you_need_06, categories_df, how='left', left_on='categorie', right_on='categorie')
    df_categories_closed_06['Counts']=1

    # Nbre de services
    df2_06=df_categories_closed_06.groupby(['name_y'], as_index=False).agg({'categorie':'count'})

    dbf2_06=df_categories_closed_06.groupby(['Fermeture_Estivale','close.actif', 'name_y'], as_index=False).agg({'categorie':'count'})
    test = dbf2_06[(dbf2_06['close.actif']==True) | (dbf2_06['Fermeture_Estivale']=='Fermé') ]
    df3_06=test.groupby(['name_y'], as_index=False).agg({'categorie':'sum'})
    df_comparaison_06 = pd.merge(dbf2_06,df3_06, how='left', left_on='name_y', right_on='name_y')

    df_comparaison_06['percent'] = (df_comparaison_06['categorie_y'] / df_comparaison_06['categorie_x']) * 100
    df_comparaison_sorted_06 = df_comparaison_06.sort_values(by='percent', ascending=False)

    df_comparaison_sorted_06['ouvert'] = df_comparaison_sorted_06.categorie_x - df_comparaison_sorted_06.categorie_y
    df_comparaison_sorted_06.rename(columns={'categorie_y':'fermé','name_y':'catégorie','categorie_x':'Nbre_de_services'}, inplace=True)
    fig = px.bar(df_comparaison_sorted_06, x="catégorie", y="Nbre_de_services", color="percent",
    hover_data=['fermé'])
    fig.update_xaxes(range=(-.5, 35))
    fig.update_layout(title="<b>Quels sont les services qui ferment le plus pendant l'été</b>",
    margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,
    xaxis_title="",
    yaxis_title="Nombre de services",)

    st.plotly_chart(fig, use_container_width=True)

    # Donnéés traitées pour construire graph 3
    df_stacked_services_06 = df_categories_closed_06[['name_y','categorie','Fermeture_Estivale','close.actif']]
    df_stacked_services_06.rename(columns={"name_y":"catégories", "categorie":"categorie_code","close.actif":"service_fermé"}, inplace=True)

    df_stacked_services_06 = pd.merge(df_stacked_services_06, pd.get_dummies(df_stacked_services_06.Fermeture_Estivale), left_index=True, right_index=True)

    df_stacked_services_06 = pd.merge(df_stacked_services_06, pd.get_dummies(df_stacked_services_06.service_fermé), left_index=True, right_index=True)

    df_stacked_services_06.drop(columns=['Fermeture_Estivale','service_fermé'], inplace=True)

    df_stacked_services_06['Categories'] = df_stacked_services_06['categorie_code'].astype(str)
    df_stacked_services_06['Categories'] = df_stacked_services_06['Categories'].str.replace(r'^10\d', 'Santé')
    df_stacked_services_06['Categories'] = df_stacked_services_06['Categories'].str.replace(r'^11\d{1,}', 'Santé')
    df_stacked_services_06['Categories'] = df_stacked_services_06['Categories'].str.replace(r'^20\d', 'Formation')
    df_stacked_services_06['Categories'] = df_stacked_services_06['Categories'].str.replace(r'^30\d', 'Hygiène')
    df_stacked_services_06['Categories'] = df_stacked_services_06['Categories'].str.replace(r'^40\d', 'Conseil')
    df_stacked_services_06['Categories'] = df_stacked_services_06['Categories'].str.replace(r'^50\d', 'Technologie')
    df_stacked_services_06['Categories'] = df_stacked_services_06['Categories'].str.replace(r'^60\d', 'Alimentation')
    df_stacked_services_06['Categories'] = df_stacked_services_06['Categories'].str.replace(r'^70\d', 'Accueil')
    df_stacked_services_06['Categories'] = df_stacked_services_06['Categories'].str.replace(r'^80\d', 'Activités')
    df_stacked_services_06['Categories'] = df_stacked_services_06['Categories'].str.replace(r'^90\d', 'Matériel')
    df_stacked_services_06['Categories'] = df_stacked_services_06['Categories'].apply(lambda x: x[:-2])

    df_stacked_services_06[True] = df_stacked_services_06[True] + df_stacked_services_06['Fermé']
    df_stacked_services_06[True].replace(2, 0)

    df_stacked_services_06 = df_stacked_services_06[['Categories','catégories','Fermé','Modification',True]]

    df_stacked_06 = df_stacked_services_06.groupby('Categories')[['Fermé', 'Modification',True]].sum().reset_index()
    df_stacked_06 = df_stacked_06.rename(columns={'Fermé':'Structure fermée','Modification':'Changement d\'horaire',True:'Service fermé'})
    df_stacked_06 = df_stacked_06[df_stacked_06.Categories !='n']

    df_stacked_per_06 = df_stacked_06.copy()

    df_stacked_per_06.iloc[:, 1:] = df_stacked_per_06.iloc[:, 1:].apply(lambda x: x.div(x.sum()).mul(100), axis=1).astype(float)
    df_stacked_per_06 = df_stacked_per_06.round(2)

    fig = px.bar(df_stacked_per_06, x="Categories", y=["Structure fermée", "Changement d'horaire", "Service fermé"], 
    color_discrete_sequence= [ '#7201a8', '#bd3786', '#d8576b'],
    text = 'value',)

    fig.update_traces(
    hovertemplate="<br>".join([
    "Categories: %{x}",
    "Poucentage: %{y}%"
    ])
    )
    fig.update_layout(title="<b>Quels impacts à l'été sur les services</b>",
    margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,
    xaxis_title="",
    yaxis_title="Nombre de services",)

    fig.update_layout(
    legend=dict(
    title = "Types d'impact",
    ),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Recuperation des données concernant les mise à jours
    df_history['userDatas'] = df_history.userDatas.astype(str).apply(lambda x:eval(x))
    df_history_bis =pd.json_normalize(df_history['userDatas'])
    df_history_bis_2 = pd.concat([df_history, df_history_bis], axis=1)

    # Extraction des données nécessaire au pie chart
    df_history_2 = df_history_bis_2[['_id','created_at','status']]

    # Mise en forme de la date pour permettre le filtrage sur les donné concernant la MàJ été 2021
    df_history_2.created_at = pd.to_datetime(df_history_2['created_at']).dt.strftime('%Y-%m-%d')

    # Filtrage des données sur la période estival 2021 
    df_history_2 = df_history_2.loc[(df_history_2['created_at']>"2021-05-31") & (df_history_2['created_at']>"2021-09-01")]

    # Après vérification, on a constater que certain compte pro ont été créés comme Simple_User, rectification pour le graph
    df_history_2.status.replace({'SIMPLE_USER': 'PRO'}, inplace=True)

    # Changement des noms pour une meilleure libilité du graph
    df_history_2.status.replace({'PRO': 'Acteurs', 'ADMIN_SOLIGUIDE': 'Soliguide'}, inplace=True)

    # Comptage des modification par type de profile
    res = pd.DataFrame(df_history_2.status.value_counts())

    fig = px.pie(values=res.status, names=res.index, color_discrete_sequence=['palevioletred'])
    fig.update_traces(textinfo="percent+label")
    fig.update_layout(title="<b>Qui actualisent les données estivales ?</b>",
    margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,)

    st.plotly_chart(fig, use_container_width=True)

    html_string = "<h2>2 229 mails envoyés et au moins 840 appels réalisés</h2>"

    st.markdown(html_string, unsafe_allow_html=True)

    html_string = "<h2>94 065 recherches ont été effectuées sur soliguide cette été</h2>"

    st.markdown(html_string, unsafe_allow_html=True)
    
    
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

