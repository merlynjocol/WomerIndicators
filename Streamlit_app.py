"""
Streamlit App
"""
# pylint: disable=wrong-import-order

import streamlit as st
from apps import information, natural_resources, climate, about, participation, knowledge 
from streamlit_option_menu import option_menu
from PIL import Image

from typing import Callable


st.set_page_config(page_title="Womer", page_icon="🌍", layout="wide")


apps = [
    {"func": information.app, "title": "Datos básicos", "icon": "house"},
    {"func": natural_resources.app, "title": "Acceso a recursos naturales", "icon": "geo-alt"},
    {"func": climate.app, "title": "Cambio climático", "icon": "hourglass-split"},
    {"func": participation.app, "title": "Participación", "icon": "geo-alt"},
    {"func": knowledge.app, "title": "Saberes Tradicionales", "icon": "geo-alt"},
    {"func": about.app, "title": "Acerca de", "icon": "info"},
]

titles = [app["title"] for app in apps]
icons = [app["icon"] for app in apps]

params = st.experimental_get_query_params()

if "page" in params:
    DEFAULT_INDEX = titles.index(params["page"][0].lower())
else:
    DEFAULT_INDEX = 0

with st.sidebar:
    logo = Image.open("images/WOMER_LOGO HORIZONTAL.png")
    st.image(logo, use_column_width=True)

    selected = option_menu(
        "TEMA",
        options=titles,
        icons=icons,
        menu_icon="list",
        default_index=DEFAULT_INDEX,
    )


for app in apps:
    if app["title"] == selected:
        page_func: Callable = app["func"]
        page_func()
        break