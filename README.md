# MCP Server para Gráficos Apache ECharts

Servidor MCP (Model Context Protocol) para construção de gráficos usando o padrão Apache ECharts. Fornece ferramentas para criar visualizações de dados profissionais com formatação em português brasileiro.

## Características

- ✅ Gráficos de linha para séries temporais
- ✅ Gráficos de barras para comparação de categorias
- ✅ Gráficos de pizza para visualização de proporções
- ✅ Gráficos combinados (linha + barra)
- ✅ Formatação automática de valores em R$
- ✅ Suporte para porcentagens e valores absolutos
- ✅ Formatação de datas em padrão brasileiro

## Instalação

```bash
# Instalar dependências com uv
uv pip install -r requirements.txt

# Ou com pip
pip install -r requirements.txt
```

## Uso

### Executar o servidor

```bash
uv run python echart_server.py
```

### Ferramentas Disponíveis

#### 1. `create_line_chart`

Cria gráficos de linha para visualizar séries temporais ou tendências.

**Parâmetros:**
- `title` (str): Título do gráfico
- `x_data` (List[str]): Valores do eixo X (ex: datas, meses)
- `y_data` (List[List[float]]): Valores do eixo Y (uma lista por série)
- `series_names` (List[str]): Nomes das séries
- `x_label` (str, opcional): Rótulo do eixo X
- `y_label` (str, opcional): Rótulo do eixo Y
- `y_format_type` (str, opcional): Tipo de formatação ('currency_brl', 'percentage', 'absolute')

**Exemplo:**
```python
result = create_line_chart(
    title="Vendas Mensais",
    x_data=["Jan", "Fev", "Mar", "Abr"],
    y_data=[[100000, 120000, 115000, 140000]],
    series_names=["Vendas 2024"],
    y_format_type="currency_brl"
)
```

#### 2. `create_bar_chart`

Cria gráficos de barras para comparar categorias ou grupos.

**Parâmetros:**
- `title` (str): Título do gráfico
- `categories` (List[str]): Categorias do eixo X
- `series_data` (List[List[float]]): Valores (uma lista por série)
- `series_names` (List[str]): Nomes das séries
- `x_label` (str, opcional): Rótulo do eixo X
- `y_label` (str, opcional): Rótulo do eixo Y
- `y_format_type` (str, opcional): Tipo de formatação
- `stack` (bool, opcional): Se True, cria barras empilhadas

**Exemplo:**
```python
result = create_bar_chart(
    title="Comparação de Vendas por Loja",
    categories=["Jan", "Fev", "Mar"],
    series_data=[
        [50000, 60000, 55000],  # Loja A
        [45000, 58000, 62000]   # Loja B
    ],
    series_names=["Loja A", "Loja B"],
    y_format_type="currency_brl"
)
```

#### 3. `create_pie_chart`

Cria gráficos de pizza para mostrar proporções ou distribuições.

**Parâmetros:**
- `title` (str): Título do gráfico
- `data` (List[Dict]): Lista de dicionários com 'name' e 'value'
- `show_percentage` (bool): Se True, mostra porcentagem no tooltip
- `radius` (str): Raio do gráfico (padrão: "50%")
- `center` (List[str]): Posição do centro [x, y]

**Exemplo:**
```python
result = create_pie_chart(
    title="Distribuição de Vendas por Categoria",
    data=[
        {"name": "Eletrônicos", "value": 45000},
        {"name": "Roupas", "value": 32000},
        {"name": "Alimentos", "value": 28000}
    ],
    show_percentage=True
)
```

#### 4. `create_combined_chart`

Cria gráficos combinados com linhas e barras.

**Parâmetros:**
- `title` (str): Título do gráfico
- `x_data` (List[str]): Valores do eixo X
- `line_data` (List[Dict], opcional): Dados para séries de linha
- `bar_data` (List[Dict], opcional): Dados para séries de barra
- `x_label` (str, opcional): Rótulo do eixo X
- `y_label` (str, opcional): Rótulo do eixo Y
- `y_format_type` (str, opcional): Tipo de formatação

**Exemplo:**
```python
result = create_combined_chart(
    title="Vendas vs Meta",
    x_data=["Jan", "Fev", "Mar"],
    bar_data=[{"name": "Vendas", "data": [100000, 120000, 115000]}],
    line_data=[{"name": "Meta", "data": [110000, 110000, 110000]}],
    y_format_type="currency_brl"
)
```

## Tipos de Formatação

### `currency_brl`
Formata valores como moeda brasileira (R$ 1.234,56)

### `percentage`
Formata valores como porcentagem (45.2%)

### `absolute`
Formata números com separador de milhares (1.234)

### `date`
Formata datas no padrão brasileiro (DD/MM/YYYY)

## Integração com Aplicações Web

Os objetos retornados pelo servidor são configurações completas do Apache ECharts que podem ser usados diretamente:

```javascript
// No frontend JavaScript
const chartConfig = await getChartFromMCP();  // Resultado do MCP server
const myChart = echarts.init(document.getElementById('chart'));
myChart.setOption(chartConfig);
```

## Estrutura do Projeto

```
echart-mcp-server/
├── echart_server.py      # Servidor MCP principal
├── formatters.py          # Funções de formatação
├── requirements.txt       # Dependências
└── README.md             # Esta documentação
```

## Requisitos

- Python 3.8+
- FastMCP
- Apache ECharts (no frontend para renderização)
