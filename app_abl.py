import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import os

# --- Questionario ---
PREGUNTAS_ES = {
    1: "¿Se siente bien consigo mismo?",
    2: "¿Se le ocurren cosas para hacer?",
    3: "Si encontrara una billetera, ¿la devolvería?",
    4: "¿Recuerda fácilmente lo que lee?",
    5: "¿Está esperando a que algo ocurra?",
    6: "¿Es importante su honor personal?",
    7: "¿Un problema afecta a toda su relación?",
    8: "¿Los gustos personales influyen en sus decisiones?",
    9: "¿Transmite fácilmente las malas noticias?",
    10: "¿Le resulta difícil mantener su posición?",
    11: "¿Hace cosas que no quiere hacer?",
    12: "¿Crea sus propias reglas en lugar de seguir las establecidas?",
    13: "¿Es necesario a veces decir mentiras?",
    14: "¿Busca palabras que no conoce?",
    15: "¿Puede iniciar actividades en su área?",
    16: "¿Está bien beber alcohol?",
    17: "¿Prefiere seguir las reglas existentes?",
    18: "¿Le resulta difícil admitir que se equivoca?",
    19: "¿Va en todas las direcciones a la vez?",
    20: "¿Le resulta difícil ponerse en marcha?",
    21: "¿Es una influencia tranquila durante una crisis?",
    22: "¿Se interrumpe fácilmente?",
    23: "¿Prefiere tomar el camino más fácil?",
    24: "¿Pierde demasiado tiempo?",
    25: "¿Cede ante la persuasión de los demás?",
    26: "¿Cree que las drogas están bien?",
    27: "¿Establece metas para usted y para otros?",
    28: "Si le dieran cambio de más, ¿lo devolvería?",
    29: "¿Se cansa al leer un libro?",
    30: "Si algo es importante, ¿lo lleva a cabo?",
    31: "¿Puede aceptar las críticas fácilmente?",
    32: "¿Planifica sus actividades?",
    33: "¿Es usualmente sincero con los demás?",
    34: "¿Tiene habilidades psíquicas?",
    35: "¿Puede lograr que otros realicen actividades con eficacia?",
    36: "¿Es importante su propia paz mental?",
    37: "¿Podría llevar a cabo una meta en 6 meses?",
    38: "¿Enfrenta situaciones dolorosas?",
    39: "¿Tiene una buena actitud ante la vida?",
    40: "¿Prefiere no tomar decisiones?",
    41: "¿Tiende a ser descuidado y desordenado?",
    42: "¿Corregiría a alguien que está equivocado?",
    43: "¿Le cuenta a la gente el último escándalo?",
    44: "¿Busca el conocimiento activamente?",
    45: "¿Termina su trabajo antes de socializar?",
    46: "¿Es descuidado con su salud?",
    47: "¿Tiende a posponer las cosas?",
    48: "¿Retrocede ante la lucha por la verdad?",
    49: "¿Le gusta aprender sobre cosas nuevas?",
    50: "¿Los demás lo mangonean?",
    51: "¿Le preocupan todavía los fracasos del pasado?",
    52: "¿Se altera fácilmente?",
    53: "¿Cree que el hombre es básicamente honesto?",
    54: "¿Lee libros?",
    55: "¿Se siente bien cuando otros pierden?",
    56: "¿Le resulta fácil expresarse?",
    57: "¿Es usted muy, muy ambicioso?",
    58: "¿Tiende a ser celoso?",
    59: "¿Prefiere quedarse con lo que ya conoce?",
    60: "¿Se mantiene al tanto de los asuntos actuales?",
    61: "¿Le pone nervioso dar un discurso?",
    62: "¿Sus metas se alinean con las de su círculo?",
    63: "¿Puede el carácter de alguien cambiar para mejor?",
    64: "¿Tiene períodos de inactividad?",
    65: "¿Promueve a amigos por encima de las cualificaciones?",
    66: "¿Es sensible o susceptible ante muchas cosas?",
    67: "¿Dramatiza las emociones para salirse con la suya?",
    68: "¿Sus creencias influyen en sus decisiones?",
    69: "¿Se siente inquieto en entornos desordenados?",
    70: "¿Alguien lo consideraría activo?",
    71: "¿Se siente deprimido a menudo?",
    72: "¿Es difícil de complacer?",
    73: "¿Cree que la gente tiene más puntos malos que buenos?",
    74: "¿Comete a menudo errores por descuido?"
}


# Preguntas con lógica inversa (responder "Sí" resta puntos)
PREGUNTAS_NEGATIVAS = [5, 7, 8, 9, 10, 11, 13, 16, 18, 19, 20, 22, 23, 24, 25, 26, 29, 40, 41, 43, 46, 47, 48, 50, 51, 52, 55, 58, 61, 64, 65, 66, 67, 68, 71, 72, 73, 74]

CATEGORIAS = {
    "Percepción (Tú)": range(1, 14),
    "Metas / Querer": range(14, 26),
    "Intención / Sueño": range(26, 38),
    "Visión": range(38, 50),
    "Mente": range(50, 62),
    "Cuerpo": range(62, 75)
}

st.set_page_config(page_title="Knowledgism ABL Profiler", layout="wide")
st.title("📊 Perfil de Capacidades y Estado de Ánimo (ABL)")
st.markdown("Created By **José Antonio Camacho**. [veco] Responde con honestidad para ver tu zona de atención.")

# --- SIDEBAR: DATOS DEL SUJETO ---
with st.sidebar:
    st.header("Datos del Evaluado")
    nombre = st.text_input("Nombre Completo", placeholder="Ej: Juan Pérez")
    if st.button("Limpiar Test"):
        st.rerun()

# --- CUERPO DEL TEST ---
respuestas = {}
tabs = st.tabs(list(CATEGORIAS.keys()))

for i, (cat, rango) in enumerate(CATEGORIAS.items()):
    with tabs[i]:
        st.subheader(f"Sección: {cat}")
        for q_id in rango:
            col1, col2 = st.columns([0.7, 0.3])
            with col1:
                st.write(f"**{q_id}.** {PREGUNTAS_ES[q_id]}")
            with col2:
                respuestas[q_id] = st.radio(f"R{q_id}", ["Sí", "Tal vez", "No"], index=1, key=f"q_{q_id}", label_visibility="collapsed")

# --- PROCESAMIENTO ---
if st.button("GENERAR RESULTADOS Y GUARDAR"):
    if not nombre:
        st.error("Por favor, ingresa un nombre antes de continuar.")
    else:
        scores_finales = {}
        for cat, rango in CATEGORIAS.items():
            puntos = 0
            for q_id in rango:
                val = 1 if respuestas[q_id] == "Sí" else (-1 if respuestas[q_id] == "No" else 0)
                if q_id in PREGUNTAS_NEGATIVAS: val *= -1
                puntos += val
            
            # Normalización 0-100
            max_p = len(rango)
            score_norm = ((puntos + max_p) / (2 * max_p)) * 100
            scores_finales[cat] = score_norm

        # --- MOSTRAR GRÁFICA ---
        st.divider()
        col_graf, col_info = st.columns([0.6, 0.4])
        
        with col_graf:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.axhspan(66, 100, color='#2ecc71', alpha=0.3) # Verde
            ax.axhspan(33, 66, color='#f1c40f', alpha=0.3) # Amarillo
            ax.axhspan(0, 33, color='#e74c3c', alpha=0.3)  # Rojo
            
            ejes = list(scores_finales.keys())
            valores = list(scores_finales.values())
            
            ax.plot(ejes, valores, marker='o', color='black', linewidth=3)
            ax.set_ylim(0, 100)
            ax.set_title(f"Perfil ABL - {nombre}")
            st.pyplot(fig)

        with col_info:
            st.success(f"¡Test de {nombre} procesado!")
            for c, s in scores_finales.items():
                zona = "VERDE" if s > 66 else ("AMARILLA" if s > 33 else "ROJA")
                st.write(f"**{c}:** {int(s)}% - Zona {zona}")

        # --- GUARDAR EN CSV ---
        filename = "historial_streamlit_abl.csv"
        registro = {"Nombre": nombre, "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M")}
        registro.update({k: round(v, 2) for k, v in scores_finales.items()})
        
        df_new = pd.DataFrame([registro])
        if not os.path.isfile(filename):
            df_new.to_csv(filename, index=False)
        else:
            df_new.to_csv(filename, mode='a', header=False, index=False)
        
        st.info(f"Datos guardados en `{filename}`")
