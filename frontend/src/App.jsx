import { useState } from "react";
import { Feedback } from "./components/Feedback";
import { OrderForm } from "./components/OrderForm";
import { ProductForm } from "./components/ProductForm";
import { ProductList } from "./components/ProductList";
import { InventoryProvider } from "./context/InventoryContext";
import { useInventory } from "./hooks/useInventory";

function InventoryDashboard() {
  const {
    products,
    totalProducts,
    page,
    pages,
    isLoading,
    isSubmitting,
    error,
    successMessage,
    loadProducts,
    createProduct,
    updateProduct,
    createOrder,
    clearMessages,
  } = useInventory();
  const [selectedProduct, setSelectedProduct] = useState(null);

  async function handleProductSubmit(payload) {
    if (selectedProduct) {
      await updateProduct(selectedProduct.external_id, payload);
      setSelectedProduct(null);
      return;
    }

    await createProduct(payload);
  }

  return (
    <main className="app-shell">
      <header className="topbar">
        <div>
          <span className="eyebrow">Inventory API</span>
          <h1>Order Stock Manager</h1>
        </div>
        <button className="secondary-button" type="button" onClick={() => loadProducts(page)}>
          Recarregar
        </button>
      </header>

      <Feedback error={error} successMessage={successMessage} onClose={clearMessages} />

      <div className="layout">
        <div className="main-column">
          <ProductList
            products={products}
            isLoading={isLoading}
            page={page}
            pages={pages}
            totalProducts={totalProducts}
            onEdit={setSelectedProduct}
            onPageChange={loadProducts}
          />
        </div>

        <aside className="side-column">
          <ProductForm
            selectedProduct={selectedProduct}
            isSubmitting={isSubmitting}
            onSubmit={handleProductSubmit}
            onCancelEdit={() => setSelectedProduct(null)}
          />
          <OrderForm
            products={products}
            isSubmitting={isSubmitting}
            onSubmit={(items) => createOrder({ items })}
          />
        </aside>
      </div>
    </main>
  );
}

export default function App() {
  return (
    <InventoryProvider>
      <InventoryDashboard />
    </InventoryProvider>
  );
}
