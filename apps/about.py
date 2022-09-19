"""
About page module
"""

import streamlit as st
from PIL import Image



def app():
    """
    About page app function
    """
    st.markdown(
        "<h1 style='text-align: center; '>Acerca de</h1>", unsafe_allow_html=True
    )

    st.subheader("")

    st.markdown ('---')

      
    st.subheader("¿Quién puede acceder a mis datos?") 
    st.markdown(
        """
        La organización indígena que dirige la investigación tiene el derecho sobre los datos. La organización indígena decide quién puede acceder a los datos y publicarlos. Trabajamos bajo los principios de CARE para asegurar la soberanía de los datos indígenas.
    """
    ) 

    st.subheader("¿Cómo tratan mis datos personales?")
    st.markdown(
        """
        Womer conecta de forma segura los datos directamente con las bases de datos. Esto asegura que todos sus datos se almacenan en la base de datos de la organización de mujeres indígenas y no directamente con Womer. Toda la gestión de datos está bajo los principios de CARE para asegurar la soberanía de los datos indígenas.
    """
    ) 

    st.subheader("¿Cómo puedo ver los datos de mi comunidad?")
    st.markdown(
        """
        Utilizar los gráficos. Elige la comunidad y la organización. Puedes explorar todos los indicadores y construir tu propio informe en función de lo que necesites o te interese. Para utilizar la solución del cuadro de mando, es necesario registrar un correo electrónico.
    """
    ) 


    st.subheader("Contáctanos")
    st.markdown(
        """
        womer.contact@womer.info
    """
    )