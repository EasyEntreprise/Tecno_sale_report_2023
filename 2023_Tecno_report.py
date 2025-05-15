# Tecno Report pour l'annee 2023.
# Vous y trouverez les donnees sur la vente des Smart Phone et Feature Phone  
#
#########################
## IMPORTATION LIBRAIRY
######
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_extras.metric_cards import style_metric_cards


# Configuration page
st.set_page_config(
    layout= "wide",
    page_title="Tecno Business Report 2023",
    page_icon="./pictures/easy-logo.jpg"
    )


#########################
## PRESENTATION AUTEUR
######

st.subheader("About the author", divider="grey")
#col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
col1, col2 = st.columns([1, 3], gap="small", vertical_alignment="center")
with col1:
    st.image("./pictures/rodrigue-N.png", width= 380)
    

with col2:
    st.title("Rodrigue NSINSULU", anchor=False)
    st.write(
        "Junior Data Analyst, Data Engener, Data Scientist, Machine and Deep Learning and  IT Cyber-security.",
    )
    st.write(
        "C.E.O at Easy Holding"
    )
st.markdown("___")

######################################################################################################################
st.markdown("<h1 style='text-align: center; color: blue;'> TECNO BUSINESS > REPORT 2023 </h1>", unsafe_allow_html= True)
st.markdown("<br/>", unsafe_allow_html= True)


#########################
## LOAD DATASET
######

file = st.file_uploader("Import your dataset", type=["xlsx", "csv"])
if file is not None :
    full_dataset = pd.read_csv(file)

    with st.expander("Show Dataset"):
        dataset = dataframe_explorer(full_dataset, case= False)
        st.dataframe(dataset, use_container_width= True)

    dataset_2023 = dataset[dataset["Annee"] == 2023]

    #########################
    ## GENERAL DATA METRIC
    ######
    st.subheader("General Data Metric", divider="rainbow")

    general_sale = dataset_2023["Vente(Pcs)"].sum()

    sp_select = ["CAMON", "SPARK", "POVA", "PHANTOM", "Tablet"]
    sp = dataset_2023[dataset_2023["Modeles"].isin(sp_select)]
    sp_sum = sp["Vente(Pcs)"].sum()

    fp = dataset_2023[dataset_2023["Modeles"] == "Feature"]
    fp_sum = fp["Vente(Pcs)"].sum()

    a, b, c = st.columns(3)
    with a :
        st.metric(label="General Sale", value= general_sale, delta="Years : 2023")

    with b :
        st.metric(label="General Smart Phone Sale", value= sp_sum, delta="Years : 2023")

    with c :
        st.metric(label="General Feature Phone Sale", value= fp_sum, delta="Years : 2023")
        
    # Style the metric
    style_metric_cards(background_color="#3c4d66", border_left_color= "#99f2c8", border_color="#0006a")

    ## Graphiqeu Carte
    pays_livrais = dataset_2023.groupby("Pays livraison", as_index= False)["Vente(Pcs)"].sum()
    #st.write(pays_livrais)
    
    pays_livraison = px.choropleth(data_frame= pays_livrais, locations= pays_livrais["Pays livraison"], locationmode="country names", color="Vente(Pcs)", color_continuous_scale = 'Viridis', title = 'Delivery countries')
    st.plotly_chart(pays_livraison)

    fig_pays_delivert = px.bar(pays_livrais, x="Pays livraison", y="Vente(Pcs)", color="Pays livraison", text="Vente(Pcs)", title="Delivery countries")
    fig_pays_delivert.update_traces(textposition = "outside")
    st.plotly_chart(fig_pays_delivert)




    #########################
    ## GENERAL DATA DRC
    ######
    st.subheader("General DRC Data", divider="rainbow")

    dataset_drc = dataset_2023[dataset_2023["Pays livraison"] == "Democratic Republic of the Congo"]

    general_drc_sale = dataset_drc["Vente(Pcs)"].sum()

    sp_drc = dataset_drc[dataset_drc["Modeles"].isin(sp_select)]
    sp_drc_sum = sp_drc["Vente(Pcs)"].sum()

    fp_drc = dataset_drc[dataset_drc["Modeles"] == "Feature"]
    fp_drc_sum = fp_drc["Vente(Pcs)"].sum()

    d, e, f = st.columns(3)
    with d :
        st.metric(label="DRC General Sale", value= general_drc_sale, delta="Years : 2023")

    with e :
        st.metric(label="DRC General Smart Phone Sale", value= sp_drc_sum, delta="Years : 2023")

    with f :
        st.metric(label="DRC General Feature Phone Sale", value= fp_drc_sum, delta="Years : 2023")
    

    #########################
    ## DRC MONTHLY SITUATION
    ######
    st.subheader("DRC Monthly situation", divider="grey")

    # Situation Mensuel
    monthly = dataset_drc.groupby(["Date"], as_index= False)["Vente(Pcs)"].sum()
    fig_month = px.line(monthly, x="Date", y="Vente(Pcs)", text="Vente(Pcs)", title="DRC Monthly sale")
    fig_month.update_traces(textposition = "top center")
    st.plotly_chart(fig_month)

    # situation Semestrielle
    weekly = dataset_drc.groupby(["Semaines"], as_index= False)["Vente(Pcs)"].sum()
    fig_weekly = px.line(weekly, x="Semaines", y="Vente(Pcs)", title="DRC Weekly sale", text="Vente(Pcs)")
    fig_weekly.update_traces(textposition = "top center")
    st.plotly_chart(fig_weekly)

    #########################
    ## DRC MODELS SITUATION
    ######
    st.subheader("DRC Models situation", divider="grey")

    col3, col4 = st.columns(2)
    with col3:
        # Graphic en 'Pie' pour la proportion
        models = dataset_drc.groupby("Modeles", as_index= False)["Vente(Pcs)"].sum()
        liste = models["Modeles"].unique()
        fig_models = go.Figure(data=[go.Pie(labels= liste, values= models["Vente(Pcs)"], title="Proportion models", opacity= 0.8)])
        fig_models.update_traces(hoverinfo = 'label+percent', textfont_size = 15, textinfo = "label+percent", pull= [0, 0, 0, 0, 0, 0.03] ,marker_line=dict(color='#FFFFFF', width=1))
        st.plotly_chart(fig_models)
        

    with col4:
        # Graphic en 'Bar' (Situation vente models)
        fig_modeles = px.bar(models, x="Modeles", y="Vente(Pcs)", color= "Modeles", text="Vente(Pcs)", title="DRC models sale situation")
        fig_modeles.update_traces(textposition = "outside")
        st.plotly_chart(fig_modeles)
        

    # Graphic 'Bar' groupe Situation models par mois
    models_mois = dataset_drc.groupby(["Modeles", "Date"], as_index= False)["Vente(Pcs)"].sum()
    fig_models_mois = px.bar(models_mois, x="Date", y="Vente(Pcs)", color="Modeles", barmode= "group", text="Vente(Pcs)", title="DRC models sale situation by month")
    fig_models_mois.update_traces(textposition = "outside")
    st.plotly_chart(fig_models_mois)
    
    # Graphic 'Line' Situation vente par models series
    serie_mois = dataset_drc.groupby("Modeles Series", as_index= False)["Vente(Pcs)"].sum()
    fig_serie_mois = px.line(serie_mois, x="Modeles Series", y="Vente(Pcs)", text="Vente(Pcs)", title="DRC models sale situation by month")
    fig_serie_mois.update_traces(textposition = "top center")
    st.plotly_chart(fig_serie_mois)

    
    
    #########################
    ## DRC REGIONS SITUATION
    ######
    st.subheader("DRC Regions situation", divider="grey")

    col5, col6, col7 = st.columns(3)
    with col5:
        # Graphic en 'Pie' pour la proportion des regions
        region = dataset_drc.groupby("Ventes Regions", as_index= False)["Vente(Pcs)"].sum()
        liste_region = region["Ventes Regions"].unique()
        fig_region = go.Figure(data=[go.Pie(labels= liste_region, values= models["Vente(Pcs)"], title="Proportion region", opacity= 0.8)])
        fig_region.update_traces(hoverinfo = 'label+percent', textfont_size = 15, textinfo = "label+percent",marker_line=dict(color='#FFFFFF', width=1))
        st.plotly_chart(fig_region)
        

    with col6:
        # Graphic en 'Bar' (Situation vente regions)
        fig_region_sale = px.bar(region, x="Ventes Regions", y="Vente(Pcs)", color= "Ventes Regions", text="Vente(Pcs)", title="DRC models sale situation")
        fig_region_sale.update_traces(textposition = "outside")
        st.plotly_chart(fig_region_sale)
        

    with col7:
        # Graphic en 'Bar' (Situation vente regions par mois)
        serie_mois = dataset_drc.groupby(["Ventes Regions", "Date"], as_index= False)["Vente(Pcs)"].sum()
        fig_serie_mois = px.bar(serie_mois, x="Date", y="Vente(Pcs)", color="Ventes Regions", barmode= "group", text="Vente(Pcs)", title="DRC models sale situation by month")
        fig_serie_mois.update_traces(textposition = "outside")
        st.plotly_chart(fig_serie_mois)
        


    #########################
    ## DRC SHOPS SITUATION
    ######
    st.subheader("DRC Shops situation", divider="grey")

    shop_unique = dataset_2023["Nom Shop"].unique()

    cola, colb = st.columns([2, 3])
    with cola:
        # Afficher le table des shops
        st.subheader("Shops by sell")
        shop = dataset_drc.groupby("Nom Shop", as_index= False)["Vente(Pcs)"].sum()
        affiche_shop = shop.sort_values(by="Vente(Pcs)", ascending= False)
        st.write(affiche_shop)
        

    with colb:
        # Graphic en 'Bar' (Situation vente regions)
        shop_select = st.selectbox("Choose your shop", shop_unique)
        dataset_drc_shop = dataset_drc[dataset_drc["Nom Shop"] == shop_select]
        shop_group = dataset_drc_shop.groupby(["Nom Shop", "Date"], as_index = False)["Vente(Pcs)"].sum()
        
        fig_shop = px.line(shop_group, x="Date", y="Vente(Pcs)", text="Vente(Pcs)" ,title=f"Monthly sell Situation for {shop_select}")
        fig_shop.update_traces(textposition ="top center")
        st.plotly_chart(fig_shop)
        
    cold, cole = st.columns([2, 3])
    with cole:
        # Graphic en 'Bar' pour le shop avec modeles par serie
        shop_serie = dataset_drc_shop.groupby("Modeles Series", as_index = False)["Vente(Pcs)"].sum()
        fig_shop_serie = px.bar(shop_serie, x="Modeles Series", y="Vente(Pcs)", text="Vente(Pcs)", color="Modeles Series", title=f"Sell shop {shop_select} by modeles serie")
        fig_shop_serie.update_traces(textposition = "outside")
        st.plotly_chart(fig_shop_serie)

    with cold:
        # Graphic en 'Bar' (Situation inactive par regions)
        
        shop_models = dataset_drc_shop.groupby("Modeles", as_index = False)["Vente(Pcs)"].sum()
        liste_models = shop_models["Modeles"].unique()
        fig_shop_modele = go.Figure(data=[go.Pie(labels= liste_models, values= shop_models["Vente(Pcs)"], title=f"Proportion of sell for shop {shop_select} by models", opacity= 0.8)])
        fig_shop_modele.update_traces(hoverinfo = 'label+percent', textfont_size = 15, textinfo = "label+percent",marker_line=dict(color='#FFFFFF', width=1))
        st.plotly_chart(fig_shop_modele)
        


    ############################
    ## DRC ACTIVATION SITUATION
    ######
    st.subheader("DRC Activation situation", divider="grey")

    

    colf, colg = st.columns(2)
    with colf:
        # Graphic en 'Bar' pour l'active et inactive
        activation = dataset_drc.groupby("Activation", as_index= False)["Vente(Pcs)"].sum()
        fig_activ = px.bar(activation, x="Activation", y="Vente(Pcs)", text="Vente(Pcs)", title="Activation and No-Activation", color="Activation")
        fig_activ.update_traces(textposition = "outside")
        st.plotly_chart(fig_activ)

    with colg:
        # Graphic en 'Bar' (Situation inactive par regions)
        noActiv = dataset_drc[dataset_drc["Activation"] == "Non Activé"]
        no_activ = noActiv.groupby("Ventes Regions", as_index= False)["Vente(Pcs)"].sum()
        fig_noActiv = px.bar(no_activ, x="Ventes Regions", y="Vente(Pcs)", text="Vente(Pcs)", title="No-Activation situation by regions", color= "Ventes Regions")
        fig_noActiv.update_traces(textposition = "outside")
        st.plotly_chart(fig_noActiv)

    # Pays d'activations ( carte du monde)
    pays_activ = dataset_drc.groupby("Pays Activation", as_index= False)["Vente(Pcs)"].sum()
    pays_list = pays_activ["Pays Activation"].unique()
    fig_monde = px.choropleth(data_frame= pays_activ, locations= pays_activ["Pays Activation"], locationmode="country names", color="Vente(Pcs)", color_continuous_scale = 'Viridis', title = 'Activation countries')
    st.plotly_chart(fig_monde)

    # Graphic bar d'activation
    
    fig_pays_activ = px.bar(pays_activ, x="Pays Activation", y="Vente(Pcs)", color="Pays Activation", text="Vente(Pcs)", title="Countries Activation of phone from DRC")
    fig_pays_activ.update_traces(textposition = "outside")
    st.plotly_chart(fig_pays_activ)



