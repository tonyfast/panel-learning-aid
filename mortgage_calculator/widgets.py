from datetime import date

import panel as pn

from mortgage_calculator.config import initial_home_cost, start_date

# define widgets
home_value_widget = pn.widgets.Spinner(
    name="Home Value ($):", start=1000, end=100_000_000, step=1000
)
down_payment_type_widget = pn.widgets.RadioButtonGroup(
    name="down_payment_type", options=["Dollars", "Percentage"], value="Dollars"
)
down_payment_dollars_value_widget = pn.widgets.Spinner(
    name="Down Payment: ($)",
    value=30_000,
    start=0,
    step=1000,
    end=int(initial_home_cost * 0.99),
)
down_payment_percentage_value_widget = pn.widgets.Spinner(
    name="Down Payment: (%)",
    value=10.0,
    start=0,
    step=1.0,
    end=99,
)

loan_amount_pane = pn.pane.Markdown(object="Loan Amount ($):")
annual_int_rate_widget = pn.widgets.Spinner(
    name="Annual Interest Rate (%):", value=3.0, start=0.01, end=25, step=0.01
)
loan_term_widget = pn.widgets.RadioButtonGroup(
    name="Loan Term Radio", options=["15", "20", "30"], value="30"
)
prop_tax_type_widget = pn.widgets.RadioButtonGroup(
    name="prop_tax_type", options=["Dollars", "Percentage"], value="Percentage"
)
prop_tax_dollars_amount_widget = pn.widgets.Spinner(
    name="Annual Property Tax: ($)", start=100, end=int(round(0.03 * initial_home_cost, 0)), step=100
)
prop_tax_percentage_amount_widget = pn.widgets.Spinner(
    name="Annual Property Tax: (%)", value=1.0, start=0.01, end=3.0, step=0.01
)
pmi_percent_widget = pn.widgets.Spinner(
    name="Annual Private Mortgage Insurance (% of loan amount):",
    value=0.5,
    start=0,
    end=5,
    step=0.01,
)
monthly_home_ins_prem_widget = pn.widgets.Spinner(
    name="Monthly Home Owner's Insurance Premium ($):", value=190, start=0, step=10
)
monthly_hoa_fees_widget = pn.widgets.Spinner(
    name="Monthly HOA Fees ($):", value=30, start=0, step=5
)
