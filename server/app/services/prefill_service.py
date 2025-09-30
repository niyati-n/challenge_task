import re
import csv
from pathlib import Path

DATA_FILE = Path("./data/data.csv")
DATA_FILE.parent.mkdir(exist_ok=True)

def extract_and_save_payment_info(email_text: str, model: str):

    #Regular expression for text
    amount_match = re.search(r"(?i)(?:Amount Due)[\s:]*([\$\€\£]?\s?[\d,]+(?:\.\d{1,2}))", email_text)
    currency_match = re.search(r"\b(USD|EUR|GBP|INR|AUD|CAD|JPY|CHF|CNY)\b", email_text)
    due_date_match = re.search(
        r"(?i)(?:Due Date|Payment Due)[:\s]*([A-Z][a-z]+ \d{1,2},? \d{4}|\d{1,2}[/-]\d{1,2}[/-]\d{2,4})", 
        email_text
    )

    subject_match = re.search(r"Subject: Invoice #[\w-]+\s+from\s+(.+?)\s*-\s*(.+)", email_text, re.IGNORECASE)
    services = re.findall(r"^- \s*([A-Za-z][A-Za-z0-9 &/_\-]+?)\s*(?:\((\d+\s*hours?)\))?$", email_text, re.MULTILINE)
    contact_match = re.search(r"(?i)(?:Best regards|Sincerely|Regards),\s*(.+)", email_text, re.DOTALL)
    services_list = [{"service": s[0].strip(), "hours": s[1]} for s in services]

    data = {
        "amount": amount_match.group(1).strip() if amount_match else "",
        "currency": currency_match.group(1).strip() if currency_match else "",
        "due_date": due_date_match.group(1).strip() if due_date_match else "",
        "company" : subject_match.group(2).strip(),  # Acme Corp
        "description" : subject_match.group(1).strip(),
        "services": services_list,
        "contact": contact_match.group(1).strip() if contact_match else "",
    }

    file_exists = DATA_FILE.exists()
    with open(DATA_FILE, mode="a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)
