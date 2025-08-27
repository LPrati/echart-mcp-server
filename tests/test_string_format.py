"""Tests for validating the string format output of chart functions."""

import pytest
import json
from echart_server import (
    create_line_chart,
    create_bar_chart,
    create_pie_chart,
    create_combined_chart
)
from conftest import parse_echarts_string

# Access the actual functions if they're wrapped
if hasattr(create_line_chart, 'fn'):
    create_line_chart = create_line_chart.fn
if hasattr(create_bar_chart, 'fn'):
    create_bar_chart = create_bar_chart.fn
if hasattr(create_pie_chart, 'fn'):
    create_pie_chart = create_pie_chart.fn
if hasattr(create_combined_chart, 'fn'):
    create_combined_chart = create_combined_chart.fn


def test_line_chart_returns_string():
    """Test that line chart returns a properly formatted string."""
    response = create_line_chart(
        title="Test Chart",
        x_data=["A", "B", "C"],
        y_data=[[1, 2, 3]],
        series_names=["Series"]
    )
    
    assert isinstance(response, str)
    assert response.startswith("```echarts\n")
    assert response.endswith("\n```")


def test_bar_chart_returns_string():
    """Test that bar chart returns a properly formatted string."""
    response = create_bar_chart(
        title="Test Chart",
        categories=["A", "B"],
        series_data=[[10, 20]],
        series_names=["Series"]
    )
    
    assert isinstance(response, str)
    assert response.startswith("```echarts\n")
    assert response.endswith("\n```")


def test_pie_chart_returns_string():
    """Test that pie chart returns a properly formatted string."""
    response = create_pie_chart(
        title="Test Chart",
        data=[{"name": "A", "value": 100}, {"name": "B", "value": 200}]
    )
    
    assert isinstance(response, str)
    assert response.startswith("```echarts\n")
    assert response.endswith("\n```")


def test_combined_chart_returns_string():
    """Test that combined chart returns a properly formatted string."""
    response = create_combined_chart(
        title="Test Chart",
        x_data=["A", "B", "C"],
        line_data=[{"name": "Line", "data": [1, 2, 3]}],
        bar_data=[{"name": "Bar", "data": [4, 5, 6]}]
    )
    
    assert isinstance(response, str)
    assert response.startswith("```echarts\n")
    assert response.endswith("\n```")


def test_json_is_properly_formatted():
    """Test that the JSON content is properly formatted with indentation."""
    response = create_line_chart(
        title="Test Chart",
        x_data=["A", "B"],
        y_data=[[100, 200]],
        series_names=["Series"]
    )
    
    # Extract JSON content
    json_content = response[len("```echarts\n"):-len("\n```")]
    
    # Verify it's valid JSON
    config = json.loads(json_content)
    assert isinstance(config, dict)
    
    # Check for proper indentation (should have newlines and spaces)
    assert "\n" in json_content
    assert "    " in json_content  # 4-space indentation


def test_unicode_characters_preserved():
    """Test that unicode characters are preserved in the output."""
    response = create_line_chart(
        title="测试图表 🚀",
        x_data=["一月", "二月", "三月"],
        y_data=[[100, 200, 300]],
        series_names=["销售额€$"]
    )
    
    assert isinstance(response, str)
    config = parse_echarts_string(response)
    
    assert config["title"]["text"] == "测试图表 🚀"
    assert config["xAxis"]["data"] == ["一月", "二月", "三月"]
    assert config["series"][0]["name"] == "销售额€$"


def test_special_characters_escaped():
    """Test that special characters are properly escaped in JSON."""
    response = create_line_chart(
        title='Title with "quotes" and \\backslash',
        x_data=["A", "B"],
        y_data=[[100, 200]],
        series_names=["Series'Name"]
    )
    
    assert isinstance(response, str)
    config = parse_echarts_string(response)
    
    assert config["title"]["text"] == 'Title with "quotes" and \\backslash'
    assert config["series"][0]["name"] == "Series'Name"


def test_formatter_javascript_preserved():
    """Test that JavaScript formatter functions are preserved as strings."""
    response = create_line_chart(
        title="Test Chart",
        x_data=["A", "B"],
        y_data=[[1000, 2000]],
        series_names=["Series"],
        y_format_type="currency_brl"
    )
    
    assert isinstance(response, str)
    config = parse_echarts_string(response)
    
    # Check that formatter is a string containing JavaScript
    assert "axisLabel" in config["yAxis"]
    formatter = config["yAxis"]["axisLabel"]["formatter"]
    assert isinstance(formatter, str)
    assert "function" in formatter
    assert "toLocaleString" in formatter


@pytest.mark.parametrize("chart_func,args", [
    (create_line_chart, {
        "title": "Test", 
        "x_data": ["A"], 
        "y_data": [[1]], 
        "series_names": ["S"]
    }),
    (create_bar_chart, {
        "title": "Test",
        "categories": ["A"],
        "series_data": [[1]],
        "series_names": ["S"]
    }),
    (create_pie_chart, {
        "title": "Test",
        "data": [{"name": "A", "value": 1}]
    }),
    (create_combined_chart, {
        "title": "Test",
        "x_data": ["A"],
        "line_data": [{"name": "L", "data": [1]}]
    })
])
def test_all_charts_follow_string_format(chart_func, args):
    """Test that all chart functions follow the same string format."""
    response = chart_func(**args)
    
    assert isinstance(response, str)
    assert response.startswith("```echarts\n")
    assert response.endswith("\n```")
    
    # Verify the JSON is parseable
    json_content = response[len("```echarts\n"):-len("\n```")]
    config = json.loads(json_content)
    assert isinstance(config, dict)
    assert "title" in config