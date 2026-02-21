import streamlit as st
import google.generativeai as genai

# 1. KONFIGURACJA STRONY I BRANDING ELEMENTO
# Zgodnie z briefem: nazwa firmy i profesjonalny wygląd[cite: 89, 46].
st.set_page_config(
    page_title="Asystent KSAT 3 - ELEMENTO", 
    page_icon="🏫",
    layout="centered"
)

# Panel boczny (Sidebar) dla budowania wizytówki firmy[cite: 112].
st.sidebar.title("Wsparcie ELEMENTO")
st.sidebar.markdown("""
### Cyfrowy Asystent KSAT 3
Dedykowane wsparcie techniczne dla przedszkoli.
---
**Status:** Aktywny 24/7 🟢
""")

st.title("Cyfrowy Asystent ELEMENTO")
st.info("Witaj! Jestem Twoją Cierpliwą Ekspertką. Pomogę Ci rozwiązać problemy z systemem KSAT 3 krok po kroku[cite: 83, 88].")

# 2. BEZPIECZNE KONFIGUROWANIE KLUCZA API
# Klucze nie mogą być wpisane "na sztywno" w kodzie[cite: 88, 34].
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("Błąd konfiguracji: Nie znaleziono klucza API w st.secrets.")
    st.stop()

# 3. DEFINICJA SYSTEM PROMPTU (Logika "Cierpliwej Ekspertki")
# Łączymy wytyczne techniczne z instrukcją dla praktykantów[cite: 32, 88, 22].
SYSTEM_INSTRUCTION = """
Jesteś "Cierpliwą Ekspertką" – asystentką wsparcia technicznego firmy ELEMENTO. 
Twoim zadaniem jest pomoc pracownikom przedszkoli w obsłudze programu KSAT 3.

ZASADY KOMUNIKACJI:
1. Pisz prostym językiem, unikaj żargonu IT. Zamiast "wyczyść cache", pisz "odśwież stronę przyciskiem F5"[cite: 87].
2. Opisuj nawigację krok po kroku (np. "Kliknij w ikonę zębatki")[cite: 32].
3. Jeśli użytkownik zgłasza błąd z wygasłym certyfikatem, najpierw zapytaj, czy widzi ikonę czerwonego kluczyka w dolnym rogu ekranu[cite: 22].
4. TWOJA WIEDZA OGRANICZA SIĘ TYLKO DO KSAT 3. Jeśli ktoś zapyta o przepisy na ciasto, uprzejmie odmów i przypomnij o swojej roli[cite: 103].
5. Jeśli nie znasz odpowiedzi, poproś o kontakt z serwisem ELEMENTO[cite: 32].
"""

# Inicjalizacja modelu gemini-1.5-flash (najszybszy i najtańszy)[cite: 110].
model = genai.GenerativeModel(
    model_name='gemini-3.1-pro',
    system_instruction=SYSTEM_INSTRUCTION
)

# 4. ZARZĄDZANIE HISTORIĄ CZATU
if "messages" not in st.session_state:
    st.session_state.messages = []

# Wyświetlanie historii (używamy nowoczesnych dymków czatu)[cite: 52, 111].
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
        with st.spinner("Przeszukuję bazę wiedzy..."):
            try:
                response = model.generate_content(prompt)
                full_response = response.text
                
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                # Obsługa błędów (Test Błędu)[cite: 102].
                st.error("Przepraszam, wystąpił problem techniczny. Spokojnie, spróbuj ponownie za chwilę lub skontaktuj się z serwisem.")


