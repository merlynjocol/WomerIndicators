import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pandas.api.types import CategoricalDtype


#PAGE_CONFIG = {"page_title":"StColab.io","page_icon":":smiley:","layout":"centered"}
#st.beta_set_page_config(**PAGE_CONFIG)

st.sidebar.markdown("# Información General")


#CONTAINER:HEADER
st.markdown ('<h1 style= "font-family:Verdana; color:Black; font-size: 40px;">  🚺 Información general</h1>', unsafe_allow_html=True)
#st.text('this is app')
st.write (''' 
las siguientes gráficas muestran la information general de las mujeres indigenas''')
st.markdown ('---')


# Data
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

# DATAFRAME Nasa Indigenous People 
df = data.loc[data['2_comunidad'] == "Nasa"]

# TOTAL INDIGENOUS WOMEN
total = data.loc[data['2_comunidad'] == "Nasa", 'ec5_uuid'].nunique()
st.write(total, 'Mujeres')

# SELECTING  the Resguardo 
resguardo = st.multiselect("SELECT A RESGUARDO", df['3_En_que_resguardo_N'].unique())

# TAMAÑO DEL HOGAR

hogar = df.groupby(['14_personas_hogar'])['ec5_uuid'].count().reset_index()
# Option 2- the problem es the result is organized by value
hogar2= df["14_personas_hogar"].value_counts().to_frame()

fig = px.bar(hogar, x="14_personas_hogar", y="ec5_uuid",  
                 
                width=700, height=400, 
                labels={ '14_personas_hogar': 'Personas en el hogar',  'ec5_uuid': 'Total hogares'}
                )
fig.update_layout(title = "Tamaño del Hogar",  title_font_size = 20)
fig.update_yaxes(tickmode="array", title_text= " ")                 
fig.update_yaxes(showgrid=True)
fig.update_traces(marker_color='#00aae6', opacity = 0.8)
fig.update_layout(template = "simple_white")

st.plotly_chart(fig, unsafe_allow_html=True)

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


# JEFATURA de hogares. Total Mujeres Cabeza de Hogar 
# functions execution
mujer_jefe = percentage(df['17_soy_jefe_hogar'])
newframe(mujer_jefe)
mujer_jefe  = onedecimal(mujer_jefe)


total = mujer_jefe .loc[1,'value']
st.write( total, "%",'Mujeres con jefatura en hogares')



#¿Cual es el mi parentesco con la persona jefe del hogar?`

jefe_hogar = df.groupby(['19_pariente_jefe'])['ec5_uuid'].count().reset_index()
jefe_hogar = jefe_hogar.sort_values('ec5_uuid')

fig = px.bar(jefe_hogar, x="19_pariente_jefe", y="ec5_uuid",  
                 
                width=700, height=400, 
                labels={ '19_pariente_jefe': 'Parentesco',  'ec5_uuid': 'Total Mujeres'}
                )
fig.update_layout(title = "¿Cual es el mi parentesco con la persona jefe del hogar?`",  title_font_size = 20)
fig.update_yaxes(tickmode="array", title_text= " ")                 
fig.update_yaxes(showgrid=True)
fig.update_traces(marker_color='#00aae6', opacity = 0.8)
fig.update_layout(template = "simple_white")
st.plotly_chart(fig, unsafe_allow_html=True)

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
                 width=500, height=400, 
                labels={ '12_Edad': 'Rango de Edad',  'ec5_uuid': 'Total Mujeres'},
                orientation='h', 
                category_orders={'12_Edad': ["15-24", "25-44", '45-54', '55-64', '+ 65 años']}
                )
fig.update_layout(title = "Estructura por Edad de las mujeres indígenas`",  title_font_size = 20)
fig.update_yaxes(tickmode="array", title_text= " ")                 
fig.update_yaxes(showgrid=True)
fig.update_traces(marker_color='#9F4F86', opacity = 0.8)
fig.update_layout(template = "simple_white")
st.plotly_chart(fig, unsafe_allow_html=True)


# EDUCATION

educacion= df.groupby(['22_educacion'])['ec5_uuid'].count().reset_index()
educacion = educacion.sort_values('ec5_uuid')

fig = px.bar(educacion, y='22_educacion', x="ec5_uuid",  
                 width=500, height=400, 
                labels={ '22_educacion': 'Educación',  'ec5_uuid': 'Total Mujeres'},
                orientation='h', 
                category_orders={'12_Edad': ["15-24", "25-44", '45-54', '55-64', '+ 65 años']}
                )
fig.update_layout(title = "Nivel de educación de las mujeres indígenas`",  title_font_size = 20)
fig.update_yaxes(tickmode="array", title_text= " ")                 
fig.update_yaxes(showgrid=True)
fig.update_traces(marker_color='#D883BB', opacity = 0.8)
fig.update_layout(template = "simple_white")
st.plotly_chart(fig, unsafe_allow_html=True)

# ESTADO CIVI*

estado_civil= df.groupby(['20_estado_civil'])['ec5_uuid'].count().reset_index()
estado_civil = estado_civil.sort_values('ec5_uuid')

estado_civil['20_estado_civil'] = estado_civil['20_estado_civil'] .replace(['No estoy casada y vivo con mi pareja hace menos de dos años',
                                                                            'No estoy casada y vivo en pareja hace más de dos años'],
                                                                           ['Vivo en pareja menos de dos años', 
                                                                            'Vivo en pareja más de dos años'])
                                                                            
                                                                            
                                                                            
#Chart
fig = px.bar(estado_civil, y='20_estado_civil', x="ec5_uuid",  
                 width=700, height=400, 
                labels={ '20_estado_civil': 'Estado civil',  'ec5_uuid': 'Total Mujeres'},
                orientation='h'
                )
fig.update_layout(title = "# Estructura por Edad de la población de mujeres`",  title_font_size = 20)
fig.update_yaxes(tickmode="array", title_text= " ")                 
fig.update_yaxes(showgrid=True)
fig.update_traces(marker_color='#374955', opacity = 0.8)
fig.update_layout(template = "simple_white")
st.plotly_chart(fig, unsafe_allow_html=True)


#MUJERES CON HIJOS
hijos =  df.groupby(['21_Tiene_hijos'])['ec5_uuid'].count().reset_index()
# functions execution
mujer_hijos = percentage(df['21_Tiene_hijos'])
newframe(mujer_hijos)
mujer_hijos = onedecimal(mujer_hijos)


total = mujer_hijos.loc[0,'value']
st.write('Porcentaje de mujeres con hijos', total, "%")


# HOGARES que hablan lengua indigena


# Note: 
df['9_lengua'] = df['9_lengua'] .replace(['Español, Lengua indigena', 'Lengua indigena, Español'],['Español', 'Español'])
lengua =  df.groupby(['9_lengua'])['ec5_uuid'].count().reset_index()

#CHART PIE 
fig_pie = px.pie(lengua, values='ec5_uuid', names='9_lengua', color='9_lengua',
                 color_discrete_map={'Español':"#374955",  'Lengua indigena':'#00aae6'},
                                    width = 600, height = 400)
fig_pie.update_layout(title="Hogares donde se comunican en la lengua indígena", title_font_size = 20)
st.plotly_chart(fig_pie, unsafe_allow_html=True)


#MUJERES Y LA LENGUA /WOMEN & LENGUAGE

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


#CHART
fig = px.bar(mujeres_lengua, y="Class", x='Value',  
                 width=700, height=400, 
                labels={ 'Value': 'Total de mujeres',  'Class': 'Categoria'},
                orientation='h'
                )
fig.update_layout(title = "Comunicación en lengua nativa usada por las mujeres",  title_font_size = 20)
fig.update_yaxes(tickmode="array", title_text= " ")                 
fig.update_yaxes(showgrid=True)
fig.update_traces(marker_color='#374955', opacity = 0.8)
fig.update_layout(template = "simple_white")
st.plotly_chart(fig, unsafe_allow_html=True)