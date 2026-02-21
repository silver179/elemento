import streamlit as st
import google.generativeai as genai

# 1. KONFIGURACJA STRONY I BRANDING ELEMENTO
st.set_page_config(
    page_title="Asystent KSAT 3 - ELEMENTO", 
    page_icon="🏫",
    layout="centered"
)

# Panel boczny
st.sidebar.title("Wsparcie ELEMENTO")
st.sidebar.markdown("""
### Cyfrowy Asystent KSAT 3
Dedykowane wsparcie techniczne dla przedszkoli.
---
**Status:** Aktywny 24/7 🟢
""")

st.title("Cyfrowy Asystent ELEMENTO")
# POPRAWKA: Usunięto błędne znaczniki [cite], które powodowały błąd NameError
st.info("Witaj! Jestem Twoją Cierpliwą Ekspertką. Pomogę Ci rozwiązać problemy z systemem KSAT 3 krok po kroku.")

# 2. BEZPIECZNE KONFIGUROWANIE KLUCZA API
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("Błąd konfiguracji: Brak klucza API w st.secrets.")
    st.stop()

# 3. DEFINICJA SYSTEM PROMPTU (Osobowość)
SYSTEM_INSTRUCTION = """
Jesteś 'Cierpliwą Ekspertką' firmy ELEMENTO. Pomagasz w KSAT 3.
1. Pisz prostym językiem.
2. Nawigację opisuj krok po kroku.
3. Jeśli błąd dotyczy certyfikatu, zapytaj o 'czerwony kluczyk'.
4. Odmawiaj odpowiedzi na pytania niezwiązane z KSAT 3 (np. przepisy na ciasto).
"""

# 4. INICJALIZACJA MODELU (Naprawa błędu 404)
# Używamy stabilnej nazwy modelu bez dopisków v1beta
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=SYSTEM_INSTRUCTION
)

# 5. ZARZĄDZANIE HISTORIĄ CZATU
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. OBSŁUGA ZAPYTAŃ
if prompt := st.chat_input("W czym mogę dzisiaj pomóc?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Przeszukuję bazę wiedzy..."):
            try:
                # Wywołanie generowania treści
                response = model.generate_content(prompt)
                full_response = response.text
                
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception:
                # Komunikat wyświetlany w razie problemów technicznych (image_86740a.png)
                st.error("Przepraszam, wystąpił problem techniczny. Spokojnie, spróbuj ponownie za chwilę lub skontaktuj się z serwisem.")
