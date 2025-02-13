import streamlit as st
import base64
from st_pages import get_nav_from_toml
import time

nav = get_nav_from_toml("STREAMLIT/.streamlit/pages.toml")

st.logo("https://raw.githubusercontent.com/KilianCadiou/Bis/main/STREAMLIT/img/Bandeau.png", size = 'large')

pg = st.navigation(nav)

pg.run()