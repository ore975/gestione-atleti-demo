import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Gestione Atleti",
    page_icon="🏃",
    layout="wide"
)

# =========================
# STATO APP
# =========================
if "athletes" not in st.session_state:
    st.session_state.athletes = []

if "injuries" not in st.session_state:
    st.session_state.injuries = []

if "medications" not in st.session_state:
    st.session_state.medications = []

if "morphology" not in st.session_state:
    st.session_state.morphology = []

if "selected_athlete" not in st.session_state:
    st.session_state.selected_athlete = None


# =========================
# HELPERS
# =========================
def athlete_label(a):
    return f"{a['cognome']} {a['nome']}"


def athlete_options():
    return [athlete_label(a) for a in st.session_state.athletes]


def get_athlete_by_label(label):
    for a in st.session_state.athletes:
        if athlete_label(a) == label:
            return a
    return None


def get_items_for_athlete(items, atleta_nome):
    return [x for x in items if x.get("atleta") == atleta_nome]


def set_selected_athlete(nome_atleta):
    st.session_state.selected_athlete = nome_atleta


st.title("🏃 Gestione Atleti")
st.caption("Demo semplice online - struttura organizzata per evolvere senza perdere lo storico")

menu = st.sidebar.radio(
    "Menu",
    [
        "Dashboard",
        "Nuovo atleta",
        "Scheda atleta",
        "Infortuni",
        "Farmacologia",
        "Statistiche"
    ]
)

# =========================
# DASHBOARD
# =========================
if menu == "Dashboard":
    st.header("Dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric("Atleti registrati", len(st.session_state.athletes))
    col2.metric("Infortuni registrati", len(st.session_state.injuries))
    col3.metric("Farmaci / integratori registrati", len(st.session_state.medications))

    st.markdown("---")
    st.subheader("Elenco atleti")

    if not st.session_state.athletes:
        st.info("Non ci sono ancora atleti inseriti. Vai su 'Nuovo atleta'.")
    else:
        elenco = []
        for a in st.session_state.athletes:
            elenco.append({
                "Atleta": athlete_label(a),
                "Sport": a.get("sport", ""),
                "Ruolo": a.get("ruolo", ""),
                "Data di nascita": a.get("data_nascita", "")
            })

        st.dataframe(pd.DataFrame(elenco), use_container_width=True, hide_index=True)

        atleta_dashboard = st.selectbox(
            "Seleziona atleta da aprire",
            athlete_options(),
            key="dashboard_select_athlete"
        )

        if st.button("Apri atleta", key="open_athlete_from_dashboard"):
            set_selected_athlete(atleta_dashboard)
            st.success(f"Atleta selezionato: {atleta_dashboard}. Vai su 'Scheda atleta'.")

# =========================
# NUOVO ATLETA
# =========================
elif menu == "Nuovo atleta":
    st.header("Nuovo atleta")

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

        st.subheader("Cartella clinica iniziale")
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
                st.session_state.selected_athlete = athlete_label(atleta)
                st.success(f"Atleta salvato: {cognome} {nome}")

# =========================
# SCHEDA ATLETA
# =========================
elif menu == "Scheda atleta":
    st.header("Scheda atleta")

    if not st.session_state.athletes:
        st.info("Non ci sono atleti registrati. Vai su 'Nuovo atleta'.")
    else:
        default_index = 0
        if st.session_state.selected_athlete in athlete_options():
            default_index = athlete_options().index(st.session_state.selected_athlete)

        atleta_scelto = st.selectbox(
            "Seleziona atleta",
            athlete_options(),
            index=default_index,
            key="scheda_atleta_select"
        )
        st.session_state.selected_athlete = atleta_scelto

        atleta = get_athlete_by_label(atleta_scelto)
        morfologia_atleta = get_items_for_athlete(st.session_state.morphology, atleta_scelto)
        infortuni_atleta = get_items_for_athlete(st.session_state.injuries, atleta_scelto)
        farmaci_atleta = get_items_for_athlete(st.session_state.medications, atleta_scelto)

        col1, col2 = st.columns([1, 2])

        with col1:
            st.subheader("Dati anagrafici")
            st.write(f"**Nome:** {atleta['nome']}")
            st.write(f"**Cognome:** {atleta['cognome']}")
            st.write(f"**Sport:** {atleta['sport']}")
            st.write(f"**Ruolo:** {atleta['ruolo']}")
            st.write(f"**Data di nascita:** {atleta['data_nascita']}")
            st.write(f"**Telefono:** {atleta['telefono']}")
            st.write(f"**Email:** {atleta['email']}")

            st.markdown("---")
            st.subheader("Alert rapidi")
            st.write(f"**Allergie:** {atleta['allergie'] or 'Nessuna indicata'}")
            st.write(f"**Infortuni registrati:** {len(infortuni_atleta)}")
            st.write(f"**Farmaci / integratori:** {len(farmaci_atleta)}")

        with col2:
            sezione = st.radio(
                "Area atleta",
                [
                    "Cartella clinica",
                    "Valutazione morfologica generale"
                ],
                key="scheda_area_radio"
            )

            if sezione == "Cartella clinica":
                st.subheader("Cartella clinica")
                st.write("**Anamnesi patologica remota**")
                st.write(atleta['anamnesi_remota'] or "Nessun dato inserito")
                st.write("**Anamnesi patologica prossima**")
                st.write(atleta['anamnesi_prossima'] or "Nessun dato inserito")
                st.write("**Allergie**")
                st.write(atleta['allergie'] or "Nessun dato inserito")
                st.write("**Note generali**")
                st.write(atleta['note'] or "Nessun dato inserito")

            elif sezione == "Valutazione morfologica generale":
                st.subheader("Valutazione morfologica generale")

                with st.form("form_morfologia"):
                    c1, c2 = st.columns(2)

                    with c1:
                        altezza = st.text_input("Altezza")
                        peso = st.text_input("Peso")
                        bmi = st.text_input("BMI")
                        lateralita = st.selectbox("Lateralita", ["Destra", "Sinistra", "Ambidestra"])

                    with c2:
                        postura = st.text_input("Valutazione posturale")
                        appoggio = st.text_input("Appoggio plantare")
                        massa_muscolare = st.text_input("Osservazioni massa muscolare")
                        note_morfologia = st.text_area("Note morfologiche")

                    salva_morfologia = st.form_submit_button("Salva valutazione morfologica")

                    if salva_morfologia:
                        voce = {
                            "atleta": atleta_scelto,
                            "altezza": altezza,
                            "peso": peso,
                            "bmi": bmi,
                            "lateralita": lateralita,
                            "postura": postura,
                            "appoggio": appoggio,
                            "massa_muscolare": massa_muscolare,
                            "note": note_morfologia
                        }
                        st.session_state.morphology.append(voce)
                        st.success("Valutazione morfologica salvata")

                if morfologia_atleta:
                    st.markdown("#### Storico valutazioni")
                    st.dataframe(pd.DataFrame(morfologia_atleta), use_container_width=True, hide_index=True)
                else:
                    st.write("Nessuna valutazione morfologica inserita.")

# =========================
# INFORTUNI
# =========================
elif menu == "Infortuni":
    st.header("Infortuni")

    if not st.session_state.athletes:
        st.info("Non ci sono atleti registrati. Vai su 'Nuovo atleta'.")
    else:
        default_index = 0
        if st.session_state.selected_athlete in athlete_options():
            default_index = athlete_options().index(st.session_state.selected_athlete)

        atleta_scelto = st.selectbox(
            "Seleziona atleta",
            athlete_options(),
            index=default_index,
            key="infortuni_select_athlete"
        )
        st.session_state.selected_athlete = atleta_scelto

        tab1, tab2 = st.tabs(["Nuovo infortunio", "Report infortuni"])

        with tab1:
            with st.form("form_infortunio"):
                c1, c2 = st.columns(2)

                with c1:
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

                with c2:
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
                            "Trauma diretto", "Trauma indiretto", "Contatto", "Non contatto",
                            "Sovraccarico", "Caduta", "Torsione", "Altro"
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
                    if not diagnosi:
                        st.error("Inserisci almeno la diagnosi.")
                    else:
                        voce = {
                            "atleta": atleta_scelto,
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
                        st.session_state.injuries.append(voce)
                        st.success(f"Infortunio salvato per {atleta_scelto}")

        with tab2:
            infortuni_atleta = get_items_for_athlete(st.session_state.injuries, atleta_scelto)
            if infortuni_atleta:
                st.dataframe(pd.DataFrame(infortuni_atleta), use_container_width=True, hide_index=True)
            else:
                st.write("Nessun infortunio registrato per questo atleta.")

# =========================
# FARMACOLOGIA
# =========================
elif menu == "Farmacologia":
    st.header("Farmacologia")

    if not st.session_state.athletes:
        st.info("Non ci sono atleti registrati. Vai su 'Nuovo atleta'.")
    else:
        default_index = 0
        if st.session_state.selected_athlete in athlete_options():
            default_index = athlete_options().index(st.session_state.selected_athlete)

        atleta_scelto = st.selectbox(
            "Seleziona atleta",
            athlete_options(),
            index=default_index,
            key="farmacologia_select_athlete"
        )
        st.session_state.selected_athlete = atleta_scelto

        tab1, tab2 = st.tabs(["Nuovo farmaco / integratore", "Archivio farmacologico"])

        with tab1:
            with st.form("form_farmaco"):
                c1, c2 = st.columns(2)

                with c1:
                    tipo_prodotto = st.selectbox("Tipologia *", ["Farmaco", "Integratore"])
                    nome_prodotto = st.text_input("Nome farmaco / integratore *")
                    principio_attivo = st.text_input("Principio attivo")
                    dosaggio = st.text_input("Dosaggio")
                    via_somministrazione = st.selectbox(
                        "Via di somministrazione",
                        ["Orale", "Intramuscolare", "Endovenosa", "Topica", "Inalatoria", "Altra"]
                    )
                    frequenza = st.text_input("Frequenza")

                with c2:
                    data_inizio = st.text_input("Data inizio")
                    data_fine = st.text_input("Data fine")
                    motivo = st.text_input("Motivo / indicazione clinica")
                    prescrittore = st.text_input("Medico prescrittore")
                    tue = st.selectbox("Necessita TUE?", ["No", "Si", "Da valutare"])
                    documentazione = st.selectbox("Documentazione presente?", ["No", "Si"])

                stato_verifica = st.selectbox(
                    "Stato verifica antidoping",
                    ["Da verificare", "Consentito", "Attenzione", "Vietato / da approfondire"]
                )
                note = st.text_area("Note")

                salva_farmaco = st.form_submit_button("Salva farmaco / integratore")

                if salva_farmaco:
                    if not nome_prodotto:
                        st.error("Inserisci almeno il nome del prodotto.")
                    else:
                        voce = {
                            "atleta": atleta_scelto,
                            "tipologia": tipo_prodotto,
                            "nome_prodotto": nome_prodotto,
                            "principio_attivo": principio_attivo,
                            "dosaggio": dosaggio,
                            "via_somministrazione": via_somministrazione,
                            "frequenza": frequenza,
                            "data_inizio": data_inizio,
                            "data_fine": data_fine,
                            "motivo": motivo,
                            "prescrittore": prescrittore,
                            "tue": tue,
                            "documentazione": documentazione,
                            "stato_verifica": stato_verifica,
                            "note": note
                        }
                        st.session_state.medications.append(voce)
                        st.success(f"Voce farmacologica salvata per {atleta_scelto}")

        with tab2:
            farmaci_atleta = get_items_for_athlete(st.session_state.medications, atleta_scelto)
            if farmaci_atleta:
                for voce in farmaci_atleta:
                    stato = voce.get("stato_verifica", "")
                    colore = "black"
                    if stato == "Vietato / da approfondire":
                        colore = "red"
                    elif stato == "Attenzione":
                        colore = "orange"
                    elif stato == "Consentito":
                        colore = "green"

                    st.markdown(
                        f"""
                        <div style='border:1px solid #ddd; padding:12px; border-radius:8px; margin-bottom:10px;'>
                            <div><strong>{voce['nome_prodotto']}</strong> - {voce['tipologia']}</div>
                            <div>Principio attivo: {voce['principio_attivo']}</div>
                            <div>Dosaggio: {voce['dosaggio']}</div>
                            <div>Motivo: {voce['motivo']}</div>
                            <div>Prescrittore: {voce['prescrittore']}</div>
                            <div>Stato antidoping: <span style='color:{colore}; font-weight:bold;'>{stato}</span></div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.write("Nessun farmaco o integratore registrato per questo atleta.")

# =========================
# STATISTICHE
# =========================
elif menu == "Statistiche":
    st.header("Statistiche")

    col1, col2, col3 = st.columns(3)
    col1.metric("Numero infortuni", len(st.session_state.injuries))
    col2.metric("Atleti coinvolti", len(set([x.get("atleta") for x in st.session_state.injuries])) if st.session_state.injuries else 0)
    col3.metric("Numero farmaci / integratori", len(st.session_state.medications))

    if st.session_state.injuries:
        st.markdown("---")
        df = pd.DataFrame(st.session_state.injuries)

        st.subheader("Infortuni per distretto")
        st.dataframe(df["distretto"].value_counts().reset_index(), use_container_width=True, hide_index=True)

        st.subheader("Infortuni per tipo")
        st.dataframe(df["tipo_tessuto"].value_counts().reset_index(), use_container_width=True, hide_index=True)

        st.subheader("Infortuni per modalita")
        st.dataframe(df["meccanismo"].value_counts().reset_index(), use_container_width=True, hide_index=True)

    if st.session_state.medications:
        st.markdown("---")
        st.subheader("Stato verifica antidoping")
        df_farmaci = pd.DataFrame(st.session_state.medications)
        st.dataframe(df_farmaci["stato_verifi
