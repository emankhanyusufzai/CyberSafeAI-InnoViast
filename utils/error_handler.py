# utils/error_handler.py
# Handles all error messages for CyberSafe AI

def handle_empty_input():
    """Handle empty or whitespace-only input"""
    return "⚠️ Please type a question before sending! I'm here to help with cybersecurity topics. 🛡️"

def handle_api_error():
    """Handle API connection errors"""
    return "❌ I'm having trouble connecting right now. Please check your internet connection and try again in a moment."

def handle_long_input():
    """Handle extremely long messages"""
    return "⚠️ Your message is too long! Please keep your question under 500 characters so I can help you better. 🛡️"

def handle_timeout_error():
    """Handle timeout errors"""
    return "⏱️ The request took too long. Please try again — I'm usually much faster! 🛡️"

def handle_unknown_error():
    """Handle any unknown errors"""
    return "🔧 Something unexpected happened. Please refresh the page and try again!"

def validate_input(user_input):
    """
    Validate user input before sending to API
    Returns: (is_valid, error_message)
    """
    # Check empty input
    if not user_input or not user_input.strip():
        return False, handle_empty_input()
    
    # Check too long
    if len(user_input) > 500:
        return False, handle_long_input()
    
    return True, None