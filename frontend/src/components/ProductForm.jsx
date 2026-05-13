import { useEffect, useState } from "react";

const emptyForm = {
  name: "",
  sku: "",
  price: "",
  stock_quantity: 0,
};

export function ProductForm({ selectedProduct, isSubmitting, onSubmit, onCancelEdit }) {
  const [form, setForm] = useState(emptyForm);

  useEffect(() => {
    if (!selectedProduct) {
      setForm(emptyForm);
      return;
    }

    setForm({
      name: selectedProduct.name,
      sku: selectedProduct.sku,
      price: selectedProduct.price,
      stock_quantity: selectedProduct.stock_quantity,
    });
  }, [selectedProduct]);

  async function handleSubmit(event) {
    event.preventDefault();
    await onSubmit({
      ...form,
      price: Number(form.price).toFixed(2),
      stock_quantity: Number(form.stock_quantity),
    });

    if (!selectedProduct) {
      setForm(emptyForm);
    }
  }

  return (
    <section className="panel">
      <div className="section-heading">
        <div>
          <span className="eyebrow">Produtos</span>
          <h2>{selectedProduct ? "Atualizar produto" : "Cadastrar produto"}</h2>
        </div>

        {selectedProduct && (
          <button className="ghost-button" type="button" onClick={onCancelEdit}>
            Cancelar
          </button>
        )}
      </div>

      <form className="form-grid" onSubmit={handleSubmit}>
        <label>
          Nome
          <input
            required
            maxLength={255}
            value={form.name}
            onChange={(event) => setForm((current) => ({ ...current, name: event.target.value }))}
            placeholder="Ex.: Teclado mecanico"
          />
        </label>

        <label>
          SKU
          <input
            required
            maxLength={100}
            value={form.sku}
            onChange={(event) => setForm((current) => ({ ...current, sku: event.target.value }))}
            placeholder="Ex.: TEC-001"
          />
        </label>

        <label>
          Preco
          <input
            required
            min="0.01"
            step="0.01"
            type="number"
            value={form.price}
            onChange={(event) => setForm((current) => ({ ...current, price: event.target.value }))}
            placeholder="0.00"
          />
        </label>

        <label>
          Estoque
          <input
            required
            min="0"
            step="1"
            type="number"
            value={form.stock_quantity}
            onChange={(event) => {
              const value = event.target.value === "" ? 0 : Number(event.target.value);
              setForm((current) => ({ ...current, stock_quantity: value }));
            }}
          />
        </label>

        <button className="primary-button" type="submit" disabled={isSubmitting}>
          {isSubmitting ? "Salvando..." : selectedProduct ? "Salvar alteracoes" : "Cadastrar"}
        </button>
      </form>
    </section>
  );
}
