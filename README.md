# Detecção de carrinhos abandonados

## Descrição

Este projeto tem como objetivo desenvolver um job para identificar carrinhos abandonados por clientes de um e-commerce, verificando se eles completaram todas as etapas do fluxo padrão de um pedido: produto (`product`) → carrinho (`basket`) → finalização (`checkout`).

## Regra de identificação de abandono

Um carrinho é considerado abandonado quando o cliente interrompe o fluxo de compra na página `basket` e fica **10 minutos ou mais sem realizar uma nova interação** dentro da sessão.

O fluxo padrão de compra é:

`product` → `basket` → `checkout`

## Exemplo 1 — Sem abandono

* O cliente visualiza `product` às 12:00.
* Visualiza `basket` às 12:02.
* Visualiza `checkout` às 12:04.
* **Não temos um abandono**, pois o cliente completou o fluxo de compra.

## Exemplo 2 — Com abandono

* O cliente visualiza `product` às 13:00.
* Visualiza `basket` às 13:01.
* O cliente fica 15 minutos sem realizar nenhuma interação.
* Como a última interação ocorreu às 13:01, a sessão é encerrada após 10 minutos, às 13:11.
* **Temos um abandono**, pois o cliente estava em `basket` e não continuou o fluxo.

## Exemplo 3 — Sem abandono

* O cliente visualiza `product` às 14:00.
* Visualiza `basket` às 14:05.
* Visualiza `product` novamente às 14:10.
* Visualiza `product` novamente às 14:16.
* Visualiza `basket` às 14:20.
* Visualiza `checkout` às 14:21.
* **Não temos um abandono**, pois o cliente continuou interagindo e posteriormente completou o fluxo.

## Tecnologias utilizadas

* **Python**
* **Apache Beam**

## Estrutura do projeto

```text
abandoned-cart-beam/
├── input/
│   └── page-views.json
├── output/
├── src/
│   └── main.py
├── tests/
├── README.md
└── requirements.txt
```

## Como executar o projeto

### 1. Criar o ambiente virtual

**Windows (PowerShell):**

```powershell
python -m venv .venv
```

**macOS e Ubuntu:**

```bash
python3 -m venv .venv
```

### 2. Ativar o ambiente virtual

**Windows (PowerShell):**

```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS e Ubuntu:**

```bash
source .venv/bin/activate
```

### 3. Instalar as dependências

No Windows, macOS e Ubuntu:

```bash
pip install -r requirements.txt
```

### 4. Executar o projeto

**Windows (PowerShell):**

```powershell
python .\src\main.py
```

**macOS e Ubuntu:**

```bash
python3 src/main.py
```

### 5. Verificar o resultado

Após a execução, os resultados dos carrinhos abandonados estarão disponíveis na pasta `output/`.

O arquivo gerado terá um nome parecido com:

```text
abandoned-carts-00000-of-00001
```

## Formato do arquivo de entrada

O arquivo `page-views.json` contém os registros das interações dos clientes:

* `timestamp`: horário em que ocorreu a interação.
* `customer`: identificação do cliente.
* `page`: página acessada pelo cliente.
* `product`: produto relacionado à interação.
