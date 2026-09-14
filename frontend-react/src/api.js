// set VITE_API_URL when deploying, otherwise talk to the local flask server
const API = import.meta.env.VITE_API_URL || "http://localhost:5000/api";

// one helper that every request goes through
async function request(path, options) {
  const response = await fetch(`${API}${path}`, options);

  // fetch does not throw on 400 or 404, so check it ourselves
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.error || "request failed");
  }

  // 204 means there is no body to read
  if (response.status === 204) return null;
  return response.json();
}

// shared settings for requests that send json
const jsonHeaders = { "Content-Type": "application/json" };

export function getApplications() {
  return request("/applications");
}

export function createApplication(data) {
  return request("/applications", {
    method: "POST",
    headers: jsonHeaders,
    body: JSON.stringify(data),
  });
}

export function updateApplication(id, data) {
  return request(`/applications/${id}`, {
    method: "PATCH",
    headers: jsonHeaders,
    body: JSON.stringify(data),
  });
}

export function deleteApplication(id) {
  return request(`/applications/${id}`, { method: "DELETE" });
}
