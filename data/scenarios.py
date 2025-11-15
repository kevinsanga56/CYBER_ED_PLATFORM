phishing_scenarios = [
    {
        'id': 1,
        'sender': "M-Pesa Support <mpesa-alert@payments-secure-ke.com>",
        'subject': "URGENT: Transaction Reversal Failed - Confirm PIN",
        'body': "Dear Customer, a recent transaction reversal failed due to a system error. To secure your account and funds, you must click the link below to confirm your Mobile PIN. Failure to confirm within 30 minutes will result in account suspension. Click here to confirm PIN:",
        'phishing_link_text': "Secure M-Pesa PIN Confirmation",
        'phishing_link_url': "#", # Placeholder for the form submission
        'safe_link_text': "I will call the official M-Pesa contact number",
        'safe_link_url': "#",
        'explanation': "SCAM DETECTED! M-Pesa will NEVER ask for your PIN via email or a link. Red flags include the urgent threat of suspension, the suspicious sender email address, and the demand for personal security details."
    },
    {
        'id': 2,
        'sender': "Supplier Invoice Department <invoices@accounts-procurement.net>",
        'subject': "ATTENTION: New Bank Details for June Payment",
        'body': "To our valued small business partner, please note that our bank details have permanently changed due to an internal merger. All future invoices, including the one attached, MUST be paid to the new account listed below. Click here to download the attached invoice and new details:",
        'phishing_link_text': "Download New Invoice and Bank Details",
        'phishing_link_url': "#", 
        'safe_link_text': "I will call the supplier on their trusted phone number to verify.",
        'safe_link_url': "#",
        'explanation': "SCAM DETECTED! This is Business Email Compromise (BEC). Always VERIFY bank account changes by calling your supplier on a phone number you already have, NOT the number listed in the suspicious email or attachment."
    },
    {
        'id': 3,
        'sender': "Gaming Platform Security <admin@gamer-support.xyz>",
        'subject': "Your Account Was Reported for Abuse: Verify Now to Avoid Ban",
        'body': "Your account was automatically flagged for violating terms of service. To prevent a permanent ban and loss of all your items/levels, click the verification link immediately. If you ignore this, your account will be deleted in 24 hours. Click here to appeal:",
        'phishing_link_text': "Login to Verify Account",
        'phishing_link_url': "#", 
        'safe_link_text': "I will close the email and log in directly through the official game website.",
        'safe_link_url': "#",
        'explanation': "SCAM DETECTED! This targets youth by creating panic about losing their investment (time/money). Real gaming platforms rarely send urgent, unverified login links. Always go to the OFFICIAL website yourself."
    }
]