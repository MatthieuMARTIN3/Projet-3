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
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

import pandas as pd
import numpy as np
# modèle
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

import seaborn as sns
import matplotlib.pyplot as plt


# BASE 

df = pd.read_csv('/Users/kilian/Documents/GitHub/Projet-3/STREAMLIT/BD/dataset_a_jour.csv')
df = df.drop_duplicates(subset=['ID'])
df = df[df['name'].isna() == False]
df['name'] = df['name'].astype(str)
df['name'] = df['name'].apply(lambda x : x.split(',') if ',' in x else x)
df['Team & Contract'] = df['Team & Contract'].apply(lambda x : int(x) if x != 'Unknown' else 0)
df = df[(df['Team & Contract'] == 0) | (df['Team & Contract'] <= 2024)]


df = df[~(df['name'].isna() == True)]
df = df[~(df['name'] == '')]

colonnes = list(df.columns)[16:-9]

colonnes.remove('Total skill')
colonnes.remove('Total movement')
colonnes.remove('Total power')
colonnes.remove('Total mentality')
colonnes.remove('Total defending')
colonnes.remove('Total goalkeeping')

for element in colonnes:
    df[element] = df[element].fillna(0)
    df[element] = df[element].astype(float)

attacking = colonnes[0:5]
skill = colonnes[5:10]
movement = colonnes[10:15]
power = colonnes[15:20]
mentality = colonnes[20:26]
defending = colonnes[26:29]
goalkeeping = colonnes[29:34]

# FONCTIONS

navigator = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)'
url_base = 'https://sofifa.com/player/'
from bs4 import BeautifulSoup
import requests

def calcul(value):

    if value == []:
        value = value
    else:
        if type(value) == list:
            value = ''.join(value)
        
        if ' ' in value:
            value = value.replace(' ', '')
            
        if '+' in value:
            a, b = value.split('+')
            return int(a) + int(b)
        elif '-' in value:
            a, b = value.split('-')
            return int(a) - int(b)
        
        value = int(value)
    
    return value

def montant(salary):
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

# KNN

# Appliquer des poids 
colonnes_fixes = ['Age',  
                      'Overall rating',  
                      'Potential',  
                      'Total attacking', 
                      'Heading accuracy', 
                      'Total skill',
                      'Curve',  
                      'Total movement', 
                      'Acceleration', 
                      'Balance',
                      'Total power',
                      'Total mentality',
                      'Interceptions',
                      'Vision',  
                      'Total defending',
                      'Total goalkeeping',
                      'Total stats',
                      'Base stats',
                      'International reputation',
                      'Pace / Diving',
                      'Shooting / Handling',
                      'Passing / Kicking',
                      'Dribbling / Reflexes',
                      'Defending / Pace',
                      'Height',
                      'Weight',
                      'Value',
                      'Wage',
                      'Release clause',
                      'Crossing',
                      'Short passing',
                      'Volleys',
                      'Dribbling',
                      'FK Accuracy',
                      'Long passing',
                      'Ball control',
                      'Sprint speed',
                      'Agility',
                      'Reactions', 
                      'Shot power',
                      'Jumping',
                      'Stamina',
                      'Strength',
                      'Long shots',
                      'Aggression',
                      'Att. Position',
                      'Penalties',
                      'Composure',
                      'Defensive awareness',
                      'Standing tackle',
                      'Sliding tackle',
                      'GK Diving',
                      'GK Handling',
                      'GK Kicking',
                      'GK Positioning',
                      'GK Reflexes',
                      'Best overall',
                      'Growth',
                      'Pied droit']

poids_fixes_dict = {
        'Age': 1,  
        'Overall rating': 1,  
        'Potential': 1,  
        'Total attacking': 0, 
        'Heading accuracy': 1, 
        'Total skill': 0,
        'Curve': 1,  
        'Total movement': 0, 
        'Acceleration': 1, 
        'Balance': 1,
        'Total power': 0,
        'Total mentality': 0,
        'Interceptions': 1,
        'Vision': 1,  
        'Total defending': 0,
        'Total goalkeeping': 0,
        'Total stats': 0,
        'Base stats': 1,
        'International reputation': 1,
        'Pace / Diving': 1,
        'Shooting / Handling': 1,
        'Passing / Kicking': 1,
        'Dribbling / Reflexes': 1,
        'Defending / Pace': 1,
        'Height': 1,
        'Weight': 1,
        'Value': 1,
        'Wage': 1,
        'Release clause': 1,
        'Crossing': 1,
        'Short passing': 1,
        'Volleys': 1,
        'Dribbling': 1,
        'FK Accuracy': 1,
        'Long passing': 1,
        'Ball control': 1,
        'Sprint speed': 1,
        'Agility': 1,
        'Reactions': 1, 
        'Shot power': 1,
        'Jumping': 1,
        'Stamina': 1,
        'Strength': 1,
        'Long shots': 1,
        'Aggression': 1,
        'Att. Position': 1,
        'Penalties': 1,
        'Composure': 1,
        'Defensive awareness': 1,
        'Standing tackle': 1,
        'Sliding tackle': 1,
        'GK Diving': 1,
        'GK Handling': 1,
        'GK Kicking': 1,
        'GK Positioning': 1,
        'GK Reflexes': 1,
        'Best overall': 1,
        'Growth': 1,
        'Pied droit': 1
        }


def poids_numerique(X, colonnes_fixes, poids_fixes_dict):
    # Appliquer les poids aux colonnes numériques existantes
    for col in colonnes_fixes:
        if col in X.columns:
            X[col] *= poids_fixes_dict[col]
    
    return X


# FONCTION 1
def encodage_X(X, type, colonnes_fixes, poids_fixes_dict):
    from sklearn.preprocessing import StandardScaler, MinMaxScaler

    index = X.index
    X_num = X.select_dtypes('number')
    X_str = X.select_dtypes('object')

    if type == 'standard':
        SN = StandardScaler()
    else:
        SN = MinMaxScaler()
    X_num_scaled = pd.DataFrame(SN.fit_transform(X_num), columns=X_num.columns, index=index)


    X_encoded = pd.concat([X_str[['name', 'ID']], poids_numerique(X_num_scaled, colonnes_fixes, poids_fixes_dict)], axis=1)
    X_encoded = X_encoded.dropna()

    return X_encoded, SN


# FONCTION 4

def joueurs_similaires(X_encoded, id_joueur, model, df_recherche):

  # Vérifier si le Pokémon existe dans le dataset
  if id_joueur not in df_recherche['ID'].values:
      return f"Le Pokémon {id_joueur} n'est pas dans le dataset."

  # Récupérer les caractéristiques du Pokémon
  joueur_a_predire = X_encoded[X_encoded['ID'] == id_joueur]

  i, indices = model.kneighbors(joueur_a_predire.select_dtypes(include=[np.number]))

  return df_recherche.iloc[indices[0]].reset_index(drop=True)






# STREAMLIT

df_final = df.copy()

with st.sidebar:
    selection = option_menu(
                menu_title=None,
                options = ["Accueil", "Trouvez un joueur", "Trouvez le joueur idéal"]
            )

if selection == 'Accueil':

    st.header("Va te faire foot !")
    st.html("<p>Bienvenue sur notre service de recommandations de joueurs de football.</p>")

    st.header("Notre équipe :")

    col1, col2 = st.columns(2)

    with col1:
        col3, col4 = st.columns(2)

        with col3:
            st.markdown("<h2 style='text-align: center; color: white;'>Matthieu</h2>", unsafe_allow_html=True)
            url = "https://www.linkedin.com/in/matthieu-martin-8063a417a/"
            st.markdown("[LinkedIn](%s)" %url)
            url = "https://github.com/MatthieuMARTIN3"
            st.markdown("[GitHub](%s)" %url)           
            st.image("/Users/kilian/Documents/GitHub/Projet-3/STREAMLIT/Images/Ctc6lbkXYAA8UoA-removebg-preview.png", width = 150)


        with col4:
            st.markdown("<h2 style='text-align: center; color: white;'>Loïc</h2>", unsafe_allow_html=True)
            url = "https://www.linkedin.com/in/loic-fotsing-637a221a8/"
            st.markdown("[LinkedIn](%s)" %url)
            url = "https://github.com/je-suis-lmfao"
            st.markdown("[GitHub](%s)" %url)       
            st.image("/Users/kilian/Documents/GitHub/Projet-3/STREAMLIT/Images/377.webp", width = 150)

    with col2:
        col5, col6 = st.columns(2)

        with col5:
            st.markdown("<h2 style='text-align: center; color: white;'>Kilian</h2>", unsafe_allow_html=True)
            url = "https://www.linkedin.com/in/kiliancadiou/"
            st.markdown("[LinkedIn](%s)" %url)
            url = "https://github.com/KilianCadiou"
            st.markdown("[GitHub](%s)" %url)       
            st.image("/Users/kilian/Documents/GitHub/Projet-3/STREAMLIT/Images/POSE_-16.png", width = 150)

        with col6:
            st.markdown("<h2 style='text-align: center; color: white;'>Malo</h2>", unsafe_allow_html=True)
            url = "https://www.linkedin.com/in/malo-le-pors-5373a8273/"
            st.markdown("[LinkedIn](%s)" %url)
            url = "https://github.com/MaloBang"
            st.markdown("[GitHub](%s)" %url)      
            st.image("/Users/kilian/Documents/GitHub/Projet-3/STREAMLIT/Images/Sans titre.png", width = 150)

elif selection == 'Trouvez un joueur':


    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'], axis = 1)
    df = df.dropna()
    df['ID'] = df['ID'].astype(str)

    df_recherche = df.copy()

    df_recherche['name'] = df_recherche['name'].apply(lambda x : ",".join(x) if type(x) == list else x)
    df_recherche['name'] = df_recherche['name'].apply(lambda x : x.lower())

    # Sélectionner un joueur similaire

    st.header("👇 Trouvez un joueur similaire à ... :")

    choix_joueur = st.text_input('Tapez le nom du joueur souhaité :')

    if choix_joueur:    
        
        recherche = choix_joueur
        recherche2 = recherche.lower().split(" ")

        for element in recherche2:
            df_recherche2 = df_recherche[df_recherche['name'].str.contains(element)]
            df_recherche = df_recherche2
        
        if len(df_recherche) == 0:
            st.markdown("Êtes-vous sûr de l'orthographe ?")
            st.markdown("Ou alors ce joueur n'est pas dans nos bases.")

        else:
            name = st.selectbox("Quel joueur parmi notre base précisément ?",(df_recherche),)


            df['name'] = df['name'].apply(lambda x : ",".join(x) if type(x) == list else x)
            df['name'] = df['name'].apply(lambda x : x.lower())

            df_recherche = df[df['name'].str.contains(name)]
            id_joueur = df_recherche['ID'].iloc[0]
            position = df_recherche['Best position'][df_recherche['ID'] == id_joueur].iloc[0]

            liste_def = ["CB", "RB", "LB"]
            liste_lat = ["RB", "RWB", "LB", "LWB"]
            liste_milieu_def = ["CDM", "CM"]
            liste_milieu_off = ["CAM", "LM", "RM"]
            liste_ailies = ["LM", "RM", "LW", "RW"]
            liste_att = ["RW", "LW", "ST", "CF"]
            gardien = ["GK"]
            liste_cara_gk = ['GK Diving', 'GK Handling', 'GK Kicking', 'GK Positioning', 'GK Reflexes']

            df_recherche = df.copy()

            if position in liste_def :
                df_recherche = df[df['Best position'].isin(liste_def)]
                df_recherche = df_recherche.drop(columns=liste_cara_gk, axis = 1)
            elif position in liste_lat :
                df_recherche = df[df['Best position'].isin(liste_lat)]
                df_recherche = df_recherche.drop(columns=liste_cara_gk, axis = 1)
            elif position in liste_milieu_def :
                df_recherche = df[df['Best position'].isin(liste_milieu_def)]
                df_recherche = df_recherche.drop(columns=liste_cara_gk, axis = 1)
            elif position in liste_milieu_off :
                df_recherche = df[df['Best position'].isin(liste_milieu_off)]
                df_recherche = df_recherche.drop(columns=liste_cara_gk, axis = 1)
            elif position in liste_ailies :
                df_recherche = df[df['Best position'].isin(liste_ailies)]
                df_recherche = df_recherche.drop(columns=liste_cara_gk, axis = 1)
            elif position in liste_att :
                df_recherche = df[df['Best position'].isin(liste_att)]
                df_recherche = df_recherche.drop(columns=liste_cara_gk, axis = 1)
            elif position in gardien :
                df_recherche = df[df['Best position'].isin(gardien)]

            X = df_recherche.copy()
            X_encoded, SN = encodage_X(X, 'standard', colonnes_fixes, poids_fixes_dict)

            k=10
            model = NearestNeighbors(n_neighbors=k, metric='euclidean')
            model.fit(X_encoded.select_dtypes(include=['number']))
            resultat = joueurs_similaires(X_encoded, id_joueur, model, df_recherche)
            
            st.dataframe(resultat)


    


elif selection == 'Trouvez le joueur idéal':



# Trouver un joueur selon certaines caractéristiques

    # for element in colonnes:
    #     for n in range(len(df_final)):
    #         if "+" in df_final[element].iloc[n] or "-" in df_final[element].iloc[n]:
    #             df_final[element].iloc[n] = calcul(df_final[element].iloc[n])
    #             df_final[element].iloc[n] = float(df_final[element].iloc[n])
    #         else:
    #             df_final[element].iloc[n]= float(df_final[element].iloc[n])

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

    attaque = ['RW', 'LW', 'CF']
    milieu = ['RM', 'LM', 'CDM', 'CAM', 'CM']
    defense = ['RB', 'LB', 'CB']
    gardien = ['GK']

    if poste in attaque:
        colonnes_spé = attacking
    elif poste in defense:
        colonnes_spé = defending
    elif poste in milieu:
        colonnes_spé = movement
    elif poste in gardien:
        colonnes_spé = goalkeeping

    st.header("Des préférences ?")

    critere_pied = st.toggle("Avez-vous un critère de pied fort ?", value = False)
    if critere_pied:
        pied = st.selectbox("Quel pied fort ?",
        ['Droit', 'Gauche'])

        if pied == 'Droit':
            pied = 1
        elif pied == 'Gauche':
            pied = 0

        df_final = df_final[df_final['Pied droit'] == pied]

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
        # budget_transfert = st.slider("Quelle valeur ?", min(df_final['Value']), max(df_final['Value']), value=(min(df_final['Value']), max(df_final['Value'])))
        # min_budget = min(budget_transfert)
        # max_budget = max(budget_transfert)

        col1, col2 = st.columns(2)
        with col2:
            max_budget = st.text_input("Quel est le coût de transfert maximum ?", max(df_final['Value']), autocomplete= str(max(df_final['Value'])))
            
        with col1:
            min_budget = st.text_input("Quel est le coût de transfert minimum ?", min(df_final['Value']), autocomplete= str(max(df_final['Value'])))
        
        max_budget = int(max_budget) 
        min_budget = int(min_budget)
        df_final = df_final[df_final['Value'] <= max_budget]
        df_final = df_final[df_final['Value'] >= min_budget]

    critere_salaire = st.toggle("Avez-vous un critère de salaire ?", value = False)
    if critere_salaire:
        # budget_salaire = st.slider("Quelle salaire ?", min(df_final['Wage']), max(df_final['Wage']), value=(min(df_final['Wage']), max(df_final['Wage'])))
        # min_salaire = min(budget_salaire)
        # max_salaire = max(budget_salaire)

        col1, col2 = st.columns(2)
        with col2:
            max_salaire = st.text_input("Quel est le salaire maximum ?", max(df_final['Wage']), autocomplete= str(max(df_final['Wage'])))
        with col1:
            min_salaire = st.text_input("Quel est le salaire minimum ?", min(df_final['Wage']), autocomplete= str(max(df_final['Wage'])))
            
        max_salaire = int(max_salaire)
        min_salaire = int(min_salaire)
        df_final = df_final[df_final['Wage'] <= max_salaire]
        df_final = df_final[df_final['Wage'] >= min_salaire]

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

            date_contrat = df_final['Team & Contract'].iloc[n]
            nom = df_final['name'].iloc[n][0]
            score = df_final['Overall rating'].iloc[n]
            salary = df_final['Wage'].iloc[n]
            achat = df_final['Value'].iloc[n]

            col6, col7, col8, col9, col10 = st.columns(5)

            with col6:
                st.markdown(f"<div style='text-align: center;'>{nom}</div>", unsafe_allow_html=True)
            with col7:
                st.markdown(f"<div style='text-align: center;'>{score}</div>", unsafe_allow_html=True)
            with col8:
                st.markdown(f"<div style='text-align: center;'>{montant(salary)}</div>", unsafe_allow_html=True)
            with col9:
                st.markdown(f"<div style='text-align: center;'>{montant(achat)}</div>", unsafe_allow_html=True)
            with col10:
                st.markdown(f"<div style='text-align: center;'>{date_contrat}</div>", unsafe_allow_html=True)

            
            col11, col12 = st.columns(2)

            with col11:
                dico_colonnes = {}
                dico_colonnes = {'Attacking' : float(df_final[attacking].iloc[n].mean()),
                        'Skill' : float(df_final[skill].iloc[n].mean()),
                        'Movement' : float(df_final[movement].iloc[n].mean()),
                        'Power' : float(df_final[power].iloc[n].mean()),
                        'Mentality' : float(df_final[mentality].iloc[n].mean()),
                        'Defending': float(df_final[defending].iloc[n].mean()),
                        'Goalkeeping' : float(df_final[goalkeeping].iloc[n].mean())}

                data = pd.DataFrame.from_dict(dico_colonnes, orient = 'index').reset_index()

                data = data.rename({'index' : 'theta',
                                    0 : 'r'},
                                axis = 1)

                if int(data['r'].sum()) > 0:

                    st.markdown(f"<div style='text-align: center;'>Statistiques Globale : {int(round(data['r'].mean(), 0))}</div>", unsafe_allow_html=True)
                    fig = px.line_polar(data, r = 'r', theta= 'theta', line_close=True)
                    fig.update_layout(polar=dict(radialaxis=dict(range=[0, 100])))

                    st.plotly_chart(fig)

            with col12:
                  
                df_final_stats = df_final[colonnes_spé]
                dico_colonnes2 = {}

                for element in colonnes_spé:
                    dico_colonnes2.update({element : df_final_stats[element].iloc[n]})

                data = pd.DataFrame.from_dict(dico_colonnes2, orient = 'index').reset_index()

                data = data.rename({'index' : 'theta',
                                    0 : 'r'},
                                axis = 1)
                if int(data['r'].sum()) > 0:
                    st.markdown(f"<div style='text-align: center;'>Statistiques Spécifiques : {int(round(data['r'].mean(), 0))}</div>", unsafe_allow_html=True)
                    
                    fig = px.line_polar(data, r = 'r', theta= 'theta', line_close=True)
                    fig.update_layout(polar=dict(radialaxis=dict(range=[0, 100])))

                    st.plotly_chart(fig)

                

    

    




    