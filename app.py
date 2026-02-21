import streamlit as st
import google.generativeai as genai
# Konfiguracja strony
st.set_page_config(page_title="Asystent KSAT 3 - ELEMENTO", page_icon="💻")
st.title("Pomoc techniczna KSAT 3")
st.info("Witaj! Opisz swój problem z programem, a postaram się pomóc krok po kroku.")
# Setup modelu (Klucz API wpiszcie tutaj lub w sekretach Streamlit)
genai.configure(api_key="TWÓJ_KLUCZ_API_Z_AI_STUDIO")
model = genai.GenerativeModel('gemini-1.5-flash',
system_instruction="TWOJA_INSTRUKCJA_SYSTEMOWA")
# Historia czatu
if "messages" not in st.session_state:
st.session_state.messages = []
for message in st.session_state.messages:
with st.chat_message(message["role"]):
st.markdown(message["content"])
# Obsługa zapytania
if prompt := st.chat_input("W czym mogę pomóc?"):
st.session_state.messages.append({"role": "user", "content": prompt})
with st.chat_message("user"):
st.markdown(prompt)
with st.chat_message("assistant"):
response = model.generate_content(prompt)
st.markdown(response.text)
st.session_state.messages.append({"role": "assistant", "content": response.text})