const AgentsPage = (() => {

  function render() {
    UI.shell("#/agents", "AI Agents", "Run individual agent checks in isolation", `
      <div class="grid grid-3">
        ${card("compliance", "Compliance Agent", "Checks spend against department policy", `
          <div class="field"><label>Department</label><input name="department" required placeholder="finance" /></div>
          <div class="field"><label>Amount</label><input type="number" step="0.01" name="amount" required /></div>
        `)}
        ${card("approval", "Approval Agent", "Checks amount against approver's authority level", `
          <div class="field"><label>Amount</label><input type="number" step="0.01" name="amount" required /></div>
          <div class="field"><label>Employee level</label>
            <select name="employee_level"><option>junior</option><option>mid</option><option>senior</option><option>executive</option></select>
          </div>
        `)}
        ${card("document", "Document Agent", "Validates document completeness", `
          <div class="field"><label>Document type</label><input name="document_type" required placeholder="invoice" /></div>
          <div class="checkbox-row" style="margin-bottom:10px;"><input type="checkbox" name="has_signature" id="dhs" checked /><label for="dhs">Has signature</label></div>
          <div class="checkbox-row"><input type="checkbox" name="has_required_fields" id="dhrf" checked /><label for="dhrf">Required fields complete</label></div>
        `)}
      </div>
    `);

    bind("compliance", "/agents/compliance", fd => ({ department: fd.get("department"), amount: parseFloat(fd.get("amount")) }));
    bind("approval", "/agents/approval", fd => ({ amount: parseFloat(fd.get("amount")), employee_level: fd.get("employee_level") }));
    bind("document", "/agents/document", fd => ({
      document_type: fd.get("document_type"),
      has_signature: fd.get("has_signature") === "on",
      has_required_fields: fd.get("has_required_fields") === "on",
    }));
  }

  function card(id, title, sub, fields) {
    return `
      <div class="card">
        <div class="card-head"><div><div class="card-title">${title}</div><div class="card-hint">${sub}</div></div></div>
        <form id="${id}Form">
          ${fields}
          <button class="btn btn-primary btn-block" type="submit" style="margin-top:4px;">Run check</button>
        </form>
        <div id="${id}Result"></div>
      </div>
    `;
  }

  function bind(id, path, toBody) {
    document.getElementById(`${id}Form`).addEventListener("submit", async (e) => {
      e.preventDefault();
      const fd = new FormData(e.target);
      const resultEl = document.getElementById(`${id}Result`);
      resultEl.innerHTML = `<div class="loading">Running</div>`;
      try {
        const res = await Api.post(path, toBody(fd));
        resultEl.innerHTML = `
          <div class="result-block">
            <div class="kv"><span class="k">Decision</span><span class="v">${UI.decisionPill(res.decision || res.status)}</span></div>
            ${res.reason ? `<div class="kv"><span class="k">Reason</span><span class="v" style="font-family:var(--body); font-weight:400; text-align:right; max-width:200px;">${UI.escapeHtml(res.reason)}</span></div>` : ""}
          </div>`;
      } catch (err) {
        resultEl.innerHTML = `<div class="error-box">${UI.escapeHtml(err.message)}</div>`;
      }
    });
  }

  return { render };
})();
