import { useContext } from "react";
import { InventoryContext } from "../context/InventoryContext";

export function useInventory() {
  const context = useContext(InventoryContext);

  if (!context) {
    throw new Error("useInventory deve ser usado dentro de InventoryProvider.");
  }

  return context;
}
