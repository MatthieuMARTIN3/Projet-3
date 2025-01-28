import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu


def accueil():
    st.title("Bienvenu sur ma page !")

with st.sidebar:
    selection = option_menu(
                menu_title=None,
                options = [" 😍 Accueil", " 😻 Les photos de mon chat"]
            )