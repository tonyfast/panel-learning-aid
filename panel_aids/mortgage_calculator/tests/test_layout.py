import holoviews as hv
from panel_aids.mortgage_calculator import tabs


def test_plots_filled():
    """Test that plots have been filled in with holoviews charts and/or overlays"""
    for tab in tabs:
        assert isinstance(
            tab.object, (hv.element.chart.Chart, hv.core.overlay.Overlay))
