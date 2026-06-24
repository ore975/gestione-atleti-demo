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

if "medications" not in st.session_state:
    st.session_state.medications = []

if "morphology" not in st.session_state:
    st.session_state.morphology = []

st.title("🏃 Gestione Atleti")
st.caption("Demo semplice online - struttura clinica atleta")

menu = st.sidebar.radio(
    "Menu",
    [
        "Dashboard",
        "Nuovo atleta",
        "Gestione generale",
        "Statistiche"
    ]
)


def athlete_label(a):
    return f"{a['cognome']} {a['nome']}"


def get_athlete_names():
    return [athlete_label(a) for a in st.session_state.athletes]


def get_items_for_athlete(items, atleta_nome):
    return [x for x in items if x.get("atleta") == atleta_nome]


# =========================
# DASHBOARD CLINICA
# =========================
if menu == "Dashboard":
    st.header("Dashboard Atleti")

    totale_atleti = len(st.session_state.athletes)
    totale_infortuni = len(st.session_state.injuries)
    totale_farmaci = len(st.session_state.medications)

    col1, col2, col3 = st.columns(3)
    col1.metric("Atleti registrati", totale_atleti)
    col2.metric("Infortuni registrati", totale_infortuni)
    col3.metric("Farmaci / integratori registrati", totale_farmaci)

    st.markdown("---")

    if not st.session_state.athletes:
        st.info("Non ci sono ancora atleti inseriti. Vai su 'Nuovo atleta'.")
    else:
        st.subheader("Elenco atleti")

        atleta_scelto = st.selectbox(
            "Seleziona atleta",
            get_athlete_names()
        )

        atleta = next(a for a in st.session_state.athletes if athlete_label(a) == atleta_scelto)
        infortuni_atleta = get_items_for_athlete(st.session_state.injuries, atleta_scelto)
        farmaci_atleta = get_items_for_athlete(st.session_state.medications, atleta_scelto)
        morfologia_atleta = get_items_for_athlete(st.session_state.morphology, atleta_scelto)

        col_left, col_right = st.columns([1, 2])

        with col_left:
            st.subheader("Scheda atleta")
            st.write(f"**Nome:** {atleta['nome']}")
            st.write(f"**Cognome:** {atleta['cognome']}")
            st.write(f"**Sport:** {atleta['sport']}")
            st.write(f"**Ruolo:** {atleta['ruolo']}")
            st.write(f"**Data di nascita:** {atleta['data_nascita']}")
            st.write(f"**Telefono:** {atleta['telefono']}")
            st.write(f"**Email:** {atleta['email']}")

            st.markdown("---")
            st.write("**Riepilogo rapido**")
            st.write(f"- Infortuni: {len(infortuni_atleta)}")
            st.write(f"- Farmaci / integratori: {len(farmaci_atleta)}")
            st.write(f"- Valutazioni morfologiche: {len(morfologia_atleta)}")

        with col_right:
            st.subheader("Cartella clinica")

            sezione = st.radio(
                "Sezione atleta",
                [
                    "1. Cartella clinica",
                    "2. Valutazione morfologica generale",
                    "3. Nuovo infortunio",
                    "4. Report infortuni",
                    "5. Farmacologia"
                ]
            )

            if sezione == "1. Cartella clinica":
                st.markdown("### Cartella clinica")
                st.write("**Anamnesi patologica remota**")
                st.write(atleta['anamnesi_remota'] or "Nessun dato inserito")
                st.write("**Anamnesi patologica prossima**")
                st.write(atleta['anamnesi_prossima'] or "Nessun dato inserito")
                st.write("**Allergie**")
                st.write(atleta['allergie'] or "Nessun dato inserito")
                st.write("**Note generali**")
                st.write(atleta['note'] or "Nessun dato inserito")

            elif sezione == "2. Valutazione morfologica generale":
                st.markdown("### Valutazione morfologica generale")

                with st.form("form_morfologia"):
                    col1, col2 = st.columns(2)

                    with col1:
                        altezza = st.text_input("Altezza")
                        peso = st.text_input("Peso")
                        bmi = st.text_input("BMI")
                        lateralita = st.selectbox("Lateralita", ["Destra", "Sinistra", "Ambidestra"])

                    with col2:
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
                    st.dataframe(pd.DataFrame(morfologia_atleta), use_container_width=True)
                else:
                    st.write("Nessuna valutazione morfologica inserita.")

            elif sezione == "3. Nuovo infortunio":
                st.markdown("### Nuovo infortunio")

                with st.form("form_infortunio_dashboard"):
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
                            ],
                            key="distretto_dashboard"
                        )

                    with col2:
                        tipo_tessuto = st.selectbox(
                            "Tipo",
                            [
                                "Articolare", "Cartilagineo", "Tendineo",
                                "Legamentoso", "Muscolare", "Osseo", "Altro"
                            ],
                            key="tipo_dashboard"
                        )
                        meccanismo = st.selectbox(
                            "Modalita",
                            [
                                "Trauma diretto", "Trauma indiretto", "Contatto", "Non contatto",
                                "Sovraccarico", "Caduta", "Torsione", "Altro"
                            ],
                            key="meccanismo_dashboard"
                        )
                        prognosi_giorni = st.number_input("Prognosi giorni", min_value=0, value=0, key="prog_dashboard")

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
                            infortunio = {
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
                            st.session_state.injuries.append(infortunio)
                            st.success(f"Infortunio salvato per {atleta_scelto}")

            elif sezione == "4. Report infortuni":
                st.markdown("### Report infortuni")

                if infortuni_atleta:
                    df_infortuni = pd.DataFrame(infortuni_atleta)
                    st.dataframe(df_infortuni, use_container_width=True)
                else:
                    st.write("Nessun infortunio registrato per questo atleta.")

            elif sezione == "5. Farmacologia":
                st.markdown("### Farmacologia")

                with st.form("form_farmaci_dashboard"):
                    col1, col2 = st.columns(2)

                    with col1:
                        tipo_prodotto = st.selectbox("Tipologia *", ["Farmaco", "Integratore"], key="tipo_far_dashboard")
                        nome_prodotto = st.text_input("Nome farmaco / integratore *")
                        principio_attivo = st.text_input("Principio attivo")
                        dosaggio = st.text_input("Dosaggio")
                        via_somministrazione = st.selectbox(
                            "Via di somministrazione",
                            ["Orale", "Intramuscolare", "Endovenosa", "Topica", "Inalatoria", "Altra"],
                            key="via_far_dashboard"
                        )
                        frequenza = st.text_input("Frequenza")

                    with col2:
                        data_inizio = st.text_input("Data inizio")
                        data_fine = st.text_input("Data fine")
                        motivo = st.text_input("Motivo / indicazione clinica")
                        prescrittore = st.text_input("Medico prescrittore")
                        tue = st.selectbox("Necessita TUE?", ["No", "Si", "Da valutare"], key="tue_dashboard")
                        documentazione = st.selectbox("Documentazione presente?", ["No", "Si"], key="doc_dashboard")

                    stato_verifica = st.selectbox(
                        "Stato verifica antidoping",
                        ["Da verificare", "Consentito", "Attenzione", "Vietato / da approfondire"],
                        key="stato_dashboard"
                    )

                    note = st.text_area("Note")

                    salva_farmaco = st.form_submit_button("Salva farmaco / integratore")

                    if salva_farmaco:
                        if not nome_prodotto:
                            st.error("Inserisci almeno il nome del prodotto.")
                        else:
                            farmaco = {
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
                            st.session_state.medications.append(farmaco)
                            st.success(f"Voce farmacologica salvata per {atleta_scelto}")

                if farmaci_atleta:
                    st.markdown("#### Archivio farmacologico")

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
    if st.session_state.athletes:
        st.subheader("Atleti inseriti")
        st.dataframe(pd.DataFrame(st.session_state.athletes), use_container_width=True)

# =========================
# GESTIONE GENERALE
# =========================
elif menu == "Gestione generale":
    st.header("Gestione generale")
    st.write("Questa area puo ospitare in futuro certificati, visite periodiche, test funzionali, idoneita sportiva e allegati.")
    st.write("Per ora la gestione clinica principale e concentrata nella Dashboard atleta.")

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
        st.dataframe(df["distretto"].value_counts().reset_index(), use_container_width=True)

        st.subheader("Infortuni per tipo")
        st.dataframe(df["tipo_tessuto"].value_counts().reset_index(), use_container_width=True)

        st.subheader("Infortuni per modalita")
        st.dataframe(df["meccanismo"].value_counts().reset_index(), use_container_width=True)

        if st.session_state.medications:
            st.markdown("---")
            st.subheader("Situazione Farmaci / Antidoping")
            df_farmaci = pd.DataFrame(st.session_state.medications)
            st.dataframe(df_farmaci["stato_verifica"].value_counts().reset_index(), use_container_width=True)
