const BASE_URL = "http://localhost:8000/api";

export async function apiFetch(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json", ...options.headers },
    ...options,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ message: res.statusText }));
    throw Object.assign(new Error(err.message), { status: res.status, data: err });
  }
  if (res.status === 204) return null;
  return res.json();
}
