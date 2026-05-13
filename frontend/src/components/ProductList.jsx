export function ProductList({
  products,
  isLoading,
  page,
  pages,
  totalProducts,
  onEdit,
  onPageChange,
}) {
  return (
    <section className="panel product-list">
      <div className="section-heading">
        <div>
          <span className="eyebrow">Estoque</span>
          <h2>Listagem de produtos</h2>
        </div>
        <strong>{totalProducts} produtos</strong>
      </div>

      {isLoading ? (
        <div className="empty-state">Carregando produtos...</div>
      ) : products.length === 0 ? (
        <div className="empty-state">Nenhum produto cadastrado.</div>
      ) : (
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Nome</th>
                <th>SKU</th>
                <th>Preco</th>
                <th>Estoque</th>
                <th />
              </tr>
            </thead>
            <tbody>
              {products.map((product) => (
                <tr key={product.external_id}>
                  <td>
                    <span className="strong">{product.name}</span>
                  </td>
                  <td>{product.sku}</td>
                  <td>{formatCurrency(product.price)}</td>
                  <td>
                    <span className={product.stock_quantity > 0 ? "stock-pill" : "stock-pill danger"}>
                      {product.stock_quantity}
                    </span>
                  </td>
                  <td className="actions-cell">
                    <button className="secondary-button" type="button" onClick={() => onEdit(product)}>
                      Editar
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <div className="pagination">
        <button
          className="ghost-button"
          type="button"
          disabled={page <= 1}
          onClick={() => onPageChange(page - 1)}
        >
          Anterior
        </button>
        <span>
          Pagina {page} de {Math.max(pages, 1)}
        </span>
        <button
          className="ghost-button"
          type="button"
          disabled={page >= pages}
          onClick={() => onPageChange(page + 1)}
        >
          Proxima
        </button>
      </div>
    </section>
  );
}

function formatCurrency(value) {
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(Number(value));
}
