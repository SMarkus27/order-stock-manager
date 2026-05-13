import { apiRequest } from "./http";

export function getProducts(page = 1, perPage = 10) {
  return apiRequest(`/products/?page=${page}&per_page=${perPage}`);
}

export function createProduct(payload) {
  return apiRequest("/products/", {
    method: "POST",
    body: payload,
  });
}

export function updateProduct(productId, payload) {
  return apiRequest(`/products/${productId}`, {
    method: "PATCH",
    body: payload,
  });
}

export function createOrder(payload) {
  return apiRequest("/orders/orders", {
    method: "POST",
    body: payload,
  });
}
