import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { apiFetch } from "@/api/client";

export function useSettings() {
  return useQuery({
    queryKey: ["settings"],
    queryFn: () => apiFetch("/settings"),
  });
}

export function useUpdateSettings() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data) =>
      apiFetch("/settings", {
        method: "PUT",
        body: JSON.stringify(data),
      }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["settings"] }),
  });
}
