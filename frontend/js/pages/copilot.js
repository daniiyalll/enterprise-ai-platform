const CopilotPage = (() => {
  let history = [];

  function render() {
    history = [];
    UI.shell("#/copilot", "Copilot", "Ask questions about a case in plain language", `
      <div class="grid grid-2">
        <div class="card">
          <div class="card-head"><div class="card-title">Case context (optional)</div><div class="card-hint">Fill in what's known — Copilot uses it to reason</div></div>
          <div class="field-row">
            <div class="field"><label>Amount</label><input type="number" step="0.01" id="cx_amount" /></div>
            <div class="field"><label>Employee level</label>
              <select id="cx_level"><option value="">—</option><option>junior</option><option>mid</option><option>senior</option><option>executive</option></select>
            </div>
          </div>
          <div class="field-row">
            <div class="field"><label>Department</label><input id="cx_dept" /></div>
            <div class="field"><label>Document type</label><input id="cx_doc" /></div>
          </div>
          <div class="field-row">
            <div class="checkbox-row"><input type="checkbox" id="cx_sig" /><label for="cx_sig">Has signature</label></div>
            <div class="checkbox-row"><input type="checkbox" id="cx_fields" /><label for="cx_fields">Fields complete</label></div>
          </div>
        </div>
        <div class="card" style="display:flex; flex-direction:column;">
          <div class="card-head"><div class="card-title">Ask Copilot</div></div>
          <div id="chatLog" style="flex:1; min-height:220px; max-height:360px; overflow-y:auto; margin-bottom:12px;">
            <div class="muted" style="font-size:13px;">Try: "Should this be approved?" or "Why would this get rejected?"</div>
          </div>
          <form id="chatForm" style="display:flex; gap:8px;">
            <input id="chatInput" placeholder="Ask a question…" required style="flex:1;" />
            <button class="btn btn-primary" type="submit">Ask</button>
          </form>
        </div>
      </div>
    `);

    document.getElementById("chatForm").addEventListener("submit", async (e) => {
      e.preventDefault();
      const input = document.getElementById("chatInput");
      const question = input.value.trim();
      if (!question) return;
      input.value = "";
      appendMsg("you", question);
      const log = document.getElementById("chatLog");
      const loadingEl = document.createElement("div");
      loadingEl.className = "loading";
      loadingEl.textContent = "Thinking";
      log.appendChild(loadingEl);
      log.scrollTop = log.scrollHeight;

      const val = (id) => document.getElementById(id).value || undefined;
      const body = {
        question,
        amount: val("cx_amount") ? parseFloat(val("cx_amount")) : undefined,
        employee_level: val("cx_level"),
        department: val("cx_dept"),
        document_type: val("cx_doc"),
        has_signature: document.getElementById("cx_sig").checked,
        has_required_fields: document.getElementById("cx_fields").checked,
      };

      try {
        const res = await Api.post("/copilot/ask", body);
        loadingEl.remove();
        const parts = [];
        if (res.agent) parts.push(`[${res.agent}] ${res.status || ""}`);
        if (res.summary) parts.push(res.summary);
        if (res.recommended_action) parts.push(`→ ${res.recommended_action}`);
        if (res.confidence !== undefined) parts.push(`(confidence: ${Math.round(res.confidence * 100)}%, ${res.confidence_level || ""})`);
        const answer = parts.length ? parts.join("\n") : (res.answer || res.response || res.message || JSON.stringify(res));
        appendMsg("bot", answer);
      } catch (err) {
        loadingEl.remove();
        appendMsg("bot", `Error: ${err.message}`, true);
      }
    });
  }

  function appendMsg(who, text, isError) {
    const log = document.getElementById("chatLog");
    const el = document.createElement("div");
    el.style.marginBottom = "10px";
    el.innerHTML = `
      <div style="font-family:var(--mono); font-size:10px; text-transform:uppercase; letter-spacing:0.5px; color:${who === "you" ? "var(--accent)" : "var(--info)"}; margin-bottom:3px;">
        ${who === "you" ? "You" : "Copilot"}
      </div>
      <div style="font-size:13.5px; color:${isError ? "var(--danger)" : "var(--text)"}; line-height:1.5; white-space:pre-line;">${UI.escapeHtml(text)}</div>
    `;
    log.appendChild(el);
    log.scrollTop = log.scrollHeight;
  }

  return { render };
})();
