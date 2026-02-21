import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Asystent KSAT 3 - ELEMENTO", page_icon="🏫")

st.sidebar.title("Wsparcie ELEMENTO")
st.sidebar.info("Status: Aktywny 24/7 🟢")

st.title("Cyfrowy Asystent ELEMENTO")
st.info("Witaj! Jestem Twoją Cierpliwą Ekspertką. Pomogę Ci z systemem KSAT 3.")

try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("Błąd: Sprawdź klucz API w Secrets!")
    st.stop()

model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction="Jesteś Cierpliwą Ekspertką ELEMENTO. Pomagasz w KSAT 3. Nie podawaj przepisów na ciasto."
)

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
        except:
            st.error("Przepraszam, wystąpił problem techniczny. Spróbuj ponownie.")
