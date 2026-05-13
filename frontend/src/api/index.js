const BASE = "/api";

async function request(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

export const api = {
  getUniversities: (params = {}) => {
    const qs = new URLSearchParams(
      Object.fromEntries(Object.entries(params).filter(([, v]) => v != null && v !== ""))
    ).toString();
    return request(`/universities${qs ? `?${qs}` : ""}`);
  },

  getUniversity: (id) => request(`/universities/${id}`),

  getCountries: () => request("/universities/countries"),

  getSpecialties: () => request("/universities/specialties"),

  chat: (messages) =>
    request("/chat", {
      method: "POST",
      body: JSON.stringify({ messages }),
    }),
};
