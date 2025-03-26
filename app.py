import streamlit as st
import pandas as pd
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

st.title("Kursmatchare: UGL-utbildningar")

st.sidebar.header("Deltagarens information")
kund_namn = st.sidebar.text_input("Namn")
kund_epost = st.sidebar.text_input("E-post")
kund_telefon = st.sidebar.text_input("Telefon")
kund_ort = st.sidebar.text_input("Deltagarens ort/plats")
kund_max_res_tid = st.sidebar.slider("Max restid (timmar)", min_value=0.5, max_value=6.0, step=0.5)

st.sidebar.header("Filtrera på kurs")
val_vecka = st.sidebar.text_input("Vecka (valfri, skriv t.ex. 12)")
val_maxpris = st.sidebar.number_input("Maxpris (SEK)", min_value=0, value=20000, step=500)

uploaded_file = st.file_uploader("Ladda upp Excel-fil med kurser", type=["xlsx"])

# Initiera geolokalisering
geolocator = Nominatim(user_agent="kursmatchare")

def hamta_koordinater(ort):
    try:
        plats = geolocator.geocode(ort)
        if plats:
            return (plats.latitude, plats.longitude)
    except:
        return None

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        expected_cols = ["Vecka", "Anläggning", "Arrangör", "Pris"]
        if not all(col in df.columns for col in expected_cols):
            st.error(f"Excel-filen måste innehålla följande kolumner: {', '.join(expected_cols)}")
        else:
            df["Pris"] = pd.to_numeric(df["Pris"], errors="coerce")
            df["Vecka"] = pd.to_numeric(df["Vecka"], errors="coerce")

            # Hämta koordinater för deltagarens ort
            if kund_ort:
                deltagarens_position = hamta_koordinater(kund_ort)
                if deltagarens_position:
                    df["Distans_km"] = df["Anläggning"].apply(lambda x: geodesic(deltagarens_position, hamta_koordinater(x)).km if hamta_koordinater(x) else None)
                    # Antag restid = distans / 70 km/h
                    df["Restid_timmar"] = df["Distans_km"] / 70
                    df = df[df["Restid_timmar"] <= kund_max_res_tid]
                else:
                    st.warning("Kunde inte hitta koordinater för deltagarens ort.")

            if val_vecka:
                try:
                    vecka = int(val_vecka)
                    df = df[df["Vecka"] == vecka]
                except ValueError:
                    st.warning("Vänligen ange en giltig veckonummer.")

            df = df[df["Pris"] <= val_maxpris]

            st.subheader("Matchade kurser")
            st.write(f"Antal träffar: {len(df)}")
            st.dataframe(df.reset_index(drop=True))

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "Ladda ner som CSV",
                data=csv,
                file_name="matchade_kurser.csv",
                mime="text/csv"
            )

    except Exception as e:
        st.error(f"Fel vid läsning av Excel-fil: {e}")
else:
    st.info("Vänligen ladda upp en Excel-fil för att visa och filtrera kurser.")
