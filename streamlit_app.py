import streamlit as st
from src.email_service import EmailService
from src.ai_agent import EmailAIAgent
import os

st.set_page_config(
    page_title="AI Email Agent",
    page_icon="📧",
    layout="wide"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "email_drafts" not in st.session_state:
    st.session_state.email_drafts = []

def main():
    st.title("📧 AI Email Agent")
    
    # Sidebar for configuration
    # In app.py, update the sidebar section:

with st.sidebar:
    st.header("Configuration")
    
    # Email provider selection
    email_provider = st.selectbox(
        "Select Email Provider",
        ["Gmail", "Outlook", "Custom SMTP"],
        index=0
    )
    
    # AI model selection - change to Groq options
    ai_model = st.selectbox(
        "Select AI Model",
        ["Groq - Llama 3 (8B)", "Groq - Mixtral (8x7B)"],
        index=0
    )
    
    # API Key input for Groq
    groq_api_key = st.text_input("Groq API Key", 
                               value=st.secrets.get("xai-SveSe6UyPDn1zSMzspehkB5UPBqHN6ht0RTaROpG1u4vU5YylKlNnMAnr8ejeEvsTRcq6bW5lPUcbM8U", ""),
                               type="password",
                               help="Get a free API key from groq.com")
    
    if groq_api_key:
        st.success("API Key provided!")
    else:
        st.warning("Please enter your Groq API key")
            
        st.divider()
        st.markdown("### About")
        st.markdown("This AI Email Agent helps you manage your inbox, draft responses, and organize emails.")
        st.markdown("Built with Streamlit and LangChain")
    
    # Main content area with tabs
    tab1, tab2, tab3 = st.tabs(["Email Assistant", "Draft Emails", "Settings"])
    
    with tab1:
        st.header("Email Assistant")
        
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("How can I help with your emails today?"):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Display assistant response
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                
                # Process the request with AI agent
                try:
                    agent = EmailAIAgent(api_key=groq_api_key)
                    response = agent.process_request(prompt)
                    
                    message_placeholder.markdown(response)
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                    # If response is a draft email, add to drafts
                    if "Here's a draft" in response:
                        draft = response.split("``````")[1] if "``````" in response and len(response.split("``````")) > 1 else response
                        st.session_state.email_drafts.append(draft)
                        
                except Exception as e:
                    message_placeholder.error(f"Error: {str(e)}")
    
    with tab2:
        st.header("Draft Emails")
        
        if not st.session_state.email_drafts:
            st.info("No draft emails yet. Ask the assistant to create one for you!")
        else:
            for i, draft in enumerate(st.session_state.email_drafts):
                with st.expander(f"Draft {i+1}"):
                    st.text_area("Email Content", draft, height=200, key=f"draft_{i}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Send Email", key=f"send_{i}"):
                            st.success("Email sent successfully!")
                    with col2:
                        if st.button("Delete Draft", key=f"delete_{i}"):
                            st.session_state.email_drafts.pop(i)
                            st.rerun()
    
    with tab3:
        st.header("Settings")
        st.info("This is a demo application. In a real implementation, you would configure email credentials here.")
        
        # Example settings form
        with st.form("settings_form"):
            st.subheader("Email Settings")
            email_address = st.text_input("Email Address")
            email_password = st.text_input("App Password", type="password", 
                                          help="For Gmail, use an App Password instead of your regular password")
            
            st.subheader("AI Settings")
            temperature = st.slider("AI Temperature", 0.0, 1.0, 0.7, 
                                   help="Higher values make the output more random, lower values make it more deterministic")
            
            submit = st.form_submit_button("Save Settings")
            if submit:
                st.success("Settings saved successfully!")

if __name__ == "__main__":
    main()
