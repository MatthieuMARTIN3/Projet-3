import streamlit as st
import base64
from st_pages import get_nav_from_toml
import time

nav = get_nav_from_toml("STREAMLIT/.streamlit/pages.toml")

st.logo("https://raw.githubusercontent.com/KilianCadiou/Bis/main/STREAMLIT/img/Bandeau.png", size = 'large')

pg = st.navigation(nav)

pg.run()

custom_css = """
    <style>
    /* Modifier l'arrière-plan de la page principale */
    .stApp {
        background-color: rgba(13, 52, 4, 0.6) !important;
    }

    /* Modifier l'arrière-plan du volet de navigation (sidebar) */
    section[data-testid="stSidebar"] {
        background-color: #666866 !important; /* Couleur gris foncé */
    }
    </style>
"""

st.markdown(custom_css, unsafe_allow_html=True)