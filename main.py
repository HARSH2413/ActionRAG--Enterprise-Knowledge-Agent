import streamlit as st
import shutil
import os
import config
from src.ingestion import ingest_documents
from src.retrieval import ask_question
from langchain_core.messages import HumanMessage, AIMessage

# --- UI CONFIG ---
st.set_page_config(page_title="Enterprise Brain", layout="wide")

# --- CSS: PINNED BOTTOM BAR & STYLING ---
st.markdown("""
<style>
    /* 1. Force the bottom container to be fixed and solid */
    [data-testid="stBottom"] {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: white;
        padding: 20px;
        z-index: 1000;
        box-shadow: 0px -2px 10px rgba(0,0,0,0.05);
    }

    /* 2. Style the input box container */
    [data-testid="stChatInput"] {
        max-width: 900px;
        margin: 0 auto;
    }

    /* 3. Push main content up so the last message isn't hidden */
    .main .block-container {
        padding-bottom: 140px; 
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Controls")
    
    # 1. API Key Form
    with st.form("api_key_form"):
        user_input_key = st.text_input("Groq API Key", type="password", help="Get key from console.groq.com")
        submitted = st.form_submit_button("✅ Submit Key")
    
    if submitted:
        st.session_state['api_key'] = user_input_key
        st.success("Key Saved!")
    
    api_key = st.session_state.get('api_key', None)

    st.divider()

    # 2. Model Selector
    smart_mode = st.toggle("Use Smart Model (70B)")
    
    st.divider()
    
    # 3. Reset Button (Windows Safe)
    if st.button("🗑️ Reset Knowledge Base"):
        st.session_state.pop("messages", None)
        if os.path.exists(config.VECTOR_DB_PATH):
            try:
                import gc
                gc.collect() 
                shutil.rmtree(config.VECTOR_DB_PATH)
                st.success("Reset Complete! Refreshing...")
                import time
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}. Please stop the app and delete 'vectorstore' folder manually.")

# --- TABS ---
tab1, tab2 = st.tabs(["💬 Chat", "🛠️ Admin"])

# --- ADMIN TAB ---
with tab2:
    st.header("Document Ingestion")
    files = st.file_uploader("Upload Files (PDF, DOCX, TXT)", accept_multiple_files=True)
    
    if st.button("Process Documents"):
        if not api_key:
            st.error("Please enter API Key in Sidebar.")
        else:
            with st.spinner("Ingesting..."):
                status = ingest_documents(files)
                if status == "Success":
                    st.success("Database Updated Successfully!")
                else:
                    st.error(status)

# --- CHAT TAB ---
with tab1:
    st.header("Secure Enterprise Brain")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display History & Action Buttons
    for i, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
            # UNIQUE FEATURE: Show "Draft Email" button only on the LATEST AI message
            if msg["role"] == "assistant" and i == len(st.session_state.messages) - 1:
                
                if st.button("✉️ Draft Email", key=f"email_btn_{i}"):
                    
                    email_prompt = f"""
                    Based on this information: "{msg['content']}"
                    Draft a short, professional email to a manager.
                    """
                    
                    with st.spinner("Drafting email..."):
                        # FIX: Pass empty list [] as history for email generation
                        email_draft, _, _ = ask_question(email_prompt, [], api_key, smart_mode)
                        st.info("⬇️ Copy this draft:")
                        st.code(email_draft, language="markdown")

    # Handle Input
    if query := st.chat_input("Ask a question about your documents..."):
        if not api_key:
            st.error("Please enter API Key in Sidebar.")
        else:
            # 1. User Message
            st.session_state.messages.append({"role": "user", "content": query})
            with st.chat_message("user"):
                st.markdown(query)

            # 2. PREPARE CHAT HISTORY
            chat_history = []
            for msg in st.session_state.messages[:-1]:
                if msg["role"] == "user":
                    chat_history.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    chat_history.append(AIMessage(content=msg["content"]))

            # 3. AI Message
            
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    answer, sources, latency = ask_question(query, chat_history, api_key, smart_mode)
                    
                    st.markdown(answer)
                    
                    # --- NEW: DETAILED CITATIONS ---
                    # Create an expander to show exactly where the AI looked
                    with st.expander("📚 View Source Evidence"):
                        for doc in sources:
                            source_name = doc.metadata.get("source", "Unknown")
                            # Try to get page number (PDFs have it, TXT files don't)
                            page_num = doc.metadata.get("page", "N/A")
                            
                            st.markdown(f"**📄 {source_name}** (Page: {page_num})")
                            # Show a small preview of the text used
                            st.caption(f"...{doc.page_content[:300]}...") 
                            st.divider()

                    st.caption(f"Latency: {latency:.2f}s")
            # 4. Save History
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
            # 5. Refresh to show the "Draft Email" button
            st.rerun()