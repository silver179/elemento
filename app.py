import streamlit as st
import google.generativeai as genai

# 1. KONFIGURACJA STRONY ELEMENTO
st.set_page_config(page_title="Platforma ELEMENTO - Cyber Bezpieczeństwo", page_icon="🏫", layout="centered")

# Sidebar z informacją o statusie
st.sidebar.title("Wsparcie ELEMENTO")
st.sidebar.info("Cyfrowy Asystent KSAT 3\nStatus: Aktywny 24/7 🟢")

# Nagłówek główny
st.title("Platforma Ochrony Przedszkoli")
st.markdown("Witaj! Wybierz moduł, aby poznać standardy bezpieczeństwa, porozmawiać z asystentem lub przeprowadzić audyt.")

# --- KONFIGURACJA MODELU GEMINI ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction="Jesteś Cierpliwą Ekspertką ELEMENTO. Pomagasz w KSAT 3. Nie podawaj przepisów na ciasto."
    )
except Exception:
    st.error("Błąd: Sprawdź konfigurację klucza API w Secrets!")
    st.stop()

# --- INTERFEJS Z ZAKŁADKAMI ---
tab1, tab2, tab3 = st.tabs(["💬 Cyfrowy Asystent", "🎬 Obejrzyj Wideo", "🛡️ Audyt KSAT 3"])

# ZAKŁADKA 1: CZAT (ASYSENT KSAT 3)
with tab1:
    st.header("Porozmawiaj z Ekspertką")
    st.info("Pomogę Ci rozwiązać problemy z systemem KSAT 3 krok po kroku.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("W czym mogę dzisiaj pomóc?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception:
                st.error("Przepraszam, wystąpił problem techniczny. Spróbuj ponownie za chwilę.")

# ZAKŁADKA 2: FILM PROMOCYJNY (Zadanie 2)
with tab2:
    st.header("Cyber Przedszkole w 120 sekund")
    st.markdown("Zobacz, jak 4 Filary ELEMENTO chronią dane Waszych podopiecznych.")
    
    try:
        st.video("wideo_przedszkole.mp4")
    except Exception:
        st.warning("Prześlij plik 'wideo_przedszkole.mp4' do folderu aplikacji, aby go wyświetlić.")

# ZAKŁADKA 3: CHECKLISTA AUDYTOWA (Zadanie 1)
with tab3:
    st.header("Szybki Audyt Bezpieczeństwa IT")
    st.markdown("Odpowiedz na pytania, aby wygenerować Scoreboard Bezpieczeństwa (0-100%).")
    st.divider()

    score = 0
    
    st.subheader("1. Legalność (Compliance)")
    q1 = st.radio(
        "Czy placówka posiada umowy powierzenia danych (Art. 28 RODO)?",
        ("Brak odpowiedzi", "Tak, kompletne", "Częściowo", "Nie")
    )
    if q1 == "Tak, kompletne": score += 10
    elif q1 == "Częściowo": score += 5

    st.subheader("2. Ciągłość (Backup)")
    q2 = st.radio(
        "Czy posiadacie backup 3-2-1 z testami odzysku?",
        ("Brak odpowiedzi", "Tak, regularnie testowany", "Mamy dyski zewnętrzne", "Brak backupu")
    )
    if q2 == "Tak, regularnie testowany": score += 10
    elif q2 == "Mamy dyski zewnętrzne": score += 5

    st.subheader("3. Higiena (Patch Management)")
    q3 = st.radio(
        "Czy systemy mają aktualne poprawki bezpieczeństwa?",
        ("Brak odpowiedzi", "Tak, automatyczne", "Czasami", "Nie")
    )
    if q3 == "Tak, automatyczne": score += 10
    elif q3 == "Czasami": score += 5

    if st.button("📊 Generuj Scoreboard", type="primary"):
        if "Brak odpowiedzi" in [q1, q2, q3]:
            st.warning("Uzupełnij wszystkie odpowiedzi!")
        else:
            final = int((score / 30) * 100)
            st.metric("Twój wynik bezpieczeństwa", f"{final}%")
            st.progress(final / 100)
            
            if final == 100:
                st.success("Wzorowo! Twoje przedszkole jest bezpieczne.")
            elif final >= 50:
                st.warning("Wymagana poprawa. Skontaktuj się z ELEMENTO Słupsk.")
            else:
                st.error("STAN KRYTYCZNY! Natychmiast umów audyt przy ul. Leszczyńskiego 1.")
