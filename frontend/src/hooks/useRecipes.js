import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { apiFetch } from "@/api/client";

export function useRecipes(params = {}) {
  const query = new URLSearchParams();
  if (params.search) query.set("search", params.search);
  if (params.status) query.set("status", params.status);
  const qs = query.toString();

  return useQuery({
    queryKey: ["recipes", params],
    queryFn: () => apiFetch(`/recipes${qs ? `?${qs}` : ""}`),
  });
}

export function useRecipe(id) {
  return useQuery({
    queryKey: ["recipes", id],
    queryFn: () => apiFetch(`/recipes/${id}`),
    enabled: !!id,
  });
}

export function useCreateRecipe() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data) =>
      apiFetch("/recipes", {
        method: "POST",
        body: JSON.stringify(data),
      }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["recipes"] }),
  });
}

export function useUpdateRecipe() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, ...data }) =>
      apiFetch(`/recipes/${id}`, {
        method: "PUT",
        body: JSON.stringify(data),
      }),
    onSuccess: (_, { id }) => {
      qc.invalidateQueries({ queryKey: ["recipes"] });
      qc.invalidateQueries({ queryKey: ["recipes", id] });
    },
  });
}

export function useDeleteRecipe() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id) =>
      apiFetch(`/recipes/${id}`, { method: "DELETE" }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["recipes"] }),
  });
}

export function useUploadRecipeImage(id) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (file) => {
      const formData = new FormData();
      formData.append("file", file);
      return apiFetch(`/recipes/${id}/image`, {
        method: "POST",
        headers: {},
        body: formData,
      });
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["recipes", id] });
    },
  });
}
