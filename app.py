import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime

# ======================================================
# CONFIGURACIÓN
# ======================================================

st.set_page_config(
    page_title="Instrumento de Ponderación",
    layout="wide"
)

st.title(
"🧬 Instrumento de Ponderación de Variables y Criterios de Severidad"
)

EXCEL_FILE="respuestas_ponderacion.xlsx"

# ======================================================
# FUNCIONES
# ======================================================

def normalizar_pesos(diccionario):

    suma=sum(diccionario.values())

    if suma==0:
        return None

    normalizados={

        k:round(
            (v/suma)*100,
            2
        )

        for k,v in diccionario.items()

    }

    return normalizados


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
"1️⃣ Información evaluador"
)

col1,col2=st.columns(2)

with col1:

    evaluador=st.text_input(
        "Nombre"
    )

    dependencia=st.text_input(
        "Dependencia"
    )

with col2:

    cargo=st.text_input(
        "Cargo"
    )

    experiencia=st.selectbox(
        "Experiencia",
        [
            "0-2 años",
            "3-5 años",
            "6-10 años",
            ">10 años"
        ]
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

La información recopilada será utilizada como insumo metodológico para apoyar
la construcción y fortalecimiento de matrices de riesgo y futuros modelos
probabilísticos orientados a la priorización y evaluación basada en riesgo.

Las respuestas obtenidas no constituyen una evaluación individual de un
producto o vacuna específica; corresponden a un ejercicio de percepción y
consenso experto

""")


# ======================================================
# VARIABLES GENERALES
# ======================================================

st.header(
"2️⃣ Variables Generales"
)

VG={

"A":"Registro suspendido",

"B":"Revisión de oficio",

"C":"Alertas sanitarias",

"D":"Eventos adversos graves",

"E":"Responsabilidad sanitaria",

"F":"Desabastecimiento"

}

pesosVG={}

for letra,pregunta in VG.items():

    st.subheader(letra)

    st.write(pregunta)

    peso=st.number_input(

        "Peso (%)",

        min_value=0.0,

        max_value=100.0,

        value=0.0,

        key=f"VG{letra}"

    )

    pesosVG[letra]=peso


normalVG=normalizar_pesos(
    pesosVG
)

if normalVG:

    st.subheader(
    "⚖️ Variables Generales normalizadas"
    )

    st.dataframe(
        pd.DataFrame({

            "Variable":
            list(
                normalVG.keys()
            ),

            "Peso":
            list(
                normalVG.values()
            )

        })
    )


# ======================================================
# VARIABLES ESPECÍFICAS
# ======================================================

st.header(
"3️⃣ Variables Específicas"
)

VE={

"A":"Condiciones almacenamiento",

"B":"Vida útil",

"C":"Artes e inserto",

"D":"Gestión riesgo",

"E":"BPM",

"F":"Liberación lotes"

}

pesosVE={}

for letra,pregunta in VE.items():

    st.subheader(
        letra
    )

    st.write(
        pregunta
    )

    peso=st.number_input(

        "Peso (%)",

        min_value=0.0,

        max_value=100.0,

        value=0.0,

        key=f"VE{letra}"

    )

    pesosVE[letra]=peso


normalVE=normalizar_pesos(
    pesosVE
)

if normalVE:

    st.subheader(
    "⚖️ Variables Específicas normalizadas"
    )

    st.dataframe(

        pd.DataFrame({

            "Variable":
            list(
                normalVE.keys()
            ),

            "Peso":
            list(
                normalVE.values()
            )

        })

    )


# ======================================================
# CRITERIOS SEVERIDAD
# ======================================================

st.header(
"4️⃣ Criterios de Severidad"
)

criterios={

"Naturaleza biológica":[

"¿La vacuna contiene microorganismos vivos capaces de replicarse?",

"¿Es vacuna con subunidades proteicas?"
],

"Característica antigénica":[

"¿La vacuna contiene uno o múltiples antígenos?"
],

"Vía administración":[

"¿Cuál es la vía administración?",

"¿Requiere reconstitución?"
],

"Dosis":[

"¿Es dosis única o multidosis?"
],

"Grupo etario":[

"¿Población inmune comprometida?"
],

"Tipo adyuvante":[

"¿Adyuvante con riesgos reconocidos?"
],

"Tipo excipientes":[

"¿Excipientes con potencial toxicidad?"
],

"Calidad":[

"¿Consistencia lotes demostrada?"
]

}


pesosCriterios={}

dimensiones={}

contador=1

for dimension,lista in criterios.items():

    st.subheader(
        dimension
    )

    dimensiones[
        dimension
    ]=0

    for criterio in lista:

        st.write(
            criterio
        )

        peso=st.number_input(

            "Peso (%)",

            min_value=0.0,

            max_value=100.0,

            value=0.0,

            key=f"criterio{contador}"

        )

        pesosCriterios[
            criterio
        ]=peso

        contador+=1


normalCrit=normalizar_pesos(
    pesosCriterios
)

if normalCrit:

    st.subheader(
    "⚖️ Criterios normalizados"
    )

    tablaCrit=pd.DataFrame({

        "Criterio":
        list(
            normalCrit.keys()
        ),

        "Peso":
        list(
            normalCrit.values()
        )

    })

    st.dataframe(
        tablaCrit,
        use_container_width=True
    )


    for dimension,lista in criterios.items():

        total=0

        for criterio in lista:

            total+=normalCrit[
                criterio
            ]

        dimensiones[
            dimension
        ]=round(
            total,
            2
        )


    st.subheader(
    "📊 Peso acumulado por dimensión"
    )

    tablaDim=pd.DataFrame({

        "Dimensión":
        list(
            dimensiones.keys()
        ),

        "Peso":
        list(
            dimensiones.values()
        )

    })

    st.dataframe(
        tablaDim,
        use_container_width=True
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
        datetime.now(),

        "evaluador":
        evaluador,

        "dependencia":
        dependencia,

        "cargo":
        cargo,

        "experiencia":
        experiencia

    }


    if normalVG:

        registro.update(normalVG)

    if normalVE:

        registro.update(normalVE)

    if normalCrit:

        registro.update(normalCrit)

    registro.update(
        dimensiones
    )

    df=pd.DataFrame(
        [registro]
    )

    guardar_respuesta(
        df
    )

    st.success(
        "✅ Evaluación almacenada correctamente"
    )

