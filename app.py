import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Gestione Atleti",
    page_icon="🏃",
    layout="wide"
)

if "athletes" not in st.session_state:
    st.session_state.athletes = []

if "injuries" not in st.session_state:
    st.session_state.injuries = []

st.title("🏃 Gestione Atleti")
st.caption("Demo semplice online - versione iniziale")

menu = st.sidebar.radio(
    "Menu",
    ["Dashboard", "Scheda atleta", "Nuovo infortunio", "Archivio infortuni", "Statistiche"]
)

# =========================
# DASHBOARD
# =========================
if menu == "Dashboard":
    st.header("Dashboard")

    totale_atleti = len(st.session_state.athletes)
    totale_infortuni = len(st.session_state.injuries)

    col1, col2, col3 = st.columns(3)
    col1.metric("Atleti registrati", totale_atleti)
    col2.metric("Infortuni registrati", totale_infortuni)

    if totale_infortuni > 0:
        prognosi_tot = 0
        for i in st.session_state.injuries:
            try:
                prognosi_tot += int(i["prognosi_giorni"])
            except:
                pass
        col3.metric("Giorni prognosi totali", prognosi_tot)
    else:
        col3.metric("Giorni prognosi totali", 0)

    st.markdown("---")

    st.subheader("Cosa fa questa demo")
    st.write("- inserimento scheda atleta")
    st.write("- inserimento infortunio")
    st.write("- archivio rapido")
    st.write("- statistiche base di fine stagione")

    st.info("Questa e una demo iniziale: i dati restano temporanei durante l'uso della sessione.")

# =========================
# SCHEDA ATLETA
# =========================
elif menu == "Scheda atleta":
    st.header("Scheda atleta")

    with st.form("form_atleta"):
        col1, col2 = st.columns(2)

        with col1:
            nome = st.text_input("Nome *")
            cognome = st.text_input("Cognome *")
            sport = st.text_input("Sport")
            ruolo = st.text_input("Ruolo")

        with col2:
            data_nascita = st.text_input("Data di nascita")
            telefono = st.text_input("Telefono")
            email = st.text_input("Email")

        st.subheader("Anamnesi")
        anamnesi_remota = st.text_area("Anamnesi patologica remota")
        anamnesi_prossima = st.text_area("Anamnesi patologica prossima")
        allergie = st.text_area("Allergie")
        note = st.text_area("Note generali")

        salva_atleta = st.form_submit_button("Salva atleta")

        if salva_atleta:
            if not nome or not cognome:
                st.error("Inserisci almeno nome e cognome.")
            else:
                atleta = {
                    "nome": nome,
                    "cognome": cognome,
                    "sport": sport,
                    "ruolo": ruolo,
                    "data_nascita": data_nascita,
                    "telefono": telefono,
                    "email": email,
                    "anamnesi_remota": anamnesi_remota,
                    "anamnesi_prossima": anamnesi_prossima,
                    "allergie": allergie,
                    "note": note
                }
                st.session_state.athletes.append(atleta)
                st.success(f"Atleta salvato: {cognome} {nome}")

    st.markdown("---")
    st.subheader("Atleti inseriti")

    if st.session_state.athletes:
        df_atleti = pd.DataFrame(st.session_state.athletes)
        st.dataframe(df_atleti, use_container_width=True)
    else:
        st.write("Nessun atleta inserito.")

# =========================
# NUOVO INFORTUNIO
# =========================
elif menu == "Nuovo infortunio":
    st.header("Nuovo infortunio")

    if not st.session_state.athletes:
        st.warning("Prima inserisci almeno un atleta nella sezione 'Scheda atleta'.")
    else:
        elenco_atleti = [
            f"{a['cognome']} {a['nome']}" for a in st.session_state.athletes
        ]

        with st.form("form_infortunio"):
            atleta = st.selectbox("Atleta *", elenco_atleti)

            col1, col2 = st.columns(2)

            with col1:
                data_evento = st.text_input("Data evento")
                stagione = st.text_input("Stagione", value="2026-2027")
                distretto = st.selectbox(
                    "Distretto anatomico",
                    [
                        "Testa", "Collo", "Spalla", "Braccio", "Gomito", "Polso",
                        "Mano", "Schiena", "Anca", "Coscia", "Ginocchio",
                        "Gamba", "Caviglia", "Piede", "Altro"
                    ]
                )

            with col2:
                tipo_tessuto = st.selectbox(
                    "Tipo",
                    [
                        "Articolare", "Cartilagineo", "Tendineo",
                        "Legamentoso", "Muscolare", "Osseo", "Altro"
                    ]
                )

                meccanismo = st.selectbox(
                    "Modalita",
                    [
                        "Trauma diretto",
                        "Trauma indiretto",
                        "Contatto",
                        "Non contatto",
                        "Sovraccarico",
                        "Caduta",
                        "Torsione",
                        "Altro"
                    ]
                )

                prognosi_giorni = st.number_input("Prognosi giorni", min_value=0, value=0)

            dinamica = st.text_area("Dinamica dell'evento")
            esame_obiettivo = st.text_area("Esame obiettivo")
            diagnosi = st.text_input("Diagnosi")
            trattamento = st.text_area("Trattamento")
            esami = st.text_area("Esami diagnostici eseguiti")
            note = st.text_area("Note")

            salva_infortunio = st.form_submit_button("Salva infortunio")

            if salva_infortunio:
                if not atleta or not diagnosi:
                    st.error("Inserisci almeno atleta e diagnosi.")
                else:
                    infortunio = {
                        "atleta": atleta,
                        "data_evento": data_evento,
                        "stagione": stagione,
                        "distretto": distretto,
                        "tipo_tessuto": tipo_tessuto,
                        "meccanismo": meccanismo,
                        "prognosi_giorni": prognosi_giorni,
                        "dinamica": dinamica,
                        "esame_obiettivo": esame_obiettivo,
                        "diagnosi": diagnosi,
                        "trattamento": trattamento,
                        "esami": esami,
                        "note": note
                    }
                    st.session_state.injuries.append(infortunio)
                    st.success(f"Infortunio salvato per {atleta}")

# =========================
# ARCHIVIO INFORTUNI
# =========================
elif menu == "Archivio infortuni":
    st.header("Archivio infortuni")

    if st.session_state.injuries:
        df_infortuni = pd.DataFrame(st.session_state.injuries)
        st.dataframe(df_infortuni, use_container_width=True)

        st.markdown("---")
        st.subheader("Dettaglio infortunio")

        opzioni = [
            f"{i+1} - {inj['atleta']} - {inj['diagnosi']}"
            for i, inj in enumerate(st.session_state.injuries)
        ]
        scelta = st.selectbox("Seleziona un infortunio", opzioni)

        indice = opzioni.index(scelta)
        inj = st.session_state.injuries[indice]

        st.write(f"**Atleta:** {inj['atleta']}")
        st.write(f"**Data evento:** {inj['data_evento']}")
        st.write(f"**Stagione:** {inj['stagione']}")
        st.write(f"**Distretto:** {inj['distretto']}")
        st.write(f"**Tipo tessuto:** {inj['tipo_tessuto']}")
        st.write(f"**Modalita:** {inj['meccanismo']}")
        st.write(f"**Prognosi giorni:** {inj['prognosi_giorni']}")
        st.write(f"**Dinamica evento:** {inj['dinamica']}")
        st.write(f"**Esame obiettivo:** {inj['esame_obiettivo']}")
        st.write(f"**Diagnosi:** {inj['diagnosi']}")
        st.write(f"**Trattamento:** {inj['trattamento']}")
        st.write(f"**Esami diagnostici eseguiti:** {inj['esami']}")
        st.write(f"**Note:** {inj['note']}")
    else:
        st.write("Nessun infortunio registrato.")

# =========================
# STATISTICHE
# =========================
elif menu == "Statistiche":
    st.header("Statistiche di fine stagione")

    if not st.session_state.injuries:
        st.write("Nessun dato disponibile.")
    else:
        df = pd.DataFrame(st.session_state.injuries)

        st.subheader("Totali")
        col1, col2 = st.columns(2)
        col1.metric("Numero infortuni", len(df))
        col2.metric("Atleti coinvolti", df["atleta"].nunique())

        st.markdown("---")

        st.subheader("Infortuni per distretto")
        st.dataframe(
            df["distretto"].value_counts().reset_index().rename(
                columns={"index": "Distretto", "distretto": "Totale"}
            ),
            use_container_width=True
        )

        st.subheader("Infortuni per tipo")
        st.dataframe(
            df["tipo_tessuto"].value_counts().reset_index().rename(
                columns={"index": "Tipo", "tipo_tessuto": "Totale"}
            ),
            use_container_width=True
        )

        st.subheader("Infortuni per modalita")
        st.dataframe(
            df["meccanismo"].value_counts().reset_index().rename(
                columns={"index": "Modalita", "meccanismo": "Totale"}
            ),
            use_container_width=True
        )
