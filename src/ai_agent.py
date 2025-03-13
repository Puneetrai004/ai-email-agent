import streamlit as st
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq  # Import Groq instead of OpenAI

class EmailAIAgent:
    """
    AI agent for email management using Groq's free LLM API.
    """
    
    def __init__(self, api_key=None):
        # Use provided API key or get from Streamlit secrets
        self.api_key = api_key or st.secrets.get("xai-SveSe6UyPDn1zSMzspehkB5UPBqHN6ht0RTaROpG1u4vU5YylKlNnMAnr8ejeEvsTRcq6bW5lPUcbM8U", "")
        
        # Initialize the Groq LLM
        self.llm = ChatGroq(
            api_key=self.api_key,
            model_name="llama3-8b-8192",  # Free Llama 3 model on Groq
            temperature=0.7
        )
        
        # Create email drafting prompt template
        self.email_template = PromptTemplate(
            input_variables=["recipient", "subject", "context"],
            template="""
            Write a professional email to {recipient} about {subject}.
            
            Additional context: {context}
            
            The email should be concise, professional, and include:
            1. A proper greeting
            2. Clear and direct message
            3. A professional closing
            
            Format the email with proper structure.
            """
        )
        
        # Create email chain
        self.email_chain = LLMChain(llm=self.llm, prompt=self.email_template)
    
    def process_request(self, prompt):
        """Process a user request and generate a response using Groq LLM"""
        prompt_lower = prompt.lower()
        
        try:
            # Handle different types of requests
            if "draft" in prompt_lower and "email" in prompt_lower:
                return self._generate_email_draft(prompt)
            
            elif "summarize" in prompt_lower or "summary" in prompt_lower:
                return self._generate_email_summary(prompt)
            
            elif "categorize" in prompt_lower or "organize" in prompt_lower:
                return self._categorize_emails(prompt)
                
            elif "search" in prompt_lower or "find" in prompt_lower:
                return self._search_emails(prompt)
                
            else:
                # General query - direct to LLM
                response = self.llm.invoke(
                    f"You are an AI email assistant. Respond to this user query about email management: {prompt}"
                )
                return response.content
                
        except Exception as e:
            return f"I encountered an error: {str(e)}. Please check your API key or try again later."
    
    def _generate_email_draft(self, prompt):
        """Generate an email draft based on user prompt using Groq LLM"""
        # Extract potential recipient, subject, and context from prompt
        recipient = "recipient@example.com"
        subject = "Meeting Request"
        context = prompt
        
        # Try to extract recipient
        if "to" in prompt.lower():
            parts = prompt.lower().split("to")
            if len(parts) > 1:
                recipient_part = parts[1].split()[0]
                if "@" in recipient_part:
                    recipient = recipient_part
        
        # Try to extract subject
        if "about" in prompt.lower() or "subject" in prompt.lower():
            if "about" in prompt.lower():
                parts = prompt.lower().split("about")
            else:
                parts = prompt.lower().split("subject")
                
            if len(parts) > 1:
                subject = parts[1].split(".")[0].strip()
        
        # Generate the email using LangChain
        try:
            email_result = self.email_chain.invoke({
                "recipient": recipient,
                "subject": subject,
                "context": context
            })
            
            return f"Here's a draft email for you:\n\n``````\n\nYou can edit this draft before sending."
            
        except Exception as e:
            return f"I couldn't generate an email draft: {str(e)}. Please check your Groq API key."
    
    def _generate_email_summary(self, prompt):
        """Generate a summary of emails using Groq LLM"""
        try:
            response = self.llm.invoke(
                "You are an AI email assistant. Generate a summary of recent emails in a user's inbox. " +
                "Format the response as a numbered list with the subject, sender, and a brief description of each email."
            )
            return response.content
        except Exception as e:
            return f"I couldn't generate an email summary: {str(e)}. Please check your Groq API key."
    
    def _categorize_emails(self, prompt):
        """Categorize emails based on content using Groq LLM"""
        try:
            response = self.llm.invoke(
                "You are an AI email assistant. Categorize a set of emails into logical groups like Work/Professional, " +
                "Personal, Financial, etc. Format the response with category headers and bullet points for each email."
            )
            return response.content
        except Exception as e:
            return f"I couldn't categorize emails: {str(e)}. Please check your Groq API key."
    
    def _search_emails(self, prompt):
        """Search for emails based on query using Groq LLM"""
        search_term = prompt.split("search")[1].strip() if "search" in prompt.lower() else prompt.split("find")[1].strip()
        
        try:
            response = self.llm.invoke(
                f"You are an AI email assistant. Show search results for emails containing the term '{search_term}'. " +
                "Format the response as a numbered list with the subject, sender, date, and a brief snippet of each email."
            )
            return response.content
        except Exception as e:
            return f"I couldn't search emails: {str(e)}. Please check your Groq API key."
