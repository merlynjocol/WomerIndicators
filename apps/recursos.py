import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pandas.api.types import CategoricalDtype




# Data upload
# enter to project / details / API / endpoints
url_info= "https://five.epicollect.net/api/export/entries/mujeres-y-recursos?form_ref=de37bfdc5fc246c2b7e5a68dec3ca944_6306549b3c43c&format=csv&per_page=1000&page=1"
data = pd.read_csv(url_info)


#change the columns names
dict = {'3_Cul_es_la_comunida' : "community",
            '4_Qu_tipo_de_cocina_' : "kitchen", 
            '5_Su_estufa_tiene_ch' : 'chimenea', 
            '6_Qu_energa_o_combus' : 'energy_cook', 
            '7_Quin_est_a_cargo_d' : 'Who_cook',
            '8_Cunto_tiempo_toma_' : 'time_cook',
            '9_Qu_transporte_se_u' : 'transport_energy', 
            '10_Cunto_tiempo_toma' : 'time_transport_energy', 
            '11_Quin_est_a_cargo_' : 'who_transport_energy',
            '12_Qu_usa_para_calen' : 'how_heating',
            '13_Qu_tipo_de_combus' :  'energy_heating',
            '14_Qu_usa_para_enfri' : 'how_cooling',
            '15_Con_qu_energa_o_c' :  'energy_cooling',
            '16_Que_utiliza_para_' :  'how_lighting',
            '17_En_su_hogar_se_pa'  :'energy_payment',
            '19_Quin_principalmen'  : 'who_pay_energy',
            '20__Cul_es_la_PRINCI'  : 'water_source',
            '21_Dnde_se_encuentra' : 'water_where',
            '22_En_su_hogar_se_ut'  : 'water_access',
            '23_Qu_modo_de_transp'  : 'water_transport',
            '24_Cunto_tiempo_toma' : 'water_time',
            '25_Cul_es_la_persona'  : 'who_transport_water',
            '26_Cuntas_viajes_se_'  : 'frequency_transport_water',
            '27_Su_PRINCIPAL_fuen' : 'water_disponibility',
            '28_En_los_ltimos_12_'  : 'last_12month_water',
            '29_Cuando_no_ha_teni'  : 'reason_no_water',
            '31_Cuenta_su_hogar_c'  : 'water_deposit',
            '32_En_el_ltimo_mes_h'  : 'last_month_water_deposit',
            '33_Cul_es_el_servici' :  'sanitary_service',
            '35_El_servicio_sanit'  : 'sanitary_light_lock',
            '36_Dnde_se_encuentra' : 'sanitary_where',
            '37_Comparte_el_servi'  : 'sanitary_sharing',
            '38_Otras_personas_pu'  : 'sanitary_security',
            '39_Hay_algn_riesgo_p' :  'sanitary_risk',
            '41_La_instalacin_tie'  : 'sanitary_hands',
            '42_Utiliza_alguno_de' : 'hand_wash',
            '44_Durante_su_ltimo_'  : 'female_privacity',
            '45_Cul_es_el_materia' : 'female_hygiene',
            '47_No_pudo_participa'  : 'female_participation',
            '49_Quin_es_la_person'  : 'who_wild_food',
            '50_Cunto_tiempo_esta'  : 'time_wild_food', 
            '51_Quin_es_la_person' : 'who_fishing',
            '52_Cunto_tiempo_esta'  : 'time_fishing',
            '53_Quin_es_la_person' : 'who_crops',
            '54_Cunto_tiempo_esta' : 'time_crops'
}

# call rename () method
data.rename(columns=dict,
          inplace=True)

df = data.copy(deep=True)



def app():
    """
    Main app that streamlit will render.
    """
    st.title("⚫ Indicadores de acceso a Recursos Naturales ")
    st.markdown ('---')


    
    # MULTIPAGES SELECTOR 
    # create your radio button with the index that we loaded

    st.sidebar.markdown ('---')
    st.sidebar.subheader("Selecciona el área")
    choice = st.sidebar.radio(" ", ('Energía','Agua','Saneamiento', 'Alimentos' ))

    # df in percentage
    def percentage(column):
        df = (column.value_counts()/column.count())*100
        df = (df.to_frame().reset_index())
        df = df.round(decimals = 1)
        return df

    # Titles charts
    def format_title(title, subtitle=None, subtitle_font_size=16):
        title = f'<b>{title}</b>'
        if not subtitle:
            return title
        subtitle = f'<span style="font-size: {subtitle_font_size}px;">{subtitle}</span>'
        return f'{title}<br>{subtitle}'   


    if choice == 'Energía':

      
        #Energy
        st.subheader("## ☀️ Energía / 3 indicadores")  
        #st.markdown ('---')
        

        indicator = st.selectbox("SELECCIONE UN INDICADOR",
        ("Proporción de la población que tiene acceso a la electricidad",
         'Proporción de la población cuya fuente primaria de energía son los combustibles y tecnologías limpios',
         'Tiempo dedicado a recolectar combustible para el consumo doméstico',
        ))     
        
        #STATE AN ERROR AND DON'T SHOW THE KEYERROR 
        if not indicator :
            st.error(" ⚠️ Por favor seleccione un indicador")
            st.stop()

        # Interactive visualization 
        if indicator == "Proporción de la población que tiene acceso a la electricidad": 
            
            #title
            st.write("#### Proporción de la población que tiene acceso a la electricidad")
            #st.write( 'SDG. Indicador 7.1.1. ')
        

            def conditions(s):
                if (s == 'Lamparas solares' ) or (s == '"Lámpara de gasolina, queroseno"' ) or (s == '"Lámpara de gasolina, queroseno", Vela' )or (s == 'Linterna de pilas recargable, Vela') or  (s == 'Lámpara de aceite o parafina, Vela, Linterna de pilas recargable'): 
                    return "No"
                
                else:
                    return "Si"

            df['Electricity'] = df['how_lighting'].apply(conditions)

            electricity =  percentage(df.Electricity)

            fig_pie = px.pie(electricity, values='Electricity', names='index', color='index',
                                    color_discrete_map={'No':'lightslategray',  'Si':'#f9ab0c'},
                                                        width = 500, height = 300)
            fig_pie.update_layout(title = format_title("% Mujeres con acceso a la Electricidad",
                                                "Iluminación"),
                            title_font_size = 20)
            #fig_pie.update_layout(title="Porcentaje de Hogares usando lengua indígena", title_font_size = 25)
            fig_pie.update_traces(textposition='inside', textfont_size=20)
            fig_pie.update_layout(margin={"r":80,"t":110,"l":0,"b":0})
            st.plotly_chart(fig_pie, unsafe_allow_html=True)



        elif indicator == 'Proporción de la población cuya fuente primaria de energía son los combustibles y tecnologías limpios':  
            
           #title
            st. write("### Proporción de la población cuya fuente primaria de energía son los combustibles y tecnologías limpias")
            st.write( 'SDG. Indicador 7.1.2. ')
        
            def conditions(s):
                if (s == 'Lamparas solares' ): 
                    return "Energías limpias"
                else:
                    return "Energias fósiles o químicas"
            
            df['clean_fuel'] = df['how_lighting'].apply(conditions)
            clean_fuel =  percentage(df.clean_fuel)

            fig_pie = px.pie(clean_fuel, values='clean_fuel', names='index', color='index',
                                    color_discrete_map={'Energías limpias':'#f9ab0c',  'Energias fósiles o químicas':'lightslategray'},
                                                        width = 500, height = 300)
            fig_pie.update_layout(title = format_title("% Mujeres con acceso a Energías limpias",
                                                        "Iluminación"),
                                        title_font_size = 20)
            #fig_pie.update_layout(title="Porcentaje de Hogares usando lengua indígena", title_font_size = 25)
            fig_pie.update_traces(textposition='inside', textfont_size=20)
            fig_pie.update_layout(margin={"r":80,"t":110,"l":0,"b":0})
            st.plotly_chart(fig_pie, unsafe_allow_html=True)



        elif indicator == 'Tiempo dedicado a recolectar combustible para el consumo doméstico':

            #title
            st. write("### Tiempo dedicado a recolectar combustible para el consumo doméstico")
            st.write( 'SDG. Indicador 7.1.2. ')
            # tiempo en cocinar alimentos 
            time_transport_energy =  percentage(df.time_transport_energy)

            time_transport_energy['index'].unique()

            # stablishing catgeories WASH
            categories = CategoricalDtype(['Menos de 1 hora',
                                        '1 hora ',
                                        '2 horas',
                                        '3 horas',
                                        '4 horas ',
                                        'No se '])



            time_transport_energy['index'] =time_transport_energy['index'].astype(categories)
            time_transport_energy = time_transport_energy.sort_values('index')

            colors = ['lightslategray']*len(df)
            colors[ 2 ] = '#f9ab0c'


            #opacity = 0.8

            fig = px.bar(time_transport_energy, x="time_transport_energy", y="index",  
                                width=600, height=300, 
                                labels={ 'time_cook': 'Proporción de Mujeres(%)',  'index': 'Tiempo invertido)'},
                                template = "simple_white", orientation='h'
                                )
            fig.update_layout(title = format_title("Tiempo invertido en transportar combustible",
                                                "Combustible. % Mujeres "),
                            title_font_size = 20)
            fig.update_yaxes(tickmode="array", title_text= " ")                 
            fig.update_yaxes(showgrid=True)
            fig.update_traces(marker_color=colors, opacity = 0.8)
            fig.update_layout(template = "simple_white")
            fig.update_layout(paper_bgcolor="rgb(255, 255, 255)", plot_bgcolor=" rgb(255, 255, 255)")
            fig.update_layout(margin={"r":80,"t":110,"l":0,"b":0})
            st.plotly_chart(fig, unsafe_allow_html=True)

    elif choice == 'Agua': 

        #AGUA
        st.subheader("## 🚰 Agua para consumo / 3 indicadores")  
        #st.markdown ('---')
        

        indicator = st.selectbox("SELECCIONE UN INDICADOR",
        ("Proporción de la población que utiliza servicios de suministro de agua potable gestionados sin riesgos. Por Instalación",
         "Proporción de la población que utiliza servicios de agua para consumo gestionados de manera insegura",
         'Tiempo dedicado a transportar agua para consumo doméstico',
        ))     
        
        #STATE AN ERROR AND DON'T SHOW THE KEYERROR 
        if not indicator :
            st.error(" ⚠️ Por favor seleccione un indicador")
            st.stop()

        # Interactive visualization 
        if indicator == "Proporción de la población que utiliza servicios de suministro de agua potable gestionados sin riesgos. Por Instalación": 

            #title
            st. write("### Proporción de la población que utiliza servicios de suministro de agua potable gestionados sin riesgos")
            st.write( 'SDG. Indicador 6.1.1. ')

            water_source =  percentage(df.water_source)

            # stablishing catgeories WASH
            categories = CategoricalDtype(['Agua de una quebrada, nacimiento ó manantial NO protegida',
                                        'Agua de una quebrada, nacimiento ó manantial protegida',
                                        'Pozo sin bomba, aljibe, jagüey o barreno ',
                                        'Pozo con bomba ',
                                        'Llave o grifo público ',
                                        'Otra fuente por tubería ', 
                                        'Acueducto con tubería dentro de la vivienda '])



            water_source['index'] = water_source['index'].astype(categories)
            water_source = water_source.sort_values('index')

            colors = ['#DCDCDC',]*len(df)
            colors[ 6 ] = '#4086ce'
            #opacity = 0.8

            fig = px.bar(water_source, x="water_source", y="index",  
                                width=700, height=300, 
                                labels={ 'water_source': 'Proporción (%)',  'index': 'Fuente de Agua)'},
                                template = "simple_white", orientation='h'
                                )
            fig.update_layout(title = format_title("% Mujeres con Servicio de Agua para Consumo",
                                                "Gestionados de Manera Segura. Por Instalación"),
                            title_font_size = 20)
            fig.update_yaxes(tickmode="array", title_text= " ")                 
            fig.update_yaxes(showgrid=True)
            fig.update_traces(marker_color=colors, opacity = 0.8)
            fig.update_layout(template = "simple_white")
            fig.update_layout(paper_bgcolor="rgb(255, 255, 255)", plot_bgcolor=" rgb(255, 255, 255)")
            fig.update_layout(margin={"r":80,"t":110,"l":0,"b":0})
            st.plotly_chart(fig, unsafe_allow_html=True)

        elif indicator == "Proporción de la población que utiliza servicios de agua para consumo gestionados de manera insegura":

            def conditions(s):
                if (s == 'Agua de una quebrada, nacimiento ó manantial NO protegida' ) or (s == 'Agua de una quebrada, nacimiento ó manantial protegida' ) or (s == 'Pozo sin bomba, aljibe, jagüey o barreno ' ): 
                    return "Agua superficial"
                
                if (s == 'Pozo con bomba ' ): 
                    return "Instalación no mejorada"
                if (s == 'Llave o grifo público ' ): 
                    return "Servicio limitado"
                if (s == 'Otra fuente por tubería ' ): 
                    return "Servicio básico"
                else:
                    return "Servicio gestionado de manera segura"


            water_source =  percentage(df.water_source)
            water_source['WASH'] = water_source['index'].apply(conditions)

            fig = px.bar(water_source,x="water_source", y="WASH", color="WASH", 
                        labels={ 'water_source': 'Proporción (%)',  'WASH': 'Servicio'},
                        width=700, height=300, 
                        color_discrete_map={'Agua superficial': '#f9ab0c',
                                                'Instalación no mejorada': '#fcd434',
                                                'Servicio limitado': '#faf559',
                                                'Servicio básico': '#DCDCDC', 
                                                'Servicio gestionado de manera segura': '#DCDCDC'},
                        template = "simple_white"
                        )
            fig.update_layout(title = format_title("% Mujeres con Servicio de Agua para Consumo",
                                                "Por categorias del Servicio"),
                            title_font_size = 20)
            fig.update_yaxes(tickmode="array", title_text= " ")                 
            fig.update_yaxes(showgrid=True)
            fig.update_yaxes(visible=True, showticklabels=False)
            fig.update_layout(template = "simple_white")
            fig.update_layout(paper_bgcolor="rgb(255, 255, 255)", plot_bgcolor=" rgb(255, 255, 255)")
            fig.update_layout(margin={"r":80,"t":110,"l":0,"b":0})
            st.plotly_chart(fig, unsafe_allow_html=True)



        elif indicator == 'Tiempo dedicado a transportar agua para consumo doméstico':

            # tiempo en cocinar alimentos 
            water_time =  percentage(df.water_time)



            colors = ['lightslategray']*len(df)
            colors[ 0 ] = '#f9ab0c'
            colors[ 1 ] = '#f9ab0c'


            #opacity = 0.8

            fig = px.bar(water_time, x="water_time", y="index",  
                                width=600, height=300, 
                                labels={ 'water_time': 'Proporción de Mujeres(%)',  'index': 'Tiempo invertido)'},
                                template = "simple_white", orientation='h'
                                )
            fig.update_layout(title = format_title("Tiempo invertido en Transportar Agua",
                                                "Para cocinar alimentos"),
                            title_font_size = 20)
            fig.update_yaxes(tickmode="array", title_text= " ")                 
            fig.update_yaxes(showgrid=True)
            fig.update_traces(marker_color=colors, opacity = 0.8)
            fig.update_layout(template = "simple_white")
            fig.update_layout(paper_bgcolor="rgb(255, 255, 255)", plot_bgcolor=" rgb(255, 255, 255)")
            fig.update_layout(margin={"r":80,"t":110,"l":0,"b":0})
            st.plotly_chart(fig, unsafe_allow_html=True)

    elif choice == 'Saneamiento': 

        #AGUA
        st.subheader("## 🚾 Saneamiento / 5 indicadores")  
        #st.markdown ('---')
        

        indicator = st.selectbox("SELECCIONE UN INDICADOR",
        ("Proporción de la población que utiliza (a) servicios de saneamiento gestionados de forma segura",
         "Proporción de Mujeres con servicio de saneamiento. Por servicio"
         'Proporción de Mujeres con servicios de saneamiento con puerta de seguridad e iluminación',
         "Proporción de mujeres que enfrentan riesgos al usar los servicios de saneamiento",
         "Proporción de la población que utiliza instalaciones para lavarse las manos con agua y jabón",
         "Proporción de mujeres con acceso a instalaciones privadas durante el período menstrual"       
        
        ))     
        
        #STATE AN ERROR AND DON'T SHOW THE KEYERROR 
        if not indicator :
            st.error(" ⚠️ Por favor seleccione un indicador")
            st.stop()


        sanitary_service  =  percentage(df.sanitary_service)
        df2 = pd.DataFrame({'index': ['Inodoro conectado a alcantarillado',
                              'Letrina de doble pozo', 
                              'Letrina colgante construida sobre una superficie de agua'],
                            'sanitary_service': [0,0,0],
                             })

        # Append the rows of the above pandas DataFrame to the existing pandas DataFrame
        sanitary_service = sanitary_service.append(df2,ignore_index=True)

        # stablishing catgeories WASH
        categories = CategoricalDtype(['Inodoro conectado a alcantarillado',
                                        'Inodoro conectado a pozo o tanque séptico ',
                                        'Inodoro a drenaje abierto',
                                        'Inodoro con destino desconocido',
                                        'Letrina de pozo',
                                        'Letrina de doble pozo',
                                        'Letrina de fosa con losa',
                                        'Letrina de fosa sin losa  o  pozo abierto',
                                        'Otra letrina de compostaje',
                                        'Letrina colgante construida sobre una superficie de agua',
                                        'Letrina con descarga a una fuente de agua, rio, laguna, etc',
                                        'Cubo, recipiente o contenedor',
                                        'No tengo instalación. Monte, campo abierto, playa, rio, laguna',
                                            ])

        sanitary_service["index"] = sanitary_service["index"].astype(categories)
        sanitary_service= sanitary_service.sort_values('index')
        
        # Interactive visualization 
        if indicator == "Proporción de la población que utiliza (a) servicios de saneamiento gestionados de forma segura":

            colors = ['#DCDCDC',]*len(df)
            colors[ 0 ] = '#4086ce'
            colors[ 1 ] = '#4086ce'
            colors[ 2 ] = '#4086ce'
            #opacity = 0.8

            fig = px.bar(sanitary_service, x="sanitary_service", y="index",  
                                width=700, height=500, 
                                labels={ 'sanitary_service': 'Proporción (%)',  'index': 'Servicio)'},
                                template = "simple_white", orientation='h'
                                )
            fig.update_layout(title = format_title("% Mujeres con Servicio de Saneamiento",
                                                "Gestionados de Manera Segura"),
                            title_font_size = 20)
            fig.update_yaxes(tickmode="array", title_text= " ")                 
            fig.update_yaxes(showgrid=True)
            fig.update_traces(marker_color=colors, opacity = 0.8)
            fig.update_layout(template = "simple_white")
            fig.update_layout(paper_bgcolor="rgb(255, 255, 255)", plot_bgcolor=" rgb(255, 255, 255)")
            fig.update_layout(margin={"r":80,"t":110,"l":0,"b":0})
            st.plotly_chart(fig, unsafe_allow_html=True)



        elif indicator == "Proporción de Mujeres con servicio de saneamiento. Por servicio":
            def conditions(s):
                if (s == 'Inodoro conectado a alcantarillado' ) or (s == 'Inodoro conectado a pozo o tanque séptico ' ) or (s ==  'Inodoro a drenaje abierto' ) : 
                    return "Servicio gestionado de manera segura"
            
                if (s == 'Inodoro con destino desconocido') or (s == 'Letrina de pozo') or (s == 'Letrina de fosa con losa')or (s == 'Letrina de doble pozo') : 
                    return "Servicio Básico"
                if (s== 'Letrina de fosa sin losa  o  pozo abierto' ) or ( s== 'Otra letrina de compostaje'): 
                    return "Servicio limitado"
                if (s == 'Letrina colgante construida sobre una superficie de agua'): 
                    return "Instalaciòn no mejorada"
                else:
                    return "Defecación al aire libre"

            sanitary_service['Service'] = sanitary_service['index'].apply(conditions)

            fig = px.bar(sanitary_service,x="sanitary_service", y='Service', color='Service', 
                        labels={ 'sanitary_service': 'Proporción (%)',  'Service': 'Servicio'},
                        width=700, height=300, 
                        color_discrete_map={'Defecación al aire libre': '#f9ab0c',
                                                'Instalación no mejorada': '#fcd434',
                                                'Servicio limitado': '#faf559',
                                                'Servicio Básico': '#DCDCDC', 
                                                'Servicio gestionado de manera segura': '#DCDCDC'},
                            )
            fig.update_layout(title = format_title("% Mujeres con Servicio de Saneamiento",
                                                "Gestionados de Manera insegura"),
                            title_font_size = 20)
            fig.update_yaxes(tickmode="array", title_text= " ")                 
            fig.update_yaxes(showgrid=False)
            #fig.update_yaxes(visible=True, showticklabels=False)
            fig.update_layout(template = "simple_white")
            #fig.update_layout(paper_bgcolor="rgb(255, 255, 255)", plot_bgcolor=" rgb(255, 255, 255)")
            fig.update_layout(margin={"r":80,"t":110,"l":0,"b":0})
            fig.update_traces(showlegend=False)
            st.plotly_chart(fig, unsafe_allow_html=True)

        elif indicator== "Proporción de Mujeres con servicios de saneamiento con puerta de seguridad e iluminación": 


            # Lighting and Security in Sanitary services 
            sanitary_light_lock=  percentage(df.sanitary_light_lock)

            colors = ['lightslategray']*len(df)
            colors[ 3 ] = 'crimson'

            #opacity = 0.8

            fig = px.bar(sanitary_light_lock, x="sanitary_light_lock", y="index",  
                                width=600, height=300, 
                                labels={ 'sanitary_light_lock': 'Proporción (%)',  'index': 'Servicio)'},
                                template = "simple_white", orientation='h'
                                )
            fig.update_layout(title = format_title("% Mujeres con iluminación y cerradura",
                                                "En el servicio de saneamiento"),
                            title_font_size = 20)
            fig.update_yaxes(tickmode="array", title_text= " ")                 
            fig.update_yaxes(showgrid=True)
            fig.update_traces(marker_color=colors, opacity = 0.8)
            fig.update_layout(template = "simple_white")
            fig.update_layout(paper_bgcolor="rgb(255, 255, 255)", plot_bgcolor=" rgb(255, 255, 255)")
            fig.update_layout(margin={"r":80,"t":110,"l":0,"b":0})
            st.plotly_chart(fig, unsafe_allow_html=True)

        elif indicator== "Proporción de mujeres que enfrentan riesgos al usar los servicios de saneamiento": 
            
            # risk for women 
            sanitary_risk =  percentage(df.sanitary_risk)

            colors = ['lightslategray']*len(df)
            colors[ 3 ] = 'crimson'
            colors[ 2 ] = 'crimson'
            colors[ 1 ] = 'crimson'


            #opacity = 0.8

            fig = px.bar(sanitary_risk , x="sanitary_risk", y="index",  
                                width=600, height=300, 
                                labels={ 'sanitary_risk ': 'Proporción (%)',  'index': 'Servicio'},
                                template = "simple_white", orientation='h',
                                )
            fig.update_layout(title = format_title("% Mujeres enfrentando riesgos",
                                                "Por el uso del Servicio de Saneamiento"),
                            title_font_size = 20)
            fig.update_yaxes(tickmode="array", title_text= " ")                 
            fig.update_yaxes(showgrid=True)
            fig.update_traces(marker_color=colors, opacity = 0.8)
            fig.update_layout(template = "simple_white")
            fig.update_layout(paper_bgcolor="rgb(255, 255, 255)", plot_bgcolor=" rgb(255, 255, 255)")
            fig.update_layout(margin={"r":80,"t":110,"l":0,"b":0})
            st.plotly_chart(fig, unsafe_allow_html=True)

        elif indicator == "Proporción de la población que utiliza instalaciones para lavarse las manos con agua y jabón":
            
            # infraestructure
            sanitary_hands =  percentage(df.sanitary_hands)

            fig_pie = px.pie(sanitary_hands, values='sanitary_hands', names='index', color='index',
                                    color_discrete_map={'No':'crimson',  'Si':'lightslategray'},
                                                        width = 500, height = 300)
            fig_pie.update_layout(title = format_title("% Mujeres utilizando instalaciones",
                                                "para el lavado de manos con agua y jabón"),
                            title_font_size = 20)
            #fig_pie.update_layout(title="Porcentaje de Hogares usando lengua indígena", title_font_size = 25)
            fig_pie.update_traces(textposition='inside', textfont_size=20)
            fig_pie.update_layout(margin={"r":80,"t":110,"l":0,"b":0})
            st.plotly_chart(fig_pie, unsafe_allow_html=True)

        elif indicator ==  "Proporción de mujeres con acceso a instalaciones privadas durante el período menstrual" : 

            female_privacity =  percentage(df.female_privacity)

            fig_pie = px.pie(female_privacity, values='female_privacity', names='index', color='index',
                                    color_discrete_map={'No he tenido privacidad':'#9F4F86',  'Si tengo privacidad':'lightslategray'},
                                                        width = 500, height = 300)
            fig_pie.update_layout(title = format_title("% Mujeres con privacidad",
                                                "Durante el periodo menstrual"),
                            title_font_size = 20)
            #fig_pie.update_layout(title="Porcentaje de Hogares usando lengua indígena", title_font_size = 25)
            fig_pie.update_traces(textposition='inside', textfont_size=20)
            fig_pie.update_layout(margin={"r":80,"t":110,"l":0,"b":0})
            st.plotly_chart(fig_pie, unsafe_allow_html=True)



     
    elif choice == 'Alimentos': 

        st.subheader("## 🍓 Alimentos  / 6 indicadores")  
        #st.markdown ('---')
        

        indicator = st.selectbox("SELECCIONE UN INDICADOR",
        ("Tiempo dedicado a recolectar plantas, hongos, flores y frutos silvestres; Pesca y caza para consumo doméstico",
         "Tiempo dedicado a la caza y la pesca para el consumo doméstico",
         'Tipo de estufa utilizada para cocinar',
         "Proporción de hogares que utilizan estufas con chimenea",
         "Tiempo dedicado a cocinar los alimentos",
         "Tiempo dedicado al trabajo de cuidados no remunerado en prácticas sostenibles. Similar al ODS 5.4.1"       
        
        ))     
        
        #STATE AN ERROR AND DON'T SHOW THE KEYERROR 
        if not indicator :
            st.error(" ⚠️ Por favor seleccione un indicador")
            st.stop()


        if indicator == "Tiempo dedicado a recolectar plantas, hongos, flores y frutos silvestres; Pesca y caza para consumo doméstico":

            # tiempo en cocinar alimentos 
            time_wild_food =  percentage(df.time_wild_food)
            time_wild_food = time_wild_food .sort_values('index')

            colors = ['lightslategray']*len(df)
            colors[ 1 ] = 'crimson'


            #opacity = 0.8

            fig = px.bar(time_wild_food, x="time_wild_food", y="index",  
                                width=600, height=300, 
                                labels={ 'time_wild_food': 'Proporción de Mujeres(%)',  'index': 'Tiempo invertido)'},
                                template = "simple_white", orientation='h'
                                )
            fig.update_layout(title = format_title("Tiempo invertido en Recolectar Alimentos ",
                                                "Del bosque y otros espacios"),
                            title_font_size = 20)
            fig.update_yaxes(tickmode="array", title_text= " ")                 
            fig.update_yaxes(showgrid=True)
            fig.update_traces(marker_color=colors, opacity = 0.8)
            fig.update_layout(template = "simple_white")
            fig.update_layout(paper_bgcolor="rgb(255, 255, 255)", plot_bgcolor=" rgb(255, 255, 255)")
            fig.update_layout(margin={"r":80,"t":110,"l":0,"b":0})
            st.plotly_chart(fig, unsafe_allow_html=True)