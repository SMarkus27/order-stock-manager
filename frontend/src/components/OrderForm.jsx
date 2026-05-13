import { useMemo, useState } from "react";

export function OrderForm({ products, isSubmitting, onSubmit }) {
  const [items, setItems] = useState([]);
  const availableProducts = useMemo(
    () => products.filter((product) => product.stock_quantity > 0),
    [products],
  );

  function addItem() {
    const firstProduct = availableProducts[0];
    if (!firstProduct) {
      return;
    }

    setItems((current) => [
      ...current,
      {
        product_external_id: firstProduct.external_id,
        quantity: 1,
      },
    ]);
  }

  function updateItem(index, item) {
    setItems((current) => current.map((currentItem, currentIndex) => (
      currentIndex === index ? item : currentItem
    )));
  }

  function removeItem(index) {
    setItems((current) => current.filter((_, currentIndex) => currentIndex !== index));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    if (items.length === 0) {
      return;
    }

    await onSubmit(items.map((item) => ({
      product_external_id: item.product_external_id,
      quantity: Number(item.quantity),
    })));
    setItems([]);
  }

  return (
    <section className="panel">
      <div className="section-heading">
        <div>
          <span className="eyebrow">Pedidos</span>
          <h2>Criar pedido</h2>
        </div>
        <button className="secondary-button" type="button" onClick={addItem} disabled={availableProducts.length === 0}>
          Adicionar item
        </button>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="order-items">
          {items.length === 0 ? (
            <div className="empty-state">Adicione produtos ao pedido.</div>
          ) : (
            items.map((item, index) => {
              const selectedProduct = products.find((product) => product.external_id === item.product_external_id);
              const maxQuantity = selectedProduct?.stock_quantity ?? 1;

              return (
                <div className="order-item" key={`${item.product_external_id}-${index}`}>
                  <label>
                    Produto
                    <select
                      value={item.product_external_id}
                      onChange={(event) => updateItem(index, {
                        product_external_id: event.target.value,
                        quantity: 1,
                      })}
                    >
                      {availableProducts.map((product) => (
                        <option key={product.external_id} value={product.external_id}>
                          {product.name} - {product.sku}
                        </option>
                      ))}
                    </select>
                  </label>

                  <label>
                    Quantidade
                    <input
                      min="1"
                      max={maxQuantity}
                      required
                      type="number"
                      value={item.quantity}
                      onChange={(event) => updateItem(index, {
                        ...item,
                        quantity: Number(event.target.value),
                      })}
                    />
                  </label>

                  <button className="ghost-button danger-text" type="button" onClick={() => removeItem(index)}>
                    Remover
                  </button>
                </div>
              );
            })
          )}
        </div>

        <button className="primary-button full-width" type="submit" disabled={isSubmitting || items.length === 0}>
          {isSubmitting ? "Criando pedido..." : "Criar pedido"}
        </button>
      </form>
    </section>
  );
}
