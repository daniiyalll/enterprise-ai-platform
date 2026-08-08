function decodeJwt(token) {
  try {
    const payload = token.split(".")[1];
    const json = decodeURIComponent(
      atob(payload.replace(/-/g, "+").replace(/_/g, "/"))
        .split("")
        .map((c) => "%" + c.charCodeAt(0).toString(16).padStart(2, "0"))
        .join("")
    );
    return JSON.parse(json);
  } catch {
    return {};
  }
}

const Session = (() => {
  function get() {
    const raw = window.localStorage.getItem("session_user");
    return raw ? JSON.parse(raw) : null;
  }
  function set(user, token) {
    window.localStorage.setItem("session_user", JSON.stringify(user));
    window.localStorage.setItem("access_token", token);
  }
  function clear() {
    window.localStorage.removeItem("session_user");
    window.localStorage.removeItem("access_token");
  }
  function role() {
    const u = get();
    return u ? u.role : null;
  }
  function isLoggedIn() {
    return !!window.localStorage.getItem("access_token");
  }
  // role hierarchy mirrors the backend's require_role / require_manager / require_employee
  function hasAny(...roles) {
    return roles.includes(role());
  }
  return { get, set, clear, role, isLoggedIn, hasAny };
})();
