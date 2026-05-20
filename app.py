import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path

st.set_page_config(
    page_title="Instrumento de Ponderación",
    layout="wide"
)

st.title("🧬 Instrumento de Ponderación de Variables y Criterios de Severidad")
st.markdown(
"""
Objetivo:
Recopilar la apreciación de expertos respecto a la importancia relativa de
variables generales, variables específicas y criterios de severidad.
"""
)

EXCEL_FILE="respuestas_ponderacion.xlsx"

# =====================================
# FUNCIONES
# =====================================

def guardar_respuesta(df):

    path=Path(EXCEL_FILE)

    if path.exists():

        existente=pd.read_excel(EXCEL_FILE)

        final=pd.concat(
            [existente,df],
            ignore_index=True
        )

    else:

        final=df

    final.to_excel(
        EXCEL_FILE,
        index=False
    )


# =====================================
# INFORMACIÓN EVALUADOR
# =====================================

st.header("1️⃣ Información del evaluador")

col1,col2=st.columns(2)

with col1:

    evaluador=st.text_input(
        "Nombre evaluador"
    )

    dependencia=st.text_input(
        "Dependencia"
    )

with col2:

    cargo=st.text_input(
        "Cargo"
    )

    experiencia=st.selectbox(
        "Experiencia en vacunas",
        [
            "0-2 años",
            "3-5 años",
            "6-10 años",
            ">10 años"
        ]
    )


respuestas={}

# =====================================
# VARIABLES GENERALES
# =====================================

st.header("2️⃣ Variables Generales")

VG={

"VG1":"¿El registro sanitario ha sido suspendido en los últimos tres años?",

"VG2":"¿El registro sanitario ha sido llamado a revisión de oficio en los últimos tres años?",

"VG3":"¿El registro sanitario ha tenido alertas sanitarias en los últimos tres años?",

"VG4":"¿El registro sanitario ha tenido eventos adversos graves en los últimos tres años?",

"VG5":"¿El medicamento ha tenido procesos en responsabilidad sanitaria?",

"VG6":"¿El medicamento presentó riesgo de desabastecimiento?"
}


for codigo,pregunta in VG.items():

    st.subheader(codigo)

    st.write(pregunta)

    with st.expander("📘 Definición"):

        st.write(
        "Definición pendiente por validar con Michael."
        )

    importancia=st.slider(
        "Nivel de importancia",
        1,
        5,
        3,
        help="""
        1=Muy baja
        2=Baja
        3=Moderada
        4=Alta
        5=Muy alta
        """,
        key=f"imp_{codigo}"
    )

    confianza=st.selectbox(
        "Confianza",
        [
            "Baja",
            "Media",
            "Alta"
        ],
        key=f"conf_{codigo}"
    )

    comentario=st.text_area(
        "Comentario",
        key=f"com_{codigo}"
    )

    respuestas[f"{codigo}_importancia"]=importancia
    respuestas[f"{codigo}_confianza"]=confianza
    respuestas[f"{codigo}_comentario"]=comentario


# =====================================
# VARIABLES ESPECÍFICAS
# =====================================

st.header("3️⃣ Variables Específicas")

VE={

"VE1":"Condiciones almacenamiento verificadas",

"VE2":"Vida útil coincide con artes y certificados",

"VE3":"Artes e inserto coinciden con RS",

"VE4":"Existe informe gestión riesgo",

"VE5":"Fabricantes con BPM vigente",

"VE6":"Lotes NO liberados por INVIMA"

}

for codigo,pregunta in VE.items():

    st.subheader(codigo)

    st.write(pregunta)

    with st.expander("📘 Definición"):

        st.write(
        "Definición pendiente por validar."
        )

    importancia=st.slider(
        "Nivel importancia",
        1,
        5,
        3,
        key=f"ve_{codigo}"
    )

    confianza=st.selectbox(
        "Confianza",
        [
            "Baja",
            "Media",
            "Alta"
        ],
        key=f"confve_{codigo}"
    )

    comentario=st.text_area(
        "Comentario",
        key=f"comve_{codigo}"
    )

    respuestas[f"{codigo}_importancia"]=importancia
    respuestas[f"{codigo}_confianza"]=confianza
    respuestas[f"{codigo}_comentario"]=comentario


# =====================================
# CRITERIOS SEVERIDAD
# =====================================

st.header("4️⃣ Criterios de Severidad")

criterios=[

"Naturaleza biológica",
"Vía administración",
"Dosis",
"Grupo etario",
"Tipo adyuvante",
"Tipo excipientes",
"Innovación científica",
"Condiciones almacenamiento",
"Calidad expediente"

]

for criterio in criterios:

    st.subheader(criterio)

    with st.expander("📘 Definición"):

        st.write(
        "Definición pendiente por validar."
        )

    importancia=st.slider(
        "Importancia",
        1,
        5,
        3,
        key=criterio
    )

    confianza=st.selectbox(
        "Confianza",
        [
            "Baja",
            "Media",
            "Alta"
        ],
        key=f"conf_{criterio}"
    )

    respuestas[f"{criterio}_importancia"]=importancia
    respuestas[f"{criterio}_confianza"]=confianza


# =====================================
# GUARDAR
# =====================================

st.markdown("---")

if st.button("💾 Guardar evaluación"):

    registro={

        "fecha":datetime.now(),
        "evaluador":evaluador,
        "dependencia":dependencia,
        "cargo":cargo,
        "experiencia":experiencia

    }

    registro.update(respuestas)

    df=pd.DataFrame([registro])

    guardar_respuesta(df)

    st.success(
    "✅ Respuesta almacenada"
    )
