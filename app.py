import streamlit as st
import google.generativeai as genai

# 1. KONFIGURACJA STRONY I BRANDING ELEMENTO [cite: 89]
st.set_page_config(
    page_title="Asystent KSAT 3 - ELEMENTO", 
    page_icon="🏫",
    layout="centered"
)

# Sidebar z informacjami o firmie [cite: 89, 112]
st.sidebar.title("Wsparcie ELEMENTO")
st.sidebar.markdown("""
### Cyfrowy Asystent KSAT 3
Dedykowane wsparcie techniczne dla placówek przedszkolnych.
---
**Status:** Aktywny 24/7 🟢
""")

st.title("Cyfrowy Asystent ELEMENTO")
st.info("Witaj! Jestem Twoją Cierpliwą Ekspertką. Pomogę Ci rozwiązać problemy z systemem KSAT 3 krok po kroku.") [cite: 88]

# 2. BEZPIECZNE KONFIGUROWANIE KLUCZA API [cite: 88]
try:
    # Pobiera klucz z .streamlit/secrets.toml lub ustawień Streamlit Cloud
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("Błąd konfiguracji: Brak klucza API w st.secrets. Dodaj klucz 'GOOGLE_API_KEY'.")
    st.stop()

# 3. DEFINICJA SYSTEM PROMPTU (Logika "Cierpliwej Ekspertki") [cite: 32, 88]
SYSTEM_INSTRUCTION = """
Jesteś "Cierpliwą Ekspertką" – asystentką wsparcia technicznego firmy ELEMENTO. [cite: 88]
Twoim zadaniem jest pomoc pracownikom przedszkoli (osobom nietechnicznym) w obsłudze programu KSAT 3. [cite: 82, 83]

ZASADY KOMUNIKACJI:
1. Pisz prostym językiem, unikaj żargonu IT. Zamiast "wyczyść cache", pisz "odśwież stronę przyciskiem F5". [cite: 32, 87]
2. Jeśli rozwiązanie wymaga nawigacji, opisz ją krok po kroku. [cite: 32, 101]
3. Bądź empatyczna i uspokajaj użytkownika w sytuacjach stresowych. [cite: 88, 102]
4. Jeśli użytkownik zgłasza błąd z wygasłym certyfikatem, najpierw zapytaj, czy widzi ikonę czerwonego kluczyka w dolnym rogu ekranu. [cite: 22]
5. TWOJA WIEDZA OGRANICZA SIĘ TYLKO DO KSAT 3. Jeśli ktoś zapyta o inne rzeczy (np. przepis na ciasto), uprzejmie odmów i przypomnij, że służysz wyłącznie do pomocy w KSAT 3. 
6. Jeśli nie znasz odpowiedzi, poproś o kontakt z serwisem ELEMENTO. [cite: 32]
"""

# Inicjalizacja modelu gemini-1.5-flash [cite: 110]
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=SYSTEM_INSTRUCTION
)

# 4. ZARZĄDZANIE HISTORIĄ CZATU (Dymki czatu) [cite: 111]
if "messages" not in st.session_state:
    st.session_state.messages = []

# Wyświetlanie historii rozmowy
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. OBSŁUGA ZAPYTAŃ UŻYTKOWNIKA [cite: 54, 58]
if prompt := st.chat_input("W czym mogę dzisiaj pomóc?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Przeszukuję instrukcje ELEMENTO..."):
            try:
                response = model.generate_content(prompt)
                full_response = response.text
                
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error("Wystąpił problem techniczny. Prosimy o kontakt z serwisem ELEMENTO.")