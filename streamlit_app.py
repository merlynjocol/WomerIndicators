"""
Streamlit App
"""
# pylint: disable=wrong-import-order

import streamlit as st
from apps import home, poblacion, about, recursos, tierras, clima, knowledge, participation
from streamlit_option_menu import option_menu
from PIL import Image

from typing import Callable


#Setting the page, title and icon

st.set_page_config(page_title="Womer", page_icon="🌍", layout="wide")

padding = 2
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)


apps = [
    {"func": home.app, "title": "Principal", "icon": "house"},
    {"func": poblacion.app, "title": "Población", "icon": "person-circle"},
    {"func": recursos.app, "title": "Recursos", "icon": "droplet"},
    {"func": tierras.app, "title": "Tierras", "icon": "image-alt"},
    {"func": clima.app, "title": "Clima", "icon": "cloud-hail"},
    {"func": knowledge.app, "title": "Saberes ancestrales", "icon": "chat-left-dots"},
    {"func": participation.app, "title": "Participación", "icon": "hand-index"},
    {"func": about.app, "title": "Acerca de", "icon": "info"},
   
    ]

# Source Icons:  https://icons.getbootstrap.com/ 
#{"func": climate.app, "title": "Clima", "icon": "info"},

titles = [app["title"] for app in apps]
icons = [app["icon"] for app in apps]

params = st.experimental_get_query_params()

if "page" in params:
    DEFAULT_INDEX = titles.index(params["page"][0].lower())
else:
    DEFAULT_INDEX = 0

with st.sidebar:
    logo = Image.open("images/WOMER_LOGO_HORIZONTAL.png")
    st.image(logo, use_column_width=True)

    selected = option_menu(
        "Menu",
        options=titles,
        icons=icons,
        menu_icon="cast",
        default_index=DEFAULT_INDEX,
    )


for app in apps:
    if app["title"] == selected:
        page_func: Callable = app["func"]
        page_func()
        break