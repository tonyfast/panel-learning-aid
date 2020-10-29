"""Plots for mortgage calculator app"""
import inspect
from datetime import date, timedelta
from functools import reduce, wraps
from typing import Union, cast

import holoviews as hv
import hvplot.pandas
import pandas as pd
import panel as pn
from bokeh.models import HoverTool
from bokeh.models.formatters import NumeralTickFormatter
from mortgage import Loan

from mortgage_calculator.config import (DOWN_PMT_PMI_THRESHOLD_PCT,
                                        MNTHS_PER_YR, start_date)
from mortgage_calculator.utils import loan_amortization_schedule
from mortgage_calculator.widgets import (annual_int_rate_widget,
                                         down_payment_dollars_value_widget,
                                         down_payment_percentage_value_widget,
                                         down_payment_type_widget,
                                         home_value_widget, loan_amount_pane,
                                         loan_term_widget,
                                         monthly_hoa_fees_widget,
                                         monthly_home_ins_prem_widget,
                                         pmi_percent_widget,
                                         prop_tax_type_widget)


def monthly_payment_breakdown_plot(
    home_cost: Union[float, int],
    interest_rate_pct: Union[float, int],
    mort_len_yr: int,
    down_payment_type: str,
    down_payment_value: Union[float, int],
    prop_tax_amt: Union[float, int],
    prop_tax_type: str,
    home_ins: Union[float, int],
    hoa_fees: Union[float, int],
    pmi_percent: Union[float, int],
):
    """Produce a bar plot of the initial monthly payment breakdown for a mortgage

    Parameters
    ----------
    home_cost : Union[float, int]
        home cost in dollars
    interest_rate_pct : Union[float, int]
        Annual interest rate percentage (e.g. 3.1)
    mort_len_yr : int
        Length of mortgage in years
    down_payment_type : str
        "Dollars" or "Percentage"
    down_payment_value : Union[float, int]
        Value of down payment on home
    prop_tax_type : str
        "Dollars" or "Percentage"
    prop_tax_amt : Union[float, int]
        amount of property tax
    home_ins : Union[float, int]
        Monthly home insurance premium in dollars
    hoa_fees : Union[float, int]
        Monthly HOA Fees in dollars
    pmi_percent : Union[float, int]
        Private Mortgage Insurance Percentage (e.g. 0.5)

    Returns
    -------
    out: holoviews.element.chart.Bars
        initial mortgage payment breakdown bar chart
    """
    down_payment_dollars, principal, loan = loan_amortization_schedule(
        home_cost, interest_rate_pct, mort_len_yr, down_payment_type, down_payment_value
    )
    if loan:
        princ_and_int = float(loan.monthly_payment)
    else:
        princ_and_int = 0

    if prop_tax_type == "Dollars":
        prop_tax_dollars = prop_tax_amt / MNTHS_PER_YR
    elif prop_tax_type == "Percentage":
        prop_tax_dollars = prop_tax_amt / 100 * home_cost / MNTHS_PER_YR
    else:
        raise Exception(
            f"prop_tax_type: {prop_tax_type} should be in {'Dollars', 'Percentage'}"
        )

    if down_payment_dollars / home_cost < DOWN_PMT_PMI_THRESHOLD_PCT / 100:
        monthly_pmi = principal * pmi_percent / 100 / MNTHS_PER_YR
    else:
        monthly_pmi = 0

    costs = [princ_and_int, prop_tax_dollars, home_ins, hoa_fees]
    index = ["Principal & Interest", "Property Tax", "Home Insurance", "HOA Fees"]
    if monthly_pmi > 0:
        costs += [monthly_pmi]
        index += ["PMI"]
    total_cost = sum(costs)

    hover = HoverTool(
        tooltips=[("Payment", "@index{safe}"), ("Amount", "@{Amount}{$0,0}")]
    )

    plot = hv.Bars(pd.DataFrame(costs, index=index, columns=["Amount"])).opts(
        yformatter=NumeralTickFormatter(format="$0,0"),
        tools=[hover],
        title=f"Initial Monthly Payment: ${total_cost:,.2f}",
        xlabel="Payment Type",
        ylabel="Monthly Payment Amount",
        color="#2e8cc7",
    )
    return plot


def mortgage_amortization_plot(
    home_cost: float,
    interest_rate_pct: float,
    mort_len_yr: int,
    down_payment_type: str,
    down_payment_value: float,
    prop_tax_type: str,
    prop_tax_amt: float,
    home_ins: float,
    hoa_fees: float,
    pmi_percent: float,
    start_date: date=start_date,
):
    """Plots the amortization schedule costs over time

    Parameters
    ----------
    home_cost : Union[float, int]
        home cost in dollars
    interest_rate_pct : Union[float, int]
        Annual interest rate percentage (e.g. 3.1)
    mort_len_yr : int
        Length of mortgage in years
    down_payment_type : str
        "Dollars" or "Percentage"
    down_payment_value : Union[float, int]
        Value of down payment on home
    prop_tax_type : str
        "Dollars" or "Percentage"
    prop_tax_amt : Union[float, int]
        amount of property tax
    home_ins : Union[float, int]
        Monthly home insurance premium in dollars
    hoa_fees : Union[float, int]
        Monthly HOA Fees in dollars
    pmi_percent : Union[float, int]
        Private Mortgage Insurance Percentage (e.g. 0.5)
    start_date : datetime.date, optional
        date at which to start the amortization, by default date.today()

    Returns
    -------
    out: holoviews.element.chart.Bars
        mortgage amortization bar chart
    """
    down_payment_dollars, principal, loan = loan_amortization_schedule(
        home_cost, interest_rate_pct, mort_len_yr, down_payment_type, down_payment_value
    )
    monthly_pmi = principal * pmi_percent / 100 / MNTHS_PER_YR

    if prop_tax_type == "Dollars":
        prop_tax_dollars = prop_tax_amt / MNTHS_PER_YR
    elif prop_tax_type == "Percentage":
        prop_tax_dollars = prop_tax_amt / 100 * home_cost / MNTHS_PER_YR

    loan_df = pd.DataFrame(loan.schedule(), dtype="float")
    loan_df.index = pd.period_range(
        start_date, periods=mort_len_yr * MNTHS_PER_YR + 1, freq="M"
    ).to_timestamp()
    loan_df.loc[:, "Principal Paid"] = loan_df.principal.cumsum()
    loan_df = loan_df.rename(
        columns={"total_interest": "Interest Paid", "balance": "Principal Remaining"}
    )

    all_indices_but_first = loan_df.number >= 1
    # set PMI payment while equity is less than DOWN_PMT_PMI_THRESHOLD_PCT
    loan_df["PMI"] = 0
    loan_df.loc[
        (loan_df["Principal Paid"] < home_cost * DOWN_PMT_PMI_THRESHOLD_PCT / 100)
        & (all_indices_but_first),
        "PMI",
    ] = monthly_pmi

    loan_df.loc[all_indices_but_first, "Property Tax"] = prop_tax_dollars   
    loan_df.loc[all_indices_but_first, "Home Insurance"] = home_ins
    loan_df.loc[all_indices_but_first, "HOA Fees"] = hoa_fees
    loan_df = loan_df.rename(columns={"principal": "Principal", "interest": "Interest"})
    loan_df["Taxes & Fees"] = loan_df.loc[
        :, ["PMI", "Property Tax", "Home Insurance", "HOA Fees"]
    ].sum(axis=1)
    yearly_grouped = loan_df.groupby(loan_df.index.year).sum().drop("number", axis=1)
    bar_graph_df = yearly_grouped.melt(
        value_vars=[
            "Principal",
            "Interest",
            "Property Tax",
            "Home Insurance",
            "HOA Fees",
            "PMI",
        ],
        var_name="payment_type",
        value_name="payment_value",
        ignore_index=False,
    )

    hover = HoverTool(
        tooltips=[
            ("Year", "@index"),
            ("Payment", "@payment_type{safe}"),
            ("Amount", "@payment_value{$0,0}"),
        ]
    )

    bar_plot = (
        hv.Bars(bar_graph_df, kdims=["index", "payment_type"], vdims=["payment_value"])
        .opts(
            yformatter=NumeralTickFormatter(format="$0,0"),
            stacked=True,
            # width=1000,
            tools=[hover],
            legend_position="bottom_right",
            xlabel="Year",
            ylabel="Annual Payment",
        )
        .opts(shared_axes=False, xrotation=70)
    )
    return bar_plot


def principal_vs_time_plot(
    home_cost: Union[float, int],
    interest_rate_pct: Union[float, int],
    mort_len_yr: int,
    down_payment_type: str,
    down_payment_value: Union[float, int],
    start_date: date=start_date,
):
    """Plot of principal paid, still owed, and interest paid over time

    Parameters
    ----------
    home_cost : Union[float, int]
        home cost in dollars
    interest_rate_pct : Union[float, int]
        Annual interest rate percentage (e.g. 3.1)
    mort_len_yr : int
        Length of mortgage in years
    down_payment_type : str
        "Dollars" or "Percentage"
    down_payment_value : Union[float, int]
        Value of down payment on home
    start_date : date, optional
        [description], by default start_date

    Returns
    -------
    out: holoviews.element.chart.Curve
        Principal over time plot
    """

    down_payment_dollars, principal, loan = loan_amortization_schedule(
        home_cost, interest_rate_pct, mort_len_yr, down_payment_type, down_payment_value
    )

    loan_df = pd.DataFrame(loan.schedule(), dtype="float")
    loan_df.index = pd.period_range(
        start_date, periods=mort_len_yr * MNTHS_PER_YR + 1, freq="M"
    ).to_timestamp()
    loan_df["Principal Paid"] = loan_df.principal.cumsum()
    loan_df = loan_df.rename(
        columns={"total_interest": "Interest Paid", "balance": "Principal Remaining"}
    )

    def curve_plot(label):
        hover = HoverTool(
            tooltips=[("Year", "@index{%b %Y}"), ("Value", f"@{{{label}}}{{$0,0}}")],
            formatters={"@index": "datetime"},
        )
        curve_opts = {"line_width": 7, "alpha": 0.7, "tools": [hover]}
        return hv.Curve(loan_df[label], label=label).opts(**curve_opts)

    curves = [
        curve_plot(label)
        for label in ["Principal Paid", "Principal Remaining", "Interest Paid"]
    ]
    composite_plot = reduce(hv.Curve.__mul__, curves)
    return composite_plot.opts(
        yformatter=NumeralTickFormatter(format="$0,0"),
        ylim=(0, principal),
        xlabel="Year",
        ylabel="Total Amount",
        legend_position="bottom_left",
    )
