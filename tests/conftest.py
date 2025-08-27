"""Pytest configuration and fixtures for ECharts MCP Server tests."""

import pytest
import sys
import os
import json
from typing import Dict, Any, List, Union

# Add parent directory to path so we can import the server modules
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import functions directly by accessing the wrapped function
from echart_server import (
    create_line_chart,
    create_bar_chart,
    create_pie_chart,
    create_combined_chart
)

from formatters import (
    format_currency_brl,
    format_percentage,
    format_absolute,
    format_date,
    create_echarts_formatter
)


@pytest.fixture
def sample_x_data() -> List[str]:
    """Sample x-axis data for testing."""
    return ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]


@pytest.fixture
def sample_y_data() -> List[List[float]]:
    """Sample y-axis data for testing (multiple series)."""
    return [
        [150000, 180000, 165000, 195000, 210000, 225000],
        [120000, 140000, 155000, 160000, 175000, 190000]
    ]


@pytest.fixture
def sample_series_names() -> List[str]:
    """Sample series names for testing."""
    return ["Series A", "Series B"]


@pytest.fixture
def sample_categories() -> List[str]:
    """Sample categories for bar charts."""
    return ["Electronics", "Clothing", "Food", "Books"]


@pytest.fixture
def sample_pie_data() -> List[Dict[str, Union[str, float]]]:
    """Sample data for pie charts."""
    return [
        {"name": "Product A", "value": 450000},
        {"name": "Product B", "value": 320000},
        {"name": "Product C", "value": 180000},
        {"name": "Product D", "value": 50000}
    ]


@pytest.fixture
def sample_line_data() -> List[Dict[str, Any]]:
    """Sample line series data for combined charts."""
    return [
        {"name": "Revenue", "data": [100000, 110000, 105000, 115000, 112000, 120000]},
        {"name": "Profit", "data": [20000, 22000, 21000, 23000, 22400, 24000]}
    ]


@pytest.fixture
def sample_bar_data() -> List[Dict[str, Any]]:
    """Sample bar series data for combined charts."""
    return [
        {"name": "Sales", "data": [95000, 102000, 98000, 112000, 108000, 118000]}
    ]


@pytest.fixture
def valid_format_types() -> List[str]:
    """Valid format types for y-axis formatting."""
    return ["currency_brl", "percentage", "absolute", None]


@pytest.fixture
def chart_functions():
    """Dictionary of chart creation functions."""
    # Access the actual function from the FunctionTool wrapper
    return {
        "line": create_line_chart.fn if hasattr(create_line_chart, 'fn') else create_line_chart,
        "bar": create_bar_chart.fn if hasattr(create_bar_chart, 'fn') else create_bar_chart,
        "pie": create_pie_chart.fn if hasattr(create_pie_chart, 'fn') else create_pie_chart,
        "combined": create_combined_chart.fn if hasattr(create_combined_chart, 'fn') else create_combined_chart
    }


@pytest.fixture
def formatter_functions():
    """Dictionary of formatter functions."""
    return {
        "currency_brl": format_currency_brl,
        "percentage": format_percentage,
        "absolute": format_absolute,
        "date": format_date,
        "create_formatter": create_echarts_formatter
    }


@pytest.fixture
def expected_chart_structure() -> Dict[str, List[str]]:
    """Expected top-level keys for each chart type."""
    return {
        "line": ["title", "tooltip", "legend", "xAxis", "yAxis", "series"],
        "bar": ["title", "tooltip", "legend", "xAxis", "yAxis", "series"],
        "pie": ["title", "tooltip", "legend", "series"],
        "combined": ["title", "tooltip", "legend", "xAxis", "yAxis", "series"]
    }


@pytest.fixture
def invalid_inputs() -> Dict[str, Any]:
    """Collection of invalid inputs for testing error handling."""
    return {
        "empty_string": "",
        "none": None,
        "empty_list": [],
        "wrong_type_string": "not_a_list",
        "wrong_type_number": 12345,
        "mismatched_lengths": {
            "y_data": [[1, 2], [3, 4], [5, 6]],
            "series_names": ["A", "B"]  # Length 2 vs 3
        }
    }


@pytest.fixture
def edge_case_values() -> Dict[str, Any]:
    """Edge case values for testing."""
    return {
        "zero": 0,
        "negative": -1000,
        "very_large": 1e12,
        "very_small": 1e-10,
        "infinity": float('inf'),
        "special_chars": "Test™ €©® 测试",
        "unicode": "🚀📊💰",
        "html_chars": "<script>alert('xss')</script>",
        "sql_injection": "'; DROP TABLE users; --"
    }


def parse_echarts_string(response: str) -> Dict[str, Any]:
    """Parse the formatted echarts string response and return the JSON config.
    
    Args:
        response: String in format ```echarts\n{json}\n```
        
    Returns:
        Parsed JSON configuration dictionary
        
    Raises:
        AssertionError: If format is invalid
    """
    assert isinstance(response, str), "Response must be a string"
    assert response.startswith("```echarts\n"), "Response must start with ```echarts followed by newline"
    assert response.endswith("\n```"), "Response must end with newline followed by ```"
    
    # Extract JSON content between markers
    json_content = response[len("```echarts\n"):-len("\n```")]
    
    try:
        config = json.loads(json_content)
    except json.JSONDecodeError as e:
        raise AssertionError(f"Invalid JSON in response: {e}")
    
    return config


def assert_valid_echarts_string(response: str) -> Dict[str, Any]:
    """Validate that response is properly formatted echarts string and return parsed config.
    
    Args:
        response: String response from chart creation function
        
    Returns:
        Parsed configuration dictionary for further validation
    """
    config = parse_echarts_string(response)
    assert_valid_echarts_config(config)
    return config


def assert_valid_echarts_config(config: Dict[str, Any]) -> None:
    """Helper function to validate ECharts configuration structure."""
    assert isinstance(config, dict), "Configuration must be a dictionary"
    assert "title" in config, "Configuration must have a title"
    assert isinstance(config["title"], dict), "Title must be a dictionary"
    assert "text" in config["title"], "Title must have text property"