from zoneinfo import ZoneInfo
import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import requests
import gspread

from google.oauth2.service_account import Credentials

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

DATABASE="respuestas.db"
BACKUP_FILE="respuestas_backup.csv"

# ======================================================
# TELEGRAM
# ======================================================

BOT_TOKEN="8960478807:AAEuplv6kUxxMQ-MjwyPq78CkwnEn4YBBBg"

CHAT_ID="5762419749"


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

    # ==========================
    # Guardar SQLite
    # ==========================

    conn=sqlite3.connect(
        DATABASE
    )

    df.to_sql(

        "evaluaciones",

        conn,

        if_exists="append",

        index=False

    )

    conn.close()


    # ==========================
    # Backup CSV
    # ==========================

    try:

        viejo=pd.read_csv(
            BACKUP_FILE
        )

        nuevo=pd.concat(

            [viejo,df],

            ignore_index=True

        )

    except:

        nuevo=df


    nuevo.to_csv(

        BACKUP_FILE,

        index=False

    )


def enviar_telegram(registro):

    try:

        mensaje=f"""

🧬 Nueva evaluación recibida

👤 Evaluador:
{registro['evaluador']}

🏢 Dependencia:
{registro['dependencia']}

🕒 Fecha:
{registro['fecha']}

"""

        url=f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        payload={

            "chat_id":CHAT_ID,

            "text":mensaje

        }

        requests.post(
            url,
            data=payload
        )

    except:

        pass


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

Este instrumento tiene como finalidad recopilar la apreciación
y experiencia de expertos respecto a la importancia relativa
de variables generales, variables específicas y criterios
de severidad asociados a vacunas.

La información será utilizada como insumo metodológico para
el fortalecimiento de matrices de riesgo y modelos probabilísticos.

""")


# ======================================================
# VARIABLES GENERALES
# ======================================================

st.header("2️⃣ Variables generales")

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

"A":"¿Las condiciones de almacenamiento del medicamento en el país han sido verificadas en los últimos tres años?",

"B":"¿En las actividades de IVC, se pudo constatar que la vida útil concedida en el registro sanitario del producto terminado, es la reportada en las artes del material de envase y empaque, y en los certificados de Producto Terminado??",

"C":"¿Durante las acciones de IVC se encontró que las artes del material de envase y empaque y el Inserto, (si lo tiene), corresponden con las que se encuentran aprobadas  en el Registro Sanitario?",

"D":"¿El expediente contiene el Informe de análisis y gestión del riesgo del producto en donde se evalúan las etapas de fabricación, con identificación de los riesgos y sus niveles asignados, además de las estrategias de mitigación y ha sido actualizado o revisado por cada modificación presentada por el interesado, en donde la norma de referencia lo incluya como requisito?",

"E":"¿Los roles establecidos en el Registro sanitario para fabricantes y acondicionadores se encuentran respaldados por certificacion de BPM vigente nacional o internacional?",

"F":"¿En los últimos tres (3) años algún lote de la vacuna NO ha sido liberado por el INVIMA?"

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
        datetime.now(
            ZoneInfo("America/Bogota")
        ).strftime(
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

    guardar_respuesta(
        df
    )

    enviar_telegram(
        registro
    )

    st.success(
        "✅ Evaluación almacenada correctamente"
    )


# ======================================================
# DESCARGA ADMIN
# ======================================================

st.markdown("---")

st.header(
"📥 Administración"
)

clave=st.text_input(

    "Clave administrador",

    type="password"

)

if clave=="INVIMA2026":

    try:

        datos=pd.read_csv(
            BACKUP_FILE
        )

        st.success(
            f"Registros encontrados: {len(datos)}"
        )

        csv=datos.to_csv(
            index=False
        )

        st.download_button(

            label="📥 Descargar respuestas CSV",

            data=csv,

            file_name="respuestas.csv",

            mime="text/csv"

        )

    except:

        st.warning(
            "Aún no existen respuestas"
        )
