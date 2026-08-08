const DecisionsPage = (() => {
  let tab = "evaluate";
  let page = 1;
  const pageSize = 15;

  function render() {
    UI.shell("#/decisions", "Decision Engine", "Run multi-agent decisions and review history", "");
    draw();
  }

  function draw() {
    UI.setContent(`
      <div class="tabs">
        <div class="tab ${tab === "evaluate" ? "active" : ""}" data-tab="evaluate">Evaluate</div>
        <div class="tab ${tab === "history" ? "active" : ""}" data-tab="history">History</div>
      </div>
      <div id="tabBody"></div>
    `);
    document.querySelectorAll("[data-tab]").forEach(t =>
      t.addEventListener("click", () => { tab = t.dataset.tab; draw(); }));

    if (tab === "evaluate") drawEvaluate(); else drawHistory();
  }

  function drawEvaluate() {
    document.getElementById("tabBody").innerHTML = `
      <div class="grid grid-2">
        <div class="card">
          <div class="card-head"><div class="card-title">Run a decision</div></div>
          <form id="evalForm">
            <div class="field-row">
              <div class="field">
                <label>Amount</label>
                <input type="number" step="0.01" name="amount" required />
              </div>
              <div class="field">
                <label>Employee level</label>
                <select name="employee_level">
                  <option>junior</option><option>mid</option><option>senior</option><option>executive</option>
                </select>
              </div>
            </div>
            <div class="field-row">
              <div class="field">
                <label>Department</label>
                <input type="text" name="department" placeholder="finance, hr, engineering…" required />
              </div>
              <div class="field">
                <label>Document type</label>
                <input type="text" name="document_type" placeholder="invoice, contract…" required />
              </div>
            </div>
            <div class="field-row">
              <div class="checkbox-row"><input type="checkbox" name="has_signature" id="hs" checked /><label for="hs">Has signature</label></div>
              <div class="checkbox-row"><input type="checkbox" name="has_required_fields" id="hrf" checked /><label for="hrf">Required fields complete</label></div>
            </div>
            <button class="btn btn-primary btn-block" type="submit">Evaluate</button>
          </form>
        </div>
        <div class="card">
          <div class="card-head"><div class="card-title">Result</div></div>
          <div id="evalResult" class="muted">Submit the form to see the agents' verdict.</div>
        </div>
      </div>
    `;

    document.getElementById("evalForm").addEventListener("submit", async (e) => {
      e.preventDefault();
      const fd = new FormData(e.target);
      const body = {
        amount: parseFloat(fd.get("amount")),
        employee_level: fd.get("employee_level"),
        department: fd.get("department"),
        document_type: fd.get("document_type"),
        has_signature: fd.get("has_signature") === "on",
        has_required_fields: fd.get("has_required_fields") === "on",
      };
      const resultEl = document.getElementById("evalResult");
      resultEl.innerHTML = `<div class="loading">Consulting agents</div>`;
      try {
        const res = await Api.post("/decisions/evaluate", body);
        resultEl.innerHTML = renderResult(res);
      } catch (err) {
        resultEl.innerHTML = `<div class="error-box">${UI.escapeHtml(err.message)}</div>`;
      }
    });
  }

  function renderResult(res) {
    const agents = (res.results || []).map(r => `
      <div class="result-block" style="margin-top:10px;">
        <div class="kv"><span class="k">Agent</span><span class="v">${UI.escapeHtml(r.agent_name || r.agent || "—")}</span></div>
        <div class="kv"><span class="k">Outcome</span><span class="v">${UI.decisionPill(r.decision || r.status)}</span></div>
        ${r.reason ? `<div class="kv"><span class="k">Reason</span><span class="v" style="font-family:var(--body); font-weight:400; text-align:right; max-width:220px;">${UI.escapeHtml(r.reason)}</span></div>` : ""}
      </div>
    `).join("");

    return `
      <div class="result-block">
        <div class="kv"><span class="k">Final decision</span><span class="v">${UI.decisionPill(res.final_decision)}</span></div>
        <div class="kv"><span class="k">Confidence</span><span class="v">${Math.round((res.overall_confidence || 0) * 100)}% (${UI.escapeHtml(res.confidence_level || "")})</span></div>
        <div class="kv"><span class="k">Agents agreed</span><span class="v">${res.agents_agreed ? "yes" : "no"}</span></div>
      </div>
      ${res.decision_explanation ? `<div class="hint-box" style="margin-top:10px;">${UI.escapeHtml(res.decision_explanation)}</div>` : ""}
      <div class="section-sub" style="margin:14px 0 0;">Per-agent breakdown</div>
      ${agents}
    `;
  }

  async function drawHistory() {
    const body = document.getElementById("tabBody");
    body.innerHTML = `
      <div class="card">
        <div class="card-head"><div class="card-title">Filters</div></div>
        <form id="filterForm" class="grid grid-4" style="margin-bottom:6px;">
          <div class="field"><label>Agent</label><input name="agent_name" placeholder="e.g. Compliance Agent" /></div>
          <div class="field"><label>Outcome</label>
            <select name="decision">
              <option value="">Any</option>
              <option value="approved">approved</option>
              <option value="rejected">rejected</option>
              <option value="review_required">review_required</option>
              <option value="failed">failed</option>
              <option value="passed">passed</option>
            </select>
          </div>
          <div class="field"><label>Username</label><input name="username" placeholder="triggered by…" /></div>
          <div class="field" style="display:flex; align-items:flex-end;"><button class="btn btn-primary btn-block" type="submit">Apply filters</button></div>
        </form>
      </div>
      <div class="card" style="margin-top:14px;">
        <div class="table-wrap" id="historyTable"><div class="loading">Loading history</div></div>
        <div class="pager" id="pager"></div>
      </div>
    `;
    document.getElementById("filterForm").addEventListener("submit", (e) => {
      e.preventDefault();
      page = 1;
      loadHistory(Object.fromEntries(new FormData(e.target)));
    });
    loadHistory({});
  }

  async function loadHistory(filters) {
    const table = document.getElementById("historyTable");
    try {
      const res = await Api.get("/decisions/history", { query: { ...filters, page, page_size: pageSize } });
      if (!res.results.length) {
        table.innerHTML = `<div class="empty"><div class="glyph">⚖</div>No decisions match these filters.</div>`;
        document.getElementById("pager").innerHTML = "";
        return;
      }
      table.innerHTML = `
        <table>
          <thead><tr><th>ID</th><th>Agent</th><th>Outcome</th><th>Confidence</th><th>Triggered by</th><th>Reason</th><th>When</th></tr></thead>
          <tbody>
            ${res.results.map(d => `
              <tr>
                <td class="mono">#${d.id}</td>
                <td>${UI.escapeHtml(d.agent_name)}</td>
                <td>${UI.decisionPill(d.decision)}</td>
                <td class="mono">${Math.round((d.confidence || 0) * 100)}%</td>
                <td>${UI.escapeHtml(d.username || "—")}</td>
                <td class="muted">${UI.escapeHtml(d.reason || "—")}</td>
                <td class="mono muted">${UI.fmtDate(d.created_at)}</td>
              </tr>
            `).join("")}
          </tbody>
        </table>
      `;
      const pages = Math.max(1, Math.ceil(res.total / res.page_size));
      document.getElementById("pager").innerHTML = `
        <button class="btn btn-ghost btn-sm" id="prevPg" ${page <= 1 ? "disabled" : ""}>← Prev</button>
        <span>Page ${res.page} of ${pages} · ${res.total} total</span>
        <button class="btn btn-ghost btn-sm" id="nextPg" ${page >= pages ? "disabled" : ""}>Next →</button>
      `;
      const prev = document.getElementById("prevPg");
      const next = document.getElementById("nextPg");
      if (prev) prev.addEventListener("click", () => { page--; loadHistory(filters); });
      if (next) next.addEventListener("click", () => { page++; loadHistory(filters); });
    } catch (err) {
      table.innerHTML = `<div class="error-box">${UI.escapeHtml(err.message)}</div>`;
    }
  }

  return { render };
})();
