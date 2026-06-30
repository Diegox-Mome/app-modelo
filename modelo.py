"""
=====================================================================
 NEXUS · Centro de Operaciones de Red
 Simulación de Propagación de Ransomware (Modelo SIR) en Wi-Fi Universitaria
 Trabajo de Matemática Aplicada
 Integrante 2: Diseño de Interfaz / Dashboard
 Integrante 1: Motor Matemático (ver función simular_modelo)
=====================================================================
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import math

# ---------------------------------------------------------------------------
# CONFIGURACIÓN GENERAL DE LA PÁGINA
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="NEXUS · Centro de Operaciones de Red",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# PARÁMETROS FIJOS DEL ESCENARIO (Documento de Especificación Técnica)
# ---------------------------------------------------------------------------
N_TOTAL = 800          # Población total de dispositivos concurrentes
I0 = 2                 # Infectados iniciales
R0_INICIAL = 0         # Removidos iniciales
S0 = N_TOTAL - I0 - R0_INICIAL   # Susceptibles iniciales = 798
T_TOTAL = 100          # Minutos de simulación
DT = 1                 # Paso de integración (Euler)


# ===========================================================================
# ============   MOTOR MATEMÁTICO — ZONA DE INTEGRANTE 1   ================
# ===========================================================================
def simular_modelo(beta: float, gamma: float, N: int = N_TOTAL, I0: int = I0,
                    R0: int = R0_INICIAL, T: int = T_TOTAL, dt: float = DT):
    """
    Motor matemático del modelo SIR (Susceptibles - Infectados - Removidos)
    aplicado a la propagación de un ransomware en una red Wi-Fi universitaria.

    >>> ESTA ES LA FUNCIÓN QUE DEBE REEMPLAZAR/COMPLETAR TU COMPAÑERO <<<
    El resto del dashboard NUNCA debe modificarse: solo necesita que esta
    función reciba (beta, gamma) y devuelva los 4 arreglos de abajo con
    exactamente esa estructura, para que el resto de la app siga funcionando.

    Parámetros
    ----------
    beta  : Tasa de infección (β)
    gamma : Tasa de remoción / aislamiento (γ)
    N     : Población total de dispositivos (por defecto 800)
    I0    : Infectados iniciales (por defecto 2)
    R0    : Removidos iniciales (por defecto 0)
    T     : Tiempo total de simulación en minutos (por defecto 100)
    dt    : Paso de integración de Euler (por defecto 1 minuto)

    Retorna
    -------
    t : np.array  -> vector de tiempo [0, 1, 2, ..., T]
    S : np.array  -> Susceptibles en cada minuto
    I : np.array  -> Infectados en cada minuto
    R : np.array  -> Removidos en cada minuto

    Ecuaciones (Método de Euler, según especificación técnica):
        S(t+1) = S(t) - (beta * S(t) * I(t) / N) * dt
        I(t+1) = I(t) + (beta * S(t) * I(t) / N - gamma * I(t)) * dt
        R(t+1) = R(t) + (gamma * I(t)) * dt
    """
    pasos = int(T / dt)
    t = np.zeros(pasos + 1)
    S = np.zeros(pasos + 1)
    I = np.zeros(pasos + 1)
    R = np.zeros(pasos + 1)

    S[0], I[0], R[0] = N - I0 - R0, I0, R0

    for i in range(pasos):
        St, It, Rt = S[i], I[i], R[i]

        nuevos_infectados = (beta * St * It / N) * dt
        nuevos_removidos = (gamma * It) * dt

        S[i + 1] = St - nuevos_infectados
        I[i + 1] = It + nuevos_infectados - nuevos_removidos
        R[i + 1] = Rt + nuevos_removidos

        S[i + 1] = max(S[i + 1], 0)
        I[i + 1] = max(I[i + 1], 0)
        R[i + 1] = max(R[i + 1], 0)

        t[i + 1] = (i + 1) * dt

    return t, S, I, R


def calcular_metricas(t, S, I, R, N=N_TOTAL):
    """
    Calcula los indicadores clave de impacto operativo a partir de los
    arreglos generados por simular_modelo(). No requiere modificación.
    """
    idx_max = int(np.argmax(I))
    t_max = t[idx_max]
    I_max = I[idx_max]
    carga_red_pct = (I_max / N) * 100
    return {
        "t_max": t_max,
        "I_max": I_max,
        "carga_red_pct": carga_red_pct,
    }
# ===========================================================================
# ========================   FIN ZONA INTEGRANTE 1   ======================
# ===========================================================================


# ---------------------------------------------------------------------------
# ESTILOS — Identidad visual "NEXUS"
# Paleta: #070a0f (fondo), #0e131b (panel), #141b26 (panel alto),
#         #3ddc97 (seguro / acento primario), #ff4d4f (alerta),
#         #5b8def (dato frío), #aab4c5 (texto secundario)
# Tipografía: Space Grotesk (display), Inter (cuerpo), JetBrains Mono (datos)
# ---------------------------------------------------------------------------
def inyectar_estilos():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

        html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

        .stApp {
            background:
                radial-gradient(circle at 10% -10%, rgba(91,141,239,0.10) 0%, transparent 45%),
                radial-gradient(circle at 90% 0%, rgba(61,220,151,0.07) 0%, transparent 40%),
                linear-gradient(180deg, #070a0f 0%, #060809 100%);
            color: #dfe4ec;
        }
        .block-container { padding-top: 1.6rem; max-width: 1280px; }

        @keyframes fadeUp {
            from { opacity: 0; transform: translateY(10px); }
            to   { opacity: 1; transform: translateY(0); }
        }
        @keyframes breathe {
            0%, 100% { opacity: 0.55; }
            50%      { opacity: 1; }
        }
        @keyframes shimmer {
            0%   { background-position: -300px 0; }
            100% { background-position: 300px 0; }
        }
        @keyframes dashFlow {
            to { stroke-dashoffset: -24; }
        }

        /* ================= SIDEBAR ================= */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0a0d13 0%, #070a0e 100%);
            border-right: 1px solid #16202c;
        }
        section[data-testid="stSidebar"] .block-container { padding-top: 1.8rem; }

        .brand-mark {
            display: flex; align-items: center; gap: 10px;
            margin-bottom: 4px;
        }
        .brand-dot {
            width: 9px; height: 9px; border-radius: 50%;
            background: #3ddc97;
            box-shadow: 0 0 10px 2px rgba(61,220,151,0.7);
            animation: breathe 2.4s ease-in-out infinite;
        }
        .brand-name {
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700; font-size: 1.05rem; letter-spacing: 1.5px;
            color: #f3f5f9;
        }
        .brand-sub {
            font-size: 0.72rem; color: #5d6a7c; margin: 2px 0 22px 19px;
            letter-spacing: 0.3px;
        }

        .panel-label {
            font-size: 0.68rem; text-transform: uppercase; letter-spacing: 1.4px;
            color: #4d5a6c; font-weight: 700; margin: 22px 0 10px 0;
            display: flex; align-items: center; gap: 8px;
        }
        .panel-label::after {
            content: ""; flex: 1; height: 1px;
            background: linear-gradient(90deg, #1c2734, transparent);
        }

        div[data-testid="stSlider"] { padding-top: 6px; padding-bottom: 2px; }
        div[data-testid="stSlider"] label p {
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 0.8rem !important;
            color: #c2c9d6 !important;
            font-weight: 500 !important;
        }
        /* Pista y pulgar del slider */
        div[data-testid="stSlider"] [data-baseweb="slider"] > div > div {
            background: #1a2330 !important;
        }
        div[data-testid="stSlider"] [role="slider"] {
            box-shadow: 0 0 0 4px rgba(91,141,239,0.18) !important;
        }

        .scn-card {
            border: 1px solid #1c2734;
            background: linear-gradient(160deg, #0e131c 0%, #0a0e15 100%);
            border-radius: 12px;
            padding: 12px 14px 10px 14px;
            margin-bottom: 10px;
            transition: border-color .25s ease, transform .25s ease;
        }
        .scn-card:hover { border-color: #2a3a52; transform: translateX(2px); }
        .scn-title {
            font-size: 0.82rem; font-weight: 700; color: #e7eaf0;
            font-family: 'Space Grotesk', sans-serif;
        }
        .scn-desc {
            font-size: 0.7rem; color: #5d6a7c; margin: 2px 0 8px 0; line-height: 1.4;
        }
        .scn-tags {
            display: flex; gap: 6px; margin-bottom: 8px;
        }
        .scn-tag {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.65rem; padding: 2px 7px; border-radius: 5px;
            background: #121a26; color: #7d8a9c; border: 1px solid #1c2734;
        }

        .stButton button {
            border-radius: 8px !important;
            font-weight: 600 !important; font-size: 0.78rem !important;
            border: 1px solid #233044 !important;
            background: #101722 !important;
            color: #c2c9d6 !important;
            transition: all .22s ease !important;
            padding: 0.45rem 0.6rem !important;
        }
        .stButton button:hover {
            border-color: #5b8def !important;
            color: #ffffff !important;
            background: #142036 !important;
            box-shadow: 0 4px 16px rgba(91,141,239,0.22);
        }
        .stButton button:active { transform: scale(0.97); }

        .sidebar-foot {
            font-size: 0.68rem; color: #3a4452; line-height: 1.7;
            margin-top: 18px; font-family: 'JetBrains Mono', monospace;
            border-top: 1px dashed #1c2734; padding-top: 14px;
        }
        .sidebar-foot b { color: #5d6a7c; }

        /* ---- Panel de resultados en el sidebar ---- */
        .sb-r0-box {
            border-radius: 12px; padding: 14px 16px; border: 1px solid;
            margin-bottom: 10px; animation: fadeUp 0.35s ease;
        }
        .sb-r0-danger {
            background: linear-gradient(140deg, rgba(255,77,79,0.14), rgba(255,77,79,0.03));
            border-color: rgba(255,77,79,0.4);
        }
        .sb-r0-safe {
            background: linear-gradient(140deg, rgba(61,220,151,0.14), rgba(61,220,151,0.03));
            border-color: rgba(61,220,151,0.4);
        }
        .sb-r0-top { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; }
        .sb-r0-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
        .sb-r0-danger .sb-r0-dot { background: #ff4d4f; box-shadow: 0 0 10px 3px rgba(255,77,79,0.55); animation: breathe 1.4s ease-in-out infinite; }
        .sb-r0-safe .sb-r0-dot   { background: #3ddc97; box-shadow: 0 0 10px 3px rgba(61,220,151,0.55); animation: breathe 2.2s ease-in-out infinite; }
        .sb-r0-formula {
            font-family: 'JetBrains Mono', monospace; font-size: 0.78rem;
            color: #aab4c5; font-weight: 600;
        }
        .sb-r0-msg {
            font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 0.88rem;
        }
        .sb-r0-danger .sb-r0-msg { color: #ff8a8c; }
        .sb-r0-safe .sb-r0-msg   { color: #4fe8ab; }

        .sb-explainer {
            font-size: 0.72rem; color: #5d6a7c; line-height: 1.55;
            margin-bottom: 4px; padding: 0 2px;
        }
        .sb-explainer b { color: #8a96a8; }

        .sb-metric {
            border: 1px solid #1a2330; border-radius: 12px;
            background: linear-gradient(150deg, #0e141d 0%, #0a0f17 100%);
            padding: 13px 15px; margin-bottom: 10px;
            animation: fadeUp 0.4s ease;
        }
        .sb-metric-label {
            font-size: 0.7rem; color: #7d8a9c; font-weight: 600;
            line-height: 1.4; margin-bottom: 6px;
        }
        .sb-metric-value {
            font-family: 'JetBrains Mono', monospace; font-size: 1.35rem;
            font-weight: 700; color: #f3f5f9;
        }
        .sb-metric-value span {
            font-size: 0.68rem; color: #4d5a6c; font-weight: 500; margin-left: 4px;
        }
        .sb-metric-bar {
            height: 4px; border-radius: 4px; background: #131b27;
            margin: 9px 0 8px 0; overflow: hidden;
        }
        .sb-metric-fill { height: 100%; border-radius: 4px; transition: width .6s cubic-bezier(.4,0,.2,1); }
        .sb-fill-blue   { background: linear-gradient(90deg, #2c63c9, #5b8def); }
        .sb-fill-red    { background: linear-gradient(90deg, #c9302c, #ff4d4f); }
        .sb-fill-orange { background: linear-gradient(90deg, #c97a1f, #ff9f40); }
        .sb-metric-note {
            font-size: 0.68rem; color: #4d5a6c; line-height: 1.5; font-style: italic;
        }

        /* ================= HEADER / HERO ================= */
        .hero {
            position: relative;
            border-radius: 18px;
            border: 1px solid #161f2b;
            background: linear-gradient(135deg, #0c1119 0%, #090d13 60%, #0a0f17 100%);
            padding: 26px 30px;
            margin-bottom: 20px;
            overflow: hidden;
            animation: fadeUp 0.5s ease;
        }
        .hero-row { display: flex; justify-content: space-between; align-items: flex-start; gap: 20px; position: relative; z-index: 2;}
        .hero-eyebrow {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.7rem; letter-spacing: 2px; color: #5b8def;
            text-transform: uppercase; margin-bottom: 8px; font-weight: 600;
        }
        .hero-title {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.7rem; font-weight: 700; color: #f6f8fb;
            margin: 0; letter-spacing: -0.3px;
        }
        .hero-desc {
            font-size: 0.86rem; color: #7d8a9c; margin-top: 6px; max-width: 560px;
        }
        .live-chip {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.72rem; font-weight: 600; color: #3ddc97;
            border: 1px solid #1f4d3c; background: rgba(61,220,151,0.07);
            border-radius: 999px; padding: 6px 14px;
            display: flex; align-items: center; gap: 8px; white-space: nowrap;
        }
        .live-chip span.dot {
            width: 7px; height: 7px; border-radius: 50%; background: #3ddc97;
            animation: breathe 1.8s ease-in-out infinite;
        }

        /* Mapa de red — pieza de firma */
        .net-wrap { margin-top: 18px; position: relative; z-index: 2; }
        .net-caption {
            font-family: 'JetBrains Mono', monospace; font-size: 0.66rem;
            color: #3a4452; margin-top: 6px; letter-spacing: 0.4px;
        }

        /* ================= ALERTA R0 ================= */
        .alert-box {
            padding: 20px 26px; border-radius: 14px; font-weight: 700;
            font-size: 1.0rem; display: flex; align-items: center; gap: 16px;
            border: 1px solid; margin-bottom: 18px; animation: fadeUp 0.4s ease;
        }
        .alert-danger {
            background: linear-gradient(120deg, rgba(255,77,79,0.13), rgba(255,77,79,0.02));
            border-color: rgba(255,77,79,0.4); color: #ff8a8c;
        }
        .alert-safe {
            background: linear-gradient(120deg, rgba(61,220,151,0.13), rgba(61,220,151,0.02));
            border-color: rgba(61,220,151,0.4); color: #4fe8ab;
        }
        .alert-icon { width: 13px; height: 13px; border-radius: 50%; flex-shrink: 0; }
        .alert-danger .alert-icon { background: #ff4d4f; box-shadow: 0 0 16px 4px rgba(255,77,79,0.55); }
        .alert-safe .alert-icon   { background: #3ddc97; box-shadow: 0 0 16px 4px rgba(61,220,151,0.55); }
        .r0-tag {
            font-family: 'JetBrains Mono', monospace; font-size: 0.82rem;
            opacity: 0.8; margin-left: auto; font-weight: 600;
        }

        /* ================= MÉTRICAS ================= */
        .metric-card {
            background: linear-gradient(150deg, #0f1622 0%, #0a0f17 100%);
            border: 1px solid #1a2330; border-radius: 14px;
            padding: 18px 20px; height: 100%; position: relative;
            overflow: hidden; transition: transform .25s ease, border-color .25s ease;
            animation: fadeUp 0.5s ease;
        }
        .metric-card:hover { transform: translateY(-3px); border-color: #2a3a52; }
        .metric-label {
            font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.9px;
            color: #5d6a7c; font-weight: 700; margin-bottom: 10px;
        }
        .metric-value {
            font-family: 'JetBrains Mono', monospace; font-size: 2rem;
            font-weight: 700; color: #f3f5f9; line-height: 1;
        }
        .metric-unit { font-size: 0.92rem; color: #4d5a6c; font-weight: 500; margin-left: 5px; }
        .metric-bar { height: 4px; border-radius: 4px; background: #131b27; margin-top: 14px; overflow: hidden; }
        .metric-bar-fill { height: 100%; border-radius: 4px; transition: width .6s cubic-bezier(.4,0,.2,1); }
        .metric-accent-blue   .metric-bar-fill { background: linear-gradient(90deg, #2c63c9, #5b8def); }
        .metric-accent-red    .metric-bar-fill { background: linear-gradient(90deg, #c9302c, #ff4d4f); }
        .metric-accent-orange .metric-bar-fill { background: linear-gradient(90deg, #c97a1f, #ff9f40); }

        /* ================= SECCIÓN ================= */
        .section-title {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 0.95rem; font-weight: 700; color: #cfd6e0;
            margin: 30px 0 14px 0; display: flex; align-items: center; gap: 10px;
            letter-spacing: 0.2px;
        }
        .section-title .idx {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.72rem; color: #5b8def; border: 1px solid #1c2c47;
            background: rgba(91,141,239,0.08); padding: 2px 8px; border-radius: 6px;
        }

        /* ================= CONTENEDOR GRÁFICO ================= */
        .chart-frame {
            border: 1px solid #161f2b; border-radius: 16px;
            background: linear-gradient(160deg, #0c111a 0%, #090d14 100%);
            padding: 6px 6px 0 6px; animation: fadeUp 0.5s ease;
        }

        /* ================= DESCARGA ================= */
        div[data-testid="stDownloadButton"] button {
            border-radius: 10px !important; font-weight: 700 !important;
            background: linear-gradient(120deg, #2c63c9, #5b8def) !important;
            border: none !important; color: white !important;
            padding: 0.6rem 1.1rem !important;
            box-shadow: 0 4px 14px rgba(91,141,239,0.25);
        }
        div[data-testid="stDownloadButton"] button:hover {
            box-shadow: 0 8px 22px rgba(91,141,239,0.4); transform: translateY(-1px);
        }

        .export-note { color: #5d6a7c; font-size: 0.82rem; padding-top: 10px; }
        .export-note b { color: #c2c9d6; }

        .main-explainer {
            color: #6b7888; font-size: 0.84rem; line-height: 1.6;
            margin: -2px 0 16px 0; max-width: 820px;
        }
        .main-explainer b { font-weight: 600; }

        hr { border-color: #161f2b !important; }
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header[data-testid="stHeader"] { background: transparent; }

        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: #0a0e15; }
        ::-webkit-scrollbar-thumb { background: #1c2734; border-radius: 4px; }
    </style>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# ESTADO INICIAL
# ---------------------------------------------------------------------------
if "beta" not in st.session_state:
    st.session_state.beta = 1.2
if "gamma" not in st.session_state:
    st.session_state.gamma = 0.05


def aplicar_escenario(beta_val, gamma_val):
    st.session_state.beta = beta_val
    st.session_state.gamma = gamma_val


# ---------------------------------------------------------------------------
# PIEZA DE FIRMA: mapa de red animado que refleja el riesgo actual (R0)
# Nodos dispuestos en cuadrícula irregular tipo "campus"; el color y el
# pulso de cada nodo dependen del nivel de riesgo calculado en vivo.
# ---------------------------------------------------------------------------
def generar_mapa_red(risk_ratio: float, n_nodos: int = 26, seed: int = 7):
    """
    risk_ratio: 0.0 (controlado) -> 1.0 (crítico). Determina cuántos nodos
    se muestran en color de alerta y la velocidad de la animación.
    """
    rng = np.random.default_rng(seed)
    w, h = 760, 130
    xs = rng.uniform(20, w - 20, n_nodos)
    ys = rng.uniform(18, h - 18, n_nodos)

    # Color seguro -> color de alerta interpolado
    safe = (61, 220, 151)
    danger = (255, 77, 79)
    risk_ratio = max(0.0, min(1.0, risk_ratio))
    n_infected_look = int(round(risk_ratio * n_nodos))

    # orden de "infección" estable según índice para que no parpadee al azar
    order = np.argsort(rng.random(n_nodos))
    infected_set = set(order[:n_infected_look])

    dur_base = 3.2 - 1.8 * risk_ratio  # más riesgo -> pulso más rápido
    dur_base = max(1.1, dur_base)

    svg_parts = [f'<svg viewBox="0 0 {w} {h}" width="100%" height="120" xmlns="http://www.w3.org/2000/svg">']

    # líneas de conexión (vecino más cercano, look de topología de red)
    pts = list(zip(xs, ys))
    for i, (x1, y1) in enumerate(pts):
        dists = [(j, (x1 - x2) ** 2 + (y1 - y2) ** 2) for j, (x2, y2) in enumerate(pts) if j != i]
        dists.sort(key=lambda d: d[1])
        for j, _ in dists[:2]:
            x2, y2 = pts[j]
            edge_color = "rgba(255,77,79,0.22)" if (i in infected_set and j in infected_set) else "rgba(91,141,239,0.14)"
            svg_parts.append(
                f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                f'stroke="{edge_color}" stroke-width="1" stroke-dasharray="4 5">'
                f'<animate attributeName="stroke-dashoffset" from="0" to="-18" '
                f'dur="{dur_base + 1:.2f}s" repeatCount="indefinite"/></line>'
            )

    for i, (x, y) in enumerate(pts):
        is_inf = i in infected_set
        color = f"rgb{danger}" if is_inf else f"rgb{safe}"
        glow = "rgba(255,77,79,0.55)" if is_inf else "rgba(61,220,151,0.45)"
        r = 4.2 if is_inf else 3.4
        dur = (dur_base * 0.7) if is_inf else (dur_base * 1.4)
        delay = (i % 7) * 0.18
        svg_parts.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{color}">'
            f'<animate attributeName="opacity" values="0.45;1;0.45" '
            f'dur="{dur:.2f}s" begin="{delay:.2f}s" repeatCount="indefinite"/></circle>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r+5}" fill="none" stroke="{glow}" stroke-width="1.4">'
            f'<animate attributeName="r" values="{r+2};{r+9};{r+2}" '
            f'dur="{dur*1.6:.2f}s" begin="{delay:.2f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0.6;0;0.6" '
            f'dur="{dur*1.6:.2f}s" begin="{delay:.2f}s" repeatCount="indefinite"/></circle>'
        )

    svg_parts.append('</svg>')
    return "".join(svg_parts)


# ---------------------------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------------------------
def construir_sidebar():
    with st.sidebar:
        st.markdown("""
            <div class="brand-mark">
                <div class="brand-dot"></div>
                <div class="brand-name">NEXUS</div>
            </div>
            <div class="brand-sub">Centro de Operaciones de Red</div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="panel-label">Parámetros del modelo</div>', unsafe_allow_html=True)

        beta = st.slider(
            "β · Tasa de infección",
            min_value=0.0, max_value=2.0, step=0.01,
            key="beta",
            help="Velocidad con la que el ransomware se propaga entre dispositivos susceptibles."
        )
        gamma = st.slider(
            "γ · Tasa de remoción",
            min_value=0.0, max_value=1.0, step=0.01,
            key="gamma",
            help="Velocidad con la que los dispositivos infectados son aislados o desconectados."
        )

        st.markdown('<div class="panel-label">Escenarios preestablecidos</div>', unsafe_allow_html=True)

        st.markdown("""
            <div class="scn-card">
                <div class="scn-title">Escenario A</div>
                <div class="scn-desc">Propagación libre — sin respuesta defensiva.</div>
                <div class="scn-tags"><span class="scn-tag">β 1.20</span><span class="scn-tag">γ 0.05</span></div>
            </div>
        """, unsafe_allow_html=True)
        st.button("Activar Escenario A", use_container_width=True, key="btn_a",
                  on_click=aplicar_escenario, args=(1.2, 0.05))

        st.markdown("""
            <div class="scn-card" style="margin-top:14px;">
                <div class="scn-title">Escenario B</div>
                <div class="scn-desc">Mitigación activa — aislamiento rápido de equipos.</div>
                <div class="scn-tags"><span class="scn-tag">β 1.20</span><span class="scn-tag">γ 0.35</span></div>
            </div>
        """, unsafe_allow_html=True)
        st.button("Activar Escenario B", use_container_width=True, key="btn_b",
                  on_click=aplicar_escenario, args=(1.2, 0.35))

        st.markdown("""
            <div class="sidebar-foot">
                <b>MODELO</b>&nbsp; SIR discreto · Euler · dt = 1 min<br>
                <b>RED</b>&nbsp;&nbsp;&nbsp;&nbsp; N = 800 · I₀ = 2 · R₀ = 0<br>
                <b>VENTANA</b> T = 100 min
            </div>
        """, unsafe_allow_html=True)

    return beta, gamma


# ---------------------------------------------------------------------------
# PANEL LATERAL DE RESULTADOS (Dashboard SecOps)
# Según la actualización del documento técnico: R0, t_max, I_max y carga de
# red deben calcularse e imprimirse en el PANEL LATERAL cada vez que se
# mueven los controles. Se recalcula en cada rerun, por lo tanto es dinámico.
# ---------------------------------------------------------------------------
def mostrar_resultados_sidebar(beta, gamma, metricas):
    r0_val = (beta / gamma) if gamma > 0 else float("inf")
    r0_text = f"{r0_val:.2f}" if math.isfinite(r0_val) else "∞"

    with st.sidebar:
        st.markdown('<div class="panel-label">Resultados en vivo</div>', unsafe_allow_html=True)

        # ---- 1. Número de Reproducción Básico (R0) ----
        if r0_val > 1:
            st.markdown(f"""
            <div class="sb-r0-box sb-r0-danger">
                <div class="sb-r0-top">
                    <span class="sb-r0-dot"></span>
                    <span class="sb-r0-formula">R₀ = β / γ = {r0_text}</span>
                </div>
                <div class="sb-r0-msg">Alerta: Propagación Epidémica (Red Inviable)</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="sb-r0-box sb-r0-safe">
                <div class="sb-r0-top">
                    <span class="sb-r0-dot"></span>
                    <span class="sb-r0-formula">R₀ = β / γ = {r0_text}</span>
                </div>
                <div class="sb-r0-msg">Propagación Controlada</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
            <div class="sb-explainer">
                Si <b>R₀ &gt; 1</b>, cada equipo infectado contagia en promedio a más
                de un equipo nuevo antes de ser aislado: el brote crece. Si
                <b>R₀ &lt; 1</b>, la red se recupera sola.
            </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="panel-label">Indicadores de impacto operativo</div>', unsafe_allow_html=True)

        # ---- 2. Minuto crítico de saturación ----
        st.markdown(f"""
            <div class="sb-metric">
                <div class="sb-metric-label">Minuto crítico de saturación (t_max):</div>
                <div class="sb-metric-value">{metricas['t_max']:.0f} <span>minutos</span></div>
                <div class="sb-metric-bar"><div class="sb-metric-fill sb-fill-blue" style="width:{min(100,(metricas['t_max']/T_TOTAL)*100):.0f}%;"></div></div>
                <div class="sb-metric-note">Indica si hay tiempo para una respuesta humana o si se necesita aislamiento automático.</div>
            </div>
        """, unsafe_allow_html=True)

        # ---- 3. Pico máximo de dispositivos comprometidos ----
        st.markdown(f"""
            <div class="sb-metric">
                <div class="sb-metric-label">Pico máximo de dispositivos comprometidos (I_max):</div>
                <div class="sb-metric-value">{metricas['I_max']:.0f} <span>dispositivos</span></div>
                <div class="sb-metric-bar"><div class="sb-metric-fill sb-fill-red" style="width:{min(100,(metricas['I_max']/N_TOTAL)*100):.0f}%;"></div></div>
                <div class="sb-metric-note">Define la capacidad mínima que necesitaría el firewall o el sistema de contención.</div>
            </div>
        """, unsafe_allow_html=True)

        # ---- 4. Carga de red afectada ----
        st.markdown(f"""
            <div class="sb-metric">
                <div class="sb-metric-label">Carga de red afectada:</div>
                <div class="sb-metric-value">{metricas['carga_red_pct']:.1f}<span>%</span></div>
                <div class="sb-metric-bar"><div class="sb-metric-fill sb-fill-orange" style="width:{min(100,metricas['carga_red_pct']):.0f}%;"></div></div>
                <div class="sb-metric-note">Cálculo: (I_max / N) × 100 — porcentaje de la red total comprometido en el pico.</div>
            </div>
        """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# HERO / HEADER con mapa de red de firma
# ---------------------------------------------------------------------------
def construir_hero(risk_ratio):
    mapa_svg = generar_mapa_red(risk_ratio)
    st.markdown(f"""
    <div class="hero">
        <div class="hero-row">
            <div>
                <div class="hero-eyebrow">Facultad de Ingeniería · Red Wi-Fi pública</div>
                <p class="hero-title">Monitoreo de propagación — Cryptoworm</p>
                <p class="hero-desc">Modelo epidemiológico SIR aplicado a 800 dispositivos
                concurrentes. Ajusta los parámetros para observar cómo cambia el
                comportamiento de la red en tiempo real.</p>
            </div>
            <div class="live-chip"><span class="dot"></span>SIMULACIÓN EN VIVO</div>
        </div>
        <div class="net-wrap">
            {mapa_svg}
            <div class="net-caption">TOPOLOGÍA DE RED — nodos en rojo representan la proporción estimada de equipos en riesgo</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# ALERTA R0
# ---------------------------------------------------------------------------
def mostrar_alerta_r0(beta, gamma):
    r0_val = (beta / gamma) if gamma > 0 else float("inf")

    if r0_val > 1:
        st.markdown(f"""
        <div class="alert-box alert-danger">
            <div class="alert-icon"></div>
            <div>Alerta: Propagación Epidémica (Red Inviable)</div>
            <div class="r0-tag">R₀ = {r0_val:.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="alert-box alert-safe">
            <div class="alert-icon"></div>
            <div>Propagación Controlada</div>
            <div class="r0-tag">R₀ = {r0_val:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    return r0_val


# ---------------------------------------------------------------------------
# TARJETAS DE MÉTRICAS
# ---------------------------------------------------------------------------
def tarjeta_metrica(col, label, value, unit, accent_class, pct_barra):
    pct_barra = max(2, min(100, pct_barra))
    col.markdown(f"""
    <div class="metric-card {accent_class}">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}<span class="metric-unit">{unit}</span></div>
        <div class="metric-bar"><div class="metric-bar-fill" style="width:{pct_barra}%;"></div></div>
    </div>
    """, unsafe_allow_html=True)


def mostrar_indicadores(metricas):
    c1, c2, c3 = st.columns(3)
    tarjeta_metrica(c1, "Minuto crítico de saturación (t_max)",
                     f"{metricas['t_max']:.0f}", "min", "metric-accent-blue",
                     pct_barra=(metricas['t_max'] / T_TOTAL) * 100)
    tarjeta_metrica(c2, "Pico máximo de dispositivos comprometidos (I_max)",
                     f"{metricas['I_max']:.0f}", "equipos", "metric-accent-red",
                     pct_barra=(metricas['I_max'] / N_TOTAL) * 100)
    tarjeta_metrica(c3, "Carga de red afectada",
                     f"{metricas['carga_red_pct']:.1f}", "%", "metric-accent-orange",
                     pct_barra=metricas['carga_red_pct'])


# ---------------------------------------------------------------------------
# GRÁFICO PRINCIPAL — Plotly, con transición animada al cambiar parámetros
# ---------------------------------------------------------------------------
def mostrar_grafico(t, S, I, R):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=t, y=S, mode="lines", name="Susceptibles",
        line=dict(color="#5b8def", width=3, shape="spline"),
        fill="tozeroy", fillcolor="rgba(91,141,239,0.07)",
        hovertemplate="Susceptibles: %{y:.0f}<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=t, y=I, mode="lines", name="Infectados",
        line=dict(color="#ff4d4f", width=3, shape="spline"),
        fill="tozeroy", fillcolor="rgba(255,77,79,0.09)",
        hovertemplate="Infectados: %{y:.0f}<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=t, y=R, mode="lines", name="Removidos",
        line=dict(color="#3ddc97", width=3, shape="spline"),
        fill="tozeroy", fillcolor="rgba(61,220,151,0.07)",
        hovertemplate="Removidos: %{y:.0f}<extra></extra>"
    ))

    idx_peak = int(np.argmax(I))
    fig.add_trace(go.Scatter(
        x=[t[idx_peak]], y=[I[idx_peak]], mode="markers",
        marker=dict(color="#ff4d4f", size=10, line=dict(color="#fff0f0", width=1.5)),
        name="Pico", hovertemplate=f"Pico: t={t[idx_peak]:.0f} min, I={I[idx_peak]:.0f}<extra></extra>",
        showlegend=False
    ))

    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#aab4c5", size=12),
        legend=dict(orientation="h", yanchor="bottom", y=1.04, xanchor="left", x=0,
                    bgcolor="rgba(0,0,0,0)", font=dict(size=12)),
        margin=dict(l=10, r=10, t=46, b=10),
        xaxis=dict(title="Tiempo (minutos)", gridcolor="rgba(255,255,255,0.045)",
                   zeroline=False, showline=False),
        yaxis=dict(title="Dispositivos", gridcolor="rgba(255,255,255,0.045)",
                   zeroline=False, showline=False),
        hovermode="x unified",
        hoverlabel=dict(bgcolor="#0e1622", font_size=12, font_family="JetBrains Mono"),
        transition=dict(duration=450, easing="cubic-in-out"),
    )

    st.markdown('<div class="chart-frame">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, key="grafico_sir")
    st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# DESCARGA DE DATOS
# ---------------------------------------------------------------------------
def mostrar_descarga(t, S, I, R):
    df = pd.DataFrame({
        "Minuto": t.astype(int),
        "Susceptibles": np.round(S, 2),
        "Infectados": np.round(I, 2),
        "Removidos": np.round(R, 2),
    })
    csv_bytes = df.to_csv(index=False).encode("utf-8")

    st.markdown('<div class="section-title"><span class="idx">03</span>Exportar resultados</div>', unsafe_allow_html=True)
    cdl, cinfo = st.columns([1, 3])
    with cdl:
        st.download_button(
            label="Descargar CSV",
            data=csv_bytes,
            file_name=f"simulacion_sir_beta{st.session_state.beta}_gamma{st.session_state.gamma}.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with cinfo:
        st.markdown(
            f'<div class="export-note"><b>{len(df)}</b> registros · '
            f'columnas: Minuto, Susceptibles, Infectados, Removidos</div>',
            unsafe_allow_html=True
        )

    with st.expander("Ver tabla de datos completa"):
        st.dataframe(df, use_container_width=True, height=320)


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main():
    inyectar_estilos()
    beta, gamma = construir_sidebar()

    t, S, I, R = simular_modelo(beta, gamma)
    metricas = calcular_metricas(t, S, I, R)
    risk_ratio = metricas["carga_red_pct"] / 100

    # Panel lateral de resultados — se recalcula y redibuja en cada
    # movimiento de los sliders (actualización del documento técnico).
    mostrar_resultados_sidebar(beta, gamma, metricas)

    construir_hero(risk_ratio)

    st.markdown('<div class="section-title"><span class="idx">01</span>Estado de la red</div>', unsafe_allow_html=True)
    mostrar_alerta_r0(beta, gamma)
    st.markdown("""
        <div class="main-explainer">
            Este resultado se recalcula al instante con cada movimiento de los
            controles del panel lateral, y también queda resumido ahí junto con
            el detalle de cada indicador.
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title"><span class="idx">02</span>Curvas de propagación S · I · R</div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="main-explainer">
            <b style="color:#5b8def;">Susceptibles</b> son los equipos conectados que aún
            no han sido infectados. <b style="color:#ff4d4f;">Infectados</b> son los que
            ejecutan el ransomware y siguen contagiando. <b style="color:#3ddc97;">Removidos</b>
            son los que ya fueron aislados o desconectados y dejaron de propagar el ataque.
            El punto rojo marca el instante exacto del pico de la epidemia (t_max, I_max).
        </div>
    """, unsafe_allow_html=True)
    mostrar_grafico(t, S, I, R)

    mostrar_descarga(t, S, I, R)


if __name__ == "__main__":
    main()