import streamlit as st
import google.generativeai as genai

# 1. KONFIGURACJA STRONY I BRANDING ELEMENTO
# Zgodnie z briefem: budujemy wizytówkę firmy [cite: 89, 112]
st.set_page_config(
    page_title="Asystent KSAT 3 - ELEMENTO", 
    page_icon="🏫",
    layout="centered"
)

# Sidebar z informacjami o firmie i statusem wsparcia [cite: 89]
st.sidebar.title("Wsparcie ELEMENTO")
st.sidebar.markdown("""
### Cyfrowy Asystent KSAT 3
Dedykowane wsparcie techniczne dla placówek przedszkolnych.
---
**Status:** Aktywny 24/7 🟢
""")

st.title("Cyfrowy Asystent ELEMENTO")
st.info("Witaj! Jestem Twoją Cierpliwą Ekspertką. Pomogę Ci rozwiązać problemy z systemem KSAT 3 krok po kroku.")

# 2. BEZPIECZNE KONFIGUROWANIE KLUCZA API
# Używamy st.secrets, aby klucze nie były widoczne publicznie na GitHubie 
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("Błąd konfiguracji: Brak klucza API w st.secrets. Dodaj klucz 'GOOGLE_API_KEY' w panelu Streamlit Cloud.")
    st.stop()

# 3. DEFINICJA SYSTEM PROMPTU (Logika "Cierpliwej Ekspertki")
# Łączymy wytyczne z briefu oraz instrukcji dla praktykantów [cite: 32, 83, 88]
SYSTEM_INSTRUCTION = """
Jesteś "Cierpliwą Ekspertką" – asystentką wsparcia technicznego firmy ELEMENTO. 
Twoim zadaniem jest pomoc pracownikom przedszkoli (osobom nietechnicznym) w obsłudze programu KSAT 3.

ZASADY KOMUNIKACJI:
1. Pisz prostym językiem, unikaj żargonu IT (np. zamiast 'wyczyść cache', pisz 'odśwież stronę przyciskiem F5')[cite: 32, 87].
2. Jeśli rozwiązanie wymaga nawigacji, opisz ją krok po kroku[cite: 32, 101].
3. Bądź empatyczna, uspokajaj użytkownika i "prowadź go za rękę"[cite: 24, 88].
4. Jeśli użytkownik zgłasza błąd z wygasłym certyfikatem, najpierw zapytaj, czy widzi ikonę czerwonego kluczyka w dolnym rogu ekranu[cite: 22].
5. TWOJA WIEDZA OGRANICZA SIĘ TYLKO DO KSAT 3. Jeśli ktoś zapyta o inne rzeczy (np. przepis na ciasto), 
   uprzejmie odmów i przypomnij, że służysz wyłącznie do pomocy w KSAT 3[cite: 103].
6. Jeśli nie znasz odpowiedzi, poproś o kontakt bezpośredni z serwisem ELEMENTO[cite: 32].
"""

# Inicjalizacja modelu gemini-1.5-flash (najnowsza wersja stabilna) 
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=SYSTEM_INSTRUCTION
)

# 4. ZARZĄDZANIE HISTORIĄ CZATU (Streamlit Chat Elements) [cite: 111]
if "messages" not in st.session_state:
    st.session_state.messages = []

# Wyświetlanie historii rozmowy w nowoczesnych dymkach [cite: 111]
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
                # Generowanie odpowiedzi z modelu Gemini
                response = model.generate_content(prompt)
                full_response = response.text
                
                st.markdown(full_response)
                # Dodanie odpowiedzi do historii
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                # Obsługa błędów zgodnie z Testem Błędu [cite: 102]
                st.error("Przepraszam, wystąpił problem techniczny przy połączeniu z modelem. Spokojnie, spróbuj odświeżyć stronę lub skontaktuj się z serwisem ELEMENTO.")
                print(f"DEBUG ERROR: {e}")