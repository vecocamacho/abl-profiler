import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import os
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# --- 1. CONFIGURACIÓN DE PÁGINA (Debe ser lo primero) ---
st.set_page_config(
    page_title="Knowledgism ABL Profiler - By Jose Antonio Camacho",
    page_icon="favicon.png",
    layout="centered"
)

# --- 2. FUNCIÓN DE CONEXIÓN A GOOGLE SHEETS ---
def guardar_en_sheets(fila):
    try:
        # Los permisos necesarios para Sheets
        scope = ["https://www.googleapis.com/auth/spreadsheets"]
        # Cargamos credenciales desde los Secrets de Streamlit (formato TOML)
        creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
        client = gspread.authorize(creds)
        # Se abre el documento Resultados_ABL
        sheet = client.open("Resultados_ABL").sheet1
        sheet.append_row(fila)
        return True
    except Exception as e:
        st.error(f"Error al conectar con Google Sheets: {e}")
        return False

# --- 3. ESTADO DE SESIÓN (Memoria de la App) ---
if 'paso' not in st.session_state:
    st.session_state.paso = 0
if 'respuestas' not in st.session_state:
    st.session_state.respuestas = {i: "Tal vez" for i in range(1, 75)}
if 'finalizado' not in st.session_state:
    st.session_state.finalizado = False

# --- 4. DISEÑO DE CABECERA (LOGOS) ---
# Logo Principal
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
st.divider()

# Título y Créditos
col_m1, col_m2 = st.columns([0.2, 0.8])
with col_m1:
    if os.path.exists("logo_mini.png"):
        st.image("logo_mini.png", width=70)
    else:
        st.write("## 🚀")

with col_m2:
    st.markdown("<h1 style='margin-top: -5px; padding-bottom: 0;'>Perfil ABL</h1>", unsafe_allow_html=True)
    st.markdown("Knowledgism ABL Profiler **By Jose Antonio Camacho (veco)**")
    st.markdown("<p style='color: gray; font-style: italic; margin-top: -15px; font-size: 0.8em;'>Análisis Profesional de Capacidades</p>", unsafe_allow_html=True)

# --- 5. BASE DE DATOS DEL TEST ---
P = {
    1: "¿Se siente bien consigo mismo?", 2: "¿Se le ocurren cosas para hacer?", 3: "Si encontrara una billetera, ¿la devolvería?", 
    4: "¿Recuerda fácilmente lo que lee?", 5: "¿Está esperando a que algo ocurra?", 6: "¿Es importante su honor personal?", 
    7: "¿Un problema afecta a toda su relación?", 8: "¿Los gustos personales influyen en sus decisiones?", 9: "¿Transmite fácilmente las malas noticias?", 
    10: "¿Le resulta difícil mantener su posición?", 11: "¿Hace cosas que no quiere hacer?", 12: "¿Crea sus propias reglas?", 
    13: "¿Es necesario a veces decir mentiras?", 14: "¿Busca palabras que no conoce?", 15: "¿Puede iniciar actividades?", 
    16: "¿Está bien beber alcohol?", 17: "¿Prefiere seguir las reglas existentes?", 18: "¿Le resulta difícil admitir errores?", 
    19: "¿Va en todas las direcciones a la vez?", 20: "¿Le resulta difícil ponerse en marcha?", 21: "¿Es tranquilo en una crisis?", 
    22: "¿Se interrumpe fácilmente?", 23: "¿Prefiere tomar el camino más fácil?", 24: "¿Pierde demasiado tiempo?", 
    25: "¿Cede ante la persuasión?", 26: "¿Cree que las drogas están bien?", 27: "¿Establece metas?", 
    28: "¿Devolvería cambio de más?", 29: "¿Se cansa al leer?", 30: "¿Lleva a cabo lo importante?", 
    31: "¿Acepta las críticas?", 32: "¿Planifica sus actividades?", 33: "¿Es sincero?", 
    34: "¿Tiene habilidades psíquicas?", 35: "¿Logra que otros sean eficaces?", 36: "¿Es importante su paz mental?", 
    37: "¿Lograría una meta en 6 meses?", 38: "¿Enfrenta situaciones dolorosas?", 39: "¿Tiene buena actitud?", 
    40: "¿Prefiere no tomar decisiones?", 41: "¿Es descuidado?", 42: "¿Corregiría a alguien errado?", 
    43: "¿Cuenta chismes o escándalos?", 44: "¿Busca conocimiento?", 45: "¿Termina el trabajo antes de socializar?", 
    46: "¿Es descuidado con su salud?", 47: "¿Tiende a posponer?", 48: "¿Retrocede ante la verdad?", 
    49: "¿Le gusta aprender?", 50: "¿Lo mangonean?", 51: "¿Le preocupan fracasos pasados?", 
    52: "¿Se altera fácilmente?", 53: "¿Cree que el hombre es honesto?", 54: "¿Lee libros?", 
    55: "¿Se siente bien si otros pierden?", 56: "¿Le resulta fácil expresarse?", 57: "¿Es muy ambicioso?", 
    58: "¿Tiende a ser celoso?", 59: "¿Prefiere lo conocido?", 60: "¿Se mantiene al tanto del mundo?", 
    61: "¿Le pone nervioso hablar en público?", 62: "¿Sus metas se alinean con su grupo?", 63: "¿Puede alguien mejorar?", 
    64: "¿Tiene períodos de inactividad?", 65: "¿Promueve amigos sobre expertos?", 66: "¿Es muy sensible?", 
    67: "¿Dramatiza emociones?", 68: "¿Sus creencias influyen?", 69: "¿Le inquieta el desorden?", 
    70: "¿Es activo?", 71: "¿Se siente deprimido?", 72: "¿Es difícil de complacer?", 
    73: "¿Ve más puntos malos que buenos?", 74: "¿Comete errores por descuido?"
}

NEG = [5, 7, 8, 9, 10, 11, 13, 16, 18, 19, 20, 22, 23, 24, 25, 26, 29, 40, 41, 43, 46, 47, 48, 50, 51, 52, 55, 58, 61, 64, 65, 66, 67, 68, 71, 72, 73, 74]
CATS = {"Percepción": range(1, 14), "Metas": range(14, 26), "Intención": range(26, 38), "Visión": range(38, 50), "Mente": range(50, 62), "Cuerpo": range(62, 75)}

# --- 6. FLUJO DE PANTALLAS ---
if not st.session_state.finalizado:
    # Pantalla 1: El Cuestionario por pasos
    nom_usuario = st.text_input("Nombre del Evaluado", placeholder="Ej: Juan Pérez", key="nombre_final")
    
    n_cats = list(CATS.keys())
    idx = st.session_state.paso
    actual = n_cats[idx]
    
    st.progress((idx + 1) / 6, text=f"Sección {idx+1} de 6: {actual}")

    with st.container(border=True):
        for q_id in CATS[actual]:
            st.write(f"**{q_id}. {P[q_id]}**")
            res_val = st.session_state.respuestas[q_id]
            st.session_state.respuestas[q_id] = st.radio(
                f"q_{q_id}", ["Sí", "Tal vez", "No"], 
                index=["Sí", "Tal vez", "No"].index(res_val), 
                key=f"radio_{q_id}", 
                horizontal=True, 
                label_visibility="collapsed"
            )
            if q_id != CATS[actual][-1]: st.divider()

    # Botones de navegación
    c_izq, c_der = st.columns(2)
    if idx > 0:
        if c_izq.button("⬅️ Anterior"):
            st.session_state.paso -= 1
            st.rerun()
    if idx < 5:
        if c_der.button("Siguiente ➡️"):
            st.session_state.paso += 1
            st.rerun()
    else:
        if c_der.button("🚀 FINALIZAR Y GUARDAR", type="primary"):
            if not nom_usuario:
                st.error("⚠️ Ingrese el nombre para poder generar el perfil.")
            else:
                st.session_state.finalizado = True
                st.rerun()

else:
    # Pantalla 2: Resultados y sincronización
    scores = {}
    for c, r in CATS.items():
        pts = 0
        for q_id in r:
            ans = st.session_state.respuestas[q_id]
            v = 1 if ans == "Sí" else (-1 if ans == "No" else 0)
            if q_id in NEG: v *= -1
            pts += v
        scores[c] = ((pts + len(r)) / (2 * len(r))) * 100

    # Sincronización única con Google Sheets
    if 'guardado_ok' not in st.session_state:
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
        fila_datos = [fecha, st.session_state.nombre_final] + [f"{round(v,1)}%" for v in scores.values()]
        if guardar_en_sheets(fila_datos):
            st.session_state.guardado_ok = True
            st.toast("✅ Sincronizado con Google Sheets", icon="📊")

    st.success(f"Perfil generado con éxito para: {st.session_state.nombre_final}")
    
    # Gráfica de Perfil
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.axhspan(66, 100, color='#2ecc71', alpha=0.15)
    ax.axhspan(33, 66, color='#f1c40f', alpha=0.15)
    ax.axhspan(0, 33, color='#e74c3c', alpha=0.15)
    ax.plot(list(scores.keys()), list(scores.values()), marker='o', color
