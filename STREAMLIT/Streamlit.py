import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
import ast
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
from bs4 import BeautifulSoup
import pickle
import requests
import re

df = pd.read_csv('/Users/kilian/Documents/GitHub/Projet-3/STREAMLIT/BD/players_3120.csv')


# CODE

list_taille = []

for n in range(len(df['Height'])):
    list_taille.append(int("".join(re.findall(r'(\d\d\d)+cm', df['Height'].iloc[n]))))

set_taille = set(list_taille)

liste_valeurs = df['Value'].to_list()
set_valeurs = []

for element in liste_valeurs:
    if 'M' not in element and 'K' not in element:
        set_valeurs.append(int(element.replace('€', '')))
    elif 'K' in element:
        set_valeurs.append(int(element.replace('K', '000').replace('€', '')))
    elif 'M' in element and '.' not in element:
        set_valeurs.append(int(element.replace('M', '000000').replace('€', '')))
    elif 'M' in element and '.' in element:
        set_valeurs.append(int(element.replace('M', '00000').replace('.', '').replace('€', '')))
        
    
set_valeurs = set(set_valeurs)

liste_salaires = df['Wage'].to_list()
set_salaires = []

for element in liste_salaires:
    if 'K' in element:
        set_salaires.append(int(element.replace('K', '000').replace('€', '')))
    else:
        set_salaires.append(int(element.replace('€', '')))
        
set_salaires = set(set_salaires)

# STREAMLIT

with st.sidebar:
    selection = option_menu(
                menu_title=None,
                options = ["Accueil", "Trouvez un joueur", "Trouvez le joueur idéal"]
            )



if selection == 'Accueil':

    st.header("Va te faire foot !")
    st.html("<p>Bienvenue sur notre service de recommendations de joueurs de football.</p>")

    st.header("Notre équipe :")

    col1, col2 = st.columns(2)

    with col1:
        col3, col4 = st.columns(2)

        with col3:
            st.markdown("<h2 style='text-align: center; color: white;'>Mathieu</h2>", unsafe_allow_html=True)
            st.image("STREAMLIT/Images/Ctc6lbkXYAA8UoA-removebg-preview.png", width = 150)

        with col4:
            st.markdown("<h2 style='text-align: center; color: white;'>Loïc</h2>", unsafe_allow_html=True)
            st.image("STREAMLIT/Images/377.webp", width = 150)

    with col2:
        col5, col6 = st.columns(2)

        with col5:
            st.markdown("<h2 style='text-align: center; color: white;'>Kilian</h2>", unsafe_allow_html=True)
            st.image("STREAMLIT/Images/POSE_-16.png", width = 150)

        with col6:
            st.markdown("<h2 style='text-align: center; color: white;'>Malo</h2>", unsafe_allow_html=True)
            st.image("STREAMLIT/Images/Sans titre.png", width = 150)

if selection == 'Trouvez un joueur':

    # Sélectionner un joueur similaire

    st.header("👇 Trouvez un joueur similaire à ... :")

    choix_joueur = st.text_input('Tapez le nom du joueur souhaité :')

    if choix_joueur:

        # On vérifie si notre film existe
        df_recherche = df.copy()
        df_recherche['name'] = df_recherche['name'].apply(lambda x : x.lower())
        recherche = choix_joueur
        recherche2 = recherche.lower().split(" ")

        for element in recherche2:
            df_recherche2 = df_recherche[df_recherche['name'].str.contains(element)]
            df_recherche = df_recherche2


        resultat = df[df['name'].str.contains(choix_joueur)]
        selected_film = st.selectbox(
            "",
            df_recherche['name'],
            index=None,
            placeholder="Select")

elif selection == 'Trouvez le joueur idéal':

# Trouver un joueur selon certaines caractéristiques

    # col1, col2, col3 = st.columns(3)

    st.header("Le poste :")
    poste = st.selectbox("Quel poste recherchez-vous ?",
    ['Gardien', 'Défenseur', 'Milieu', 'Attaquant'])

    if poste == 'Milieu':
        st.selectbox("Quel poste au milieu de terrain ?",
        ['Milieu droit', 'Milieu gauche', 'Milieu défensif', 'Milieu offensif'])
    elif poste == 'Défenseur':
        st.selectbox("Quel poste en défense ?",
        ['Latéral droit', 'Latéral gauche', 'Défenseur central'])
    elif poste == 'Attaquant':
        st.selectbox("Quel poste en attaque ?",
        ['Ailier droit', 'Ailier gauche', 'Attaquant central'])

    st.header("Parlons chiffres :")

    budget_transfert = st.slider("Quelle valeur ?", min(set_valeurs), max(set_valeurs), value=(min(set_valeurs), max(set_valeurs)))

    budget_salaire = st.slider("Quelle salaire ?", min(set_salaires), max(set_salaires), value=(min(set_salaires), max(set_salaires)))


    st.header("Des préférences ?")

    critere_pied = st.toggle("Avez-vous un critère de pied ?", value = False)
    if critere_pied:
        st.selectbox("Quel pied ?",
        ['Droit', 'Gauche'])

    critere_age = st.toggle("Avez-vous un critère d'âge ?", value = False)
    if critere_age:
        age = st.slider("Quelle tranche d'âge ?", int(df['Age'].min()), int(df['Age'].max()), value = (int(df['Age'].min()), int(df['Age'].max())))

    critere_taille = st.toggle("Avez-vous un critère de taille ?", value = False)
    if critere_taille:
        Height = st.slider("Quelle taille ?", min(set_taille), max(set_taille), value=(min(set_taille), max(set_taille)))





    