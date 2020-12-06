import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium
import json
from bokeh.plotting import figure, output_notebook, show, output_file
from bokeh.models import HoverTool, Title


# Barre de nativation :
df = pd.read_csv("ebola_2014_2016_clean.csv")


st.sidebar.write("Navigation :  ")
page = st.sidebar.radio("",('Accueil', "La maladie d'Ebola", 'Présentation du projet', 'Voir le dataset'))
if(page == "Accueil"):
    st.title("DIDIER Antoine - DINDART Juliette")
    st.header("Ebola - dashboard")
    st.write("Ce projet est de créer un dashboard sur un dataset en streamlit")
elif(page =="La maladie d'Ebola"):
    st.title("Ebola - Présentation")
    st.write("Le virus Ebola est l'agent infectieux qui provoque, chez l'humain et les autres primates, des fièvres souvent hémorragiques — la maladie à virus Ebola — à l'origine d'épidémies historiques notables par leur ampleur et leur sévérité. La transmission entre humains a lieu avant tout par contact direct avec des fluides corporels.")
elif(page == "Présentation du projet"):
    st.write("kyaaa")

    # st.bar_chart(df['Cumulative no. of confirmed, probable and suspected cases'])
    # st.bar_chart(df['Cumulative no. of confirmed, probable and suspected deaths'])

    test = df
    output = test.groupby(["Date"])["Cumulative no. of confirmed, probable and suspected cases"].sum()
    output
    output = output.reset_index()

    p = figure(plot_width=800, plot_height=300)
    p.title.text = 'Evolution of cases and death in the world'
    p.vbar(x=df["Date"], width=0.5, bottom=0,
           top=output["Cumulative no. of confirmed, probable and suspected cases"], color="orange",
           legend_label="Cases")
    p.vbar(x=df["Date"], width=0.5, bottom=0,
           top=df["Cumulative no. of confirmed, probable and suspected deaths"], color="red", legend_label="Deaths")
    p.legend.location = "top_right"
    p.legend.click_policy = "hide"
    p.add_layout(Title(text="Date", align="center"), "below")
    p.add_layout(Title(text="Number of cases and deaths", align="center"), "left")

    st.write(p)

    # ------ MAP INTERACTIVE ------

    # permet de filtrer l'année : bouton radio pour selectionner année
    annee = st.radio("choisir une année", ('2014', '2015', '2016'))
    datelst = df['Date'].unique()
    dateliste = []
    for i in datelst:
        if i.startswith(annee):
            dateliste.append(i)
    # affichage des dates disponible selon l'année choisie
    choix_map = st.selectbox("Choisir une date pour la carte : ", dateliste)
    mask = df["Date"] == choix_map
    map_df = df[mask]

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

    # call to render Folium map in Streamlit
    folium_static(m)

    output = df.groupby(["Country", "Date"])["Cumulative no. of confirmed, probable and suspected cases"].sum()
    st.write(output)

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


elif(page == "Voir le dataset"):
    # ouverture et affichage du csv
    df = pd.read_csv("ebola_2014_2016_clean.csv")
    st.title("Ebola dataset 2014 - 2016")  # titre du csv
    st.write(df)






