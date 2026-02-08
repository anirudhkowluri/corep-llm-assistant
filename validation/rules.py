def validate(corep):
    warnings = []

    if "rows" not in corep or not isinstance(corep["rows"], list):
        warnings.append("Invalid or missing 'rows' structure in the generated report.")
        return warnings

    rows = corep["rows"]
    
    # helper to find row
    def find_row(code):
        return next((r for r in rows if r.get("row_code") == code), None)

    r010 = find_row("r010")
    r060 = find_row("r060")

    if not r010:
        warnings.append("Row r010 (CET1 Capital) is missing.")
    if not r060:
        warnings.append("Row r060 (Retained Earnings) is missing.")

    if r010 and r060:
        # Example validation logic: In some simplified scenarios, user might expect them equal?
        # The original code checked inequality. Let's keep a similar logic but safer.
        # However, typically CET1 >= Retained Earnings. The original code was checking equality, 
        # which might be a specific business rule for this simplified prototype.
        # "CET1 capital does not equal retained earnings" implies they should be equal in this specific dummy scenario?
        # I will preserve the original intent but make it safe.
        amount_r010 = r010.get("amount", 0)
        amount_r060 = r060.get("amount", 0)
        
        if amount_r010 != amount_r060:
             warnings.append(f"CET1 capital ({amount_r010}) does not equal retained earnings ({amount_r060}).")

    return warnings
