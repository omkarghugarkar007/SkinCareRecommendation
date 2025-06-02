import os
import streamlit as st
import chromadb
import chromadb.utils.embedding_functions as embedding_functions
from dotenv import load_dotenv

# Your helper functions
from utils import findIntent, getProducts, recommQuestion, recommFinalQuery, RAG

load_dotenv()

# ──────────────────────────────────────────────────────────────────────────────
# 1.  Initialize ChromaDB collections
# ──────────────────────────────────────────────────────────────────────────────

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    model_name="text-embedding-3-large",
    api_key=os.environ["OPENAI_API_KEY"]
)

# Catalog (products) collection
catalog_client = chromadb.PersistentClient(path="catalog")
catalog_collection = catalog_client.get_collection(
    name="catalogs",
    embedding_function=openai_ef
)

# Docs (for RAG) collection
docs_client = chromadb.PersistentClient(path="docs")
docs_collection = docs_client.get_collection(
    name="docs",
    embedding_function=openai_ef
)


# ──────────────────────────────────────────────────────────────────────────────
# 2.  Streamlit: set up page and session_state
# ──────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="SkinCare Recommendations",
    page_icon="🛍️",
    layout="centered"
)
st.title("🛍️ SkinCare Recommendations")

if "stage" not in st.session_state:
    # stage can be:
    #   "awaiting_initial" → waiting for the very first query
    #   "ask_followup"     → displayed initial products, now prompting follow-up
    #   "show_final"       → showing final products after follow-up
    #   "show_rag"         → showing RAG answer
    st.session_state.stage = "awaiting_initial"

if "user_input" not in st.session_state:
    st.session_state.user_input = ""


def try_rerun():
    """
    Attempt to call st.experimental_rerun(), but if it's missing,
    do nothing (Streamlit will re-render on next interaction).
    """
    try:
        st.experimental_rerun()
    except AttributeError:
        # If experimental_rerun() is not available, just pass.
        # The user can manually refresh the app to start over.
        pass


def on_submit():
    """
    Shared callback for the “Submit” button:
    - If stage == "awaiting_initial": process initial query
    - If stage == "ask_followup": process follow-up answer
    """
    text = st.session_state.user_input.strip()
    if not text:
        return

    # ──────────────────────────────────────────────────────────────────────────
    # 1) First‐time user query
    # ──────────────────────────────────────────────────────────────────────────
    if st.session_state.stage == "awaiting_initial":
        st.session_state.initial_query = text
        intent = findIntent(text)
        st.session_state.intent = intent

        if intent == "Recommendation":
            # Fetch initial products
            initial = getProducts(text, catalog_collection)
            st.session_state.initial_products = initial

            # Generate the follow-up question
            followup = recommQuestion(text)
            st.session_state.followup_question = followup

            # Move to next stage
            st.session_state.stage = "ask_followup"
            st.session_state.user_input = ""  # clear the input box

        else:
            # RAG‐based path
            hits = docs_collection.query(
                query_texts=[text],
                n_results=5
            )
            answer = RAG(hits, text)
            st.session_state.rag_answer = answer
            st.session_state.stage = "show_rag"
            st.session_state.user_input = ""  # clear the input box

    # ──────────────────────────────────────────────────────────────────────────
    # 2) Follow-up answer
    # ──────────────────────────────────────────────────────────────────────────
    elif st.session_state.stage == "ask_followup":
        followup_answer = text
        orig = st.session_state.initial_query

        refined_q = recommFinalQuery(orig, followup_answer)
        st.session_state.final_query = refined_q

        final_prods = getProducts(refined_q, catalog_collection)
        st.session_state.final_products = final_prods

        st.session_state.stage = "show_final"
        st.session_state.user_input = ""  # clear the input box


# ──────────────────────────────────────────────────────────────────────────────
# 3.  Render the single text_input & Submit button (when appropriate)
# ──────────────────────────────────────────────────────────────────────────────

if st.session_state.stage in ("awaiting_initial", "ask_followup"):
    if st.session_state.stage == "awaiting_initial":
        label = "Enter your question or request:"
    else:  # "ask_followup"
        label = st.session_state.followup_question

    st.text_input(
        label=label,
        key="user_input",
        on_change=on_submit
    )
    st.button("Submit", on_click=on_submit)


# ──────────────────────────────────────────────────────────────────────────────
# 4.  After submit: display content depending on new stage
# ──────────────────────────────────────────────────────────────────────────────

# 4A) If intent == "Recommendation" and now stage == "ask_followup",
#     show the initial products + the follow-up prompt (input box is already rendered above)
if st.session_state.stage == "ask_followup":
    st.subheader("💡 Initial Product Recommendations")
    initial = st.session_state.initial_products
    if not initial:
        st.info("No initial products matched your query.")
    else:
        for prod in initial:
            name = prod.get("Name", "Unknown Product")
            price = prod.get("price", "N/A")
            margin = prod.get("margin", 0.0)
            margin_pct = f"{margin * 100:.1f}%"
            with st.container():
                st.markdown(f"**{name}**  \nPrice: ${price}  \nMargin: {margin_pct}")
                st.markdown("---")
    st.stop()


# 4B) If the follow-up was just answered → stage == "show_final"
if st.session_state.stage == "show_final":
    st.subheader("🎯 Final Product Recommendations")
    final = st.session_state.final_products
    if not final:
        st.info("No products found for that refined query.")
    else:
        for prod in final:
            name = prod.get("Name", "Unknown Product")
            price = prod.get("price", "N/A")
            margin = prod.get("margin", 0.0)
            margin_pct = f"{margin * 100:.1f}%"
            with st.container():
                st.markdown(f"**{name}**  \nPrice: ${price}  \nMargin: {margin_pct}")
                st.markdown("---")

    # “Start Over” button
    if st.button("🔄 Start Over"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        try_rerun()

    # If rerun isn’t available, show a message:
    if "stage" not in st.session_state:
        st.markdown("• Session cleared. If nothing changed, please refresh the page to start over.")

    st.stop()


# 4C) If intent ≠ Recommendation → stage == "show_rag"
if st.session_state.stage == "show_rag":
    st.subheader("📖 RAG-Based Answer")
    st.write(st.session_state.rag_answer)

    if st.button("🔄 New Query"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        try_rerun()

    if "stage" not in st.session_state:
        st.markdown("• Session cleared. If nothing changed, please refresh the page to start a new query.")

    st.stop()
