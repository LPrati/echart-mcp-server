"""Tests for formatter functions according to ECharts specification."""

import pytest
from datetime import datetime
from formatters import (
    format_currency_brl,
    format_percentage,
    format_absolute,
    format_date,
    get_formatter_function,
    create_echarts_formatter
)


class TestCurrencyFormatter:
    """Tests for Brazilian Real currency formatter."""
    
    def test_format_currency_basic(self):
        """Test basic currency formatting."""
        assert format_currency_brl(1234.56) == "R$ 1.234,56"
        assert format_currency_brl(1000) == "R$ 1.000,00"
        assert format_currency_brl(0) == "R$ 0,00"
    
    def test_format_currency_large_numbers(self):
        """Test currency formatting with large numbers."""
        assert format_currency_brl(1000000) == "R$ 1.000.000,00"
        assert format_currency_brl(1234567.89) == "R$ 1.234.567,89"
    
    def test_format_currency_small_numbers(self):
        """Test currency formatting with small numbers."""
        assert format_currency_brl(0.01) == "R$ 0,01"
        assert format_currency_brl(0.99) == "R$ 0,99"
        assert format_currency_brl(10.50) == "R$ 10,50"
    
    def test_format_currency_negative(self):
        """Test currency formatting with negative values."""
        assert format_currency_brl(-1000) == "R$ -1.000,00"
        assert format_currency_brl(-50.25) == "R$ -50,25"
    
    def test_format_currency_rounding(self):
        """Test currency rounding to 2 decimal places."""
        assert format_currency_brl(10.999) == "R$ 11,00"
        assert format_currency_brl(10.994) == "R$ 10,99"
        assert format_currency_brl(10.995) == "R$ 10,99"  # Banker's rounding rounds to even


class TestPercentageFormatter:
    """Tests for percentage formatter."""
    
    def test_format_percentage_basic(self):
        """Test basic percentage formatting."""
        assert format_percentage(45.2) == "45.2%"
        assert format_percentage(100) == "100.0%"
        assert format_percentage(0) == "0.0%"
    
    def test_format_percentage_decimal_places(self):
        """Test percentage formatting with different decimal places."""
        assert format_percentage(45.234, 1) == "45.2%"
        assert format_percentage(45.234, 2) == "45.23%"
        assert format_percentage(45.234, 3) == "45.234%"
        assert format_percentage(45.234, 0) == "45%"
    
    def test_format_percentage_rounding(self):
        """Test percentage rounding."""
        assert format_percentage(45.25, 1) == "45.2%"
        assert format_percentage(45.26, 1) == "45.3%"
        assert format_percentage(99.95, 1) == "100.0%"
    
    def test_format_percentage_negative(self):
        """Test percentage formatting with negative values."""
        assert format_percentage(-10.5) == "-10.5%"
        assert format_percentage(-0.1) == "-0.1%"


class TestAbsoluteFormatter:
    """Tests for absolute number formatter."""
    
    def test_format_absolute_integers(self):
        """Test absolute formatting with integers."""
        assert format_absolute(1234) == "1.234"
        assert format_absolute(1000000) == "1.000.000"
        assert format_absolute(0) == "0"
        assert format_absolute(1) == "1"
    
    def test_format_absolute_with_decimals(self):
        """Test absolute formatting with decimal places."""
        assert format_absolute(1234.56, 2) == "1.234,56"
        assert format_absolute(1000.5, 1) == "1.000,5"
        assert format_absolute(0.123, 3) == "0,123"
    
    def test_format_absolute_negative(self):
        """Test absolute formatting with negative values."""
        assert format_absolute(-1234) == "-1.234"
        assert format_absolute(-1234.56, 2) == "-1.234,56"
    
    def test_format_absolute_large_numbers(self):
        """Test absolute formatting with very large numbers."""
        assert format_absolute(1234567890) == "1.234.567.890"
        assert format_absolute(9999999999) == "9.999.999.999"


class TestDateFormatter:
    """Tests for date formatter."""
    
    def test_format_date_basic(self):
        """Test basic date formatting."""
        assert format_date("2024-12-25") == "25/12/2024"
        assert format_date("2024-01-01") == "01/01/2024"
        assert format_date("2024-06-15") == "15/06/2024"
    
    def test_format_date_custom_formats(self):
        """Test date formatting with custom input/output formats."""
        assert format_date("2024-12-25", "%Y-%m-%d", "%d/%m/%Y") == "25/12/2024"
        assert format_date("25/12/2024", "%d/%m/%Y", "%Y-%m-%d") == "2024-12-25"
        assert format_date("2024-12-25", "%Y-%m-%d", "%B %d, %Y") == "December 25, 2024"
    
    def test_format_date_invalid(self):
        """Test date formatting with invalid dates."""
        # Invalid dates should return as-is
        assert format_date("invalid-date") == "invalid-date"
        assert format_date("2024-13-01") == "2024-13-01"  # Invalid month
        assert format_date("2024-12-32") == "2024-12-32"  # Invalid day
        assert format_date("") == ""
        assert format_date(None) == None


class TestGetFormatterFunction:
    """Tests for get_formatter_function."""
    
    def test_get_formatter_by_type(self):
        """Test getting formatter function by type."""
        currency_fn = get_formatter_function('currency_brl')
        assert currency_fn(1234.56) == "R$ 1.234,56"
        
        percentage_fn = get_formatter_function('percentage')
        assert percentage_fn(45.2) == "45.2%"
        
        absolute_fn = get_formatter_function('absolute')
        assert absolute_fn(1234) == "1.234"
        
        date_fn = get_formatter_function('date')
        assert date_fn("2024-12-25") == "25/12/2024"
    
    def test_get_formatter_none(self):
        """Test getting formatter with None type."""
        none_fn = get_formatter_function(None)
        assert none_fn(123) == "123"
        assert none_fn("test") == "test"
    
    def test_get_formatter_invalid_type(self):
        """Test getting formatter with invalid type."""
        invalid_fn = get_formatter_function('invalid_type')
        # Should return default (string conversion)
        assert invalid_fn(123) == "123"


class TestCreateEchartsFormatter:
    """Tests for JavaScript formatter creation."""
    
    def test_create_currency_formatter(self):
        """Test JavaScript currency formatter creation."""
        formatter = create_echarts_formatter('currency_brl')
        assert "function(value)" in formatter
        assert "toLocaleString('pt-BR'" in formatter
        assert "style: 'currency'" in formatter
        assert "currency: 'BRL'" in formatter
    
    def test_create_percentage_formatter(self):
        """Test JavaScript percentage formatter creation."""
        formatter = create_echarts_formatter('percentage')
        assert "function(value)" in formatter
        assert "toFixed(1)" in formatter
        assert "+ '%'" in formatter
    
    def test_create_absolute_formatter(self):
        """Test JavaScript absolute formatter creation."""
        formatter = create_echarts_formatter('absolute')
        assert "function(value)" in formatter
        assert "toLocaleString('pt-BR')" in formatter
    
    def test_create_date_formatter(self):
        """Test JavaScript date formatter creation."""
        formatter = create_echarts_formatter('date')
        assert "function(value)" in formatter
        assert "new Date(value)" in formatter
        assert "toLocaleDateString('pt-BR')" in formatter
    
    def test_create_default_formatter(self):
        """Test JavaScript default formatter creation."""
        formatter = create_echarts_formatter(None)
        assert "function(value)" in formatter
        assert "return value" in formatter
        
        formatter_invalid = create_echarts_formatter('invalid')
        assert "function(value)" in formatter_invalid
        assert "return value" in formatter_invalid
    
    def test_formatter_syntax(self):
        """Test that all formatters have valid JavaScript syntax."""
        format_types = ['currency_brl', 'percentage', 'absolute', 'date', None]
        
        for format_type in format_types:
            formatter = create_echarts_formatter(format_type)
            # Check basic JavaScript function structure
            assert formatter.startswith("function")
            assert "return" in formatter
            assert formatter.count("{") == formatter.count("}")
            assert "value" in formatter  # parameter is used


class TestFormatterEdgeCases:
    """Test edge cases for formatters."""
    
    def test_format_infinity(self):
        """Test formatters with infinity values."""
        inf = float('inf')
        assert format_currency_brl(inf) == "R$ ∞"
        assert format_percentage(inf) == "inf%"
        # format_absolute with infinity will raise OverflowError when converting to int
    
    def test_format_very_small_numbers(self):
        """Test formatters with very small numbers."""
        assert format_currency_brl(0.001) == "R$ 0,00"
        assert format_percentage(0.001, 3) == "0.001%"
        assert format_absolute(0.00001, 5) == "0,00001"
    
    def test_format_zero(self):
        """Test formatters with zero."""
        assert format_currency_brl(0) == "R$ 0,00"
        assert format_percentage(0) == "0.0%"
        assert format_absolute(0) == "0"
    
    def test_format_type_conversion(self):
        """Test formatters with values that need type conversion."""
        # Integer inputs
        assert format_currency_brl(100) == "R$ 100,00"
        assert format_percentage(50) == "50.0%"
        assert format_absolute(1000) == "1.000"


@pytest.mark.parametrize("value,expected", [
    (1234.56, "R$ 1.234,56"),
    (1000000, "R$ 1.000.000,00"),
    (0.99, "R$ 0,99"),
    (-500, "R$ -500,00"),
])
def test_currency_parametrized(value, expected):
    """Parametrized tests for currency formatter."""
    assert format_currency_brl(value) == expected


@pytest.mark.parametrize("value,decimals,expected", [
    (45.234, 1, "45.2%"),
    (100, 0, "100%"),
    (0.5, 2, "0.50%"),
    (-10, 1, "-10.0%"),
])
def test_percentage_parametrized(value, decimals, expected):
    """Parametrized tests for percentage formatter."""
    assert format_percentage(value, decimals) == expected


@pytest.mark.parametrize("format_type,js_content", [
    ("currency_brl", "toLocaleString('pt-BR'"),
    ("percentage", "toFixed(1) + '%'"),
    ("absolute", "toLocaleString('pt-BR')"),
    ("date", "toLocaleDateString('pt-BR')"),
    (None, "return value"),
])
def test_javascript_formatter_content(format_type, js_content):
    """Test that JavaScript formatters contain expected content."""
    formatter = create_echarts_formatter(format_type)
    assert js_content in formatter