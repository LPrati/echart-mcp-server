"""Tests for validating ECharts option configurations according to documentation."""

import pytest
from typing import Dict, Any, List
from conftest import parse_echarts_string, assert_valid_echarts_string


def test_title_option_structure(chart_functions, sample_x_data, sample_y_data, sample_series_names):
    """Test that title option follows ECharts specification."""
    # Create a sample chart
    response = chart_functions["line"](
        title="Test Chart",
        x_data=sample_x_data,
        y_data=sample_y_data,
        series_names=sample_series_names
    )
    config = assert_valid_echarts_string(response)
    
    # Validate title structure
    assert "title" in config
    assert isinstance(config["title"], dict)
    assert "text" in config["title"]
    assert config["title"]["text"] == "Test Chart"
    assert "left" in config["title"]
    assert config["title"]["left"] == "center"


def test_title_with_special_characters(chart_functions, sample_x_data, sample_y_data, sample_series_names):
    """Test title handling with special characters and unicode."""
    special_titles = [
        "Sales™ Report 2024",
        "Revenue €$ Analysis",
        "测试图表 🚀",
        "Q1 & Q2 <Results>",
        "Report: 'Quarterly' \"Analysis\""
    ]
    
    for title in special_titles:
        response = chart_functions["line"](
            title=title,
            x_data=sample_x_data,
            y_data=sample_y_data,
            series_names=sample_series_names
        )
        config = assert_valid_echarts_string(response)
        assert config["title"]["text"] == title


def test_tooltip_trigger_types(chart_functions, sample_x_data, sample_y_data, 
                               sample_series_names, sample_pie_data):
    """Test that tooltip trigger is set correctly for different chart types."""
    # Line chart should have axis trigger
    line_response = chart_functions["line"](
        title="Line Chart",
        x_data=sample_x_data,
        y_data=sample_y_data,
        series_names=sample_series_names
    )
    line_config = assert_valid_echarts_string(line_response)
    assert line_config["tooltip"]["trigger"] == "axis"
    
    # Bar chart should have axis trigger
    bar_response = chart_functions["bar"](
        title="Bar Chart",
        categories=sample_x_data,
        series_data=sample_y_data,
        series_names=sample_series_names
    )
    bar_config = assert_valid_echarts_string(bar_response)
    assert bar_config["tooltip"]["trigger"] == "axis"
    
    # Pie chart should have item trigger
    pie_response = chart_functions["pie"](
        title="Pie Chart",
        data=sample_pie_data
    )
    pie_config = assert_valid_echarts_string(pie_response)
    assert pie_config["tooltip"]["trigger"] == "item"


def test_tooltip_formatter_pie_chart(chart_functions, sample_pie_data):
    """Test tooltip formatter configuration for pie charts."""
    # With percentage
    response_with_percentage = chart_functions["pie"](
        title="Pie Chart",
        data=sample_pie_data,
        show_percentage=True
    )
    config_with_percentage = assert_valid_echarts_string(response_with_percentage)
    assert "formatter" in config_with_percentage["tooltip"]
    assert "{d}%" in config_with_percentage["tooltip"]["formatter"]
    
    # Without percentage
    response_without_percentage = chart_functions["pie"](
        title="Pie Chart",
        data=sample_pie_data,
        show_percentage=False
    )
    config_without_percentage = assert_valid_echarts_string(response_without_percentage)
    assert "formatter" in config_without_percentage["tooltip"]
    assert "{d}%" not in config_without_percentage["tooltip"]["formatter"]


def test_legend_data_alignment(chart_functions, sample_x_data, sample_y_data, sample_series_names):
    """Test that legend data aligns with series names."""
    response = chart_functions["line"](
        title="Test Chart",
        x_data=sample_x_data,
        y_data=sample_y_data,
        series_names=sample_series_names
    )
    config = assert_valid_echarts_string(response)
    
    assert "legend" in config
    assert "data" in config["legend"]
    assert config["legend"]["data"] == sample_series_names
    
    # Verify each series name appears in series
    for i, series in enumerate(config["series"]):
        assert series["name"] == sample_series_names[i]


def test_legend_positioning(chart_functions, sample_x_data, sample_y_data, 
                           sample_series_names, sample_pie_data):
    """Test legend positioning for different chart types."""
    # Line/Bar charts: bottom position
    line_response = chart_functions["line"](
        title="Line Chart",
        x_data=sample_x_data,
        y_data=sample_y_data,
        series_names=sample_series_names
    )
    line_config = assert_valid_echarts_string(line_response)
    assert line_config["legend"]["bottom"] == 8  # Updated config uses bottom: 8
    assert line_config["legend"]["left"] == "center"
    
    # Pie chart: horizontal center (updated config)
    pie_response = chart_functions["pie"](
        title="Pie Chart",
        data=sample_pie_data
    )
    pie_config = assert_valid_echarts_string(pie_response)
    assert pie_config["legend"]["orient"] == "horizontal"  # Updated to horizontal
    assert pie_config["legend"]["left"] == "center"  # Updated to center


def test_xaxis_configuration(chart_functions, sample_x_data, sample_y_data, sample_series_names):
    """Test xAxis configuration follows specification."""
    response = chart_functions["line"](
        title="Test Chart",
        x_data=sample_x_data,
        y_data=sample_y_data,
        series_names=sample_series_names,
        x_label="Month"
    )
    config = assert_valid_echarts_string(response)
    
    assert "xAxis" in config
    assert config["xAxis"]["type"] == "category"
    assert config["xAxis"]["data"] == sample_x_data
    assert config["xAxis"]["name"] == "Month"
    assert config["xAxis"]["nameLocation"] == "middle"
    assert config["xAxis"]["nameGap"] == 30


def test_yaxis_configuration(chart_functions, sample_x_data, sample_y_data, sample_series_names):
    """Test yAxis configuration follows specification."""
    response = chart_functions["line"](
        title="Test Chart",
        x_data=sample_x_data,
        y_data=sample_y_data,
        series_names=sample_series_names,
        y_label="Revenue"
    )
    config = assert_valid_echarts_string(response)
    
    assert "yAxis" in config
    assert config["yAxis"]["type"] == "value"
    assert config["yAxis"]["name"] == "Revenue"
    assert config["yAxis"]["nameLocation"] == "middle"
    assert config["yAxis"]["nameGap"] == 50


def test_axis_label_formatter_application(chart_functions, sample_x_data, sample_y_data, sample_series_names):
    """Test that formatter is correctly applied to yAxis when format_type is specified."""
    format_types = ["currency_brl", "percentage", "absolute"]
    
    for format_type in format_types:
        response = chart_functions["line"](
            title="Test Chart",
            x_data=sample_x_data,
            y_data=sample_y_data,
            series_names=sample_series_names,
            y_format_type=format_type
        )
        config = assert_valid_echarts_string(response)
        
        assert "axisLabel" in config["yAxis"]
        assert "formatter" in config["yAxis"]["axisLabel"]
        assert "function" in config["yAxis"]["axisLabel"]["formatter"]
        assert "valueFormatter" in config["tooltip"]


def test_axis_pointer_configuration(chart_functions, sample_x_data, sample_y_data, 
                                   sample_series_names, sample_bar_data, sample_line_data):
    """Test axisPointer configuration for different chart types."""
    # Bar chart should have shadow pointer
    bar_response = chart_functions["bar"](
        title="Bar Chart",
        categories=sample_x_data,
        series_data=sample_y_data,
        series_names=sample_series_names
    )
    bar_config = assert_valid_echarts_string(bar_response)
    assert "axisPointer" in bar_config["tooltip"]
    assert bar_config["tooltip"]["axisPointer"]["type"] == "shadow"
    
    # Combined chart should have cross pointer
    combined_response = chart_functions["combined"](
        title="Combined Chart",
        x_data=sample_x_data,
        line_data=sample_line_data,
        bar_data=sample_bar_data
    )
    combined_config = assert_valid_echarts_string(combined_response)
    assert "axisPointer" in combined_config["tooltip"]
    assert combined_config["tooltip"]["axisPointer"]["type"] == "cross"


def test_empty_axis_labels(chart_functions, sample_x_data, sample_y_data, sample_series_names):
    """Test that empty axis labels are handled correctly."""
    # Without labels (should be empty strings)
    response_no_labels = chart_functions["line"](
        title="Test Chart",
        x_data=sample_x_data,
        y_data=sample_y_data,
        series_names=sample_series_names
    )
    config_no_labels = assert_valid_echarts_string(response_no_labels)
    assert config_no_labels["xAxis"]["name"] == ""
    assert config_no_labels["yAxis"]["name"] == ""
    
    # With labels
    response_with_labels = chart_functions["line"](
        title="Test Chart",
        x_data=sample_x_data,
        y_data=sample_y_data,
        series_names=sample_series_names,
        x_label="Time",
        y_label="Value"
    )
    config_with_labels = assert_valid_echarts_string(response_with_labels)
    assert config_with_labels["xAxis"]["name"] == "Time"
    assert config_with_labels["yAxis"]["name"] == "Value"


@pytest.mark.parametrize("chart_type", ["line", "bar", "combined"])
def test_required_keys_present(chart_type, chart_functions, sample_x_data, sample_y_data, 
                              sample_series_names, sample_line_data, sample_bar_data,
                              expected_chart_structure):
    """Test that all required top-level keys are present for each chart type."""
    if chart_type == "line":
        response = chart_functions["line"](
            title="Test",
            x_data=sample_x_data,
            y_data=sample_y_data,
            series_names=sample_series_names
        )
        config = assert_valid_echarts_string(response)
    elif chart_type == "bar":
        response = chart_functions["bar"](
            title="Test",
            categories=sample_x_data,
            series_data=sample_y_data,
            series_names=sample_series_names
        )
        config = assert_valid_echarts_string(response)
    elif chart_type == "combined":
        response = chart_functions["combined"](
            title="Test",
            x_data=sample_x_data,
            line_data=sample_line_data,
            bar_data=sample_bar_data
        )
        config = assert_valid_echarts_string(response)
    
    expected_keys = expected_chart_structure[chart_type]
    for key in expected_keys:
        assert key in config, f"Missing required key '{key}' in {chart_type} chart"