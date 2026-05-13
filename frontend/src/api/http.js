const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/v1";

export async function apiRequest(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
    body: options.body ? JSON.stringify(options.body) : undefined,
  });

  if (!response.ok) {
    const message = await readErrorMessage(response);
    throw new Error(message || "Nao foi possivel concluir a requisicao.");
  }

  if (response.status === 204) {
    return undefined;
  }

  return response.json();
}

async function readErrorMessage(response) {
  try {
    const data = await response.json();
    if (typeof data.detail === "string") {
      return data.detail;
    }
    return JSON.stringify(data.detail ?? data);
  } catch {
    return response.statusText;
  }
}
