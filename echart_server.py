"""
MCP Server para construção de gráficos usando Apache ECharts.

Este servidor fornece ferramentas para criar gráficos de linha, barra e pizza
no padrão Apache ECharts, com suporte para formatação de dados em português brasileiro.
"""

import argparse
import json
from typing import List, Dict, Any, Optional, Union
from fastmcp import FastMCP
from formatters import create_echarts_formatter

mcp = FastMCP("EChart Graph Builder")


def format_echarts_response(config: Dict[str, Any]) -> str:
    """
    Converte configuração ECharts em string formatada.
    
    Args:
        config: Dicionário com a configuração do gráfico ECharts.
        
    Returns:
        String formatada com ```echarts\n{json}\n```
    """
    json_str = json.dumps(config, ensure_ascii=False, indent=4)
    return f"```echarts\n{json_str}\n```"


@mcp.tool
def create_line_chart(
    title: str,
    x_data: List[str],
    y_data: List[List[Union[int, float]]],
    series_names: List[str],
    x_label: Optional[str] = None,
    y_label: Optional[str] = None,
    y_format_type: Optional[str] = None
) -> str:
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
        String formatada com configuração completa do gráfico ECharts.
    """
    if len(y_data) != len(series_names):
        raise ValueError("Número de séries de dados deve corresponder ao número de nomes de séries")
    
    formatter_js = create_echarts_formatter(y_format_type)
    
    config = {
        "title": {
            "text": title,
            "left": "center"
        },
        "grid": {
            "top": 56,
            "right": 8,
            "left": 8,
            "bottom": 64,
            "containLabel": True
        },
        "tooltip": {
            "trigger": "axis",
            "confine": True,
            "axisPointer": {"type": "line", "snap": True},
            "order": "valueDesc"
        },
        "legend": {
            "data": series_names,
            "type": "scroll",
            "bottom": 8,
            "left": "center",
            "itemWidth": 12,
            "itemHeight": 8,
            "textStyle": {"fontSize": 11}
        },
        "xAxis": {
            "type": "category",
            "data": x_data,
            "name": x_label or "",
            "nameLocation": "middle",
            "nameGap": 30,
            "boundaryGap": False,
            "axisLabel": {
                "interval": 0,
                "hideOverlap": True,
                "fontSize": 11
            }
        },
        "yAxis": {
            "type": "value",
            "name": y_label or "",
            "nameLocation": "middle",
            "nameGap": 50
        },
        "dataZoom": [
            {"type": "inside", "xAxisIndex": 0}
        ],
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
    
    return format_echarts_response(config)


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
) -> str:
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
        String formatada com configuração completa do gráfico ECharts.
    """
    if len(series_data) != len(series_names):
        raise ValueError("Número de séries de dados deve corresponder ao número de nomes de séries")
    
    formatter_js = create_echarts_formatter(y_format_type)

    max_cat_len = max((len(str(c)) for c in categories), default=0)
    x_label_rotate = 0 if max_cat_len <= 8 else (30 if max_cat_len <= 14 else 45)

    
    config = {
        "title": {
            "text": title,
            "left": "center"
        },
        "grid": {
            "top": 56,
            "right": 8,
            "left": 8,
            "bottom": 72,
            "containLabel": True
        },

        "tooltip": {
            "trigger": "axis",
            "confine": True,
            "axisPointer": {"type": "shadow", "snap": True},
            "order": "valueDesc"
        },

        "legend": {
            "data": series_names,
            "type": "scroll",
            "bottom": 8,
            "left": "center",
            "itemWidth": 12,
            "itemHeight": 8,
            "textStyle": {"fontSize": 11}
        },
        "xAxis": {
            "type": "category",
            "data": categories,
            "name": x_label or "",
            "nameLocation": "middle",
            "nameGap": 30,
            "axisTick": {"alignWithLabel": True},
            "axisLabel": {
                "interval": 0,
                "hideOverlap": True,
                "rotate": x_label_rotate,
                "fontSize": 11
            }
        },
        "yAxis": {
            "type": "value",
            "name": y_label or "",
            "nameLocation": "middle",
            "nameGap": 50
        },
        "dataZoom": [
            {"type": "inside", "xAxisIndex": 0}
        ],
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
    
    return format_echarts_response(config)


@mcp.tool
def create_pie_chart(
    title: str,
    data: List[Dict[str, Union[str, int, float]]],
    show_percentage: bool = True,
    radius: str = "50%",
    center: List[str] = None
) -> str:
    """
    Cria um gráfico de pizza no padrão Apache ECharts.
    
    Args:
        title: Título do gráfico.
        data: Lista de dicionários com 'name' e 'value' para cada fatia.
        show_percentage: Se True, mostra porcentagem no tooltip.
        radius: Raio do gráfico (padrão: "50%").
        center: Posição do centro [x, y] (padrão: ["50%", "50%"]).
        
    Returns:
        String formatada com configuração completa do gráfico ECharts.
    """
    if not all('name' in item and 'value' in item for item in data):
        raise ValueError("Cada item de dados deve conter 'name' e 'value'")
    
    if center is None:
        center = ["50%", "50%"]
    
    legend_data = [item['name'] for item in data]
    num_slices = len(data)
    show_value_labels = num_slices <= 6

    if show_percentage:
        label_fmt = "{d}%"
        tooltip_fmt = "{a} <br/>{b}: {c} ({d}%)"
    else:
        label_fmt = "{c}"
        tooltip_fmt = "{a} <br/>{b}: {c}"
    
    config = {
        "title": {
            "text": title,
            "left": "center"
        },

        "tooltip": {
            "trigger": "item",
            "confine": True,
            "order": "valueDesc",
            "formatter": tooltip_fmt
        },

        "legend": {
            "data": legend_data,
            "type": "scroll",
            "bottom": 8,
            "left": "center",
            "orient": "horizontal",
            "itemWidth": 12,
            "itemHeight": 8,
            "textStyle": {"fontSize": 11}
        },

        "series": [
            {
                "name": title,
                "type": "pie",
                "radius": radius,
                "center": center,

                "avoidLabelOverlap": True,
                "minAngle": 3,
                "padAngle": 1,
                "selectedOffset": 6,

                "label": {
                    "show": show_value_labels,
                    "formatter": label_fmt,
                    "fontSize": 11,
                    "position": "outside"
                },
                "labelLine": {
                    "show": show_value_labels,
                    "length": 8,
                    "length2": 6,
                    "smooth": True
                },
                "labelLayout": { "hideOverlap": True },

                "data": data,

                "emphasis": {
                    "focus": "self",
                    "scale": True,
                    "scaleSize": 8,
                    "itemStyle": {
                        "shadowBlur": 12,
                        "shadowOffsetX": 0,
                        "shadowColor": "rgba(0, 0, 0, 0.35)"
                    },
                    "label": { "show": True }
                },

                "itemStyle": {
                    "borderColor": "#fff",
                    "borderWidth": 1
                }
            }
        ],

    }
    
    if show_percentage:
        config["tooltip"]["formatter"] = "{a} <br/>{b}: {c} ({d}%)"
    else:
        config["tooltip"]["formatter"] = "{a} <br/>{b}: {c}"
    
    return format_echarts_response(config)


@mcp.tool
def create_combined_chart(
    title: str,
    x_data: List[str],
    line_data: Optional[List[Dict[str, Any]]] = None,
    bar_data: Optional[List[Dict[str, Any]]] = None,
    x_label: Optional[str] = None,
    y_label: Optional[str] = None,
    y_format_type: Optional[str] = None
) -> str:
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
        String formatada com configuração completa do gráfico ECharts.
    """
    if not line_data and not bar_data:
        raise ValueError("Deve fornecer pelo menos dados de linha ou barra")
    
    formatter_js = create_echarts_formatter(y_format_type)
    
    all_series_names = []
    if line_data:
        all_series_names.extend([item['name'] for item in line_data])
    if bar_data:
        all_series_names.extend([item['name'] for item in bar_data])
    
    max_cat_len = max((len(str(c)) for c in x_data), default=0)
    x_label_rotate = 0 if max_cat_len <= 8 else (30 if max_cat_len <= 14 else 45)
    show_value_labels = len(x_data) <= 6
    has_bars = bool(bar_data)


    config = {
        "title": {
            "text": title,
            "left": "center"
        },

        "grid": {
            "top": 56,
            "right": 8,
            "left": 8,
            "bottom": 72,
            "containLabel": True
        },

        "tooltip": {
            "trigger": "axis",
            "confine": True,
            "axisPointer": {"type": "cross", "snap": True},
            "order": "valueDesc"
        },

        "legend": {
            "data": all_series_names,
            "type": "scroll",
            "bottom": 8,
            "left": "center",
            "itemWidth": 12,
            "itemHeight": 8,
            "textStyle": {"fontSize": 11}
        },

        "xAxis": {
            "type": "category",
            "data": x_data,
            "name": x_label or "",
            "nameLocation": "middle",
            "nameGap": 30,
            "boundaryGap": has_bars,
            "axisTick": {"alignWithLabel": True},
            "axisLabel": {
                "interval": 0,
                "hideOverlap": True,
                "rotate": x_label_rotate,
                "fontSize": 11
            }
        },
        "yAxis": {
            "type": "value",
            "name": y_label or "",
            "nameLocation": "middle",
            "nameGap": 50
        },
        "dataZoom": [
            {"type": "inside", "xAxisIndex": 0}
        ],
        "series": []
    }
    
    if line_data:
        for item in line_data:
            config["series"].append({
                "name": item["name"],
                "type": "line",
                "data": item["data"],
                "smooth": True,
                "symbol": "circle",
                "symbolSize": 8,
                "lineStyle": {"width": 3},
                "showSymbol": True,
                "emphasis": {"focus": "series"},
                "labelLayout": {"hideOverlap": True},
                "endLabel": {"show": True, "formatter": "{a}: {c}", "distance": 6}
            })
    
    if bar_data:
        for item in bar_data:
            series_cfg: Dict[str, Any] = {
                "name": item["name"],
                "type": "bar",
                "data": item["data"],
                "barMaxWidth": 36,
                "barGap": "10%",
                "emphasis": {"focus": "series"},
                "labelLayout": {"hideOverlap": True}
            }
            if show_value_labels:
                series_cfg["label"] = {
                    "show": True,
                    "position": "top",
                    "formatter": "{c}%" if y_format_type == "percentage" else "{c}"
                }
            config["series"].append(series_cfg)
    
    if y_format_type:
        config["yAxis"]["axisLabel"] = {"formatter": formatter_js}
        config["tooltip"]["valueFormatter"] = formatter_js
    
    return format_echarts_response(config)


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