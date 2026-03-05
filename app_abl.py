import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import os

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Knowledgism ABL Profiler - By Jose Antonio Camacho",
    page_icon="favicon.png",
    layout="centered"
)

# --- 2. INICIALIZACIÓN DE ESTADO ---
if 'paso' not in st.session_state:
    st.session_state.paso = 0
if 'respuestas' not in st.session_state:
    st.session_state.respuestas = {i: "Tal vez" for i in range(1, 75)}
if 'finalizado' not in st.session_state:
    st.session_state.finalizado = False

# --- 3. IDENTIDAD VISUAL ---
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)

st.divider()

col_m1, col_m2 = st.columns([0.2, 0.8])
with col_m1:
    if os.path.exists("logo_mini.png"):
        st.image("logo_mini.png", width=70)
    else:
        st.write("## 🚀")

with col_m2:
    st.markdown("<h1 style='margin-top: -5px; padding-bottom: 0;'>Perfil ABL</h1>", unsafe_allow_html=True)
    st.markdown("<p style='margin-top: -10px;'>Knowledgism ABL Profiler <b>By Jose Antonio Camacho (veco)</b></p>", unsafe_allow_html=True)
    st.markdown("<p style='color: gray; font-style: italic; margin-top: -15px; font-size: 0.8em;'>Análisis Profesional de Capacidades</p>", unsafe_allow_html=True)

# --- 4. DICCIONARIO DE PREGUNTAS ---
PREGUNTAS_ES = {
    1: "¿Se siente bien consigo mismo?", 2: "¿Se le ocurren cosas para hacer?",
    3: "Si encontrara una billetera, ¿la devolvería?", 4: "¿Recuerda fácilmente lo que lee?",
    5: "¿Está esperando a que algo ocurra?", 6: "¿Es importante su honor personal?",
    7: "¿Un problema afecta a toda su relación?", 8: "¿Los gustos personales influyen en sus decisiones?",
    9: "¿Transmite fácilmente las malas noticias?", 10: "¿Le resulta difícil mantener su posición?",
    11: "¿Hace cosas que no quiere hacer?", 12: "¿Crea sus propias reglas en lugar de seguir las establecidas?",
    13: "¿Es necesario a veces decir mentiras?", 14: "¿Busca palabras que no conoce?",
    15: "¿Puede iniciar actividades en su área?", 16: "¿Está bien beber alcohol?",
    17: "¿Prefiere seguir las reglas existentes?", 18: "¿Le resulta difícil admitir que se equivoca?",
    19: "¿Va en todas las direcciones a la vez?", 20: "¿Le resulta difícil ponerse en marcha?",
    21: "¿Es una influencia tranquila durante una crisis?", 22: "¿Se interrumpe fácilmente?",
    23: "¿Prefiere tomar el camino más fácil?", 24: "¿Pierde demasiado tiempo?",
    25: "¿Cede ante la persuasión de los demás?", 26: "¿Cree que las drogas están bien?",
    27: "¿Establece metas para usted y para otros?", 28: "Si le dieran cambio de más, ¿lo devolvería?",
    29: "¿Se cansa al leer un libro?", 30: "Si algo es importante, ¿lo lleva a cabo?",
    31: "¿Puede aceptar las críticas fácilmente?", 32: "¿Planifica sus actividades?",
    33: "¿Es usualmente sincero con los demás?", 34: "¿Tiene habilidades psíquicas?",
    35: "¿Puede lograr que otros realicen actividades con eficacia?", 36: "¿Es importante su propia paz mental?",
    37: "¿Podría llevar a cabo una meta en 6 meses?", 38: "¿Enfrenta situaciones dolorosas?",
    39: "¿Tiene una buena actitud ante la vida?", 40: "¿Prefiere no tomar decisiones?",
    41: "¿Tiende a ser descuidado y desordenado?", 42: "¿Corregiría a alguien que está equivocado?",
    43: "¿Le cuenta a la gente el último escándalo?", 44: "¿Busca el conocimiento activamente?",
    45: "¿Termina su trabajo antes de socializar?", 46: "¿Es descuidado con su salud?",
    47: "¿Tiende a posponer las cosas?", 48: "¿Retrocede ante la lucha por la verdad?",
    49: "¿Le gusta aprender sobre cosas nuevas?", 50: "¿Los demás lo mangonean?",
    51: "¿Le preocupan todavía los fracasos del pasado?", 52: "¿Se altera fácilmente?",
    53: "¿Cree que el hombre es básicamente honesto?", 54: "¿Lee libros?",
    55: "¿Se siente bien cuando otros pierden?", 56: "¿Le resulta fácil expresarse?",
    57: "¿Es usted muy, muy ambicioso?", 58: "¿Tiende a ser celoso?",
    59: "¿Prefiere quedarse con lo que ya conoce?", 60: "¿Se mantiene al tanto de los asuntos actuales?",
    61: "¿Le pone nervioso dar un discurso?", 62: "¿Sus metas se alinean con las de su círculo?",
    63: "¿Puede el carácter de alguien cambiar para mejor?", 64: "¿Tiene períodos de inactividad?",
    65: "¿Prom
