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

import streamlit as st

# Konfiguracja strony
st.set_page_config(page_title="Platforma Ochrony ELEMENTO", page_icon="🏫", layout="centered")

st.image("https://via.placeholder.com/800x200.png?text=ELEMENTO+-+Cyber+Bezpieczenstwo+Przedszkoli", use_container_width=True) # Zastąp to w przyszłości Waszym prawdziwym banerem

st.title("Platforma Ochrony Przedszkoli")
st.markdown("Witaj! Wybierz moduł z poniższych zakładek, aby poznać standardy bezpieczeństwa lub przeprowadzić błyskawiczny audyt swojej placówki.")

# Tworzymy dwie zakładki (Tabs) dla porządku na stronie
tab1, tab2 = st.tabs(["🎬 Obejrzyj Wideo", "🛡️ Audyt KSAT 3"])

# ZAKŁADKA 1: FILM PROMOCYJNY (Zadanie 2)
with tab1:
    st.header("Cyber Przedszkole w 120 sekund")
    st.markdown("Czy wiesz, że w 2025 roku przedszkola stały się jednym z głównych celów ataków hakerskich? Zobacz nasz krótki materiał i dowiedz się, jak 4 Filary ELEMENTO chronią dane Waszych podopiecznych.")
    
    # TUTAJ WYŚWIETLAMY WYGENEROWANY FILM
    # Pobierz film z naszego czatu, nazwij go 'wideo_przedszkole.mp4' i wrzuć do folderu z aplikacją.
    try:
        st.video("wideo_przedszkole.mp4")
    except Exception:
        st.info("💡 Wskazówka techniczna: Pobierz wygenerowany przed chwilą film, zapisz go w folderze z projektem jako 'wideo_przedszkole.mp4' i odśwież stronę, aby się tutaj pojawił.")


# ZAKŁADKA 2: CHECKLISTA KSAT (Zadanie 1)
with tab2:
    st.header("Szybki Audyt Bezpieczeństwa IT")
    st.markdown("Odpowiedz na 3 krótkie pytania, aby sprawdzić, czy dane w Twojej placówce są bezpieczne.")
    st.divider()

    score = 0
    max_score = 30 

    # Pytanie 1: Legalność
    st.subheader("1. Legalność (Compliance)")
    q1 = st.radio(
        "Czy placówka posiada aktualne i podpisane umowy powierzenia przetwarzania danych (Art. 28 RODO) ze wszystkimi dostawcami IT?",
        ("Wybierz odpowiedź...", "Tak, mamy pełną dokumentację", "Częściowo / Nie wiem", "Nie, brakuje nam tego")
    )
    if q1 == "Tak, mamy pełną dokumentację": score += 10
    elif q1 == "Częściowo / Nie wiem": score += 5

    # Pytanie 2: Ciągłość
    st.subheader("2. Ciągłość Działania (Backup)")
    q2 = st.radio(
        "Czy wdrożono fizyczny i chmurowy backup w modelu 3-2-1 oraz kiedy ostatnio wykonano test odzyskiwania danych?",
        ("Wybierz odpowiedź...", "Tak, pełny model 3-2-1 (testowany w tym miesiącu)", "Mamy tylko pendrive/dysk zewnętrzny", "Brak procedur backupu")
    )
    if q2 == "Tak, pełny model 3-2-1 (testowany w tym miesiącu)": score += 10
    elif q2 == "Mamy tylko pendrive/dysk zewnętrzny": score += 5

    # Pytanie 3: Higiena
    st.subheader("3. Higiena Cyfrowa (Patch Management)")
    q3 = st.radio(
        "Czy stacje robocze i systemy są regularnie aktualizowane, a luki w zabezpieczeniach łatane?",
        ("Wybierz odpowiedź...", "Tak, proces jest zautomatyzowany", "Robi to informatyk 'z doskoku'", "Aktualizacje są wyłączone, bo spowalniają komputery")
    )
    if q3 == "Tak, proces jest zautomatyzowany": score += 10
    elif q3 == "Robi to informatyk 'z doskoku'": score += 5

    st.divider()

    # Generowanie Wyniku
    if st.button("📊 Generuj Scoreboard Bezpieczeństwa", type="primary"):
        if "Wybierz odpowiedź..." in [q1, q2, q3]:
            st.warning("Proszę odpowiedzieć na wszystkie pytania przed wygenerowaniem raportu.")
        else:
            final_percentage = int((score / max_score) * 100)
            
            st.subheader("Wynik Audytu KSAT:")
            st.progress(final_percentage / 100)
            
            if final_percentage == 100:
                st.success(f"**{final_percentage}% - Wzorowo!** Wasze przedszkole jest cyfrową twierdzą.")
            elif final_percentage >= 50:
                st.warning(f"**{final_percentage}% - Wymaga poprawy.** Macie podstawy, ale luki w systemie narażają Was na wyciek danych.")
                st.info("Zalecamy konsultację z ekspertem ELEMENTO w celu uszczelnienia procedur.")
            else:
                st.error(f"**{final_percentage}% - STAN KRYTYCZNY!** Obraz nędzy i rozpaczy. Dane dzieci są zagrożone.")
                st.error("Natychmiast umów darmowy audyt KSAT. Elemento Słupsk, ul. Leszczyńskiego 1.")

