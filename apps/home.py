"""
Home page
"""

import streamlit as st
from PIL import Image


def app():
    """
    Main app that streamlit will render.
    """
    
    
    
    st.markdown ('<h1 style= "font-family:Verdana; color:Black; font-size: 48px;">Women in Ecosystem Restoration</h1>', unsafe_allow_html=True)
    
     
       
    st.subheader(
        """
        📈 Womer WebApp ayuda a las mujeres y jóvenes indígenas a investigar sobre el nexo entre género y cambio climático para mejorar las politicas públicas y su participación en espacios de decisión climática

    """
    ) 



    st.subheader("¿Cómo funciona Womer WebApp?")
    st.markdown(
        """
        ⬇️ la WebApp descarga automáticamente los datos recolectados con la aplicación EPICOLECT5

        📈 Elige la comunidad y la organización. Puedes explorar todos los indicadores y construir tu propio informe en función de lo que necesites o te interese. Para utilizar la solución del cuadro de mando, es necesario registrar un correo electrónico

        🌎 Las gráficas presentadas corresponden a los indicadores seleccionados para analizar la dimensión de género en el cambio climático 
        
        📄 Permite la fácil elaboración de Informes mediante gráficos interactivos con indicadores sobre género y medio ambiente. 
        
        🔊 Puedes utilizar los informes  apoyan las investigaciones, estrategias de inciencia y dar voz a las mujeres indígenas a través de usar los datos. 
    """
    ) 

    st.subheader("Soberanía indígena de los datos")
    st.markdown(
        """
        La organización indígena decide quién puede acceder a los datos y publicarlos. Trabajamos bajo los PRINCIPIOS CARE para asegurar la soberanía de los datos indígenas.
    """
    ) 

    st.subheader("Contáctanos")
    st.markdown(
        """
        womer.contact@womer.info
    """
    )

    st.subheader('''Designed by: ''')
    st.markdown(
        """
        Merlyn J. Hurtado @merlynjocol
    """
    )  


    # Footer Slidebar


    st.sidebar.markdown ('---')
    st.sidebar.header("Con el apoyo de: ")

    # Logos in columns

    st.sidebar.image('https://github.com/merlynjocol/WomerWebApp/blob/main/images/Crowd4SDG-removebg-preview.png?raw=true', width=200)

    
    col1, col2 = st.sidebar.columns([1.4, 1.2])
    with col1:
        st.image('https://github.com/merlynjocol/WomerWebApp/blob/main/images/Citizen-Cyberlab.png?raw=true', width=120)

    with col2:
        st.image('https://github.com/merlynjocol/WomerWebApp/blob/main/images/LEARNING%20PLANET.png?raw=true', width=70)


