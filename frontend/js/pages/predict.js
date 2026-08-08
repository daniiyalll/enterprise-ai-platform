const PredictPage = (() => {

  function render() {
    UI.shell("#/predict", "Risk Prediction", "RandomForest model trained on historical workflow risk", `
      <div class="grid grid-2">
        <div class="card">
          <div class="card-head">
            <div>
              <div class="card-title">Score a workflow</div>
              <div class="card-hint">Model input: process_duration_hours, num_approvals, priority_level</div>
            </div>
          </div>
          <form id="predictForm">
            <div class="field">
              <label>Process duration (hours)</label>
              <input type="number" step="0.1" name="duration" required placeholder="e.g. 24" />
            </div>
            <div class="field">
              <label>Number of approvals required</label>
              <input type="number" step="1" name="approvals" required placeholder="e.g. 2" />
            </div>
            <div class="field">
              <label>Priority level</label>
              <select name="priority">
                <option value="1">1 — Low</option>
                <option value="2">2 — Medium</option>
                <option value="3">3 — High</option>
              </select>
            </div>
            <button class="btn btn-primary btn-block" type="submit">Predict risk</button>
          </form>
        </div>
        <div class="card">
          <div class="card-head"><div class="card-title">Prediction</div></div>
          <div id="predictResult" class="muted">Submit values to see the model's risk classification.</div>
        </div>
      </div>
    `);

    document.getElementById("predictForm").addEventListener("submit", async (e) => {
      e.preventDefault();
      const fd = new FormData(e.target);
      const features = [parseFloat(fd.get("duration")), parseFloat(fd.get("approvals")), parseFloat(fd.get("priority"))];
      const resultEl = document.getElementById("predictResult");
      resultEl.innerHTML = `<div class="loading">Scoring</div>`;
      try {
        const res = await Api.post("/ai/predict", { features });
        resultEl.innerHTML = `
          <div class="result-block">
            ${Object.entries(res).map(([k, v]) => `
              <div class="kv"><span class="k">${UI.escapeHtml(k)}</span><span class="v">${UI.escapeHtml(typeof v === "object" ? JSON.stringify(v) : v)}</span></div>
            `).join("")}
          </div>
        `;
      } catch (err) {
        resultEl.innerHTML = `<div class="error-box">${UI.escapeHtml(err.message)}</div>`;
      }
    });
  }

  return { render };
})();
