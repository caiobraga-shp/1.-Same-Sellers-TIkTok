import streamlit as st

def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(
    page_title="📚 Pesquisa de Sellers",
    page_icon="assets/logo.svg",
    layout="wide"
)

# --- SIDEBAR: LOGO ---
st.sidebar.image(
    "assets/logo.svg",
    use_container_width=True
)

# --- PAGE SETUP ---
home_page = st.Page(
    "views/home.py",
    title="Home",
    default=True,
)

form_page = st.Page(
    "views/form.py",
    title="Formulário",
)

dashboard_page = st.Page(
    "views/dashboard.py",
    title="Dashboard",
)

# --- NAVIGATION ---
pg = st.navigation(
    [
        home_page,
        form_page,
        dashboard_page
    ]
)

# --- SIDEBAR FOOTER ---
st.sidebar.markdown("Made with ❤️ by **Shopee Competitive Intelligence**")

# --- RUN ---
pg.run()
