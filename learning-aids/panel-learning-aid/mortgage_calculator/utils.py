from mortgage import Loan


def loan_amortization_schedule(
    home_cost, interest_rate_pct, mort_len_yr, down_payment_type, down_payment_value
):
    """Calculates the amortization schedule given the home cost, interest rate, amortization length, and down payment info.

    Parameters
    ----------
    home_cost : float or int
    interest_rate_pct : float or int
        Annual interest rate in dollars
    mort_len_yr : int
        Length of time over which the loan is repaid
    down_payment_type : str
        Units of the down_payment_value parameter ("Dollars" or "Percentage")
    down_payment_value : float or int
        Value of the down payment on the home in the units given by down_payment_type

    Returns
    -------
    down_payment_dollars:
        down_payment amount in dollars
    principal:
        initial loan balance
    loan: mortgage.Loan
        contains the complete loan repayment information

    Examples
    --------
    >>> print(loan_amortization_schedule(300_000, 3, 30, 'Dollars', 30_000))
    (30000, 270000, <Loan principal=270000, interest=0.03, term=30>)

    >>> print(loan_amortization_schedule(300_000, 3, 30, 'Percentage', 10.0))
    (30000.0, 270000.0, <Loan principal=270000, interest=0.03, term=30>)
    """
    if down_payment_type == "Dollars":
        down_payment_dollars = down_payment_value
    elif down_payment_type == "Percentage":
        down_payment_dollars = down_payment_value / 100 * home_cost

    principal = home_cost - down_payment_dollars
    loan = Loan(principal, interest_rate_pct / 100, mort_len_yr)
    return down_payment_dollars, principal, loan
