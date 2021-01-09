# TODO Étudier les corrélation entre pays limitrophes
# TODO Étudier les politiques des pays et ajouter sur les graph quand il y a eu par ex une campagne de vaccination pour voir si y a eu des évolutions
# TODO Peut être croiser avec d'autres données pour pas que ce soit trop "léger"
# TODO Utiliser folium pour des cartographies interactives stylées (compatible streamlit)

import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium
import json
from bokeh.plotting import figure, show
from bokeh.models import HoverTool, Title
import plotly.express as px
import datetime

df = pd.read_csv("ebola_2014_2016_clean.csv")
dfFolium = pd.read_csv("ebola_2014_2016_clean.csv")
df["Date"] = pd.to_datetime(df["Date"])

date = pd.read_csv("dates.csv")
date["date"] = pd.to_datetime(date["date"])

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

    st.write("La maladie à virus Ebola est une maladie virale aiguë sévère.")
    st.write(
        "• Durée d’incubation (temps écoulé entre l’infection et l’apparition des symptômes) : très variable, de 2 à 21 jours.")
    st.write(
        "• Premiers symptômes « pseudo grippaux » : apparition brutale d’une fièvre supérieure à 38°C, faiblesse intense, douleurs musculaires, maux de tête, irritation de la gorge.")
    st.write(
        "• Symptômes plus spécifiques : vomissements, diarrhées, éruptions cutanées, atteinte rénale et hépatique et, dans certains cas, hémorragies internes et externes.")
    st.write(
        "• Diagnostic : uniquement confirmé par des tests en laboratoire ; l’analyse des échantillons est exécutée dans des conditions de confinement extrêmement rigoureuses.")

elif (page == "Présentation du projet"):

    st.title("Présentation du projet")

    st.header("**Affichage des cas et morts cummulés**")
    # st.write("Nombre cummulé des cas d'Ebola")
    # st.bar_chart(df['Cumulative no. of confirmed, probable and suspected cases'])
    # st.write("Nombre cummulé des morts d'Ebola")
    # st.bar_chart(df['Cumulative no. of confirmed, probable and suspected deaths'])

    # ------------------------------------ GRAPH BOKEH ------------------------------

    test = df
    dfcases = test.groupby(["Date"])["Cumulative no. of confirmed, probable and suspected cases"].sum()
    dfcases = dfcases.reset_index()

    test = df
    dfdeaths = test.groupby(["Date"])["Cumulative no. of confirmed, probable and suspected deaths"].sum()
    dfdeaths = dfdeaths.reset_index()

    # on fusionne les deux dataframes obtenus avec le groupby
    dfcases["Cumulative no. of confirmed, probable and suspected deaths"] = dfdeaths[
        "Cumulative no. of confirmed, probable and suspected deaths"]

    # ---------------------------------- DATES IMPORTANTES EBOLA -------------------------------
    # Les 27 et 29 mars 2015, l'ensemble de la population sierra-léonaise est confinée à domicile afin de lutter contre l'épidémie

    # ----------------------- AFFICHER LES DATASET DU GRAPH BOKEH --------------------------
    printdfcase = st.checkbox("Afficher le dataset du graphique")
    if printdfcase:
        st.write(dfcases)

    TOOLTIPS = [
        ("Evenement", "@action"),
    ]

    p = figure(plot_width=1000, plot_height=600, x_axis_type="datetime", tooltips=TOOLTIPS)
    p.title.text = 'Evolution of cases and deaths in the world'
    p.vbar(x="Date", width=1, bottom=0, source=dfcases,
           top="Cumulative no. of confirmed, probable and suspected cases", color="orange",
           legend_label="Cases", muted_color="orange", muted_alpha=0.2)
    p.vbar(x="Date", width=1, bottom=0, source=dfcases,
           top="Cumulative no. of confirmed, probable and suspected deaths", color="red",
           legend_label="Deaths", muted_color="red", muted_alpha=0.2)
    p.diamond(x="date", size=10, legend_label="Important dates", source=date,
              muted_color="blue", muted_alpha=0.2)
    p.legend.location = "top_right"
    p.legend.click_policy = "mute"
    p.add_layout(Title(text="Date", align="center"), "below")
    p.add_layout(Title(text="Number of cases and deaths", align="center"), "left")

    p.add_tools(HoverTool(
        tooltips=[
            ('date', '$Date{%F}'),
            ('Cases', '@Cumulative no. of confirmed, probable and suspected cases'),
            # use @{ } for field names with spaces
            ('Deaths', '@Cumulative no. of confirmed, probable and suspected deaths'),
        ],

        formatters={
            'Date': 'datetime',  # use 'datetime' formatter for 'date' field
            # use default 'numeral' formatter for other fields
        },

        # display a tooltip whenever the cursor is vertically in line with a glyph
        mode='vline'
    ))

    st.write(p)

    # ------------------------------- DISCUSSION GRAPH BOKEH ------------------------------
    st.header("Analysons le graphe ci-dessus :")
    st.subheader("Début de l'épidémie")
    st.write("Tout d'abord nous pouvons voir que les cas augmentent très fortement, les morts sont très élevés, comme nous avons pu le voir dans la présentation de la maladie, le taux de mortalité est entre 25% et 80%")
    st.subheader("L'arrivée des soins :")
    st.write("Quelles mesures ont été prises pour endiquer la progression de l'épidémie ? Le Sierra-Leone, pays le plus touché a décrété un confinement de la population du 19 au 21 septembre. Or on peut voir d'après la courbe que ce confinement n'a pas eu d'effet, les cas augmentent toujours autant.")
    st.write("La communauté internationale a ensuite envoyé de nombreuses équipes de médecins et du matériel pour tenter d'aider les équipes locales. Hélicoptères, véhicules et soignants ont permis de soigner les malades, ceci est observable par l'atténuation de la courbe des morts qui stagne pendant une semaine puis repart à la hausse mais avec un coefficient plus bas que précedemment.")
    st.subheader("La fin de l'épidémie :")
    st.write("Début Mai 2015, l'OMS annonce la fin de l'épidémie d'Ebola. Quelques cas seront toujours rescencés mais contrôlés, les morts seront beaucoup moins nombreux.")





    # ---------------------------------- MAP INTERACTIVE --------------------------------

    st.header("**Carte interactive sur l'épidémie d'Ebola**")
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

    """
    #essai d'ajout de legende interactive sur folium
    #non fontcionnel erreur: The truth value of a Series is ambiguous. Use a.empty, a.bool(), a.item(), a.any() or a.all().
    NIL = folium.features.GeoJson(
        state_geo,
        style_function=style_function,
        control=False,
        highlight_function=highlight_function,
        tooltip=folium.features.GeoJsonTooltip(
            fields=[map_df['Country'], map_df['Cumulative no. of confirmed, probable and suspected cases']],
            aliases=['Country: ', 'Cumulative no. of confirmed, probable and suspected cases'],
            style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
            #sticky=True
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


    test = df
    output = test.groupby(["Date","Country"])["Cumulative no. of confirmed, probable and suspected cases"].sum()
    output
    output = output.reset_index()


    fig = px.choropleth(df, locations="Country", color="Cumulative no. of confirmed, probable and suspected cases",
                    locationmode='country names', hover_name="Country",
                    animation_frame=df["Date"].dt.strftime('%Y-%m-%d'),
                    title='Ebola spread over time', color_continuous_scale="Sunsetdark")
    fig.update(layout_coloraxis_showscale=False)
    st.plotly_chart(fig)



    #graph données par pays
    p = figure(plot_width=400, plot_height=400)
    p.hbar_stack(['Cumulative no. of confirmed, probable and suspected cases', 'Cumulative no. of confirmed, probable and suspected deaths'], y='index', height=0.8, color=("grey", "lightgrey"), source=output)
    st.write(p)






elif (page == "Voir le dataset"):
    # ouverture et affichage du csv
    df = pd.read_csv("ebola_2014_2016_clean.csv")
    st.title("Ebola dataset 2014 - 2016")  # titre du csv
    st.write(df)

    date["date"] = pd.to_datetime(date["date"])
    st.write(date)
