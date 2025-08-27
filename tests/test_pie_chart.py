"""Tests specific to pie chart functionality according to ECharts specification."""

import pytest
from echart_server import create_pie_chart
from conftest import parse_echarts_string, assert_valid_echarts_string

# Access the actual function if it's wrapped
if hasattr(create_pie_chart, 'fn'):
    create_pie_chart = create_pie_chart.fn


def test_pie_chart_basic_structure(sample_pie_data):
    """Test basic pie chart structure matches ECharts specification."""
    response = create_pie_chart(
        title="Basic Pie Chart",
        data=sample_pie_data
    )
    config = assert_valid_echarts_string(response)
    
    # Check structure
    assert "series" in config
    assert len(config["series"]) == 1
    assert config["series"][0]["type"] == "pie"
    assert config["series"][0]["name"] == "Basic Pie Chart"
    assert config["series"][0]["data"] == sample_pie_data
    
    # Check default radius and center
    assert config["series"][0]["radius"] == "50%"
    assert config["series"][0]["center"] == ["50%", "50%"]
    
    # Check emphasis configuration
    assert "emphasis" in config["series"][0]
    assert "itemStyle" in config["series"][0]["emphasis"]


def test_pie_chart_tooltip_configuration():
    """Test pie chart has item trigger for tooltip."""
    response = create_pie_chart(
        title="Pie Chart",
        data=[{"name": "A", "value": 100}, {"name": "B", "value": 200}]
    )
    config = assert_valid_echarts_string(response)
    
    assert config["tooltip"]["trigger"] == "item"


def test_pie_chart_legend_configuration():
    """Test pie chart legend has horizontal orientation at center."""
    data = [
        {"name": "Category A", "value": 100},
        {"name": "Category B", "value": 200},
        {"name": "Category C", "value": 150}
    ]
    
    response = create_pie_chart(
        title="Pie with Legend",
        data=data
    )
    config = assert_valid_echarts_string(response)
    
    assert config["legend"]["orient"] == "horizontal"  # Updated config
    assert config["legend"]["left"] == "center"  # Updated config
    assert config["legend"]["data"] == ["Category A", "Category B", "Category C"]


def test_pie_chart_percentage_formatter():
    """Test pie chart formatter with and without percentage."""
    data = [{"name": "A", "value": 100}, {"name": "B", "value": 200}]
    
    # With percentage (default)
    response_with = create_pie_chart(
        title="With Percentage",
        data=data,
        show_percentage=True
    )
    config_with = assert_valid_echarts_string(response_with)
    assert "{d}%" in config_with["tooltip"]["formatter"]
    assert config_with["tooltip"]["formatter"] == "{a} <br/>{b}: {c} ({d}%)"
    
    # Without percentage
    response_without = create_pie_chart(
        title="Without Percentage",
        data=data,
        show_percentage=False
    )
    config_without = assert_valid_echarts_string(response_without)
    assert "{d}%" not in config_without["tooltip"]["formatter"]
    assert config_without["tooltip"]["formatter"] == "{a} <br/>{b}: {c}"


def test_pie_chart_custom_radius():
    """Test pie chart with custom radius settings."""
    data = [{"name": "A", "value": 100}]
    
    # Single radius value
    response = create_pie_chart(
        title="Custom Radius",
        data=data,
        radius="75%"
    )
    config = assert_valid_echarts_string(response)
    assert config["series"][0]["radius"] == "75%"
    
    # Test with different radius values
    radii = ["10%", "30%", "50%", "80%", "100%"]
    for radius in radii:
        response = create_pie_chart(
            title=f"Radius {radius}",
            data=data,
            radius=radius
        )
        config = assert_valid_echarts_string(response)
        assert config["series"][0]["radius"] == radius


def test_pie_chart_custom_center():
    """Test pie chart with custom center position."""
    data = [{"name": "A", "value": 100}]
    
    # Custom center
    custom_center = ["40%", "60%"]
    response = create_pie_chart(
        title="Custom Center",
        data=data,
        center=custom_center
    )
    config = assert_valid_echarts_string(response)
    assert config["series"][0]["center"] == custom_center
    
    # Default center when None
    response_default = create_pie_chart(
        title="Default Center",
        data=data,
        center=None
    )
    config_default = assert_valid_echarts_string(response_default)
    assert config_default["series"][0]["center"] == ["50%", "50%"]


def test_pie_chart_emphasis_configuration():
    """Test pie chart emphasis state configuration."""
    response = create_pie_chart(
        title="Emphasis Test",
        data=[{"name": "A", "value": 100}]
    )
    config = assert_valid_echarts_string(response)
    
    emphasis = config["series"][0]["emphasis"]
    assert "itemStyle" in emphasis
    assert emphasis["itemStyle"]["shadowBlur"] == 12  # Updated value
    assert emphasis["itemStyle"]["shadowOffsetX"] == 0
    assert emphasis["itemStyle"]["shadowColor"] == "rgba(0, 0, 0, 0.35)"  # Updated opacity


def test_pie_chart_data_validation():
    """Test that pie chart validates data format."""
    # Valid data
    valid_data = [
        {"name": "Item1", "value": 100},
        {"name": "Item2", "value": 200}
    ]
    response = create_pie_chart(title="Valid", data=valid_data)
    config = assert_valid_echarts_string(response)
    assert config["series"][0]["data"] == valid_data
    
    # Invalid data - missing 'name'
    with pytest.raises(ValueError, match="Cada item de dados deve conter 'name' e 'value'"):
        create_pie_chart(
            title="Invalid",
            data=[{"value": 100}, {"name": "B", "value": 200}]
        )
    
    # Invalid data - missing 'value'
    with pytest.raises(ValueError, match="Cada item de dados deve conter 'name' e 'value'"):
        create_pie_chart(
            title="Invalid",
            data=[{"name": "A"}, {"name": "B", "value": 200}]
        )


def test_pie_chart_single_item():
    """Test pie chart with single data item."""
    response = create_pie_chart(
        title="Single Item",
        data=[{"name": "Only Item", "value": 1000}]
    )
    config = assert_valid_echarts_string(response)
    
    assert len(config["series"][0]["data"]) == 1
    assert config["series"][0]["data"][0]["name"] == "Only Item"
    assert config["series"][0]["data"][0]["value"] == 1000


def test_pie_chart_many_items():
    """Test pie chart with many data items."""
    data = [{"name": f"Item {i}", "value": i * 10} for i in range(50)]
    
    response = create_pie_chart(
        title="Many Items",
        data=data
    )
    config = assert_valid_echarts_string(response)
    
    assert len(config["series"][0]["data"]) == 50
    assert len(config["legend"]["data"]) == 50


def test_pie_chart_zero_values():
    """Test pie chart with zero values."""
    data = [
        {"name": "Zero", "value": 0},
        {"name": "Non-zero", "value": 100}
    ]
    
    response = create_pie_chart(
        title="With Zero",
        data=data
    )
    config = assert_valid_echarts_string(response)
    
    assert config["series"][0]["data"] == data


def test_pie_chart_negative_values():
    """Test pie chart with negative values (should work but may not display correctly)."""
    data = [
        {"name": "Negative", "value": -50},
        {"name": "Positive", "value": 150}
    ]
    
    response = create_pie_chart(
        title="With Negative",
        data=data
    )
    config = assert_valid_echarts_string(response)
    
    assert config["series"][0]["data"] == data


def test_pie_chart_decimal_values():
    """Test pie chart with decimal values."""
    data = [
        {"name": "Decimal 1", "value": 33.33},
        {"name": "Decimal 2", "value": 66.67}
    ]
    
    response = create_pie_chart(
        title="Decimal Values",
        data=data
    )
    config = assert_valid_echarts_string(response)
    
    assert config["series"][0]["data"] == data


def test_pie_chart_special_characters_in_names():
    """Test pie chart with special characters in data names."""
    data = [
        {"name": "Item™", "value": 100},
        {"name": "Item & Co.", "value": 200},
        {"name": "测试项目", "value": 150},
        {"name": "Item <special>", "value": 250}
    ]
    
    response = create_pie_chart(
        title="Special Names",
        data=data
    )
    config = assert_valid_echarts_string(response)
    
    assert config["series"][0]["data"] == data
    legend_names = [item["name"] for item in data]
    assert config["legend"]["data"] == legend_names


def test_pie_chart_very_long_names():
    """Test pie chart with very long item names."""
    long_name = "This is a very long item name that might cause display issues " * 2
    data = [
        {"name": long_name, "value": 100},
        {"name": "Short", "value": 200}
    ]
    
    response = create_pie_chart(
        title="Long Names",
        data=data
    )
    config = assert_valid_echarts_string(response)
    
    assert config["series"][0]["data"][0]["name"] == long_name
    assert config["legend"]["data"][0] == long_name


def test_pie_chart_different_radius_formats():
    """Test pie chart with different radius format possibilities."""
    data = [{"name": "Test", "value": 100}]
    
    # Percentage string
    response = create_pie_chart(
        title="Percentage Radius",
        data=data,
        radius="60%"
    )
    config = assert_valid_echarts_string(response)
    assert config["series"][0]["radius"] == "60%"


def test_pie_chart_different_center_formats():
    """Test pie chart with different center position formats."""
    data = [{"name": "Test", "value": 100}]
    
    # Percentage positions
    center_positions = [
        ["0%", "0%"],
        ["25%", "25%"],
        ["50%", "50%"],
        ["75%", "75%"],
        ["100%", "100%"]
    ]
    
    for center in center_positions:
        response = create_pie_chart(
            title="Center Test",
            data=data,
            center=center
        )
        config = assert_valid_echarts_string(response)
        assert config["series"][0]["center"] == center


def test_pie_chart_all_parameters():
    """Test pie chart with all parameters specified."""
    data = [
        {"name": "Category A", "value": 300},
        {"name": "Category B", "value": 500},
        {"name": "Category C", "value": 200}
    ]
    
    response = create_pie_chart(
        title="Full Configuration",
        data=data,
        show_percentage=True,
        radius="70%",
        center=["45%", "55%"]
    )
    config = assert_valid_echarts_string(response)
    
    assert config["title"]["text"] == "Full Configuration"
    assert config["series"][0]["data"] == data
    assert config["series"][0]["radius"] == "70%"
    assert config["series"][0]["center"] == ["45%", "55%"]
    assert "{d}%" in config["tooltip"]["formatter"]


def test_pie_chart_no_axis():
    """Test that pie charts don't have xAxis or yAxis."""
    response = create_pie_chart(
        title="No Axis",
        data=[{"name": "A", "value": 100}]
    )
    config = assert_valid_echarts_string(response)
    
    assert "xAxis" not in config
    assert "yAxis" not in config