# utils/risk_checker.py
# Classifies cybersecurity risk levels based on keywords

def check_risk_level(user_input):
    """
    Check if user message contains risk-related keywords
    Returns risk level and badge
    """
    text = user_input.lower()
    
    # High risk keywords
    high_risk = [
        "otp", "shared my password", "clicked suspicious link",
        "gave my bank details", "ransomware attacked", "hacked",
        "virus on my computer", "someone logged in", "account compromised",
        "lost access", "money transferred", "fraud", "scammed"
    ]
    
    # Medium risk keywords
    medium_risk = [
        "suspicious email", "strange message", "unknown link",
        "public wifi", "weak password", "no antivirus",
        "not updated", "shared personal info", "unknown app installed"
    ]
    
    # Check high risk first
    for keyword in high_risk:
        if keyword in text:
            return {
                "level": "HIGH",
                "badge": "🔴 High Risk",
                "color": "red",
                "message": "⚠️ **Immediate action required!** This is a serious situation."
            }
    
    # Check medium risk
    for keyword in medium_risk:
        if keyword in text:
            return {
                "level": "MEDIUM",
                "badge": "🟡 Medium Risk",
                "color": "orange",
                "message": "⚠️ **Take action soon** to protect yourself."
            }
    
    return None  # No specific risk detected