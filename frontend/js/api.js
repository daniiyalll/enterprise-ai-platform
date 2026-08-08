/**
 * Thin fetch wrapper around the backend API.
 * Every call throws an Error with a human-readable .message on failure,
 * and automatically attaches the bearer token when one is stored.
 */
const Api = (() => {

  function token() {
    return window.localStorage.getItem("access_token");
  }

  async function request(path, { method = "GET", body, form, auth = true, query } = {}) {
    const headers = {};
    let payload = body;

    if (form) {
      payload = new URLSearchParams(form);
      headers["Content-Type"] = "application/x-www-form-urlencoded";
    } else if (body !== undefined) {
      headers["Content-Type"] = "application/json";
      payload = JSON.stringify(body);
    }

    if (auth && token()) {
      headers["Authorization"] = `Bearer ${token()}`;
    }

    let url = `${window.API_BASE}${path}`;
    if (query) {
      const qs = Object.entries(query)
        .filter(([, v]) => v !== undefined && v !== null && v !== "")
        .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`)
        .join("&");
      if (qs) url += `?${qs}`;
    }

    let res;
    try {
      res = await fetch(url, { method, headers, body: payload });
    } catch (e) {
      throw new Error(
        `Could not reach the API at ${window.API_BASE}. Is the backend running and is CORS enabled?`
      );
    }

    let data = null;
    const text = await res.text();
    if (text) {
      try { data = JSON.parse(text); } catch { data = text; }
    }

    if (!res.ok) {
      const detail = (data && (data.detail || data.message)) || res.statusText || "Request failed";
      const msg = typeof detail === "string" ? detail : JSON.stringify(detail);
      const err = new Error(msg);
      err.status = res.status;
      throw err;
    }

    return data;
  }

  return {
    get:    (path, opts) => request(path, { ...opts, method: "GET" }),
    post:   (path, body, opts) => request(path, { ...opts, method: "POST", body }),
    put:    (path, body, opts) => request(path, { ...opts, method: "PUT", body }),
    del:    (path, opts) => request(path, { ...opts, method: "DELETE" }),
    form:   (path, form, opts) => request(path, { ...opts, method: "POST", form }),
    hasToken: () => !!token(),
  };
})();
