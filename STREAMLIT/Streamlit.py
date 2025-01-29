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
from bs4 import BeautifulSoup
import requests

# BASE 

df = pd.read_csv('/Users/kilian/Documents/GitHub/Projet-3/STREAMLIT/BD/players_3120.csv')

# FONCTIONS

navigator = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)'
url_base = 'https://sofifa.com/player/'
from bs4 import BeautifulSoup
import requests

def revenue(test):
    if 'M' not in test and 'K' not in test:
        resultat = int(test.replace('€', ''))
    elif 'K' in test and '.' not in test:
        resultat = int(test.replace('K', '000').replace('€', ''))
    elif 'K' in test and '.'  in test:
        resultat = int(test.replace('K', '00').replace('€', ''))
    elif 'M' in test and '.' not in test:
        resultat = int(test.replace('M', '000000').replace('€', ''))
    elif 'M' in test and '.' in test:
        resultat = int(test.replace('M', '00000').replace('.', '').replace('€', ''))

    return resultat

df['Revenue'] = df['Wage'].apply(revenue)
df['Valeur'] = df['Value'].apply(revenue)
df['Best position'] = df['Best position'].apply(lambda x : x.replace('RWB', 'RB').replace('LWB', 'LB')).replace('ST', 'CF')
df['Height'] = df['Height'].apply(lambda x : int(x[:3]))

df_final = df.copy()

# WEB SCRAPING

def end_contract(id):
    id = int(id)
    url_finale_title = f'{url_base}{id}'
    html_title = requests.get(url_finale_title, headers={'User-Agent': navigator})
    html_title2 = html_title.content
    soup_title = BeautifulSoup(html_title2, 'html.parser')

    for balise_parent in soup_title.find_all('div', class_='grid attribute'):
        if 'Contract valid until' in balise_parent.get_text().strip():
                end_contract = balise_parent.get_text().strip()

    try:
        end_year = max(re.findall('\d{4,}', end_contract))
        end_year = int(end_year)
    except:
        end_year = 'Unknown'
    
    return end_year

def salaire(id):
    id = int(id)
    url_finale_title = f'{url_base}{id}'
    html_title = requests.get(url_finale_title, headers={'User-Agent': navigator})
    html_title2 = html_title.content
    soup_title = BeautifulSoup(html_title2, 'html.parser')

    for balise_parent2 in soup_title.find_all('div', class_='col'):
        if 'Value' in balise_parent2.get_text().strip():
            valeur = balise_parent2.get_text().strip()
        if 'Wage' in balise_parent2.get_text().strip():
            salary = balise_parent2.get_text().strip()

    valeur = valeur[:-5]
    salary = salary[:-4]
                
    chiffres = [valeur, salary]
    new_chiffres = []

    for element in chiffres:
        if 'M' not in element and 'K' not in element:
            new_chiffres.append(int(element.replace('€', '')))
        elif 'K' in element and '.' not in element:
            new_chiffres.append(int(element.replace('K', '000').replace('€', '')))
        elif 'K' in element and '.'  in element:
            new_chiffres.append(int(element.replace('K', '00').replace('€', '')))
        elif 'M' in element and '.' not in element:
            new_chiffres.append(int(element.replace('M', '000000').replace('€', '')))
        elif 'M' in element and '.' in element:
            new_chiffres.append(int(element.replace('M', '00000').replace('.', '').replace('€', '')))

    valeur = int(new_chiffres[0])

    salary = int(new_chiffres[1])
    salary = str(salary)

    if len(salary) > 3:
        if len(salary) > 6:
            if len(salary) > 9:
                if len(salary) > 12:
                    salary = salary[:-12] + ' ' + salary[-12:-9] + ' ' + salary[-9:-6] + ' ' + salary[-6:-3] + ' ' + salary[-3:]
                else:
                    salary = salary[:-9] + ' ' + salary[-9:-6] + ' ' + salary[-6:-3] + ' ' + salary[-3:]
            else:
                salary = salary[:-6] + ' ' + salary[-6:-3] + ' ' + salary[-3:]
        else:
            salary = salary[:-3] + ' ' + salary[-3:]
    else:
        salary = salary

    salary = salary + ' €'

    return salary

def valeur(id):
    id = int(id)
    url_finale_title = f'{url_base}{id}'
    html_title = requests.get(url_finale_title, headers={'User-Agent': navigator})
    html_title2 = html_title.content
    soup_title = BeautifulSoup(html_title2, 'html.parser')

    for balise_parent2 in soup_title.find_all('div', class_='col'):
        if 'Value' in balise_parent2.get_text().strip():
            valeur = balise_parent2.get_text().strip()
        if 'Wage' in balise_parent2.get_text().strip():
            salary = balise_parent2.get_text().strip()

    valeur = valeur[:-5]
    salary = salary[:-4]
                
    chiffres = [valeur, salary]
    new_chiffres = []

    for element in chiffres:
        if 'M' not in element and 'K' not in element:
            new_chiffres.append(int(element.replace('€', '')))
        elif 'K' in element and '.' not in element:
            new_chiffres.append(int(element.replace('K', '000').replace('€', '')))
        elif 'K' in element and '.'  in element:
            new_chiffres.append(int(element.replace('K', '00').replace('€', '')))
        elif 'M' in element and '.' not in element:
            new_chiffres.append(int(element.replace('M', '000000').replace('€', '')))
        elif 'M' in element and '.' in element:
            new_chiffres.append(int(element.replace('M', '00000').replace('.', '').replace('€', '')))

    valeur = int(new_chiffres[0])

    salary = int(new_chiffres[1])

    valeur = str(valeur)
    
    if len(valeur) > 3:
        if len(valeur) > 6:
            if len(valeur) > 9:
                if len(valeur) > 12:
                    valeur = valeur[:-12] + ' ' + valeur[-12:-9] + ' ' + valeur[-9:-6] + ' ' + valeur[-6:-3] + ' ' + valeur[-3:]
                else:
                    valeur = valeur[:-9] + ' ' + valeur[-9:-6] + ' ' + valeur[-6:-3] + ' ' + valeur[-3:]
            else:
                valeur = valeur[:-6] + ' ' + valeur[-6:-3] + ' ' + valeur[-3:]
        else:
            valeur = valeur[:-3] + ' ' + valeur[-3:]
    else:
        valeur = valeur

    valeur = valeur + ' €'

    return valeur

def name(id):
    id = int(id)
    url_finale_title = f'{url_base}{id}'
    html_title = requests.get(url_finale_title, headers={'User-Agent': navigator})
    html_title2 = html_title.content
    soup_title = BeautifulSoup(html_title2, 'html.parser')

    name = ''

    for balise_parent in soup_title.find_all('div', class_='profile clearfix'):
        for balise_parent2 in soup_title.find_all('h1'):
            name += balise_parent2.get_text().strip() + ','

    name = name[:-1]
    name = name.split(',')
    name = name[0]

    return name

def overall(id):
    id = int(id)
    url_finale_title = f'{url_base}{id}'
    html_title = requests.get(url_finale_title, headers={'User-Agent': navigator})
    html_title2 = html_title.content
    soup_title = BeautifulSoup(html_title2, 'html.parser')

    for balise_parent2 in soup_title.find_all('div', class_= 'grid'):
            if 'Overall' in balise_parent2.get_text().strip():
                overall = balise_parent2.get_text().strip()

    try:
        overall = int(overall[:2])
    except:
        overall = 'Unknown'

    return overall


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
            st.markdown("<h2 style='text-align: center; color: white;'>Matthieu</h2>", unsafe_allow_html=True)
            st.image("/Users/kilian/Documents/GitHub/Projet-3/STREAMLIT/Images/Ctc6lbkXYAA8UoA-removebg-preview.png", width = 150)

        with col4:
            st.markdown("<h2 style='text-align: center; color: white;'>Loïc</h2>", unsafe_allow_html=True)
            st.image("/Users/kilian/Documents/GitHub/Projet-3/STREAMLIT/Images/377.webp", width = 150)

    with col2:
        col5, col6 = st.columns(2)

        with col5:
            st.markdown("<h2 style='text-align: center; color: white;'>Kilian</h2>", unsafe_allow_html=True)
            st.image("/Users/kilian/Documents/GitHub/Projet-3/STREAMLIT/Images/POSE_-16.png", width = 150)

        with col6:
            st.markdown("<h2 style='text-align: center; color: white;'>Malo</h2>", unsafe_allow_html=True)
            st.image("/Users/kilian/Documents/GitHub/Projet-3/STREAMLIT/Images/Sans titre.png", width = 150)

elif selection == 'Trouvez un joueur':

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
    ['... Choisir', 'Gardien', 'Défenseur', 'Milieu', 'Attaquant'])

    if poste == 'Milieu':
        poste = st.selectbox("Quel poste au milieu de terrain ?",
        ['Milieu droit', 'Milieu gauche', 'Milieu défensif', 'Milieu offensif', 'Milieu polyvalent'])
    elif poste == 'Défenseur':
        poste = st.selectbox("Quel poste en défense ?",
        ['Arrière droit', 'Arrière gauche', 'Défenseur central'])
    elif poste == 'Attaquant':
        poste = st.selectbox("Quel poste en attaque ?",
        ['Ailier droit', 'Ailier gauche', 'Attaquant central'])

    if poste == 'Gardien':
        poste = 'GK'
    elif poste == 'Arrière droit':
        poste = 'RB'
    elif poste == 'Arrière gauche':
        poste = 'LB'
    elif poste == 'Défenseur central':
        poste = 'CB'
    elif poste == 'Milieu droit':
        poste = 'RM'
    elif poste == 'Milieu gauche':
        poste = 'LM'
    elif poste == 'Milieu défensif':
        poste = 'CDM'
    elif poste == 'Milieu offensif':
        poste = 'CAM'
    elif poste == 'Milieu polyvalent':
        poste = 'CM'
    elif poste == 'Ailier droit':
        poste = 'RW'
    elif poste == 'Ailier gauche':
        poste = 'LW'
    elif poste == 'Attaquant central':
        poste = 'CF'

    df_final = df_final[df_final['Best position'].str.contains(poste)]


    st.header("Des préférences ?")

    critere_pied = st.toggle("Avez-vous un critère de pied fort ?", value = False)
    if critere_pied:
        pied = st.selectbox("Quel pied fort ?",
        ['Droit', 'Gauche'])

        if pied == 'Droit':
            pied = 'Right'
        elif pied == 'Gauche':
            pied = 'Left'

        df_final = df_final[df_final['foot'] == pied]

    critere_age = st.toggle("Avez-vous un critère d'âge ?", value = False)
    if critere_age:
        age = st.slider("Quelle tranche d'âge ?", int(df['Age'].min()), int(df['Age'].max()), value = (int(df['Age'].min()), int(df['Age'].max())))
        min_age = min(age)
        max_age = max(age)
        df_final = df_final[df_final['Age'] >= min_age]
        df_final = df_final[df_final['Age'] <= max_age]

    critere_taille = st.toggle("Avez-vous un critère de taille ?", value = False)
    if critere_taille:
        taille = st.slider("Quelle taille ?", min(df['Height']), max(df['Height']), value=(min(df['Height']), max(df['Height'])))
        min_taille = min(taille)
        max_taille = max(taille)
        df_final = df_final[df_final['Height'] <= max_taille]
        df_final = df_final[df_final['Height'] >= min_taille]

    
    st.header("Parlons chiffres :")
    
    critere_budget = st.toggle("Avez-vous un critère de coût de transfert ?", value = False)
    if critere_budget:
        # budget_transfert = st.slider("Quelle valeur ?", min(df_final['Valeur']), max(df_final['Valeur']), value=(min(df_final['Valeur']), max(df_final['Valeur'])))
        # min_budget = min(budget_transfert)
        # max_budget = max(budget_transfert)

        col1, col2 = st.columns(2)
        with col2:
            max_budget = st.text_input("Quel est le coût de transfert maximum ?", max(df_final['Valeur']), autocomplete= str(max(df_final['Valeur'])))
            
        with col1:
            min_budget = st.text_input("Quel est le coût de transfert minimum ?", min(df_final['Valeur']), autocomplete= str(max(df_final['Valeur'])))
        
        max_budget = int(max_budget) 
        min_budget = int(min_budget)
        df_final = df_final[df_final['Valeur'] <= max_budget]
        df_final = df_final[df_final['Valeur'] >= min_budget]

    critere_salaire = st.toggle("Avez-vous un critère de salaire ?", value = False)
    if critere_salaire:
        # budget_salaire = st.slider("Quelle salaire ?", min(df_final['Revenue']), max(df_final['Revenue']), value=(min(df_final['Revenue']), max(df_final['Revenue'])))
        # min_salaire = min(budget_salaire)
        # max_salaire = max(budget_salaire)

        col1, col2 = st.columns(2)
        with col2:
            max_salaire = st.text_input("Quel est le salaire maximum ?", max(df_final['Revenue']), autocomplete= str(max(df_final['Revenue'])))
        with col1:
            min_salaire = st.text_input("Quel est le salaire minimum ?", min(df_final['Revenue']), autocomplete= str(max(df_final['Revenue'])))
            
        max_salaire = int(max_salaire)
        min_salaire = int(min_salaire)
        df_final = df_final[df_final['Revenue'] <= max_salaire]
        df_final = df_final[df_final['Revenue'] >= min_salaire]

    df_final = df_final.sort_values(by = 'Overall rating', ascending = False)

    resultats = st.button("Montrer / Actualiser les résultats", type = 'primary')

    if resultats:

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.markdown("<h6 style='text-align: center; color: white;'>Name</h6>", unsafe_allow_html=True)
        with col2:
            st.markdown("<h6 style='text-align: center; color: white;'>Overall rating</h6>", unsafe_allow_html=True)
        with col3:
            st.markdown("<h6 style='text-align: center; color: white;'>Salaire</h6>", unsafe_allow_html=True)
        with col4:
            st.markdown("<h6 style='text-align: center; color: white;'>Valeur</h6>", unsafe_allow_html=True)
        with col5:
            st.markdown("<h6 style='text-align: center; color: white;'>Fin de contrat</h6>", unsafe_allow_html=True)

        for n in range(len(df_final)):

            id = df_final['ID'].iloc[n]
            date_contrat = end_contract(id)

            try:
                if date_contrat >= 2024 or date_contrat == 'Unknown':
                
                    nom = name(id)
                    score = overall(id)
                    salary = salaire(id)
                    achat = valeur(id)

                    with col1:
                        st.markdown(f"<div style='text-align: center;'>{nom}</div>", unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"<div style='text-align: center;'>{score}</div>", unsafe_allow_html=True)
                    with col3:
                        st.markdown(f"<div style='text-align: center;'>{salary}</div>", unsafe_allow_html=True)
                    with col4:
                        st.markdown(f"<div style='text-align: center;'>{achat}</div>", unsafe_allow_html=True)
                    with col5:
                        st.markdown(f"<div style='text-align: center;'>{date_contrat}</div>", unsafe_allow_html=True)
            
            except:
                pass



    

    




    