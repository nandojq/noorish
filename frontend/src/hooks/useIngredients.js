import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { apiFetch } from "@/api/client";

export function useIngredients(params = {}) {
  const query = new URLSearchParams();
  if (params.search) query.set("search", params.search);
  if (params.category) query.set("category", params.category);
  if (params.dataQuality) query.set("dataQuality", params.dataQuality);
  const qs = query.toString();

  return useQuery({
    queryKey: ["ingredients", params],
    queryFn: () => apiFetch(`/ingredients${qs ? `?${qs}` : ""}`),
  });
}

export function useIngredient(id) {
  return useQuery({
    queryKey: ["ingredients", id],
    queryFn: () => apiFetch(`/ingredients/${id}`),
    enabled: !!id,
  });
}

export function useCreateIngredient() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data) =>
      apiFetch("/ingredients", {
        method: "POST",
        body: JSON.stringify(data),
      }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["ingredients"] }),
  });
}

export function useUpdateIngredient() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, ...data }) =>
      apiFetch(`/ingredients/${id}`, {
        method: "PUT",
        body: JSON.stringify(data),
      }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["ingredients"] }),
  });
}

export function useDeleteIngredient() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id) =>
      apiFetch(`/ingredients/${id}`, { method: "DELETE" }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["ingredients"] }),
  });
}

export function useSearchUSDA(q) {
  return useQuery({
    queryKey: ["usda-search", q],
    queryFn: () => apiFetch(`/ingest/usda/search?q=${encodeURIComponent(q)}`),
    enabled: !!q && q.length >= 2,
  });
}

export function useImportUSDA() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data) =>
      apiFetch("/ingest/usda/import", {
        method: "POST",
        body: JSON.stringify(data),
      }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["ingredients"] }),
  });
}

export function useSearchOFF(params = {}) {
  const query = new URLSearchParams();
  if (params.q) query.set("q", params.q);
  if (params.barcode) query.set("barcode", params.barcode);
  const qs = query.toString();

  return useQuery({
    queryKey: ["off-search", params],
    queryFn: () => apiFetch(`/ingest/off/search?${qs}`),
    enabled: !!(params.q || params.barcode),
  });
}

export function useImportOFF() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data) =>
      apiFetch("/ingest/off/import", {
        method: "POST",
        body: JSON.stringify(data),
      }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["ingredients"] }),
  });
}
