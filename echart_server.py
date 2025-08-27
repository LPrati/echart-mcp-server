"""
MCP Server para construção de gráficos usando Apache ECharts.

Este servidor fornece ferramentas para criar gráficos de linha, barra e pizza
no padrão Apache ECharts, com suporte para formatação de dados em português brasileiro.
"""

import argparse
from typing import List, Dict, Any, Optional, Union
from fastmcp import FastMCP
from formatters import create_echarts_formatter

mcp = FastMCP("EChart Graph Builder")


@mcp.tool
def create_line_chart(
    title: str,
    x_data: List[str],
    y_data: List[List[Union[int, float]]],
    series_names: List[str],
    x_label: Optional[str] = None,
    y_label: Optional[str] = None,
    y_format_type: Optional[str] = None
) -> Dict[str, Any]:
    """
    Cria um gráfico de linhas no padrão Apache ECharts.
    
    Args:
        title: Título do gráfico.
        x_data: Lista de valores para o eixo X (ex: datas, categorias).
        y_data: Lista de listas com valores do eixo Y (uma lista por série).
        series_names: Lista com nomes das séries.
        x_label: Rótulo do eixo X (opcional).
        y_label: Rótulo do eixo Y (opcional).
        y_format_type: Tipo de formatação do eixo Y ('currency_brl', 'percentage', 'absolute', None).
        
    Returns:
        Configuração completa do gráfico ECharts.
    """
    if len(y_data) != len(series_names):
        raise ValueError("Número de séries de dados deve corresponder ao número de nomes de séries")
    
    formatter_js = create_echarts_formatter(y_format_type)
    
    config = {
        "title": {
            "text": title,
            "left": "center"
        },
        "tooltip": {
            "trigger": "axis"
        },
        "legend": {
            "data": series_names,
            "top": "bottom"
        },
        "xAxis": {
            "type": "category",
            "data": x_data,
            "name": x_label or "",
            "nameLocation": "middle",
            "nameGap": 30
        },
        "yAxis": {
            "type": "value",
            "name": y_label or "",
            "nameLocation": "middle",
            "nameGap": 50
        },
        "series": []
    }
    
    for i, (name, data) in enumerate(zip(series_names, y_data)):
        config["series"].append({
            "name": name,
            "type": "line",
            "data": data,
            "smooth": True
        })
    
    if y_format_type:
        config["yAxis"]["axisLabel"] = {"formatter": formatter_js}
        config["tooltip"]["valueFormatter"] = formatter_js
    
    return config


@mcp.tool
def create_bar_chart(
    title: str,
    categories: List[str],
    series_data: List[List[Union[int, float]]],
    series_names: List[str],
    x_label: Optional[str] = None,
    y_label: Optional[str] = None,
    y_format_type: Optional[str] = None,
    stack: Optional[bool] = False
) -> Dict[str, Any]:
    """
    Cria um gráfico de barras no padrão Apache ECharts.
    
    Args:
        title: Título do gráfico.
        categories: Lista de categorias do eixo X.
        series_data: Lista de listas com valores (uma lista por série).
        series_names: Lista com nomes das séries.
        x_label: Rótulo do eixo X (opcional).
        y_label: Rótulo do eixo Y (opcional).
        y_format_type: Tipo de formatação do eixo Y ('currency_brl', 'percentage', 'absolute', None).
        stack: Se True, cria barras empilhadas.
        
    Returns:
        Configuração completa do gráfico ECharts.
    """
    if len(series_data) != len(series_names):
        raise ValueError("Número de séries de dados deve corresponder ao número de nomes de séries")
    
    formatter_js = create_echarts_formatter(y_format_type)
    
    config = {
        "title": {
            "text": title,
            "left": "center"
        },
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {
                "type": "shadow"
            }
        },
        "legend": {
            "data": series_names,
            "top": "bottom"
        },
        "xAxis": {
            "type": "category",
            "data": categories,
            "name": x_label or "",
            "nameLocation": "middle",
            "nameGap": 30
        },
        "yAxis": {
            "type": "value",
            "name": y_label or "",
            "nameLocation": "middle",
            "nameGap": 50
        },
        "series": []
    }
    
    for i, (name, data) in enumerate(zip(series_names, series_data)):
        series_config = {
            "name": name,
            "type": "bar",
            "data": data
        }
        if stack:
            series_config["stack"] = "total"
        config["series"].append(series_config)
    
    if y_format_type:
        config["yAxis"]["axisLabel"] = {"formatter": formatter_js}
        config["tooltip"]["valueFormatter"] = formatter_js
    
    return config


@mcp.tool
def create_pie_chart(
    title: str,
    data: List[Dict[str, Union[str, int, float]]],
    show_percentage: bool = True,
    radius: str = "50%",
    center: List[str] = None
) -> Dict[str, Any]:
    """
    Cria um gráfico de pizza no padrão Apache ECharts.
    
    Args:
        title: Título do gráfico.
        data: Lista de dicionários com 'name' e 'value' para cada fatia.
        show_percentage: Se True, mostra porcentagem no tooltip.
        radius: Raio do gráfico (padrão: "50%").
        center: Posição do centro [x, y] (padrão: ["50%", "50%"]).
        
    Returns:
        Configuração completa do gráfico ECharts.
    """
    if not all('name' in item and 'value' in item for item in data):
        raise ValueError("Cada item de dados deve conter 'name' e 'value'")
    
    if center is None:
        center = ["50%", "50%"]
    
    legend_data = [item['name'] for item in data]
    
    config = {
        "title": {
            "text": title,
            "left": "center"
        },
        "tooltip": {
            "trigger": "item"
        },
        "legend": {
            "data": legend_data,
            "orient": "vertical",
            "left": "left"
        },
        "series": [
            {
                "name": title,
                "type": "pie",
                "radius": radius,
                "center": center,
                "data": data,
                "emphasis": {
                    "itemStyle": {
                        "shadowBlur": 10,
                        "shadowOffsetX": 0,
                        "shadowColor": "rgba(0, 0, 0, 0.5)"
                    }
                }
            }
        ]
    }
    
    if show_percentage:
        config["tooltip"]["formatter"] = "{a} <br/>{b}: {c} ({d}%)"
    else:
        config["tooltip"]["formatter"] = "{a} <br/>{b}: {c}"
    
    return config


@mcp.tool
def create_combined_chart(
    title: str,
    x_data: List[str],
    line_data: Optional[List[Dict[str, Any]]] = None,
    bar_data: Optional[List[Dict[str, Any]]] = None,
    x_label: Optional[str] = None,
    y_label: Optional[str] = None,
    y_format_type: Optional[str] = None
) -> Dict[str, Any]:
    """
    Cria um gráfico combinado de linhas e barras no padrão Apache ECharts.
    
    Args:
        title: Título do gráfico.
        x_data: Lista de valores para o eixo X.
        line_data: Lista de dicionários com 'name' e 'data' para séries de linha.
        bar_data: Lista de dicionários com 'name' e 'data' para séries de barra.
        x_label: Rótulo do eixo X (opcional).
        y_label: Rótulo do eixo Y (opcional).
        y_format_type: Tipo de formatação do eixo Y ('currency_brl', 'percentage', 'absolute', None).
        
    Returns:
        Configuração completa do gráfico ECharts.
    """
    if not line_data and not bar_data:
        raise ValueError("Deve fornecer pelo menos dados de linha ou barra")
    
    formatter_js = create_echarts_formatter(y_format_type)
    
    all_series_names = []
    if line_data:
        all_series_names.extend([item['name'] for item in line_data])
    if bar_data:
        all_series_names.extend([item['name'] for item in bar_data])
    
    config = {
        "title": {
            "text": title,
            "left": "center"
        },
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {
                "type": "cross"
            }
        },
        "legend": {
            "data": all_series_names,
            "top": "bottom"
        },
        "xAxis": {
            "type": "category",
            "data": x_data,
            "name": x_label or "",
            "nameLocation": "middle",
            "nameGap": 30
        },
        "yAxis": {
            "type": "value",
            "name": y_label or "",
            "nameLocation": "middle",
            "nameGap": 50
        },
        "series": []
    }
    
    if line_data:
        for item in line_data:
            config["series"].append({
                "name": item['name'],
                "type": "line",
                "data": item['data'],
                "smooth": True
            })
    
    if bar_data:
        for item in bar_data:
            config["series"].append({
                "name": item['name'],
                "type": "bar",
                "data": item['data']
            })
    
    if y_format_type:
        config["yAxis"]["axisLabel"] = {"formatter": formatter_js}
        config["tooltip"]["valueFormatter"] = formatter_js
    
    return config


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EChart MCP Server")
    parser.add_argument(
        "--host", 
        type=str, 
        default="127.0.0.1",
        help="Host to bind the server (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=8000,
        help="Port to bind the server (default: 8000)"
    )
    
    args = parser.parse_args()
    
    mcp.run(
        transport="sse", 
        host=args.host,
        port=args.port,
        show_banner=False
    )