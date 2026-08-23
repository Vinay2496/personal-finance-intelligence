# Rule-based category mapping.
# Keys are lowercase keywords to look for in the merchant/description.
# This is intentionally simple and easy to extend — add new keywords as needed.

CATEGORY_RULES = {
    "Food": ["zomato", "swiggy", "dominos", "pizza", "restaurant", "cafe", "starbucks", "mcdonald"],
    "Transport": ["uber", "ola", "rapido", "irctc", "petrol", "fuel", "metro"],
    "Shopping": ["amazon", "flipkart", "myntra", "ajio", "meesho"],
    "Entertainment": ["netflix", "spotify", "hotstar", "prime video", "bookmyshow", "youtube"],
    "Utilities": ["electricity", "water board", "gas", "broadband", "wifi", "internet", "recharge"],
    "Rent": ["rent", "landlord"],
    "Health": ["pharmacy", "hospital", "clinic", "apollo", "medplus", "diagnostic"],
    "Groceries": ["bigbasket", "grofers", "blinkit", "zepto", "dmart", "grocery"],
    "Income": ["salary", "stipend", "refund", "cashback", "interest credit"],
    "Transfer": ["upi", "neft", "imps", "transfer"],
}

DEFAULT_CATEGORY = "Other"


def categorize_transaction(description: str, merchant: str, transaction_type: str) -> str:
    """
    Rule-based categorization: checks description/merchant text against known keywords.
    Falls back to 'Income' for credit transactions and 'Other' for everything else
    that doesn't match a rule.
    """
    text = f"{description} {merchant}".lower()

    for category, keywords in CATEGORY_RULES.items():
        for keyword in keywords:
            if keyword in text:
                return category

    if transaction_type == "credit":
        return "Income"

    return DEFAULT_CATEGORY