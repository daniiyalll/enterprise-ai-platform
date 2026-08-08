const DashboardPage = (() => {

  async function render() {
    UI.shell("#/dashboard", "Dashboard", "Live snapshot of workflows and decisions", `<div class="loading">Loading stats</div>`);
    try {
      const s = await Api.get("/dashboard/stats");
      UI.setContent(`
        <div class="grid grid-4">
          ${stat("Total Workflows", s.total_workflows, "accent", `${s.active_workflows} active`)}
          ${stat("Pending Workflows", s.pending_workflows, "info", "awaiting action")}
          ${stat("Total Decisions", s.total_decisions, "accent", `avg confidence ${(s.average_confidence * 100).toFixed(0)}%`)}
          ${stat("Approvals", s.total_approvals, "success", "approved / passed")}
          ${stat("Rejections", s.total_rejections, "danger", "rejected outright")}
          ${stat("Review Required", s.pending_requests, "info", "needs manual review")}
          ${stat("Compliance Failures", s.compliance_failures, "danger", "Compliance Agent")}
          ${stat("Document Rejections", s.document_rejections, "danger", "Document Agent")}
        </div>

        <div class="grid grid-2" style="margin-top:16px;">
          <div class="card">
            <div class="card-head">
              <div>
                <div class="card-title">Decision outcomes</div>
                <div class="card-hint">Share of all recorded decisions</div>
              </div>
            </div>
            ${outcomeBars(s)}
          </div>
          <div class="card">
            <div class="card-head">
              <div>
                <div class="card-title">Quick actions</div>
                <div class="card-hint">Jump straight into the workflow</div>
              </div>
            </div>
            <div style="display:flex; flex-direction:column; gap:10px;">
              <button class="btn btn-block" data-nav="#/decisions">Evaluate a decision →</button>
              <button class="btn btn-block" data-nav="#/workflows">Create a workflow →</button>
              <button class="btn btn-block" data-nav="#/mining">Open process mining →</button>
            </div>
          </div>
        </div>
      `);
      document.querySelectorAll("[data-nav]").forEach(el => {
        el.addEventListener("click", () => { window.location.hash = el.dataset.nav; });
      });
    } catch (err) {
      UI.setContent(`<div class="error-box">${UI.escapeHtml(err.message)}</div>`);
    }
  }

  function stat(label, value, tone, foot) {
    return `
      <div class="stat ${tone}">
        <div class="stat-label">${label}</div>
        <div class="stat-value">${value ?? 0}</div>
        <div class="stat-foot">${foot}</div>
      </div>`;
  }

  function outcomeBars(s) {
    const total = Math.max(s.total_decisions, 1);
    const rows = [
      ["Approved", s.total_approvals],
      ["Rejected", s.total_rejections],
      ["Review required", s.pending_requests],
    ];
    return rows.map(([label, val]) => {
      const pct = Math.round((val / total) * 100);
      return `
        <div class="bar-row">
          <div class="bar-label">${label}</div>
          <div class="bar-track"><div class="bar-fill" style="width:${pct}%"></div></div>
          <div class="bar-val">${pct}%</div>
        </div>`;
    }).join("");
  }

  return { render };
})();
