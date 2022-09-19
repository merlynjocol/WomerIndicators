import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pandas.api.types import CategoricalDtype




# Data upload
# enter to project / details / API / endpoints
url_info= "https://five.epicollect.net/api/export/entries/mi-info?form_ref=9361e82b02d84041b1d74ae3b7957177_63064c4d6ea93&format=csv&per_page=1000&page=1"

data = pd.read_csv(url_info)



#change the columns names
dict = {'1_Todas_las_respuest' : '1_consentimiento' , 
        '2_Cul_es_la_comunida': '2_comunidad', 
        '8_Cul_es_el_nombre_d' : '8_vereda', 
        '9_Cul_es_la_lengua_q': '9_lengua',
       '10_Habla_la_lengua_i': '10_Habla_lengua_i', 
        '11_Entiende_la_lengu': '11_Entiende_lengua_i', 
        '12_En_cul_rango_de_e':  '12_Edad',
       '13_Usted_se_identifi' : '13_genero', 
        '14_Cuntas_personas_q': '14_personas_hogar', 
        '15_Cuntos_menores_de': '15_menores_hogar',
        '16_Cuntas_personas_m': '16_mayores_hogar', 
        '17_Es_usted_la_perso': '17_soy_jefe_hogar',
        '18_La_persona_jefe_d': '18_jefe_hogar',
       '19_Cul_es_su_parente': '19_pariente_jefe',
        '20_Cul_es_su_estado_':'20_estado_civil', 
        '22_Cul_es_el_ltimo_n': '22_educacion', 
        '23_Asiste_en_este_mo': '23_asiste_educ', 
        '24_Por_favor_escriba': '24_id_indigena'
        }


# call rename () method
data.rename(columns=dict,
          inplace=True)
#PAGE_CONFIG = {"page_title":"StColab.io","page_icon":":smiley:","layout":"centered"}
#st.beta_set_page_config(**PAGE_CONFIG)


def app():
    """
    Main app that streamlit will render.
    """
    st.title("⚫ Datos de la Población de Mujeres Indígenas")

    st.markdown ('---')

    
    # DATAFRAME Nasa Indigenous People 
    df = data.loc[data['2_comunidad'] == "Nasa"]

    #    TOTAL INDIGENOUS WOMEN
    total = data.loc[data['2_comunidad'] == "Nasa", 'ec5_uuid'].nunique()

    # SELECTING  the Resguardo 
    resguardo = st.multiselect("SELECCIONE UN RESGUARDO", df['3_En_que_resguardo_N'].unique())


    # DEFINE FUNTIONS

    # function for calculate percentage
    def percentage(column):
        return (column.value_counts()/column.count())*100

    # funtion to create dataframe
    def newframe(df):
        return (df.to_frame().reset_index())

     # funtion to change name and 1 decimal
    def onedecimal(df):
        return (df.reset_index(name='value').round(decimals = 1))


    # SECTION: Total mujeres indigenas
    row1_col1, row1_col2, row1_col3, row1_col4 = st.columns(4)
    with row1_col1:
        st.write("### Número Total de Mujeres Indígenas")
        

    with row1_col2:
        st.title(total)
        st.write("##")
    
    with row1_col3:
        st.write('### Porcentaje de mujeres con hijos')

    with row1_col4:
        #hijos =  df.groupby(['21_Tiene_hijos'])['ec5_uuid'].count().reset_index()
        # functions execution
        mujer_hijos = percentage(df['21_Tiene_hijos'])
        newframe(mujer_hijos)
        mujer_hijos = onedecimal(mujer_hijos)

        total = mujer_hijos.loc[0,'value']       
        st.title(total, "%")
        st.write("%")



    # SECTION: Women information
    
    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:

        # EDAD
        edad = df.groupby(['12_Edad'])['ec5_uuid'].count().reset_index()
        edad['12_Edad'] = edad['12_Edad'] .replace([' 45-54', 'Mayor de 65 años'],['45-54', '+ 65 años'])


        # dont need 
        categories = CategoricalDtype(["15-24", "25-44", '45-54', '55-64', '+ 65 años'], 
            ordered=True
        )
        edad['12_Edad'] = edad['12_Edad'].astype(categories)
        edad.sort_values('12_Edad')

        fig = px.bar(edad, y="12_Edad", x="ec5_uuid",  
                        width=500, height=300, 
                        labels={ '12_Edad': 'Rango de Edad',  'ec5_uuid': 'Total Mujeres'},
                        orientation='h', 
                        category_orders={'12_Edad': ["15-24", "25-44", '45-54', '55-64', '+ 65 años']}
                        )
        fig.update_layout(title = "Edad de las mujeres indígenas`",  title_font_size = 25)
        fig.update_yaxes(tickmode="array", title_text= " ")                 
        fig.update_yaxes(showgrid=True)
        fig.update_traces(marker_color='#24b3ab', opacity = 0.8)
        fig.update_layout(template = "simple_white")
        fig.update_layout(paper_bgcolor="rgb(255, 255, 255)", plot_bgcolor=" rgb(255, 255, 255)")
        fig.update_layout(margin={"r":80,"t":110,"l":0,"b":0})
        st.plotly_chart(fig, unsafe_allow_html=True)
 
   
    with row2_col2: 
        # EDUCATION

        educacion= df.groupby(['22_educacion'])['ec5_uuid'].count().reset_index()
        educacion = educacion.sort_values('ec5_uuid')

        fig = px.bar(educacion, y='22_educacion', x="ec5_uuid",  
                        width=500, height=300, 
                        labels={ '22_educacion': 'Educación',  'ec5_uuid': 'Total Mujeres'},
                        orientation='h', 
                        category_orders={'12_Edad': ["15-24", "25-44", '45-54', '55-64', '+ 65 años']}
                        )
        fig.update_layout(title = "Nivel de educación de las mujeres indígenas`",  title_font_size = 25)
        fig.update_yaxes(tickmode="array", title_text= " ")                 
        fig.update_yaxes(showgrid=True)
        fig.update_traces(marker_color='#24b3ab', opacity = 0.8)
        fig.update_layout(template = "simple_white")
        fig.update_layout(paper_bgcolor="rgb(255, 255, 255)", plot_bgcolor=" rgb(255, 255, 255)")
        fig.update_layout(margin={"r":80,"t":110,"l":0,"b":0})
        st.plotly_chart(fig, unsafe_allow_html=True)


    
    row3_col1, row3_col2 = st.columns(2)
    
    with row3_col1:

        # ESTADO CIVIL / data
        estado_civil= df.groupby(['20_estado_civil'])['ec5_uuid'].count().reset_index()
        estado_civil = estado_civil.sort_values('ec5_uuid')
        estado_civil['20_estado_civil'] = estado_civil['20_estado_civil'] .replace(['No estoy casada y vivo con mi pareja hace menos de dos años',
                                                                                    'No estoy casada y vivo en pareja hace más de dos años'],)
                                                                 
        #Chart
        fig = px.bar(estado_civil, y='20_estado_civil', x="ec5_uuid",  
                        width=500, height=300, 
                        labels={ '20_estado_civil': 'Estado civil',  'ec5_uuid': 'Total Mujeres'},
                        orientation='h'
                        )
        fig.update_layout(title = "Estado civil de las mujeres`",  title_font_size = 25)
        fig.update_yaxes(tickmode="array", title_text= " ")                 
        fig.update_yaxes(showgrid=True)
        fig.update_traces(marker_color='#24b3ab', opacity = 0.8)
        fig.update_layout(template = "simple_white")
        fig.update_layout(paper_bgcolor="rgb(255, 255, 255)", plot_bgcolor=" rgb(255, 255, 255)")
        fig.update_layout(margin={"r":80,"t":110,"l":0,"b":0})
        st.plotly_chart(fig, unsafe_allow_html=True)

    with row3_col2: 
        st.write("##")


    
    st.markdown ('---')
   
    st.write("## 🏠 Hogares de las Mujeres Indígenas")  


    # SECTION:  Jefatura de hogares

    row3_col1, row3_col2 = st.columns(2)
    
    with row3_col1:
        
    
        mujer_jefe = percentage(df['17_soy_jefe_hogar'])
        newframe(mujer_jefe)
        mujer_jefe  = onedecimal(mujer_jefe)
        total = mujer_jefe .loc[1,'value']

        st.write("#### Porcentaje de Mujeres a cargo del Hogar")
        st.title(total)


    with row3_col2: 

        # Parentesco
        jefe_hogar = df.groupby(['19_pariente_jefe'])['ec5_uuid'].count().reset_index()
        jefe_hogar = jefe_hogar.sort_values('ec5_uuid')

        fig = px.bar(jefe_hogar, x="19_pariente_jefe", y="ec5_uuid",  
                    
                    width=500, height=300, 
                    labels={ '19_pariente_jefe': 'Parentesco',  'ec5_uuid': 'Total Mujeres'}
                    )
        fig.update_layout(title = "Parentesco con la persona jefe del hogar",  title_font_size = 25)
        fig.update_yaxes(tickmode="array", title_text= " ")                 
        fig.update_yaxes(showgrid=True)
        fig.update_traces(marker_color='#24b3ab', opacity = 0.8)
        fig.update_layout(template = "simple_white")
        fig.update_layout(paper_bgcolor="rgb(255, 255, 255)", plot_bgcolor=" rgb(255, 255, 255)")
        fig.update_layout(margin={"r":80,"t":110,"l":0,"b":0})
        st.plotly_chart(fig, unsafe_allow_html=True)


    row4_col1, row4_col2 = st.columns(2)

    with row4_col1:
        # TAMAÑO DEL HOGAR
        hogar = df.groupby(['14_personas_hogar'])['ec5_uuid'].count().reset_index()

        fig = px.bar(hogar, x="14_personas_hogar", y="ec5_uuid",  
                    width=500, height=400, 
                    labels={ '14_personas_hogar': 'Personas en el hogar',  'ec5_uuid': 'Total hogares'},
                    template = "simple_white"
                    )
        fig.update_layout(title = "Tamaño del Hogar",  title_font_size = 25)
        fig.update_yaxes(tickmode="array", title_text= " ")                 
        fig.update_yaxes(showgrid=True)
        fig.update_traces(marker_color='#24b3ab', opacity = 0.8)
        fig.update_layout(paper_bgcolor="rgb(255, 255, 255)", plot_bgcolor=" rgb(255, 255, 255)")
        fig.update_layout(margin={"r":80,"t":110,"l":0,"b":0})
        st.plotly_chart(fig, unsafe_allow_html=True)

    

    with row4_col2:
        # HOGARES que hablan lengua indigena
        # Note: (variable por revisar)
        df['9_lengua'] = df['9_lengua'] .replace(['Español, Lengua indigena', 'Lengua indigena, Español'],['Español', 'Español'])
        lengua =  df.groupby(['9_lengua'])['ec5_uuid'].count().reset_index()

        fig_pie = px.pie(lengua, values='ec5_uuid', names='9_lengua', color='9_lengua',
                        color_discrete_map={'Español':"#374955",  'Lengua indigena':'#24b3ab'},
                                            width = 500, height = 300)
        fig_pie.update_layout(title="Porcentaje de Hogares usando lengua indígena", title_font_size = 25)
        fig_pie.update_traces(textposition='inside', textfont_size=20)
        fig_pie.update_layout(margin={"r":80,"t":110,"l":0,"b":0})
        st.plotly_chart(fig_pie, unsafe_allow_html=True)


    st.markdown ('---')
   
   # SECTION: Women and language 
    st.write("## 💬 Uso de la Lengua Ancestral")  

    def conditions(s):
        if (s['10_Habla_lengua_i'] == 'Si') and (s['11_Entiende_lengua_i'] == 'Si'):
            return "Habla y Entiende"
        if (s['10_Habla_lengua_i'] == 'Si') and (s['11_Entiende_lengua_i'] == 'No'):
            return "Habla y No entiende"
        if (s['10_Habla_lengua_i'] == 'No') and (s['11_Entiende_lengua_i'] == 'Si'):
            return "Entiende pero No habla"
        else:
            return "No habla, No entiende"

    hablar_entender = df[['10_Habla_lengua_i', '11_Entiende_lengua_i']].copy()
    hablar_entender['Class'] =hablar_entender.apply(conditions, axis=1)
    mujeres_lengua =  hablar_entender.groupby('Class')['10_Habla_lengua_i'].count().to_frame().reset_index()
    mujeres_lengua .rename(columns = {'10_Habla_lengua_i':'Value'}, inplace = True)


    fig = px.bar(mujeres_lengua, y="Class", x='Value',  
                    width=700, height=300, 

                    labels={ 'Value': 'Total de mujeres',  'Class': 'Categoria'},
                    orientation='h'
                    )
    fig.update_layout(title = "Comunicación en lengua nativa usada por las mujeres",  title_font_size = 20)
    fig.update_yaxes(tickmode="array", title_text= " ")                 
    fig.update_yaxes(showgrid=True)
    fig.update_traces(marker_color='#374955', opacity = 0.8)
    fig.update_layout(template = "simple_white")
    fig.update_layout(paper_bgcolor="rgb(255, 255, 255)", plot_bgcolor=" rgb(255, 255, 255)")
    fig.update_layout(margin={"r":80,"t":110,"l":0,"b":0})
    st.plotly_chart(fig, unsafe_allow_html=True)
