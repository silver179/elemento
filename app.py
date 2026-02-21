import streamlit as st
import google.generativeai as genai

# 1. KONFIGURACJA STRONY I BRANDING ELEMENTO
st.set_page_config(
    page_title="Asystent KSAT 3 - ELEMENTO", 
    page_icon="🏫",
    layout="centered"
)

# Sidebar z informacjami o firmie
st.sidebar.image("https://via.placeholder.com/150?text=ELEMENTO") # Tutaj możesz wstawić logo ELEMENTO
st.sidebar.title("Wsparcie ELEMENTO")
st.sidebar.markdown("""
### Cyfrowy Asystent KSAT 3
Dedykowane wsparcie techniczne dla placówek przedszkolnych.
---
**Status:** Aktywny 24/7 🟢
""")

st.title("Cyfrowy Asystent ELEMENTO")
st.info("Witaj! Jestem Twoją Cierpliwą Ekspertką. Pomogę Ci rozwiązać problemy z systemem KSAT 3 krok po kroku.")

# 2. BEZPIECZNE KONFIGUROWANIE KLUCZA API (zgodnie z wymogiem st.secrets)
try:
    # Pobiera klucz z .streamlit/secrets.toml (lokalnie) lub z panelu Streamlit Cloud
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("Błąd konfiguracji: Nie znaleziono klucza API. Upewnij się, że dodałeś GOOGLE_API_KEY do sekcji Secrets.")
    st.stop()

# 3. DEFINICJA SYSTEM PROMPTU (Logika "Cierpliwej Ekspertki")
SYSTEM_INSTRUCTION = """
Jesteś "Cierpliwą Ekspertką" – asystentką wsparcia technicznego firmy ELEMENTO. 
Twoim zadaniem jest pomoc pracownikom przedszkoli (osobom nietechnicznym) w obsłudze programu KSAT 3.

ZASADY KOMUNIKACJI:
1. Pisz prostym językiem, unikaj żargonu IT. Zamiast "wyczyść cache", pisz "odśwież stronę przyciskiem F5".
2. Jeśli rozwiązanie wymaga nawigacji, opisz ją krok po kroku (np. "Kliknij w ikonę zębatki").
3. Bądź empatyczna i uspokajaj użytkownika.
4. TWOJA WIEDZA OGRANICZA SIĘ TYLKO DO KSAT 3. Jeśli ktoś zapyta o inne rzeczy (np. przepis na ciasto), 
   uprzejmie odmów i przypomnij, że służysz wyłącznie do pomocy w KSAT 3.
5. Jeśli użytkownik zgłasza błąd z wygasłym certyfikatem, najpierw zapytaj, czy widzi ikonę 
   czerwonego kluczyka w dolnym rogu ekranu.
6. Jeśli nie znasz odpowiedzi, poproś o kontakt z serwisem ELEMENTO.
"""

# Inicjalizacja modelu gemini-1.5-flash
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=SYSTEM_INSTRUCTION
)

# 4. ZARZĄDZANIE HISTORIĄ CZATU (Streamlit Chat Elements)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Wyświetlanie historii rozmowy
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. OBSŁUGA ZAPYTAŃ UŻYTKOWNIKA
if prompt := st.chat_input("W czym mogę dzisiaj pomóc?"):
    # Dodanie pytania użytkownika do historii
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generowanie odpowiedzi asystenta
    with st.chat_message("assistant"):
        with st.spinner("Przeszukuję instrukcje ELEMENTO..."):
            try:
                # Wysłanie zapytania do modelu
                response = model.generate_content(prompt)
                full_response = response.text
                
                st.markdown(full_response)
                # Dodanie odpowiedzi do historii
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Wystąpił problem techniczny. Prosimy o kontakt z serwisem ELEMENTO.")
                print(f"Błąd: {e}")