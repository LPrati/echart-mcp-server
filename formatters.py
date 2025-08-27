"""
Formatadores para dados dos gráficos ECharts.

Este módulo fornece funções para formatar diferentes tipos de dados
usados nos gráficos, incluindo valores monetários em reais brasileiros,
porcentagens e datas.
"""

from typing import Union, List
from datetime import datetime


def format_currency_brl(value: Union[int, float]) -> str:
    """
    Formata um valor numérico como moeda brasileira.
    
    Args:
        value: Valor numérico a ser formatado.
        
    Returns:
        String formatada em reais brasileiros (ex: R$ 1.234,56).
    """
    # Handle special values
    if value != value:  # NaN check
        return "R$ NaN"
    if value == float('inf'):
        return "R$ ∞"
    if value == float('-inf'):
        return "R$ -∞"
    
    parts = f"{value:,.2f}".split(".")
    integer_part = parts[0].replace(",", ".")
    decimal_part = parts[1] if len(parts) > 1 else "00"
    return f"R$ {integer_part},{decimal_part}"


def format_percentage(value: Union[int, float], decimal_places: int = 1) -> str:
    """
    Formata um valor numérico como porcentagem.
    
    Args:
        value: Valor numérico a ser formatado.
        decimal_places: Número de casas decimais (padrão: 1).
        
    Returns:
        String formatada como porcentagem (ex: 45.2%).
    """
    return f"{value:.{decimal_places}f}%"


def format_absolute(value: Union[int, float], decimal_places: int = 0) -> str:
    """
    Formata um valor numérico absoluto com separador de milhares.
    
    Args:
        value: Valor numérico a ser formatado.
        decimal_places: Número de casas decimais (padrão: 0).
        
    Returns:
        String formatada com separador de milhares (ex: 1.234).
    """
    if decimal_places == 0:
        formatted = f"{int(value):,}".replace(",", ".")
    else:
        parts = f"{value:,.{decimal_places}f}".split(".")
        integer_part = parts[0].replace(",", ".")
        decimal_part = parts[1]
        formatted = f"{integer_part},{decimal_part}"
    return formatted


def format_date(date_str: str, input_format: str = "%Y-%m-%d", output_format: str = "%d/%m/%Y") -> str:
    """
    Formata uma string de data para o padrão brasileiro.
    
    Args:
        date_str: String da data a ser formatada.
        input_format: Formato de entrada da data (padrão: YYYY-MM-DD).
        output_format: Formato de saída da data (padrão: DD/MM/YYYY).
        
    Returns:
        String da data formatada no padrão brasileiro.
    """
    try:
        date_obj = datetime.strptime(date_str, input_format)
        return date_obj.strftime(output_format)
    except (ValueError, TypeError):
        return date_str


def get_formatter_function(format_type: str):
    """
    Retorna a função de formatação apropriada baseada no tipo.
    
    Args:
        format_type: Tipo de formatação ('currency_brl', 'percentage', 'absolute', 'date', None).
        
    Returns:
        Função de formatação apropriada ou função identidade se None.
    """
    formatters = {
        'currency_brl': lambda v: format_currency_brl(v),
        'percentage': lambda v: format_percentage(v),
        'absolute': lambda v: format_absolute(v),
        'date': lambda v: format_date(v) if isinstance(v, str) else str(v),
        None: lambda v: str(v)
    }
    return formatters.get(format_type, formatters[None])


def create_echarts_formatter(format_type: str) -> str:
    """
    Cria uma string de template para formatação no ECharts.
    
    Args:
        format_type: Tipo de formatação ('currency_brl', 'percentage', 'absolute', 'date', None).
        
    Returns:
        String contendo o template para usar no formatter do ECharts.
    """
    if format_type == 'currency_brl':
        # Template simples para moeda brasileira
        return "R$ {value}"
    elif format_type == 'percentage':
        # Template para porcentagem
        return "{value}%"
    elif format_type == 'absolute':
        # Template para valor absoluto
        return "{value}"
    elif format_type == 'date':
        # Template para data (limitado, mas funcional)
        return "{value}"
    else:
        return "{value}"