import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { apiFetch } from "@/api/client";

export function useMenus() {
  return useQuery({
    queryKey: ["menus"],
    queryFn: () => apiFetch("/menus"),
  });
}

export function useMenu(id) {
  return useQuery({
    queryKey: ["menus", id],
    queryFn: () => apiFetch(`/menus/${id}`),
    enabled: !!id,
  });
}

export function useCreateMenu() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data) =>
      apiFetch("/menus", {
        method: "POST",
        body: JSON.stringify(data),
      }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["menus"] }),
  });
}

export function useUpdateMenu() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, ...data }) =>
      apiFetch(`/menus/${id}`, {
        method: "PUT",
        body: JSON.stringify(data),
      }),
    onSuccess: (_, { id }) => {
      qc.invalidateQueries({ queryKey: ["menus"] });
      qc.invalidateQueries({ queryKey: ["menus", id] });
    },
  });
}

export function useDeleteMenu() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id) =>
      apiFetch(`/menus/${id}`, { method: "DELETE" }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["menus"] }),
  });
}

export function useMenuNutrition(id) {
  return useQuery({
    queryKey: ["menus", id, "nutrition"],
    queryFn: () => apiFetch(`/menus/${id}/nutrition`),
    enabled: !!id,
  });
}

export function useGroceryList(id) {
  return useQuery({
    queryKey: ["menus", id, "grocery-list"],
    queryFn: () => apiFetch(`/menus/${id}/grocery-list`),
    enabled: !!id,
  });
}
