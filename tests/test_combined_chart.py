"""Tests specific to combined chart functionality according to ECharts specification."""

import pytest
from echart_server import create_combined_chart
from conftest import parse_echarts_string, assert_valid_echarts_string

# Access the actual function if it's wrapped
if hasattr(create_combined_chart, 'fn'):
    create_combined_chart = create_combined_chart.fn


def test_combined_chart_basic_structure(sample_x_data, sample_line_data, sample_bar_data):
    """Test basic combined chart structure matches ECharts specification."""
    response = create_combined_chart(
        title="Combined Chart",
        x_data=sample_x_data,
        line_data=sample_line_data,
        bar_data=sample_bar_data
    )
    config = assert_valid_echarts_string(response)
    
    # Check that both line and bar series exist
    assert len(config["series"]) == len(sample_line_data) + len(sample_bar_data)
    
    # Check line series
    for i, line_series in enumerate(sample_line_data):
        series = config["series"][i]
        assert series["type"] == "line"
        assert series["name"] == line_series["name"]
        assert series["data"] == line_series["data"]
        assert series["smooth"] is True
    
    # Check bar series
    for i, bar_series in enumerate(sample_bar_data):
        series = config["series"][len(sample_line_data) + i]
        assert series["type"] == "bar"
        assert series["name"] == bar_series["name"]
        assert series["data"] == bar_series["data"]


def test_combined_chart_only_line_data(sample_x_data, sample_line_data):
    """Test combined chart with only line data."""
    response = create_combined_chart(
        title="Only Lines",
        x_data=sample_x_data,
        line_data=sample_line_data,
        bar_data=None
    )
    config = assert_valid_echarts_string(response)
    
    assert len(config["series"]) == len(sample_line_data)
    for series in config["series"]:
        assert series["type"] == "line"


def test_combined_chart_only_bar_data(sample_x_data, sample_bar_data):
    """Test combined chart with only bar data."""
    response = create_combined_chart(
        title="Only Bars",
        x_data=sample_x_data,
        line_data=None,
        bar_data=sample_bar_data
    )
    config = assert_valid_echarts_string(response)
    
    assert len(config["series"]) == len(sample_bar_data)
    for series in config["series"]:
        assert series["type"] == "bar"


def test_combined_chart_legend_consolidation(sample_x_data, sample_line_data, sample_bar_data):
    """Test that legend includes all series names from both line and bar data."""
    response = create_combined_chart(
        title="Legend Test",
        x_data=sample_x_data,
        line_data=sample_line_data,
        bar_data=sample_bar_data
    )
    config = assert_valid_echarts_string(response)
    
    expected_legend = []
    expected_legend.extend([item["name"] for item in sample_line_data])
    expected_legend.extend([item["name"] for item in sample_bar_data])
    
    assert config["legend"]["data"] == expected_legend


def test_combined_chart_axis_pointer():
    """Test combined chart has cross axis pointer."""
    response = create_combined_chart(
        title="Cross Pointer",
        x_data=["A", "B"],
        line_data=[{"name": "Line", "data": [1, 2]}],
        bar_data=[{"name": "Bar", "data": [3, 4]}]
    )
    config = assert_valid_echarts_string(response)
    
    assert config["tooltip"]["axisPointer"]["type"] == "cross"


def test_combined_chart_no_data_error():
    """Test that combined chart requires at least one data series."""
    with pytest.raises(ValueError, match="Deve fornecer pelo menos dados de linha ou barra"):
        create_combined_chart(
            title="No Data",
            x_data=["A", "B"],
            line_data=None,
            bar_data=None
        )


def test_combined_chart_multiple_line_series():
    """Test combined chart with multiple line series."""
    x_data = ["Q1", "Q2", "Q3", "Q4"]
    line_data = [
        {"name": "Revenue", "data": [100, 120, 140, 160]},
        {"name": "Profit", "data": [20, 24, 28, 32]},
        {"name": "Growth", "data": [5, 6, 7, 8]}
    ]
    
    response = create_combined_chart(
        title="Multiple Lines",
        x_data=x_data,
        line_data=line_data,
        bar_data=None
    )
    config = assert_valid_echarts_string(response)
    
    assert len(config["series"]) == 3
    for i, series in enumerate(config["series"]):
        assert series["type"] == "line"
        assert series["smooth"] is True
        assert series["name"] == line_data[i]["name"]


def test_combined_chart_multiple_bar_series():
    """Test combined chart with multiple bar series."""
    x_data = ["Jan", "Feb", "Mar"]
    bar_data = [
        {"name": "Product A", "data": [50, 60, 70]},
        {"name": "Product B", "data": [40, 45, 50]},
        {"name": "Product C", "data": [30, 35, 40]}
    ]
    
    response = create_combined_chart(
        title="Multiple Bars",
        x_data=x_data,
        line_data=None,
        bar_data=bar_data
    )
    config = assert_valid_echarts_string(response)
    
    assert len(config["series"]) == 3
    for i, series in enumerate(config["series"]):
        assert series["type"] == "bar"
        assert series["name"] == bar_data[i]["name"]


def test_combined_chart_mixed_many_series():
    """Test combined chart with many series of both types."""
    x_data = ["A", "B"]
    line_data = [{"name": f"Line {i}", "data": [i, i+1]} for i in range(5)]
    bar_data = [{"name": f"Bar {i}", "data": [i*2, i*2+1]} for i in range(5)]
    
    response = create_combined_chart(
        title="Many Series",
        x_data=x_data,
        line_data=line_data,
        bar_data=bar_data
    )
    config = assert_valid_echarts_string(response)
    
    assert len(config["series"]) == 10
    # First 5 should be lines
    for i in range(5):
        assert config["series"][i]["type"] == "line"
    # Last 5 should be bars
    for i in range(5, 10):
        assert config["series"][i]["type"] == "bar"


def test_combined_chart_with_formatters():
    """Test combined chart with different formatter types."""
    x_data = ["Jan", "Feb"]
    line_data = [{"name": "Revenue", "data": [1000, 1200]}]
    bar_data = [{"name": "Costs", "data": [800, 900]}]
    
    formatters = ["currency_brl", "percentage", "absolute", None]
    
    for formatter in formatters:
        response = create_combined_chart(
            title="Formatted",
            x_data=x_data,
            line_data=line_data,
            bar_data=bar_data,
            y_format_type=formatter
        )
        config = assert_valid_echarts_string(response)
        
        if formatter:
            assert "axisLabel" in config["yAxis"]
            assert "formatter" in config["yAxis"]["axisLabel"]
            assert "valueFormatter" in config["tooltip"]
        else:
            assert "axisLabel" not in config["yAxis"]


def test_combined_chart_axis_labels():
    """Test combined chart with axis labels."""
    response = create_combined_chart(
        title="With Labels",
        x_data=["Q1", "Q2"],
        line_data=[{"name": "Line", "data": [100, 110]}],
        bar_data=[{"name": "Bar", "data": [90, 95]}],
        x_label="Quarter",
        y_label="Value ($)"
    )
    config = assert_valid_echarts_string(response)
    
    assert config["xAxis"]["name"] == "Quarter"
    assert config["yAxis"]["name"] == "Value ($)"
    assert config["xAxis"]["nameLocation"] == "middle"
    assert config["yAxis"]["nameLocation"] == "middle"


def test_combined_chart_negative_values():
    """Test combined chart with negative values."""
    response = create_combined_chart(
        title="Negative Values",
        x_data=["A", "B", "C"],
        line_data=[{"name": "Profit", "data": [-100, 0, 100]}],
        bar_data=[{"name": "Loss", "data": [-50, -25, 0]}]
    )
    config = assert_valid_echarts_string(response)
    
    assert config["series"][0]["data"] == [-100, 0, 100]
    assert config["series"][1]["data"] == [-50, -25, 0]


def test_combined_chart_decimal_values():
    """Test combined chart with decimal values."""
    response = create_combined_chart(
        title="Decimals",
        x_data=["A", "B"],
        line_data=[{"name": "Precise Line", "data": [10.5, 20.75]}],
        bar_data=[{"name": "Precise Bar", "data": [15.333, 25.667]}]
    )
    config = assert_valid_echarts_string(response)
    
    assert config["series"][0]["data"] == [10.5, 20.75]
    assert config["series"][1]["data"] == [15.333, 25.667]


def test_combined_chart_special_characters():
    """Test combined chart with special characters in series names."""
    response = create_combined_chart(
        title="Special Names",
        x_data=["X1", "X2"],
        line_data=[
            {"name": "Revenue™", "data": [100, 110]},
            {"name": "测试线条", "data": [90, 95]}
        ],
        bar_data=[
            {"name": "Cost & Expense", "data": [80, 85]},
            {"name": "Profit <NET>", "data": [20, 25]}
        ]
    )
    config = assert_valid_echarts_string(response)
    
    assert config["series"][0]["name"] == "Revenue™"
    assert config["series"][1]["name"] == "测试线条"
    assert config["series"][2]["name"] == "Cost & Expense"
    assert config["series"][3]["name"] == "Profit <NET>"


def test_combined_chart_empty_data_arrays():
    """Test combined chart with empty data arrays in series."""
    response = create_combined_chart(
        title="Empty Arrays",
        x_data=[],
        line_data=[{"name": "Empty Line", "data": []}],
        bar_data=[{"name": "Empty Bar", "data": []}]
    )
    config = assert_valid_echarts_string(response)
    
    assert config["xAxis"]["data"] == []
    assert config["series"][0]["data"] == []
    assert config["series"][1]["data"] == []


def test_combined_chart_series_order():
    """Test that line series always come before bar series."""
    response = create_combined_chart(
        title="Series Order",
        x_data=["A", "B"],
        line_data=[
            {"name": "Line 1", "data": [1, 2]},
            {"name": "Line 2", "data": [3, 4]}
        ],
        bar_data=[
            {"name": "Bar 1", "data": [5, 6]},
            {"name": "Bar 2", "data": [7, 8]}
        ]
    )
    config = assert_valid_echarts_string(response)
    
    # First two should be lines
    assert config["series"][0]["type"] == "line"
    assert config["series"][0]["name"] == "Line 1"
    assert config["series"][1]["type"] == "line"
    assert config["series"][1]["name"] == "Line 2"
    
    # Last two should be bars
    assert config["series"][2]["type"] == "bar"
    assert config["series"][2]["name"] == "Bar 1"
    assert config["series"][3]["type"] == "bar"
    assert config["series"][3]["name"] == "Bar 2"


def test_combined_chart_smooth_line_property():
    """Test that all line series in combined chart have smooth property."""
    response = create_combined_chart(
        title="Smooth Lines",
        x_data=["A", "B"],
        line_data=[
            {"name": "Line 1", "data": [1, 2]},
            {"name": "Line 2", "data": [3, 4]},
            {"name": "Line 3", "data": [5, 6]}
        ],
        bar_data=None
    )
    config = assert_valid_echarts_string(response)
    
    for series in config["series"]:
        if series["type"] == "line":
            assert series["smooth"] is True


def test_combined_chart_no_stack_on_bars():
    """Test that bar series in combined chart don't have stack property."""
    response = create_combined_chart(
        title="No Stack",
        x_data=["A", "B"],
        line_data=None,
        bar_data=[
            {"name": "Bar 1", "data": [1, 2]},
            {"name": "Bar 2", "data": [3, 4]}
        ]
    )
    config = assert_valid_echarts_string(response)
    
    for series in config["series"]:
        if series["type"] == "bar":
            assert "stack" not in series


@pytest.mark.parametrize("format_type,expected_content", [
    ("currency_brl", "toLocaleString('pt-BR'"),
    ("percentage", "toFixed(1) + '%'"),
    ("absolute", "toLocaleString('pt-BR')"),
    (None, None)
])
def test_combined_chart_formatter_content(format_type, expected_content):
    """Test that formatters contain expected JavaScript code."""
    response = create_combined_chart(
        title="Formatter Test",
        x_data=["A", "B"],
        line_data=[{"name": "Line", "data": [100, 200]}],
        bar_data=[{"name": "Bar", "data": [150, 250]}],
        y_format_type=format_type
    )
    config = assert_valid_echarts_string(response)
    
    if expected_content:
        formatter = config["yAxis"]["axisLabel"]["formatter"]
        assert expected_content in formatter
        assert formatter.startswith("function")
    else:
        assert "axisLabel" not in config["yAxis"]