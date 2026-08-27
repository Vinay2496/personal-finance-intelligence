from app.services.categorization import categorize_transaction


def test_food_keyword_zomato():
    assert categorize_transaction("Payment to Zomato", "Zomato", "debit") == "Food"


def test_transport_keyword_uber():
    assert categorize_transaction("Uber ride", "Uber India", "debit") == "Transport"


def test_shopping_keyword_amazon():
    assert categorize_transaction("Amazon.in purchase", "Amazon", "debit") == "Shopping"


def test_case_insensitive_matching():
    assert categorize_transaction("ZOMATO ORDER", "ZOMATO", "debit") == "Food"


def test_first_matching_category_wins():
    # "rent" appears in CATEGORY_RULES only under Rent - sanity check exact match
    assert categorize_transaction("Monthly rent payment", "Landlord", "debit") == "Rent"


def test_unmatched_debit_falls_back_to_other():
    assert categorize_transaction("Random unclear payment", "XYZ Corp", "debit") == "Other"


def test_unmatched_credit_falls_back_to_income():
    assert categorize_transaction("Unknown credit entry", "Some Company", "credit") == "Income"


def test_explicit_salary_credit():
    assert categorize_transaction("Monthly salary", "Employer Pvt Ltd", "credit") == "Income"


def test_utilities_keyword_electricity():
    assert categorize_transaction("Electricity bill payment", "State Board", "debit") == "Utilities"