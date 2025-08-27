"""Tests specific to bar chart functionality according to ECharts specification."""

import pytest
from echart_server import create_bar_chart
from conftest import parse_echarts_string, assert_valid_echarts_string

# Access the actual function if it's wrapped
if hasattr(create_bar_chart, 'fn'):
    create_bar_chart = create_bar_chart.fn


def test_bar_chart_basic_structure(sample_categories, sample_y_data, sample_series_names):
    """Test basic bar chart structure matches ECharts specification."""
    response = create_bar_chart(
        title="Basic Bar Chart",
        categories=sample_categories,
        series_data=sample_y_data[:2],  # Use first 2 series
        series_names=sample_series_names
    )
    config = assert_valid_echarts_string(response)
    
    # Check series structure
    assert len(config["series"]) == len(sample_series_names)
    for i, series in enumerate(config["series"]):
        assert series["type"] == "bar"
        assert series["name"] == sample_series_names[i]
        assert series["data"] == sample_y_data[i]
        assert "stack" not in series  # No stacking by default


def test_bar_chart_stacked():
    """Test stacked bar chart configuration."""
    categories = ["Q1", "Q2", "Q3", "Q4"]
    series_data = [[100, 120, 140, 160], [80, 90, 100, 110]]
    series_names = ["Product A", "Product B"]
    
    response = create_bar_chart(
        title="Stacked Bar Chart",
        categories=categories,
        series_data=series_data,
        series_names=series_names,
        stack=True
    )
    config = assert_valid_echarts_string(response)
    
    # Check stacking configuration
    for series in config["series"]:
        assert "stack" in series
        assert series["stack"] == "total"


def test_bar_chart_not_stacked():
    """Test non-stacked bar chart configuration."""
    response = create_bar_chart(
        title="Non-Stacked",
        categories=["A", "B", "C"],
        series_data=[[1, 2, 3], [4, 5, 6]],
        series_names=["S1", "S2"],
        stack=False
    )
    config = assert_valid_echarts_string(response)
    
    for series in config["series"]:
        assert "stack" not in series


def test_bar_chart_axis_pointer():
    """Test bar chart has shadow axis pointer."""
    response = create_bar_chart(
        title="Bar Chart",
        categories=["Cat1", "Cat2"],
        series_data=[[100, 200]],
        series_names=["Sales"]
    )
    config = assert_valid_echarts_string(response)
    
    assert config["tooltip"]["axisPointer"]["type"] == "shadow"


def test_bar_chart_single_series():
    """Test bar chart with single series."""
    response = create_bar_chart(
        title="Single Series Bar",
        categories=["Jan", "Feb", "Mar"],
        series_data=[[150, 230, 180]],
        series_names=["Monthly Sales"]
    )
    config = assert_valid_echarts_string(response)
    
    assert len(config["series"]) == 1
    assert config["series"][0]["name"] == "Monthly Sales"
    assert config["series"][0]["type"] == "bar"
    assert len(config["series"][0]["data"]) == 3


def test_bar_chart_many_series():
    """Test bar chart with many series."""
    categories = ["Q1", "Q2"]
    num_series = 20
    series_names = [f"Series {i}" for i in range(num_series)]
    series_data = [[i * 10, i * 15] for i in range(num_series)]
    
    response = create_bar_chart(
        title="Many Series",
        categories=categories,
        series_data=series_data,
        series_names=series_names
    )
    config = assert_valid_echarts_string(response)
    
    assert len(config["series"]) == num_series
    for i in range(num_series):
        assert config["series"][i]["name"] == f"Series {i}"


def test_bar_chart_with_formatters():
    """Test bar chart with different formatter types."""
    formatters = ["currency_brl", "percentage", "absolute", None]
    
    for formatter in formatters:
        response = create_bar_chart(
            title="Formatted Bar",
            categories=["A", "B"],
            series_data=[[100, 200]],
            series_names=["Data"],
            y_format_type=formatter
        )
        config = assert_valid_echarts_string(response)
        
        if formatter:
            assert "axisLabel" in config["yAxis"]
            assert "formatter" in config["yAxis"]["axisLabel"]
            assert "valueFormatter" in config["tooltip"]
        else:
            assert "axisLabel" not in config["yAxis"]


def test_bar_chart_data_validation():
    """Test that bar chart validates data consistency."""
    with pytest.raises(ValueError, match="Número de séries de dados deve corresponder"):
        create_bar_chart(
            title="Invalid",
            categories=["A", "B"],
            series_data=[[1, 2], [3, 4], [5, 6]],  # 3 series
            series_names=["S1", "S2"]  # 2 names
        )


def test_bar_chart_negative_values():
    """Test bar chart with negative values."""
    response = create_bar_chart(
        title="Negative Values",
        categories=["Loss", "Break Even", "Profit"],
        series_data=[[-500, 0, 1000]],
        series_names=["Financial Results"]
    )
    config = assert_valid_echarts_string(response)
    
    assert config["series"][0]["data"] == [-500, 0, 1000]


def test_bar_chart_decimal_values():
    """Test bar chart with decimal values."""
    response = create_bar_chart(
        title="Decimals",
        categories=["A", "B", "C"],
        series_data=[[10.5, 20.75, 30.333]],
        series_names=["Precise Data"]
    )
    config = assert_valid_echarts_string(response)
    
    assert config["series"][0]["data"] == [10.5, 20.75, 30.333]


def test_bar_chart_axis_labels():
    """Test bar chart axis label configuration."""
    response = create_bar_chart(
        title="With Labels",
        categories=["Cat1", "Cat2"],
        series_data=[[100, 200]],
        series_names=["Data"],
        x_label="Category",
        y_label="Value (units)"
    )
    config = assert_valid_echarts_string(response)
    
    assert config["xAxis"]["name"] == "Category"
    assert config["yAxis"]["name"] == "Value (units)"
    assert config["xAxis"]["nameLocation"] == "middle"
    assert config["yAxis"]["nameLocation"] == "middle"
    assert config["xAxis"]["nameGap"] == 30
    assert config["yAxis"]["nameGap"] == 50


def test_bar_chart_empty_labels():
    """Test bar chart with empty/missing labels."""
    response = create_bar_chart(
        title="No Labels",
        categories=["A", "B"],
        series_data=[[1, 2]],
        series_names=["Test"]
    )
    config = assert_valid_echarts_string(response)
    
    assert config["xAxis"]["name"] == ""
    assert config["yAxis"]["name"] == ""


def test_bar_chart_special_category_names():
    """Test bar chart with special characters in categories."""
    special_categories = ["Q1'24", "Q2\"24", "Q3<24>", "Q4&24", "测试类别"]
    response = create_bar_chart(
        title="Special Categories",
        categories=special_categories,
        series_data=[[100, 110, 120, 130, 140]],
        series_names=["Revenue"]
    )
    config = assert_valid_echarts_string(response)
    
    assert config["xAxis"]["data"] == special_categories


def test_bar_chart_long_category_names():
    """Test bar chart with very long category names."""
    long_category = "This is a very long category name that might cause display issues"
    categories = [long_category, "Short", long_category]
    
    response = create_bar_chart(
        title="Long Categories",
        categories=categories,
        series_data=[[100, 200, 300]],
        series_names=["Values"]
    )
    config = assert_valid_echarts_string(response)
    
    assert config["xAxis"]["data"] == categories


def test_bar_chart_many_categories():
    """Test bar chart with many categories."""
    categories = [f"Category_{i}" for i in range(50)]
    series_data = [[i * 10 for i in range(50)]]
    
    response = create_bar_chart(
        title="Many Categories",
        categories=categories,
        series_data=series_data,
        series_names=["Data"]
    )
    config = assert_valid_echarts_string(response)
    
    assert len(config["xAxis"]["data"]) == 50
    assert len(config["series"][0]["data"]) == 50


def test_bar_chart_stacked_multiple_series():
    """Test stacked bar chart with multiple series."""
    response = create_bar_chart(
        title="Stacked Multiple",
        categories=["Jan", "Feb", "Mar"],
        series_data=[
            [100, 120, 140],
            [80, 90, 100],
            [60, 70, 80]
        ],
        series_names=["Product A", "Product B", "Product C"],
        stack=True
    )
    config = assert_valid_echarts_string(response)
    
    assert len(config["series"]) == 3
    for series in config["series"]:
        assert series["stack"] == "total"


def test_bar_chart_mixed_stack_configuration():
    """Test that stack parameter affects all series uniformly."""
    # With stack=True
    response_stacked = create_bar_chart(
        title="Stacked",
        categories=["A", "B"],
        series_data=[[10, 20], [30, 40], [50, 60]],
        series_names=["S1", "S2", "S3"],
        stack=True
    )
    config_stacked = assert_valid_echarts_string(response_stacked)
    
    for series in config_stacked["series"]:
        assert series["stack"] == "total"
    
    # With stack=False
    response_not_stacked = create_bar_chart(
        title="Not Stacked",
        categories=["A", "B"],
        series_data=[[10, 20], [30, 40], [50, 60]],
        series_names=["S1", "S2", "S3"],
        stack=False
    )
    config_not_stacked = assert_valid_echarts_string(response_not_stacked)
    
    for series in config_not_stacked["series"]:
        assert "stack" not in series


def test_bar_chart_zero_values():
    """Test bar chart with all zero values."""
    response = create_bar_chart(
        title="All Zeros",
        categories=["A", "B", "C", "D"],
        series_data=[[0, 0, 0, 0]],
        series_names=["Zero Data"]
    )
    config = assert_valid_echarts_string(response)
    
    assert config["series"][0]["data"] == [0, 0, 0, 0]


@pytest.mark.parametrize("format_type,expected_content", [
    ("currency_brl", "toLocaleString('pt-BR'"),
    ("percentage", "toFixed(1) + '%'"),
    ("absolute", "toLocaleString('pt-BR')"),
    (None, None)
])
def test_bar_chart_formatter_content(format_type, expected_content):
    """Test that formatters contain expected JavaScript code."""
    response = create_bar_chart(
        title="Formatter Test",
        categories=["A", "B"],
        series_data=[[100, 200]],
        series_names=["Test"],
        y_format_type=format_type
    )
    config = assert_valid_echarts_string(response)
    
    if expected_content:
        formatter = config["yAxis"]["axisLabel"]["formatter"]
        assert expected_content in formatter
        assert formatter.startswith("function")
    else:
        assert "axisLabel" not in config["yAxis"]