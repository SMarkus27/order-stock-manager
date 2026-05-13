# order-stock-manager

Aplicacao para gerenciamento de estoque e pedidos. O projeto tem um backend em
FastAPI com PostgreSQL e um frontend React/Vite em JavaScript.

## Funcionalidades

- Listar produtos com paginacao.
- Cadastrar produtos.
- Atualizar produtos.
- Remover produtos pela API.
- Criar pedidos com baixa de estoque.
- Exibir mensagens de sucesso e erro no frontend.

## Estrutura

```text
backend/
  main.py
  src/
    api/manager/v1/
    config/
    models/
frontend/
  src/
    api/
    components/
    context/
    hooks/
```

## Docker

O jeito mais simples de rodar o projeto completo e via Docker Compose.

```bash
docker compose up -d
```

Servicos expostos:

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:3002`
- PostgreSQL: `localhost:5432`

Para usar outra porta para o frontend no host:

```bash
FRONTEND_PORT=3001 docker compose up -d
```

Para verificar se a API subiu:

```bash
curl http://localhost:8000/health
```

## Backend

Backend em FastAPI com SQLAlchemy async e PostgreSQL.

Principais dependencias:

- FastAPI
- Uvicorn
- SQLAlchemy
- asyncpg
- Pydantic
- python-decouple

Variavel obrigatoria:

No arquivo .env em /backend:

```bash
DATABASE_URL=url
```

A API cria as tabelas automaticamente na inicializacao.

Documentacao interativa:

- Swagger: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Rotas principais

Base da API: `http://localhost:8000/api/v1`

| Metodo | Rota | Descricao |
| --- | --- | --- |
| `GET` | `/products/?page=1&per_page=10` | Lista produtos com paginacao |
| `GET` | `/products/{external_id}` | Busca um produto |
| `POST` | `/products/` | Cria um produto |
| `PATCH` | `/products/{external_id}` | Atualiza um produto |
| `DELETE` | `/products/{external_id}` | Remove um produto |
| `POST` | `/orders/orders` | Cria um pedido |

Health check fora do prefixo `/api/v1`:

| Metodo | Rota | Descricao |
| --- | --- | --- |
| `GET` | `/health` | Verifica se a API esta online |

Exemplo de produto:

```json
{
  "name": "Teclado mecanico",
  "sku": "TEC-001",
  "price": "199.90",
  "stock_quantity": 10
}
```

Exemplo de pedido:

```json
{
  "items": [
    {
      "product_external_id": "00000000-0000-0000-0000-000000000000",
      "quantity": 2
    }
  ]
}
```

## Frontend

Frontend em React com Vite, usando JavaScript e JSX.

Principais arquivos:

- `frontend/src/api/http.js`: cliente HTTP e tratamento de erro.
- `frontend/src/api/inventory.js`: chamadas para produtos e pedidos.
- `frontend/src/context/InventoryContext.jsx`: estado global do inventario.
- `frontend/src/components/`: formularios, lista e feedback visual.

Para rodar localmente:

```bash
cd frontend
npm install
npm run dev
```

O Vite local usa `http://localhost:3000` por padrao.

Por padrao, o frontend chama a API em:

```text
http://localhost:8000/api/v1
```

Para alterar a URL da API:

```bash
VITE_API_BASE_URL=http://localhost:8000/api/v1 npm run dev
```

Build de producao:

```bash
cd frontend
npm run build
```

Preview do build:

```bash
npm run preview
```


