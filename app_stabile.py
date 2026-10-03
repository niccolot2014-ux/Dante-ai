import streamlit as st
from google import genai

st.set_page_config(page_title="Gemini 1.5 Stabile", layout="centered")

st.markdown("""
    <style>
        .reportview-container { background: #191919; }
        h1 { font-family: 'Courier New', Courier, monospace; font-weight: 300; color: #4285F4; text-align: center; }
        p { color: #A0AEC0; text-align: center; font-size: 14px; }
        .risposta-box {
            background-color: #2D3748; padding: 20px; border-radius: 8px;
            border-left: 4px solid #4285F4; color: #F7FAFC;
            font-family: 'Georgia', serif; line-height: 1.6; margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🔺 TETRAKTYS STABILE (1.5)</h1>", unsafe_allow_html=True)
st.markdown("<p>Versione ad alta disponibilità tramite Gemini AI</p>", unsafe_allow_html=True)

# Recupero della chiave automatica dai Secrets condivisi
api_key = st.secrets["GEMINI_API_KEY"]

def esegui_codice_dante(input_utente, client):
    # LIVELLO 1: Il Vertice (Modello Stabile)
    res_1 = client.models.generate_content(
        model='gemini-1.5-flash',
        contents=f"Analizza: '{input_utente}'. Rispondi SOLO con 'VIRGILIO' o 'BEATRICE'."
    )
    guida = res_1.text.strip().capitalize()

    # LIVELLO 2: La Dualità (Modello Stabile)
    prompt_cantica = f"Tu sei {guida}. Analizza: '{input_utente}'. Scegli tra INFERNO o PURGATORIO se sei Virgilio, o tra PURGATORIO o PARADISO se sei Beatrice. Rispondi SOLO con il nome della cantica."
    res_2 = client.models.generate_content(model='gemini-1.5-flash', contents=prompt_cantica)
    cantica = res_2.text.strip().capitalize()

    # LIVELLO 3: La Triade
    contesti = {
        "Inferno": "Contesto: Contrappasso, buio, giustizia punitiva, disperazione.",
        "Purgatorio": "Contesto: Sette cornici, purificazione, speranza, salita della montagna.",
        "Paradiso": "Contesto: Luce ineffabile, armonia delle sfere, pura grazia divina."
    }
    contesto_armonico = contesti.get(cantica, contesti["Inferno"])

    # LIVELLO 4: La Molteplicità (Modello Stabile)
    prompt_finale = f"Tu sei un agente AI della Divina Commedia (Tetraktys). Richiesta: '{input_utente}'. Guida: {guida}. Cantica: {cantica}. Frequenza: {contesto_armonico}. Genera la risposta. Se richiesto, usa terzine incatenate dantesche (ABA BCB), altrimenti una prosa nobile nello stile di {guida} nel {cantica}."
    
    res_4 = client.models.generate_content(model='gemini-1.5-flash', contents=prompt_finale)
    return guida, cantica, res_4.text

input_utente = st.text_input("", placeholder="Chiedi alla Tetraktys Stabile...")

if st.button("Evoca il responso"):
    if not input_utente:
        st.warning("Il campo di testo è vuoto.")
    else:
        client = genai.Client(api_key=api_key)
        with st.spinner("L'Oltretomba sta rispondendo..."):
            try:
                guida, cantica, risposta_finale = esegui_codice_dante(input_utente, client)
                st.markdown(f"🧬 *Percorso calcolato: Vertice ➔ {guida} ➔ {cantica}*")
                st.markdown(f'<div class="risposta-box">{risposta_finale.replace("\n", "<br>")}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Errore: {e}")
