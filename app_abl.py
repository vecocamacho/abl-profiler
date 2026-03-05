import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import os

# 1. SETUP
st.set_page_config(page_title="ABL Profiler - Jose Antonio Camacho", layout="centered")

if 'paso' not in st.session_state: st.session_state.paso = 0
if 'respuestas' not in st.session_state: st.session_state.respuestas = {i: "Tal vez" for i in range(1, 75)}
if 'finalizado' not in st.session_state: st.session_state.finalizado = False

# 2. CABECERA CON ESTILO
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
    st.markdown(f"<p style='margin-top: -10px;'>Knowledgism ABL Profiler <b>By Jose Antonio Camacho (veco)</b></p>", unsafe_allow_html=True)

# 3. PREGUNTAS
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

# 4. NAVEGACIÓN
n_cats = list(CATS.keys())

if not st.session_state.finalizado:
    nom = st.text_input("Nombre:", key="nom_eval")
    idx = st.session_state.paso
    actual = n_cats[idx]
    
    st.progress((idx + 1) / 6, text=f"{actual} ({idx+1}/6)")

    with st.container(border=True):
        for q_id in CATS[actual]:
            st.write(f"**{q_id}. {P[q_id]}**")
            res = st.session_state.respuestas[q_id]
            st.session_state.respuestas[q_id] = st.radio(f"q{q_id}", ["Sí", "Tal vez", "No"], index=["Sí", "Tal vez", "No"].index(res), key=f"r{q_id}", horizontal=True, label_visibility="collapsed")
            st.divider()

    c1, c2 = st.columns(2)
    if idx > 0:
        if c1.button("⬅️ Anterior"): 
            st.session_state.paso -= 1
            st.rerun()
    if idx < 5:
        if c2.button("Siguiente ➡️"): 
            st.session_state.paso += 1
            st.rerun()
    else:
        if c2.button("🚀 FINALIZAR", type="primary"):
            if not nom: st.error("Falta nombre")
            else: 
                st.session_state.finalizado = True
                st.rerun()

# 5. RESULTADOS
else:
    scores = {}
    for c, r in CATS.items():
        pts = 0
        for q_id in r:
            ans = st.session_state.respuestas[q_id]
            v = 1 if ans == "Sí" else (-1 if ans == "No" else 0)
            if q_id in NEG: v *= -1
            pts += v
        scores[c] = ((pts + len(r)) / (2 * len(r))) * 100

    st.success(f"Perfil de {st.session_state.nom_eval}")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.axhspan(66, 100, color='green', alpha=0.2)
    ax.axhspan(33, 66, color='yellow', alpha=0.2)
    ax.axhspan(0, 33, color='red', alpha=0.2)
    ax.plot(list(scores.keys()), list(scores.values()), marker='o', color='black')
    ax.set_ylim(0, 100)
    st.pyplot(fig)
    
    if st.button("🔄 Nuevo"):
        st.session_state.clear()
        st.rerun()
