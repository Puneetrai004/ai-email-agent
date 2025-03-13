import re
from datetime import datetime

def extract_email_addresses(text):
    """Extract email addresses from text"""
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(email_pattern, text)

def extract_dates(text):
    """Extract dates from text (simplified)"""
    # This is a simplified implementation
    # In a real application, use a more robust date extraction library
    date_patterns = [
        r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
        r'\d{1,2}/\d{1,2}/\d{4}',  # MM/DD/YYYY or DD/MM/YYYY
        r'\d{1,2}-\d{1,2}-\d{4}'  # MM-DD-YYYY or DD-MM-YYYY
    ]
    
    dates = []
    for pattern in date_patterns:
        dates.extend(re.findall(pattern, text))
    
    return dates

def format_email_body(body, format_type="plain"):
    """Format email body based on type"""
    if format_type == "plain":
        return body
    elif format_type == "html":
        # Convert plain text to simple HTML
        paragraphs = body.split("\n\n")
        html_paragraphs = [f"<p>{p}</p>" for p in paragraphs]
        return "".join(html_paragraphs)
    else:
        return body

def get_current_date():
    """Get current date formatted for emails"""
    return datetime.now().strftime("%B %d, %Y")

def parse_email_thread(email_body):
    """Parse an email thread to extract previous messages"""
    # This is a simplified implementation
    # In a real application, use more robust parsing
    
    # Try to split by common reply indicators
    indicators = [
        "On .* wrote:",  # Standard email client format
        "From:",  # Another common indicator
        "-{3,}Original Message-{3,}"  # Original message indicator
    ]
    
    messages = [email_body]
    
    for indicator in indicators:
        new_messages = []
        for message in messages:
            parts = re.split(indicator, message, flags=re.MULTILINE)
            new_messages.extend(parts)
        messages = new_messages
    
    # Clean up and return messages
    return [msg.strip() for msg in messages if msg.strip()]
