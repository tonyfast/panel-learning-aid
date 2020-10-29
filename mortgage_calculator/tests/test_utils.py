from mortgage import Loan
from mortgage_calculator.utils import loan_amortization_schedule


def test_loan_amortization_schedule():
    down_payment_dollars, principal, loan = loan_amortization_schedule(300_000, 3.0, 30, 'Percentage', 10)
    assert down_payment_dollars == 30_000
    assert principal == 270_000
