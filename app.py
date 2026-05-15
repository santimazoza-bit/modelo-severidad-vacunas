import streamlit as st
import pandas as pd
from datetime import datetime
from openpyxl import load_workbook
from pathlib import Path

# =====================================
# CONFIGURACIÓN GENERAL
# =====================================

st.set_page_config(
    page_title="Sistema de Evaluación de Severidad - Vacunas",
    layout="wide"
)

st.title("🧬 Sistema de Evaluación de Severidad y Riesgo Regulatorio")
st.markdown("### Modelo probabilístico basado en percepción experta")

# =====================================
# ARCHIVO DE RESPUESTAS
# =====================================

EXCEL_FILE = "respuestas_evaluacion_vacunas.xlsx"

# =====================================
# FUNCIONES
# =====================================

def calcular_score(respuestas):
    
    score = 0
    peso_total = 0

    pesos = {
        "vg": 0.20,
        "ve": 0.35,
        "severidad": 0.45
    }

    # VARIABLES GENERALES
    vg_scores = []
    for i in range(1, 7):
        vg_scores.append(respuestas.get(f"vg{i}_impacto", 0))

    promedio_vg = sum(vg_scores) / len(vg_scores)

    # VARIABLES ESPECÍFICAS
    ve_scores = []
    for i in range(1, 7):
        ve_scores.append(respuestas.get(f"ve{i}_impacto", 0))

    promedio_ve = sum(ve_scores) / len(ve_scores)

    # DIMENSIONES DE SEVERIDAD
    sev_scores = []

    dimensiones = [
        "naturaleza_biologica",
        "via_administracion",
        "dosis",
        "grupo_etario",
        "adyuvante",
        "excipientes",
        "innovacion",
        "almacenamiento",
        "calidad_expediente"
    ]

    for dim in dimensiones:
        sev_scores.append(respuestas.get(dim, 0))

    promedio_severidad = sum(sev_scores) / len(sev_scores)

    score = (
        promedio_vg * pesos["vg"] +
        promedio_ve * pesos["ve"] +
        promedio_severidad * pesos["severidad"]
    ) * 20

    return round(score, 2)


def clasificar_riesgo(score):

    if score <= 20:
        return "BAJO 🟢"
    elif score <= 40:
        return "MODERADO 🟡"
    elif score <= 60:
        return "ALTO 🟠"
    elif score <= 80:
        return "MUY ALTO 🔴"
    else:
        return "CRÍTICO ⚫"


def guardar_respuesta(dataframe):

    path = Path(EXCEL_FILE)

    if path.exists():
        existing_df = pd.read_excel(EXCEL_FILE)
        final_df = pd.concat([existing_df, dataframe], ignore_index=True)
    else:
        final_df = dataframe

    final_df.to_excel(EXCEL_FILE, index=False)


# =====================================
# INFORMACIÓN EVALUADOR
# =====================================

st.header("1️⃣ Información del Evaluador")

col1, col2 = st.columns(2)

with col1:
    evaluador = st.text_input("Nombre del evaluador")
    dependencia = st.selectbox(
        "Dependencia",
        [
            "Registros sanitarios",
            "Farmacovigilancia",
            "IVC",
            "Calidad",
            "Laboratorio",
            "Comisión revisora",
            "Otro"
        ]
    )

with col2:
    cargo = st.text_input("Cargo")
    experiencia = st.selectbox(
        "Experiencia en vacunas",
        [
            "0-2 años",
            "3-5 años",
            "6-10 años",
            ">10 años"
        ]
    )

# =====================================
# INFORMACIÓN PRODUCTO
# =====================================

st.header("2️⃣ Información del Producto")

col1, col2 = st.columns(2)

with col1:
    vacuna = st.text_input("Nombre de la vacuna")
    expediente = st.text_input("Expediente / Registro sanitario")
    titular = st.text_input("Titular")

with col2:
    tecnologia = st.selectbox(
        "Tecnología vacuna",
        [
            "ARN mensajero",
            "Vector viral",
            "Virus vivo atenuado",
            "Inactivada",
            "Recombinante",
            "Conjugada",
            "Otra"
        ]
    )

    via = st.selectbox(
        "Vía administración",
        [
            "Intramuscular",
            "Subcutánea",
            "Intradérmica",
            "Oral",
            "Intranasal"
        ]
    )

# =====================================
# VARIABLES GENERALES
# =====================================

st.header("3️⃣ Variables Generales")

variables_generales = {
    "VG1": "¿El registro sanitario ha sido suspendido en los últimos 3 años?",
    "VG2": "¿Ha sido llamado a revisión de oficio?",
    "VG3": "¿Ha tenido alertas sanitarias?",
    "VG4": "¿Ha tenido eventos adversos graves?",
    "VG5": "¿Tiene procesos en responsabilidad sanitaria?",
    "VG6": "¿Presentó riesgo de desabastecimiento?"
}

respuestas = {}

for idx, (codigo, pregunta) in enumerate(variables_generales.items(), start=1):

    st.subheader(codigo)
    st.write(pregunta)

    col1, col2, col3 = st.columns(3)

    with col1:
        respuesta = st.radio(
            f"Respuesta {codigo}",
            ["Sí", "No", "No aplica"],
            key=f"resp_{codigo}"
        )

    with col2:
        impacto = st.slider(
            f"Impacto percibido {codigo}",
            1,
            5,
            3,
            key=f"impacto_{codigo}"
        )

    with col3:
        confianza = st.selectbox(
            f"Confianza {codigo}",
            ["Baja", "Media", "Alta"],
            key=f"conf_{codigo}"
        )

    justificacion = st.text_area(
        f"Justificación técnica {codigo}",
        key=f"just_{codigo}"
    )

    respuestas[f"vg{idx}_respuesta"] = respuesta
    respuestas[f"vg{idx}_impacto"] = impacto
    respuestas[f"vg{idx}_confianza"] = confianza
    respuestas[f"vg{idx}_justificacion"] = justificacion

# =====================================
# VARIABLES ESPECÍFICAS
# =====================================

st.header("4️⃣ Variables Específicas")

variables_especificas = {
    "VE1": "Condiciones almacenamiento verificadas",
    "VE2": "Vida útil coincide con artes y certificados",
    "VE3": "Artes e inserto coinciden con RS aprobado",
    "VE4": "Existe gestión formal de riesgo",
    "VE5": "Fabricantes cuentan con BPM vigente",
    "VE6": "Algún lote NO fue liberado por INVIMA"
}

for idx, (codigo, pregunta) in enumerate(variables_especificas.items(), start=1):

    st.subheader(codigo)
    st.write(pregunta)

    col1, col2, col3 = st.columns(3)

    with col1:
        respuesta = st.radio(
            f"Respuesta {codigo}",
            ["Sí", "No", "Parcial"],
            key=f"resp_ve_{codigo}"
        )

    with col2:
        impacto = st.slider(
            f"Severidad percibida {codigo}",
            1,
            5,
            3,
            key=f"impacto_ve_{codigo}"
        )

    with col3:
        confianza = st.selectbox(
            f"Confianza {codigo}",
            ["Baja", "Media", "Alta"],
            key=f"conf_ve_{codigo}"
        )

    justificacion = st.text_area(
        f"Justificación técnica {codigo}",
        key=f"just_ve_{codigo}"
    )

    respuestas[f"ve{idx}_respuesta"] = respuesta
    respuestas[f"ve{idx}_impacto"] = impacto
    respuestas[f"ve{idx}_confianza"] = confianza
    respuestas[f"ve{idx}_justificacion"] = justificacion

# =====================================
# DIMENSIONES DE SEVERIDAD
# =====================================

st.header("5️⃣ Dimensiones de Severidad")

st.markdown("### Califique cada dimensión según la severidad percibida")

severidades = {
    "naturaleza_biologica": "Naturaleza biológica / característica antigénica",
    "via_administracion": "Vía de administración",
    "dosis": "Dosis",
    "grupo_etario": "Grupo etario",
    "adyuvante": "Tipo de adyuvante",
    "excipientes": "Tipo de excipientes o aditivos",
    "innovacion": "Innovación científica",
    "almacenamiento": "Condiciones de almacenamiento",
    "calidad_expediente": "Calidad del expediente"
}

for key, label in severidades.items():

    valor = st.slider(
        label,
        1,
        5,
        3,
        key=key
    )

    respuestas[key] = valor

# =====================================
# PONDERACIÓN EXPERTA
# =====================================

st.header("6️⃣ Ponderación Experta")

st.markdown(
    "Distribuya importancia relativa a cada dimensión. El sistema normalizará automáticamente los pesos para que sumen 100%."
)

col1, col2, col3 = st.columns(3)

with col1:
    peso_naturaleza = st.number_input(
        "Naturaleza biológica",
        0,
        100,
        20
    )

    peso_via = st.number_input(
        "Vía administración",
        0,
        100,
        10
    )

    peso_dosis = st.number_input(
        "Dosis",
        0,
        100,
        10
    )

with col2:
    peso_grupo = st.number_input(
        "Grupo etario",
        0,
        100,
        15
    )

    peso_adyuvante = st.number_input(
        "Adyuvante",
        0,
        100,
        10
    )

    peso_excipientes = st.number_input(
        "Excipientes",
        0,
        100,
        10
    )

with col3:
    peso_innovacion = st.number_input(
        "Innovación",
        0,
        100,
        15
    )

    peso_almacenamiento = st.number_input(
        "Almacenamiento",
        0,
        100,
        5
    )

    peso_expediente = st.number_input(
        "Calidad expediente",
        0,
        100,
        5
    )

# =====================================
# NORMALIZACIÓN AUTOMÁTICA DE PESOS
# =====================================

pesos_originales = {
    "Naturaleza biológica": peso_naturaleza,
    "Vía administración": peso_via,
    "Dosis": peso_dosis,
    "Grupo etario": peso_grupo,
    "Adyuvante": peso_adyuvante,
    "Excipientes": peso_excipientes,
    "Innovación": peso_innovacion,
    "Almacenamiento": peso_almacenamiento,
    "Calidad expediente": peso_expediente
}

suma_pesos = sum(pesos_originales.values())

st.markdown("---")
st.subheader("⚖️ Normalización automática de pesos")

if suma_pesos == 0:
    st.error("⚠️ La suma de ponderaciones no puede ser 0")
    pesos_normalizados = {}
else:

    pesos_normalizados = {
        k: round((v / suma_pesos) * 100, 2)
        for k, v in pesos_originales.items()
    }

    st.info(f"Suma ingresada por el evaluador: {suma_pesos}")

    st.markdown("### Pesos normalizados automáticamente")

    df_pesos = pd.DataFrame({
        "Dimensión": list(pesos_normalizados.keys()),
        "Peso Normalizado (%)": list(pesos_normalizados.values())
    })

    st.dataframe(df_pesos, use_container_width=True)

    st.success(
        "✅ Los pesos fueron ajustados automáticamente para sumar 100%"
    )

# =====================================
# REGLAS DE DECISIÓN
# =====================================

st.header("7️⃣ Reglas de Decisión")

criterios_criticos = st.multiselect(
    "Seleccione criterios que aumenten automáticamente la criticidad",
    [
        "Eventos adversos graves",
        "Población neonatal",
        "Tecnología novedosa",
        "Fallas cadena frío",
        "Alertas sanitarias",
        "Riesgo desabastecimiento",
        "Deficiencias calidad expediente"
    ]
)

comentarios_finales = st.text_area(
    "Comentarios finales del evaluador"
)

# =====================================
# RESULTADO FINAL
# =====================================

st.header("8️⃣ Resultado Final")

score = calcular_score(respuestas)
clasificacion = clasificar_riesgo(score)

st.metric(
    "Score Final",
    score
)

st.metric(
    "Clasificación",
    clasificacion
)

# =====================================
# GUARDAR
# =====================================

if st.button("💾 Guardar Evaluación"):

    registro = {
        "fecha": datetime.now(),
        "evaluador": evaluador,
        "dependencia": dependencia,
        "cargo": cargo,
        "experiencia": experiencia,
        "vacuna": vacuna,
        "expediente": expediente,
        "titular": titular,
        "tecnologia": tecnologia,
        "via": via,
        "score": score,
        "clasificacion": clasificacion,
        "criterios_criticos": ", ".join(criterios_criticos),
        "comentarios": comentarios_finales
    }

    registro.update(respuestas)

    df = pd.DataFrame([registro])

    guardar_respuesta(df)

    st.success("✅ Evaluación guardada correctamente")

    st.download_button(
        label="📥 Descargar respuestas Excel",
        data=open(EXCEL_FILE, "rb"),
        file_name=EXCEL_FILE,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# =====================================
# FOOTER
# =====================================

st.markdown("---")
st.markdown(
    "Sistema de evaluación basado en riesgo y percepción experta"
)
