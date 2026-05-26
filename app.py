import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime
import requests

# ======================================================
# CONFIGURACIÓN
# ======================================================

st.set_page_config(
    page_title="Instrumento IVC SOA",
    layout="wide"
)

st.title(
"🧬 Instrumento de ponderación de variables del Modelo IVC SOA y criterios de severidad del riesgo"
)

EXCEL_FILE="respuestas_ponderacion.xlsx"

# WEBHOOK POWER AUTOMATE
WEBHOOK="PEGA_AQUI_TU_URL_COMPLETA"


# ======================================================
# FUNCIONES
# ======================================================

def normalizar_pesos(diccionario):

    suma=sum(diccionario.values())

    if suma==0:
        return None

    return {

        k:round(
            (v/suma)*100,
            2
        )

        for k,v in diccionario.items()

    }


def guardar_respuesta_local(df):

    archivo=Path(EXCEL_FILE)

    if archivo.exists():

        viejo=pd.read_excel(
            EXCEL_FILE
        )

        nuevo=pd.concat(
            [viejo,df],
            ignore_index=True
        )

    else:

        nuevo=df

    nuevo.to_excel(
        EXCEL_FILE,
        index=False
    )


def enviar_sharepoint(registro):

    try:

        headers={

            "Content-Type":"application/json"

        }

        response=requests.post(

            WEBHOOK,
            json=registro,
            headers=headers,
            timeout=30

        )

        return {

            "codigo":response.status_code,

            "detalle":response.text

        }

    except Exception as e:

        return {

            "codigo":"ERROR",

            "detalle":str(e)

        }



# ======================================================
# EVALUADOR
# ======================================================

st.header(
"1️⃣ Información del evaluador"
)

col1,col2=st.columns(2)

with col1:

    evaluador=st.text_input(
        "Nombre"
    )

with col2:

    dependencia=st.text_input(
        "Dependencia / Cargo"
    )


# ======================================================
# FINALIDAD
# ======================================================

st.header(
"📘 Finalidad"
)

st.info("""

Este instrumento tiene como finalidad recopilar la apreciación y experiencia
de expertos respecto a la importancia relativa de variables generales,
variables específicas y criterios de severidad asociados a vacunas.

La información recopilada servirá para construcción y validación de modelos
de riesgo y priorización basados en riesgo.

""")


# ======================================================
# VARIABLES GENERALES
# ======================================================

st.header(
"2️⃣ Variables generales"
)

VG={

"A":"¿El registro sanitario ha sido suspendido en los últimos tres años?",

"B":"¿El registro sanitario ha sido llamado a revisión de oficio en los últimos tres años?",

"C":"¿El registro sanitario ha tenido alertas sanitarias en los últimos tres años?",

"D":"¿El registro sanitario ha tenido eventos adversos graves en los últimos tres años?",

"E":"¿El medicamento ha tenido o tiene algún proceso en Responsabilidad Sanitaria en los últimos tres años?",

"F":"¿El medicamento presentó riesgo de desabastecimiento en los últimos tres años?"

}

pesosVG={}

for letra,pregunta in VG.items():

    st.subheader(letra)

    st.write(pregunta)

    pesosVG[letra]=st.number_input(

        "Peso (%)",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        key=f"VG_{letra}"

    )

normalVG=normalizar_pesos(
    pesosVG
)


# ======================================================
# VARIABLES ESPECÍFICAS
# ======================================================

st.header(
"3️⃣ Variables específicas"
)

VE={

"A":"Las condiciones de almacenamiento del medicamento en el país han sido verificadas en los últimos tres años?",

"B":"En actividades de IVC se pudo constatar la vida útil reportada?",

"C":"Las artes e inserto corresponden con el RS?",

"D":"Existe informe análisis y gestión riesgo actualizado?",

"E":"Fabricantes y acondicionadores con BPM vigente?",

"F":"Algún lote NO fue liberado por INVIMA?"

}

pesosVE={}

for letra,pregunta in VE.items():

    st.subheader(letra)

    st.write(pregunta)

    pesosVE[letra]=st.number_input(

        "Peso (%)",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        key=f"VE_{letra}"

    )

normalVE=normalizar_pesos(
    pesosVE
)


# ======================================================
# SEVERIDAD
# ======================================================

st.header(
"4️⃣ Severidad"
)

SEV={

"A":"Naturaleza biológica / Característica antigénica",

"B":"Vía de administración",

"C":"Dosis",

"D":"Grupo etario",

"E":"Tipo de adyuvante",

"F":"Tipo de excipientes o aditivos",

"G":"Innovación científica",

"H":"Condiciones de almacenamiento",

"I":"Calidad del expediente"

}

pesosSEV={}

for letra,criterio in SEV.items():

    st.subheader(letra)

    st.write(criterio)

    pesosSEV[letra]=st.number_input(

        "Peso (%)",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        key=f"SEV_{letra}"

    )

normalSEV=normalizar_pesos(
    pesosSEV
)


# ======================================================
# GUARDAR
# ======================================================

st.markdown("---")

if st.button(
"💾 Guardar evaluación"
):

    registro={

        "fecha":
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "evaluador":
        evaluador,

        "dependencia":
        dependencia

    }

    if normalVG:

        for k,v in normalVG.items():

            registro[f"VG_{k}"]=v


    if normalVE:

        for k,v in normalVE.items():

            registro[f"VE_{k}"]=v


    if normalSEV:

        for k,v in normalSEV.items():

            registro[f"SEV_{k}"]=v


    df=pd.DataFrame(
        [registro]
    )

    guardar_respuesta_local(
        df
    )


    resultado=enviar_sharepoint(
        registro
    )


    if resultado["codigo"]==200:

        st.success(
            "✅ Guardado local y enviado a SharePoint"
        )

    else:

        st.warning(
            f"""
⚠ Guardado local correcto

Código:
{resultado['codigo']}

Detalle:
{resultado['detalle']}
"""
        )
