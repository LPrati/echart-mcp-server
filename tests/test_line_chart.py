"""Tests specific to line chart functionality according to ECharts specification."""

import pytest
from echart_server import create_line_chart
from conftest import parse_echarts_string, assert_valid_echarts_string

# Access the actual function if it's wrapped
if hasattr(create_line_chart, 'fn'):
    create_line_chart = create_line_chart.fn


def test_line_chart_basic_structure(sample_x_data, sample_y_data, sample_series_names):
    """Test basic line chart structure matches ECharts specification."""
    response = create_line_chart(
        title="Basic Line Chart",
        x_data=sample_x_data,
        y_data=sample_y_data,
        series_names=sample_series_names
    )
    config = assert_valid_echarts_string(response)
    
    # Check series structure
    assert len(config["series"]) == len(sample_series_names)
    for i, series in enumerate(config["series"]):
        assert series["type"] == "line"
        assert series["name"] == sample_series_names[i]
        assert series["data"] == sample_y_data[i]
        assert series["smooth"] is True  # Server always uses smooth


def test_line_chart_single_series():
    """Test line chart with single series."""
    response = create_line_chart(
        title="Single Series",
        x_data=["Q1", "Q2", "Q3", "Q4"],
        y_data=[[100, 120, 110, 130]],
        series_names=["Revenue"]
    )
    config = assert_valid_echarts_string(response)
    
    assert len(config["series"]) == 1
    assert config["series"][0]["name"] == "Revenue"
    assert config["series"][0]["type"] == "line"
    assert len(config["series"][0]["data"]) == 4


def test_line_chart_multiple_series():
    """Test line chart with many series."""
    x_data = ["Jan", "Feb", "Mar"]
    series_names = [f"Series {i}" for i in range(10)]
    y_data = [[i * 100, i * 110, i * 120] for i in range(10)]
    
    response = create_line_chart(
        title="Multiple Series",
        x_data=x_data,
        y_data=y_data,
        series_names=series_names
    )
    config = assert_valid_echarts_string(response)
    
    assert len(config["series"]) == 10
    for i in range(10):
        assert config["series"][i]["name"] == f"Series {i}"
        assert config["series"][i]["data"] == y_data[i]


def test_line_chart_smooth_option():
    """Test that line charts always have smooth option set to true."""
    response = create_line_chart(
        title="Smooth Lines",
        x_data=["A", "B", "C"],
        y_data=[[1, 2, 3]],
        series_names=["Test"]
    )
    config = assert_valid_echarts_string(response)
    
    assert config["series"][0]["smooth"] is True


def test_line_chart_with_formatters():
    """Test line chart with different formatter types."""
    formatters = ["currency_brl", "percentage", "absolute", None]
    
    for formatter in formatters:
        response = create_line_chart(
            title="Formatted Chart",
            x_data=["Jan", "Feb"],
            y_data=[[100, 200]],
            series_names=["Sales"],
            y_format_type=formatter
        )
        config = assert_valid_echarts_string(response)
        
        if formatter:
            assert "axisLabel" in config["yAxis"]
            assert "formatter" in config["yAxis"]["axisLabel"]
            assert "valueFormatter" in config["tooltip"]
            assert "function" in config["yAxis"]["axisLabel"]["formatter"]
        else:
            assert "axisLabel" not in config["yAxis"]


def test_line_chart_data_validation():
    """Test that line chart validates data consistency."""
    # Mismatched series data and names
    with pytest.raises(ValueError, match="Número de séries de dados deve corresponder"):
        create_line_chart(
            title="Invalid",
            x_data=["A", "B"],
            y_data=[[1, 2], [3, 4], [5, 6]],  # 3 series
            series_names=["S1", "S2"]  # 2 names
        )


def test_line_chart_with_negative_values():
    """Test line chart handles negative values correctly."""
    response = create_line_chart(
        title="Negative Values",
        x_data=["Q1", "Q2", "Q3", "Q4"],
        y_data=[[-100, -50, 0, 50]],
        series_names=["Profit/Loss"]
    )
    config = assert_valid_echarts_string(response)
    
    assert config["series"][0]["data"] == [-100, -50, 0, 50]


def test_line_chart_with_decimal_values():
    """Test line chart handles decimal values correctly."""
    response = create_line_chart(
        title="Decimal Values",
        x_data=["A", "B", "C"],
        y_data=[[1.5, 2.7, 3.14159]],
        series_names=["Precise"]
    )
    config = assert_valid_echarts_string(response)
    
    assert config["series"][0]["data"] == [1.5, 2.7, 3.14159]


def test_line_chart_with_zero_values():
    """Test line chart handles zero values correctly."""
    response = create_line_chart(
        title="Zero Values",
        x_data=["A", "B", "C", "D"],
        y_data=[[0, 0, 0, 0]],
        series_names=["All Zeros"]
    )
    config = assert_valid_echarts_string(response)
    
    assert config["series"][0]["data"] == [0, 0, 0, 0]


def test_line_chart_axis_labels():
    """Test axis label configuration."""
    response = create_line_chart(
        title="With Labels",
        x_data=["Jan", "Feb"],
        y_data=[[100, 200]],
        series_names=["Data"],
        x_label="Month",
        y_label="Revenue (R$)"
    )
    config = assert_valid_echarts_string(response)
    
    assert config["xAxis"]["name"] == "Month"
    assert config["yAxis"]["name"] == "Revenue (R$)"
    assert config["xAxis"]["nameLocation"] == "middle"
    assert config["yAxis"]["nameLocation"] == "middle"


def test_line_chart_empty_labels():
    """Test line chart with empty/missing labels."""
    response = create_line_chart(
        title="No Labels",
        x_data=["A", "B"],
        y_data=[[1, 2]],
        series_names=["Test"]
    )
    config = assert_valid_echarts_string(response)
    
    assert config["xAxis"]["name"] == ""
    assert config["yAxis"]["name"] == ""


def test_line_chart_very_long_series_names():
    """Test line chart with very long series names."""
    long_name = "This is a very long series name that might cause display issues " * 3
    response = create_line_chart(
        title="Long Names",
        x_data=["A", "B"],
        y_data=[[1, 2]],
        series_names=[long_name]
    )
    config = assert_valid_echarts_string(response)
    
    assert config["series"][0]["name"] == long_name
    assert config["legend"]["data"][0] == long_name


def test_line_chart_special_characters_in_data():
    """Test line chart with special characters in x_data."""
    special_x_data = ["Q1'24", "Q2\"24", "Q3<24>", "Q4&24", "测试"]
    response = create_line_chart(
        title="Special Characters",
        x_data=special_x_data,
        y_data=[[100, 110, 120, 130, 140]],
        series_names=["Revenue"]
    )
    config = assert_valid_echarts_string(response)
    
    assert config["xAxis"]["data"] == special_x_data


def test_line_chart_large_dataset():
    """Test line chart with large dataset."""
    x_data = [f"Point_{i}" for i in range(1000)]
    y_data = [[i * 1.5 for i in range(1000)]]
    series_names = ["Large Dataset"]
    
    response = create_line_chart(
        title="Large Dataset",
        x_data=x_data,
        y_data=y_data,
        series_names=series_names
    )
    config = assert_valid_echarts_string(response)
    
    assert len(config["xAxis"]["data"]) == 1000
    assert len(config["series"][0]["data"]) == 1000


def test_line_chart_mixed_numeric_types():
    """Test line chart with mixed int and float values."""
    response = create_line_chart(
        title="Mixed Types",
        x_data=["A", "B", "C", "D"],
        y_data=[[100, 100.5, 101, 101.75]],
        series_names=["Mixed"]
    )
    config = assert_valid_echarts_string(response)
    
    assert config["series"][0]["data"] == [100, 100.5, 101, 101.75]


@pytest.mark.parametrize("format_type,expected_content", [
    ("currency_brl", "toLocaleString('pt-BR'"),
    ("percentage", "toFixed(1) + '%'"),
    ("absolute", "toLocaleString('pt-BR')"),
    (None, None)
])
def test_line_chart_formatter_content(format_type, expected_content):
    """Test that formatters contain expected JavaScript code."""
    response = create_line_chart(
        title="Formatter Test",
        x_data=["A", "B"],
        y_data=[[100, 200]],
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