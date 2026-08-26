const UI = (() => {

  function toast(message, type = "default") {
    const host = document.getElementById("toast");
    const item = document.createElement("div");
    item.className = `toast-item ${type}`;
    item.textContent = message;
    host.appendChild(item);
    setTimeout(() => item.remove(), 3600);
  }

  function escapeHtml(str) {
    if (str === null || str === undefined) return "";
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function fmtDate(iso) {
    if (!iso) return "—";
    const d = new Date(iso);
    if (isNaN(d.getTime())) return iso;
    return d.toLocaleString(undefined, {
      month: "short", day: "numeric", hour: "2-digit", minute: "2-digit"
    });
  }

  function fmtTime() {
    return new Date().toLocaleTimeString(undefined, { hour: "2-digit", minute: "2-digit" });
  }

  function initials(name) {
    if (!name) return "?";
    return name.slice(0, 2).toUpperCase();
  }

  function decisionPill(decision) {
    const d = (decision || "").toLowerCase();
    if (["approved", "passed"].includes(d)) return `<span class="pill pill-success">${escapeHtml(decision)}</span>`;
    if (["rejected", "failed"].includes(d)) return `<span class="pill pill-danger">${escapeHtml(decision)}</span>`;
    if (d === "review_required") return `<span class="pill pill-warn">review required</span>`;
    return `<span class="pill pill-muted">${escapeHtml(decision || "unknown")}</span>`;
  }

  function statusPill(status, isActive) {
    if (isActive === false) return `<span class="pill pill-muted">inactive</span>`;
    const s = (status || "").toLowerCase();
    if (s === "active" || s === "approved") return `<span class="pill pill-success">${escapeHtml(status)}</span>`;
    if (s === "pending") return `<span class="pill pill-warn">${escapeHtml(status)}</span>`;
    if (s === "rejected" || s === "cancelled") return `<span class="pill pill-danger">${escapeHtml(status)}</span>`;
    return `<span class="pill pill-info">${escapeHtml(status || "unknown")}</span>`;
  }

  const NAV = [
    { group: "Overview", items: [
      { path: "#/dashboard", label: "Dashboard", icon: "◈", roles: ["admin", "manager"] },
    ]},
    { group: "Operations", items: [
      { path: "#/workflows", label: "Workflows", icon: "▤", roles: ["admin", "manager", "employee"] },
      { path: "#/decisions", label: "Decisions", icon: "⚖", roles: ["admin", "manager"] },
      { path: "#/mining", label: "Process Mining", icon: "◫", roles: ["admin", "manager"] },
    ]},
    { group: "Intelligence", items: [
      { path: "#/agents", label: "AI Agents", icon: "◆", roles: ["admin", "manager", "employee"] },
      { path: "#/predict", label: "Risk Prediction", icon: "▲", roles: ["admin", "manager", "employee"] },
      { path: "#/copilot", label: "Copilot", icon: "✦", roles: ["admin", "manager", "employee"] },
    ]},
    { group: "Admin", items: [
      { path: "#/users", label: "Users", icon: "☰", roles: ["admin"] },
    ]},
  ];

  function shell(activePath, title, sub, innerHtml) {
    const user = Session.get() || {};
    const role = user.role || "employee";

    const navHtml = NAV.map(group => {
      const items = group.items.filter(i => i.roles.includes(role));
      if (!items.length) return "";
      return `
        <div class="nav-group">
          <div class="nav-label">${group.group}</div>
          ${items.map(i => `
            <div class="nav-item ${i.path === activePath ? "active" : ""}" data-nav="${i.path}">
              <span class="tick"></span>
              <span class="nav-icon">${i.icon}</span>
              <span>${i.label}</span>
            </div>
          `).join("")}
        </div>`;
    }).join("");

    document.getElementById("app").innerHTML = `
      <div class="shell">
        <aside class="sidebar">
          <div class="brand">
            <div class="brand-mark">
              <img src="assets/logo.svg" alt="CortexFlow" class="brand-logo" />
            </div>
            <div>
              <div class="brand-name">CortexFlow</div>
              <div class="brand-sub">Workflow Intelligence</div>
            </div>
          </div>
          ${navHtml}
          <div class="sidebar-foot">
            <div class="user-chip">
              <div class="user-avatar">${initials(user.username)}</div>
              <div>
                <div class="user-name">${escapeHtml(user.username || "—")}</div>
                <div class="user-role">${escapeHtml(role)}</div>
              </div>
            </div>
            <button class="logout-btn" id="logoutBtn">Sign out</button>
          </div>
        </aside>
        <div class="main">
          <div class="topbar">
            <div>
              <div class="topbar-title">${title}</div>
              <div class="topbar-sub">${sub || ""}</div>
            </div>
            <div class="topbar-time mono" id="clock">${fmtTime()}</div>
          </div>
          <div class="content" id="pageContent">${innerHtml}</div>
        </div>
      </div>
    `;

    document.querySelectorAll("[data-nav]").forEach(el => {
      el.addEventListener("click", () => { window.location.hash = el.dataset.nav; });
    });
    document.getElementById("logoutBtn").addEventListener("click", () => {
      Session.clear();
      window.location.hash = "#/login";
    });

    if (window.__clockInterval) clearInterval(window.__clockInterval);
    window.__clockInterval = setInterval(() => {
      const c = document.getElementById("clock");
      if (c) c.textContent = fmtTime();
    }, 30000);
  }

  function setContent(html) {
    const el = document.getElementById("pageContent");
    if (el) el.innerHTML = html;
  }

  return { toast, escapeHtml, fmtDate, initials, decisionPill, statusPill, shell, setContent, NAV };
})();
