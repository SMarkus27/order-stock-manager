import { createContext, useCallback, useEffect, useMemo, useState } from "react";
import * as inventoryApi from "../api/inventory";

export const InventoryContext = createContext(null);

const PER_PAGE = 10;

export function InventoryProvider({ children }) {
  const [products, setProducts] = useState([]);
  const [totalProducts, setTotalProducts] = useState(0);
  const [page, setPage] = useState(1);
  const [pages, setPages] = useState(1);
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);

  const clearMessages = useCallback(() => {
    setError(null);
    setSuccessMessage(null);
  }, []);

  const loadProducts = useCallback(async (nextPage = page) => {
    setIsLoading(true);
    setError(null);

    try {
      const data = await inventoryApi.getProducts(nextPage, PER_PAGE);
      setProducts(data.items);
      setTotalProducts(data.total);
      setPage(data.page);
      setPages(data.pages);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro ao carregar produtos.");
    } finally {
      setIsLoading(false);
    }
  }, [page]);

  const createProduct = useCallback(async (payload) => {
    setIsSubmitting(true);
    clearMessages();

    try {
      await inventoryApi.createProduct(payload);
      setSuccessMessage("Produto cadastrado com sucesso.");
      await loadProducts(1);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro ao cadastrar produto.");
      throw err;
    } finally {
      setIsSubmitting(false);
    }
  }, [clearMessages, loadProducts]);

  const updateProduct = useCallback(async (productId, payload) => {
    setIsSubmitting(true);
    clearMessages();

    try {
      await inventoryApi.updateProduct(productId, payload);
      setSuccessMessage("Produto atualizado com sucesso.");
      await loadProducts(page);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro ao atualizar produto.");
      throw err;
    } finally {
      setIsSubmitting(false);
    }
  }, [clearMessages, loadProducts, page]);

  const createOrder = useCallback(async (payload) => {
    setIsSubmitting(true);
    clearMessages();

    try {
      await inventoryApi.createOrder(payload);
      setSuccessMessage("Pedido criado com sucesso.");
      await loadProducts(page);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro ao criar pedido.");
      throw err;
    } finally {
      setIsSubmitting(false);
    }
  }, [clearMessages, loadProducts, page]);

  useEffect(() => {
    void loadProducts(1);
  }, []);

  const value = useMemo(() => ({
    products,
    totalProducts,
    page,
    pages,
    perPage: PER_PAGE,
    isLoading,
    isSubmitting,
    error,
    successMessage,
    loadProducts,
    createProduct,
    updateProduct,
    createOrder,
    clearMessages,
  }), [
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
  ]);

  return (
    <InventoryContext.Provider value={value}>
      {children}
    </InventoryContext.Provider>
  );
}
