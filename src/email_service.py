class EmailService:
    """
    A simplified email service class for demonstration purposes.
    In a real implementation, this would connect to actual email providers.
    """
    
    def __init__(self, provider="Gmail"):
        self.provider = provider
        self.connected = False
    
    def connect(self, username=None, password=None):
        """Simulate connecting to an email service"""
        # In a real implementation, this would use SMTP or API authentication
        self.connected = True
        return self.connected
    
    def get_emails(self, folder="inbox", limit=10):
        """Simulate retrieving emails from a folder"""
        # This is a mock implementation
        sample_emails = [
            {
                "id": "1",
                "subject": "Meeting Tomorrow",
                "sender": "john.doe@example.com",
                "date": "2025-03-12",
                "body": "Hi there, can we schedule a meeting tomorrow at 2 PM?",
                "read": False
            },
            {
                "id": "2",
                "subject": "Project Update",
                "sender": "manager@company.com",
                "date": "2025-03-11",
                "body": "Please provide an update on the current project status by Friday.",
                "read": True
            },
            {
                "id": "3",
                "subject": "Invoice #12345",
                "sender": "billing@service.com",
                "date": "2025-03-10",
                "body": "Your invoice #12345 is attached. Payment is due in 30 days.",
                "read": True
            }
        ]
        return sample_emails[:limit]
    
    def send_email(self, to, subject, body, cc=None, bcc=None):
        """Simulate sending an email"""
        # In a real implementation, this would use SMTP or API calls
        if not self.connected:
            raise Exception("Not connected to email service")
        
        # Simulate successful sending
        return {
            "success": True,
            "message": f"Email sent to {to} with subject '{subject}'",
            "id": "msg_123456"
        }
    
    def create_draft(self, to, subject, body, cc=None, bcc=None):
        """Simulate creating a draft email"""
        if not self.connected:
            raise Exception("Not connected to email service")
        
        # Simulate successful draft creation
        return {
            "success": True,
            "message": f"Draft created for {to} with subject '{subject}'",
            "id": "draft_123456"
        }
    
    def search_emails(self, query, folder="inbox", limit=10):
        """Simulate searching emails"""
        # This would implement actual search logic in a real service
        all_emails = self.get_emails(folder, 10)
        
        # Simple search implementation
        results = []
        for email in all_emails:
            if (query.lower() in email["subject"].lower() or 
                query.lower() in email["body"].lower() or
                query.lower() in email["sender"].lower()):
                results.append(email)
                
        return results[:limit]
