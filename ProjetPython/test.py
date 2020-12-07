#TODO Étudier les corrélation entre pays limitrophes
#TODO Étudier les politiques des pays et ajouter sur les graph quand il y a eu par ex une campagne de vaccination pour voir si y a eu des évolutions
#TODO Peut être croiser avec d'autres données pour pas que ce soit trop "léger"
#TODO Utiliser folium pour des cartographies interactives stylées (compatible streamlit)

import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium
import json
from bokeh.plotting import figure, show
from bokeh.models import HoverTool, Title
import datetime

df = pd.read_csv("ebola_2014_2016_clean.csv")
dfFolium = pd.read_csv("ebola_2014_2016_clean.csv")
df["Date"] = pd.to_datetime(df["Date"])

# Barre de nativation :
st.sidebar.write("Navigation :  ")
page = st.sidebar.radio("", ('Accueil', "La maladie d'Ebola", 'Présentation du projet', 'Voir le dataset'))
if (page == "Accueil"):
    st.title("DIDIER Antoine - DINDART Juliette")
    st.header("Ebola - dashboard")
    st.image("streamlit_logo.png")
    st.write(
        "Ce projet est de créer un dashboard sur un dataset en streamlit. L'objectif est d'analyser le dataset et de comprendre comment l'épidémie s'est propagée en Afrique et en Europe ainsi que de voir comment la communauté internationale a pu gérer cette crise.")
    st.write("Lien de notre Github : https://github.com/Quercus00/Ebola-dashboard")

elif (page == "La maladie d'Ebola"):
    st.title("Ebola - Présentation")
    st.write(
        "Le virus Ebola est l'agent infectieux qui provoque, chez l'humain et les autres primates, des fièvres souvent hémorragiques — la maladie à virus Ebola — à l'origine d'épidémies historiques notables par leur ampleur et leur sévérité. La transmission entre humains a lieu avant tout par contact direct avec des fluides corporels.")
    st.write(
        "La maladie qu'il engendre, pour laquelle il n'existe pas jusqu'ici de traitement homologué, présente un taux de létalité allant de 25 % à 90 % chez l'humain ; l'épidémie qui a sévi en Afrique de l'Ouest en 2014 et 2015 affichait ainsi une létalité de 39,5 % au 27 mars 2016, avec 11 323 morts sur 28 646 cas recensés.Après un test efficace en 2015 lors d'une épidémie en Guinée, un premier vaccin a été annoncé à la fin de 2016 et utilisé pour une campagne vaccinale en Afrique de l'Ouest en 2017 ainsi qu’en République démocratique du Congo en 2019")
    st.header("Les symptômes")
    st.write(
        "Cette image ci-dessous représente les symptômes distinctifs d'une personne contaminée par le virus Ebola.")
    st.image("symptomes.jpg")

elif (page == "Présentation du projet"):

    st.title("Présentation du projet")

    st.header("Affichage des cas et morts cummulés")
    # st.write("Nombre cummulé des cas d'Ebola")
    # st.bar_chart(df['Cumulative no. of confirmed, probable and suspected cases'])
    # st.write("Nombre cummulé des morts d'Ebola")
    # st.bar_chart(df['Cumulative no. of confirmed, probable and suspected deaths'])

    #------------------------------------ GRAPH BOKEH ------------------------------

    test = df
    dfcases = test.groupby(["Date"])["Cumulative no. of confirmed, probable and suspected cases"].sum()
    dfcases = dfcases.reset_index()


    test = df
    dfdeaths = test.groupby(["Date"])["Cumulative no. of confirmed, probable and suspected deaths"].sum()
    dfdeaths = dfdeaths.reset_index()

    #on fusionne les deux dataframes obtenus avec le groupby
    dfcases["Cumulative no. of confirmed, probable and suspected deaths"] = dfdeaths["Cumulative no. of confirmed, probable and suspected deaths"]


    #---------------------------------- DATES IMPORTANTES EBOLA -------------------------------
    #Les 27 et 29 mars 2015, l'ensemble de la population sierra-léonaise est confinée à domicile afin de lutter contre l'épidémie

    # ----------------------- AFFICHER LES DATASET DU GRAPH BOKEH --------------------------
    printdfcase = st.checkbox("Afficher le dataset du graph")
    if printdfcase:
        st.write(dfcases)


    p = figure(plot_width=1000, plot_height=600, x_axis_type="datetime")
    p.title.text = 'Evolution of cases and deaths in the world'
    p.vbar(x="Date", width=1, bottom=0, source=dfcases,
           top="Cumulative no. of confirmed, probable and suspected cases", color="orange",
           legend_label="Cases", muted_color="orange", muted_alpha=0.2)
    p.vbar(x="Date", width=1, bottom=0, source=dfcases,
           top="Cumulative no. of confirmed, probable and suspected deaths", color="red",
           legend_label="Deaths", muted_color="red", muted_alpha=0.2)
    p.legend.location = "top_right"
    p.legend.click_policy = "mute"
    p.add_layout(Title(text="Date", align="center"), "below")
    p.add_layout(Title(text="Number of cases and deaths", align="center"), "left")

    p.add_tools(HoverTool(
        tooltips=[
            ('date', '@Date{%F}'),
            ('Cases', '@Cumulative no. of confirmed, probable and suspected cases'),  # use @{ } for field names with spaces
            ('deaths', '@Cumulative no. of confirmed, probable and suspected deaths'),
        ],

        formatters={
            'Date': 'datetime',  # use 'datetime' formatter for 'date' field
            # use default 'numeral' formatter for other fields
        },

        # display a tooltip whenever the cursor is vertically in line with a glyph
        mode='vline'
    ))


    st.write(p)


    #------------------------------- DISCUSSION GRAPH BOKEH ------------------------------
    st.write("Analysons le graphe ci-dessus : ")
    st.write("Tout d'abord nous pouvons voir que les cas augmentent très fortement, les morts sont très élevés, comme nous avons pu le voir dans la présentation de la maladie, le taux de mortalité est entre 25% et 80%")

    # ---------------------------------- MAP INTERACTIVE --------------------------------

    # permet de filtrer l'année : bouton radio pour selectionner année

    annee = st.radio("choisir une année", ('2014', '2015', '2016'))
    datelst = dfFolium['Date'].unique()
    dateliste = []
    for i in datelst:
        if i.startswith(annee):
            dateliste.append(i)
    # affichage des dates disponible selon l'année choisie
    choix_map = st.selectbox("Choisir une date pour la carte : ", dateliste)
    mask = dfFolium["Date"] == choix_map
    map_df = dfFolium[mask]

    # creation d'une carte centrée sur l'Afrique avec les données de la date choisie
    m = folium.Map(location=[12.486503, 14.141404], zoom_start=3)

    # créé avec https://geojson-maps.ash.ms/
    with open('custom.geo.json') as f:
        state_geo = json.load(f)
    for i in state_geo['features']:
        i['id'] = i['properties']['name']

    style_function = lambda x: {'fillColor': '#ffffff',
                                'color': '#000000',
                                'fillOpacity': 0.1,
                                'weight': 0.1}
    highlight_function = lambda x: {'fillColor': '#000000',
                                    'color': '#000000',
                                    'fillOpacity': 0.50,
                                    'weight': 0.1}

    folium.Choropleth(
        geo_data=state_geo,
        name='evolution',
        data=map_df,
        columns=['Country', 'Cumulative no. of confirmed, probable and suspected cases'],
        key_on='feature.id',
        fill_color='YlOrRd',
        # highlight_function=highlight_function,
        # couleurs de la légende. Autres couleurs possibles : ‘BuGn’, ‘BuPu’, ‘GnBu’, ‘OrRd’, ‘PuBu’, ‘PuBuGn’, ‘PuRd’, ‘RdPu’, ‘YlGn’, ‘YlGnBu’, ‘YlOrBr’, and ‘YlOrRd’
        fill_opacity=0.7,
        line_opacity=0.1,
        nan_fill_color='white',  # couleur par défaut pour les pays sans données
        legend_name='Cumulative cases Rate (%)',
        highlight=True,
    ).add_to(m)

    """"
    NIL = folium.features.GeoJson(
        map_df,
        style_function=style_function,
        control=False,
        highlight_function=highlight_function,
        tooltip=folium.features.GeoJsonTooltip(
            fields=['Country', 'Cumulative no. of confirmed, probable and suspected cases', 'Date'],
            aliases=['Country: ', 'Cumulative no. of confirmed, probable and suspected cases', 'Date'],
            style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
        )
    )
    m.add_child(NIL)
    m.keep_in_front(NIL)
    folium.LayerControl().add_to(m)
    """

    # call to render Folium map in Streamlit
    folium_static(m)

    dfcases = df.groupby(["Country", "Date"])["Cumulative no. of confirmed, probable and suspected cases"].sum()
    st.write(dfcases)

    """
    test = df
    output = test.groupby(["Date","Country"])["Cumulative no. of confirmed, probable and suspected cases"].sum()
    output
    output = output.reset_index()

    fig = px.scatter_geo(output, locations="Country", color="Country",
                         hover_name="Country", size="Cumulative no. of confirmed, probable and suspected cases",
                         projection="equirectangular", animation_frame="Date")
    st.write(fig)

    """


elif (page == "Voir le dataset"):
    # ouverture et affichage du csv
    df = pd.read_csv("ebola_2014_2016_clean.csv")
    st.title("Ebola dataset 2014 - 2016")  # titre du csv
    st.write(df)
