import logging
from datetime import date

import panel as pn

from mortgage_calculator.config import initial_home_cost, start_date
from mortgage_calculator.my_logging import get_logger
from mortgage_calculator.plots import (monthly_payment_breakdown_plot,
                                       mortgage_amortization_plot,
                                       principal_vs_time_plot)
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
                                         prop_tax_dollars_amount_widget,
                                         prop_tax_percentage_amount_widget,
                                         prop_tax_type_widget)

logger = logging.getLogger(__name__)

down_payment_value_widget = down_payment_dollars_value_widget
prop_tax_amount_widget = prop_tax_percentage_amount_widget

left_widget_box = pn.WidgetBox(
    home_value_widget,
    "Down Payment:",
    down_payment_type_widget,
    down_payment_value_widget,
    loan_amount_pane,
    annual_int_rate_widget,
    "Loan Term",
    loan_term_widget,
    sizing_mode="stretch_width",
)
down_payment_value_left_widget_box_index = left_widget_box.objects.index(down_payment_value_widget)

right_widget_box = pn.WidgetBox(
    "Property Tax:",
    prop_tax_type_widget,
    prop_tax_amount_widget,
    pmi_percent_widget,
    monthly_home_ins_prem_widget,
    monthly_hoa_fees_widget,
    sizing_mode="stretch_width",
)
prop_tax_amount_right_widget_box_index = right_widget_box.objects.index(prop_tax_amount_widget)

num_tab_plots = 3
tabs = pn.Tabs(*tuple(("placeholder", "") for _ in range(num_tab_plots)), dynamic=True)
layout = pn.Column(
    pn.pane.Markdown("# Mortgage Payment Calculator", align="center"),
    pn.Row(
        left_widget_box,
        right_widget_box,
    ),
    tabs,
    "*Home appreciation/depreciation not accounted for",
    sizing_mode="stretch_width",
    max_width=1000,
)

# convenience pane update funcs
def set_down_payment_value_widget(new_widget, index=down_payment_value_left_widget_box_index):
    left_widget_box.__setitem__(index, new_widget)

def set_prop_tax_value_widget(new_widget, index=prop_tax_amount_right_widget_box_index):
    right_widget_box.__setitem__(index, new_widget)
    
def set_plot(index, new_panel):
    tabs.__setitem__(index, new_panel)


def update(event):
    global down_payment_value_widget, prop_tax_amount_widget
    

    logger.debug(
        f"App Update - initial widget values: {[(x.name, x.value) for x in [home_value_widget, annual_int_rate_widget, loan_term_widget, down_payment_type_widget, down_payment_value_widget, prop_tax_amount_widget, prop_tax_type_widget, monthly_home_ins_prem_widget, monthly_hoa_fees_widget, pmi_percent_widget]]}"
    )
    logger.debug(f'update event: {event}')

    # input validation
    home_value = home_value_widget.value
    annual_int_rate = annual_int_rate_widget.value
    loan_term = int(loan_term_widget.value)
    down_payment_type = down_payment_type_widget.value
    down_payment_value = down_payment_value_widget.value
    prop_tax_amount = prop_tax_amount_widget.value
    prop_tax_type = prop_tax_type_widget.value
    monthly_home_ins_prem = monthly_home_ins_prem_widget.value
    monthly_hoa_fees = monthly_hoa_fees_widget.value
    pmi_percent = pmi_percent_widget.value

    # trim all Spinner widget values to max
    if isinstance(event.obj, pn.widgets.input.Spinner):
        if event.obj.end and event.obj.value > event.obj.end:
            logging.debug(f'trimming widget value {event.obj.value} to {event.obj.end}')
            
            # triggers another call to update
            event.obj.value = event.obj.end
            return

    # update loan amount
    if event.obj in {home_value_widget, down_payment_value_widget}:
        _, principal, _ = loan_amortization_schedule(
            home_value,
            annual_int_rate,
            loan_term,
            down_payment_type,
            down_payment_value,
        )
        # doesn't trigger another call to update
        loan_amount_pane.object = f"### Loan Amount : ${principal:0,.0f}"
        logger.debug(f'Updated Loan Amount Pane: ${principal:0,.0f}')
        

    # update down payment from $ to % when down payment type changed
    if event.obj is down_payment_type_widget:
        if event.new == "Percentage":
            down_payment_value_widget = down_payment_percentage_value_widget  
            new_value = round(
                down_payment_value / home_value * 100, 2
            )

        elif event.new == "Dollars":
            down_payment_value_widget = down_payment_dollars_value_widget
            new_value =  round(
                home_value * down_payment_value / 100, 0
            )
        logger.debug(f'down_payment_value_widget.value = {new_value}')
        down_payment_value_widget.value = new_value
        set_down_payment_value_widget(down_payment_value_widget)
        return
            

    # update down_payment_value_widget_max when home value changes
    if event.obj is home_value_widget:
        if down_payment_type == 'Dollars':
            down_payment_dollars_value_widget.end = int(home_value * 0.99)
            logger.debug(f'down_payment_value_widget.end = {home_value * 0.99}')
        if prop_tax_type == 'Dollars':
            prop_tax_dollars_amount_widget.end = int(home_value * 0.03)
            logger.debug(f'prop_tax_dollars_amount_widget.end = {home_value * 0.03}')

    if event.obj is prop_tax_type_widget:
        if event.new == "Percentage":
            prop_tax_amount_widget = prop_tax_percentage_amount_widget
            prop_tax_amount_widget.value = round(
                prop_tax_amount / home_value * 100, 2
            )  # triggers another update call
        elif event.new == "Dollars":
            prop_tax_amount_widget = prop_tax_dollars_amount_widget
            prop_tax_amount_widget.value = round(
                home_value * prop_tax_amount / 100, 0
            )  # triggers another update call
        set_prop_tax_value_widget(prop_tax_amount_widget)
        return

    # update monthly payment plot
    new_panel = pn.panel(
            monthly_payment_breakdown_plot(
                home_value,
                annual_int_rate,
                loan_term,
                down_payment_type,
                down_payment_value,
                prop_tax_amount,
                prop_tax_type,
                monthly_home_ins_prem,
                monthly_hoa_fees,
                pmi_percent,
            ),
            name="Mortgage Payment Breakdown",
            sizing_mode="stretch_width",
        )
    set_plot(0, new_panel)

    # update mortgage amortization plot
    new_panel = pn.panel(
                    mortgage_amortization_plot(
                        home_value,
                        annual_int_rate,
                        loan_term,
                        down_payment_type,
                        down_payment_value,
                        prop_tax_type,
                        prop_tax_amount,
                        monthly_home_ins_prem,
                        monthly_hoa_fees,
                        pmi_percent,
                    ),
            name="Amortization Schedule",
            sizing_mode="stretch_width"
    )
    set_plot(1, new_panel)

    # update principal over time plot
    new_panel = pn.panel(
                    principal_vs_time_plot(
                        home_value,
                        annual_int_rate,
                        loan_term,
                        down_payment_type,
                        down_payment_value,
                    ),
                    name="Principal Over Time",
                    sizing_mode="stretch_width",
    )
    set_plot(2, new_panel)
    return None


# register watchers  (loan_amount_pane not included)
for widget in [
    home_value_widget,
    down_payment_type_widget,
    down_payment_dollars_value_widget,
    down_payment_percentage_value_widget,
    annual_int_rate_widget,
    loan_term_widget,
    prop_tax_type_widget,
    prop_tax_percentage_amount_widget,
    prop_tax_dollars_amount_widget,
    monthly_home_ins_prem_widget,
    monthly_hoa_fees_widget,
    pmi_percent_widget,
]:
    widget.param.watch(update, "value")

# trigger an initial watcher
home_value_widget.value = initial_home_cost
logger.debug('----------Done triggering initial watcher----------')
layout.servable()
