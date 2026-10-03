import streamlit as st
import anthropic

st.set_page_config(page_title="Claude Tetraktys", layout="centered")

st.markdown("""
    <style>
        .reportview-container { background: #191919; }
        h1 { font-family: 'Courier New', Courier, monospace; font-weight: 300; color: #E2E8F0; text-align: center; }
        p { color: #A0AEC0; text-align: center; font-size: 14px; }
        .risposta-box {
            background-color: #2D3748; padding: 20px; border-radius: 8px;
            border-left: 4px solid #ED8936; color: #F7FAFC;
            font-family: 'Georgia', serif; line-height: 1.6; margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🔺 TETRAKTYS DANTESCA</h1>", unsafe_allow_html=True)
st.markdown("<p>Inserisci il tuo quesito per attivare il codice geometrico tramite Claude AI</p>", unsafe_allow_html=True)

with st.expander("🔑 Configurazione API Key"):
    api_key = st.text_input("Inserisci Anthropic API Key:", type="password")

def esegui_codice_dante(input_utente, client):
    res_1 = client.messages.create(
        model="claude-3-5-haiku-20241022", max_tokens=10, temperature=0,
        messages=[{"role": "user", "content": f"Analizza: '{input_utente}'. Rispondi SOLO con 'VIRGILIO' o 'BEATRICE'."}]
    )
    guida = res_1.content.text.strip().capitalize()

    prompt_cantica = f"Tu sei {guida}. Analizza: '{input_utente}'. Scegli tra INFERNO o PURGATORIO se sei Virgilio, o tra PURGATORIO o PARADISO se sei Beatrice. Rispondi SOLO con il nome della cantica."
    res_2 = client.messages.create(
        model="claude-3-5-haiku-20241022", max_tokens=10, temperature=0,
        messages=[{"role": "user", "content": prompt_cantica}]
    )
    cantica = res_2.content.text.strip().capitalize()

    contesti = {
        "Inferno": "Contesto: Contrappasso, buio, giustizia punitiva, disperazione.",
        "Purgatorio": "Contesto: Sette cornici, purificazione, speranza, salita della montagna.",
        "Paradiso": "Contesto: Luce ineffabile, armonia delle sfere, pura grazia divina."
    }
    contesto_armonico = contesti.get(cantica, contesti["Inferno"])

    prompt_finale = f"Tu sei un agente AI della Divina Commedia (Tetraktys). Richiesta: '{input_utente}'. Guida: {guida}. Cantica: {cantica}. Frequenza: {contesto_armonico}. Genera la risposta. Se richiesto, usa terzine incatenate dantesche (ABA BCB), altrimenti una prosa nobile nello stile di {guida} nel {cantica}."
    
    res_4 = client.messages.create(
        model="claude-3-5-sonnet-20241022", max_tokens=800, temperature=0.5,
        messages=[{"role": "user", "content": prompt_finale}]
    )
    return guida, cantica, res_4.content.text

input_utente = st.text_input("", placeholder="Chiedi alla Tetraktys...")

if st.button("Evoca il responso"):
    if not api_key:
        st.error("Inserisci la tua API Key!")
    elif not input_utente:
        st.warning("Il campo di testo è vuoto.")
    else:
        client = anthropic.Anthropic(api_key=api_key)
        with st.spinner("L'Oltretomba sta rispondendo..."):
            try:
                guida, cantica, risposta_finale = esegui_codice_dante(input_utente, client)
                st.markdown(f"🧬 *Percorso calcolato: Vertice ➔ {guida} ➔ {cantica}*")
                st.markdown(f'<div class="risposta-box">{risposta_finale.replace("\n", "<br>")}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Errore: {e}")

