import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime

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


def guardar_respuesta(df):

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
"📘 Finalidad del instrumento"
)

st.info("""

Este instrumento tiene como finalidad recopilar la apreciación y experiencia
de expertos respecto a la importancia relativa de variables generales,
variables específicas y criterios de severidad asociados a vacunas.

La información recopilada servirá como insumo metodológico para la construcción,
fortalecimiento y validación de matrices de riesgo y modelos probabilísticos
orientados a la priorización y evaluación basada en riesgo.

Las respuestas obtenidas no constituyen una evaluación individual de un producto
o vacuna específica.

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

    st.write(
        pregunta
    )

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

if normalVG:

    st.info(
        f"Suma ingresada: {round(sum(pesosVG.values()),2)}%"
    )

    st.dataframe(

        pd.DataFrame({

            "Variable":
            list(normalVG.keys()),

            "Peso normalizado (%)":
            list(normalVG.values())

        })

    )


# ======================================================
# VARIABLES ESPECÍFICAS
# ======================================================

st.header(
"3️⃣ Variables específicas"
)

VE={

"A":"¿Las condiciones de almacenamiento del medicamento en el país han sido verificadas en los últimos tres años?",

"B":"¿En las actividades de IVC, se pudo constatar que la vida útil concedida en el registro sanitario del producto terminado, es la reportada en las artes del material de envase y empaque y en los certificados de Producto Terminado?",

"C":"¿Durante las acciones de IVC se encontró que las artes del material de envase y empaque y el inserto corresponden con las aprobadas en el Registro Sanitario?",

"D":"¿El expediente contiene el informe de análisis y gestión del riesgo actualizado?",

"E":"¿Los roles establecidos para fabricantes y acondicionadores cuentan con BPM vigente?",

"F":"¿En los últimos tres años algún lote NO ha sido liberado por INVIMA?"

}

pesosVE={}

for letra,pregunta in VE.items():

    st.subheader(
        letra
    )

    st.write(
        pregunta
    )

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

if normalVE:

    st.info(
        f"Suma ingresada: {round(sum(pesosVE.values()),2)}%"
    )

    st.dataframe(

        pd.DataFrame({

            "Variable":
            list(normalVE.keys()),

            "Peso normalizado (%)":
            list(normalVE.values())

        })

    )


# ======================================================
# SEVERIDAD
# ======================================================

st.header(
"4️⃣ Severidad"
)

SEVERIDAD={

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

pesosSeveridad={}

for letra,criterio in SEVERIDAD.items():

    st.subheader(
        letra
    )

    st.write(
        criterio
    )

    pesosSeveridad[letra]=st.number_input(

        "Peso (%)",

        min_value=0.0,

        max_value=100.0,

        value=0.0,

        key=f"SEV_{letra}"

    )


normalSeveridad=normalizar_pesos(
    pesosSeveridad
)

if normalSeveridad:

    st.info(
        f"Suma ingresada: {round(sum(pesosSeveridad.values()),2)}%"
    )

    st.dataframe(

        pd.DataFrame({

            "Criterio":
            list(normalSeveridad.keys()),

            "Peso normalizado (%)":
            list(normalSeveridad.values())

        })

    )


# ======================================================
# GUARDAR
# ======================================================

st.markdown("---")

if st.button(
"💾 Guardar evaluación"
):

    registro={

        "fecha":datetime.now(),

        "evaluador":evaluador,

        "dependencia":dependencia

    }

    if normalVG:

        for k,v in normalVG.items():

            registro[f"VG_{k}"]=v


    if normalVE:

        for k,v in normalVE.items():

            registro[f"VE_{k}"]=v


    if normalSeveridad:

        for k,v in normalSeveridad.items():

            registro[f"SEV_{k}"]=v


    df=pd.DataFrame(
        [registro]
    )

    guardar_respuesta(
        df
    )

    st.success(
        "✅ Evaluación almacenada correctamente"
    )
    

