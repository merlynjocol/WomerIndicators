import pandas as pd
import numpy as np
import datetime
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import folium
from IPython.display import HTML
from pandas.api.types import CategoricalDtype

# Data upload
# enter to project / details / API / endpoints
url_info= "https://five.epicollect.net/api/export/entries/mujeres-y-tierras?form_ref=53c94816cee44815a184eeb52f374d87_63025ec233674&format=csv&per_page=1000&page=1"

data = pd.read_csv(url_info)

dict = {'4_Este_hogar_ha_trab':  "trabajo_agricola",
        '5_La_actividad_agrco': "agricola_actividad", 
        '6_Este_hogar_ha_cria': "cria_animales", 
        '7_La_cra_o_el_cuidad': "cria_actividad", 
        '8_Este_hogar_ha_cria': "cria_peces", 
        '9_Realiz_la_pesca_pa' : 'pesca_actividad',
        '10_Cuntos_adultos_vi': "total_adultos", 
        '11_Es_propietaria_ut': "mujer_propietaria", 
        '12_Existe_algn_docum': "doc_propiedad",
        '13_Cal_es_el_otro_do' : "otro_doc", 
        '14_La_persona_duea_d': "hogar_propietario", 
        '15_La_persona_propie': "otra_propietaria",
        '16_La_persona_propie': "otra_vender", 
        '17_La_persona_propie': "otra_trasmitir", 
        '18_Tiene_derecho_a_v': "derecho_vender",
        '19_Tiene_derecho_a_t': "derecho_trasmitir", 
        '20_Cul_es_su_estado_': "estado_civil", 
        '21_En_caso_de_separa': "derecho_por_separacion",
        '22_Cul_es_la_razn_po': "razon", 
        '23_Despues_de_la_sep': "recibio_tierra", 
        '24_Cul_es_la_razn_po': "razon_no_recibirtierra",
        '25_Este_hogar_tiene_': "hogar_con_bosques", 
        '26_Es_usted_propieta': "propietaria_bosques", 
        '27_Usted_puede_acced': "acceso_bosques",
        '28_Cul_es_la_razn_po': "razon_no_bosques", 
        '29_Participa_en_espa': "participacion_manejo_rn", 
        '30__Cul_es_su_papel_': "role_participacion",
        '31_Eres_parte_de_la_': "participacion_turismo", 
        '32_Tienes_un_telfono': "tel_mobil", 
        '33__Tienes_servicio_':"internet",
        '34_Tienes_acceso_a_c': "free_internet", 
        '35_Ha_recibido_educa': "educacion_igualdad"
        }

# call rename () method
data.rename(columns=dict,
          inplace=True)

df = data.copy(deep=True)


def app():
    """
    Main app that streamlit will render.
    """
    st.title("⚫ Indicadores de derecho a tierras")
    st.markdown ('---')
    st.write("El indicador 5.a.1 se centra en las tierras agrícolas, ya que constituyen un insumo fundamental en países de ingresos bajos y medianos en los que, con frecuencia, las estrategias de reducción de la pobreza y desarrollose basan en el sector agrícola")
 
   
    # DEFINE FUNTIONS

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


    indicator = st.selectbox("SELECCIONE UN INDICADOR",
        ("Total hogares agricolas",
         'Indicador 5.a.1(a). Porcentaje de personas con propiedad o derechos seguros sobre tierras agrícolas',
         'Indicador 5.a.1.(b). Proporción de mujeres entre los propietarios o titulares de derechos de tierras agrícolas',
         
        ))     

    #STATE AN ERROR AND DON'T SHOW THE KEYERROR 
    if not indicator :
        st.error(" ⚠️ Por favor seleccione un indicador")
        st.stop()

        # Interactive visualization 
    #if indicator == "Total hogares agricolas": 
            















    with st.expander("ℹ️ Indicador 5.a.1 INFO"):
        st.markdown(""" El 5.a.1 solo se refiere a: 
            🟢 La población adulta agrícola como Todos los adultos que viven en hogares agrícolas, esto es,hogares que hayan trabajado la tierra con fines agrícolas o que hayan criado o cuidado ganado en los últimos 12 meses, con independencia del destino final de la producción. Cabe señalar que quedarán excluidos de la población de referencia los hogares cuyos miembros participen en la agricultura solo como asalariados.
            🟢 el indicador 5.a.1 se basa en tres medidas indirectas para determinar los derechos de tenencia:
            • la posesión de un documento reconocido legalmente a nombre de la persona;
            • el derecho de la persona a vender la tierra;
            • el derecho de la persona de transmitir por herencia la tierra.

            🟢La presencia de una de las tres medidas indirectas es suficiente para definir a una persona como propietaria o titular de facto de derechos de tenencia de tierras agrícolas. La ventaja de este sistema es su aplicabilidad en
            países con distinto grado de difusión de documentos jurídicamente vinculantes.

            More info in: (https://www.fao.org/3/ca4885es/CA4885ES.pdf)""")

                          