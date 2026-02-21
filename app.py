import streamlit as st
import google.generativeai as genai

# Konfiguracja strony i branding [cite: 25, 37]
st.set_page_config(page_title="Asystent KSAT 3 - ELEMENTO", page_icon="🏫")
st.sidebar.image("https://via.placeholder.com/150?text=ELEMENTO") # Miejsce na logo firmowe
st.sidebar.title("Wsparcie Techniczne")
st.sidebar.info("Oficjalny asystent firmy ELEMENTO dla pracowników przedszkoli obsługujących system KSAT 3.")

st.title("Pomoc techniczna KSAT 3")
st.markdown("Witaj! Jestem Twoją Cyfrową Ekspertką. Opisz swój problem, a pomogę Ci go rozwiązać krok po kroku.")

# Bezpieczne pobieranie klucza API z sekretów 
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception:
    st.error("Błąd konfiguracji: Brak klucza API w st.secrets. Dodaj klucz 'GOOGLE_API_KEY'.")
    st.stop()

# Inicjalizacja modelu gemini-1.5-flash [cite: 47]
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction="""Wklej tutaj treść System Promptu z punktu 1 powyżej."""
)

# Zarządzanie historią czatu [cite: 25]
if "messages" not in st.session_state:
    st.session_state.messages = []

# Wyświetlanie historii w dymkach czatu [cite: 48]
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Obsługa zapytań użytkownika
if prompt := st.chat_input("W czym mogę dzisiaj pomóc?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Przeszukuję instrukcje..."):
            try:
                # Generowanie odpowiedzi z uwzględnieniem kontekstu (RAG musi być skonfigurowany w AI Studio)
                response = model.generate_content(prompt)
                full_response = response.text
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Wystąpił nieoczekiwany problem: {e}. Prosimy o kontakt z serwisem ELEMENTO.")