import datetime

import pandas as pd
from panel_aids.mortgage_calculator import (monthly_payment_breakdown_plot,
                                            mortgage_amortization_plot,
                                            principal_vs_time_plot)


def test_monthly_payment_breakdown_plot():
    actual_plot = monthly_payment_breakdown_plot(home_cost=300_000,
                                                 interest_rate_pct=3.0,
                                                 mort_len_yr=30,
                                                 down_payment_type='Dollars',
                                                 down_payment_value=30_000,
                                                 prop_tax_amt=3_000,
                                                 prop_tax_type='Dollars',
                                                 home_ins=300,
                                                 hoa_fees=30,
                                                 pmi_percent=0.5)

    actual_data = actual_plot.data.Amount
    expected_data = pd.Series([1138.33, 250.00, 300.00, 30.00, 112.50])
    assert actual_data.equals(expected_data)


def test_mortgage_amortization_plot():
    actual_plot = mortgage_amortization_plot(300_000, 3.0, 30, 'Dollars', 30_000, 'Dollars', 3_000, 300, 30, 0.5,
                                             datetime.date(2020, 1, 1))
    actual_data = actual_plot.data.loc[0:4, 'payment_value'].round(2)
    expected_data = pd.Series([5160.83, 5794.03, 5970.26, 6151.85, 6338.97])
    assert actual_data.equals(expected_data)


def test_principal_vs_time_plot():
    actual_plot = principal_vs_time_plot(
        300_000, 3.0, 30, 'Percentage', 10, datetime.date(2020, 1, 1))
    actual_data = actual_plot.data[(
        'Curve', 'Principal_Paid')].data.loc[0:4, 'Principal Paid'].round(2)
    expected_data = pd.Series([0, 463.33, 927.82, 1393.47, 1860.29])
    assert actual_data.equals(expected_data)
