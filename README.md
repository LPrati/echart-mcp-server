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
# Executar com configurações padrão (127.0.0.1:8000)
uv run python echart_server.py

# Especificar host e porta customizados
uv run python echart_server.py --host 0.0.0.0 --port 8080

# Ver opções disponíveis
uv run python echart_server.py --help
```

#### Parâmetros de Execução

- `--host`: Endereço IP para bind do servidor (padrão: `127.0.0.1`)
  - Use `127.0.0.1` para acesso local apenas
  - Use `0.0.0.0` para aceitar conexões de qualquer interface (útil em Docker)
  
- `--port`: Porta para o servidor (padrão: `8000`)

#### Exemplos de Uso

```bash
# Desenvolvimento local
python echart_server.py

# Produção/Docker - aceitar conexões externas
python echart_server.py --host 0.0.0.0 --port 8080

# Porta customizada mantendo acesso local
python echart_server.py --port 3000
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

**Retorno:**
String formatada no padrão:
```
```echarts
{
    "title": {...},
    "xAxis": {...},
    ...
}
```
```

**Exemplo:**
```python
result = create_line_chart(
    title="Vendas Mensais",
    x_data=["Jan", "Fev", "Mar", "Abr"],
    y_data=[[100000, 120000, 115000, 140000]],
    series_names=["Vendas 2024"],
    y_format_type="currency_brl"
)
# result será uma string começando com ```echarts
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

**Retorno:**
String formatada com configuração ECharts.

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
# result será uma string com a configuração completa do gráfico
```

#### 3. `create_pie_chart`

Cria gráficos de pizza para mostrar proporções ou distribuições.

**Parâmetros:**
- `title` (str): Título do gráfico
- `data` (List[Dict]): Lista de dicionários com 'name' e 'value'
- `show_percentage` (bool): Se True, mostra porcentagem no tooltip
- `radius` (str): Raio do gráfico (padrão: "50%")
- `center` (List[str]): Posição do centro [x, y]

**Retorno:**
String formatada com configuração ECharts.

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
# result será uma string formatada no padrão especificado
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

**Retorno:**
String formatada com configuração ECharts.

**Exemplo:**
```python
result = create_combined_chart(
    title="Vendas vs Meta",
    x_data=["Jan", "Fev", "Mar"],
    bar_data=[{"name": "Vendas", "data": [100000, 120000, 115000]}],
    line_data=[{"name": "Meta", "data": [110000, 110000, 110000]}],
    y_format_type="currency_brl"
)
# result será uma string formatada para uso direto
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

As ferramentas retornam strings formatadas com a configuração completa do Apache ECharts:

```javascript
// No frontend JavaScript
const response = await getChartFromMCP();  // String retornada do MCP server
// A string vem no formato ```echarts\n{...}\n```
// Extrair o JSON da string
const jsonContent = response.slice(11, -4);  // Remove ```echarts\n e \n```
const chartConfig = JSON.parse(jsonContent);

// Usar no ECharts
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
