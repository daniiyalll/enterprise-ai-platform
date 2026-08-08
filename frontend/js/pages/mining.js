const MiningPage = (() => {

  async function render() {
    UI.shell("#/mining", "Process Mining", "Discovered from the workflow event log (PM4Py)", `<div class="loading">Mining event log</div>`);
    try {
      const summary = await Api.get("/process-mining/summary");
      draw(summary);
    } catch (err) {
      UI.setContent(`<div class="error-box">${UI.escapeHtml(err.message)}</div>`);
    }
  }

  function draw(s) {
    UI.setContent(`
      <div class="grid grid-4">
        <div class="stat accent"><div class="stat-label">Total Cases</div><div class="stat-value">${s.total_cases}</div></div>
        <div class="stat info"><div class="stat-label">Avg Duration</div><div class="stat-value">${s.performance.avg_case_duration_hours}h</div></div>
        <div class="stat"><div class="stat-label">Activities</div><div class="stat-value">${s.activities.length}</div></div>
        <div class="stat"><div class="stat-label">Avg Steps / Case</div><div class="stat-value">${s.performance.avg_activities_per_case}</div></div>
      </div>

      <div class="grid grid-2" style="margin-top:16px;">
        <div class="card">
          <div class="card-head"><div class="card-title">Case performance</div></div>
          <div class="result-block">
            <div class="kv"><span class="k">Min duration</span><span class="v">${s.performance.min_case_duration_hours}h</span></div>
            <div class="kv"><span class="k">Avg duration</span><span class="v">${s.performance.avg_case_duration_hours}h</span></div>
            <div class="kv"><span class="k">Max duration</span><span class="v">${s.performance.max_case_duration_hours}h</span></div>
            <div class="kv"><span class="k">Avg activities / case</span><span class="v">${s.performance.avg_activities_per_case}</span></div>
          </div>
        </div>
        <div class="card">
          <div class="card-head"><div class="card-title">Activities</div></div>
          <div style="display:flex; flex-wrap:wrap; gap:6px;">
            ${s.activities.map(a => `<span class="pill pill-info">${UI.escapeHtml(a)}</span>`).join("")}
          </div>
          <div class="card-hint" style="margin-top:14px;">Start activities</div>
          <div style="display:flex; flex-wrap:wrap; gap:6px; margin-top:6px;">
            ${Object.keys(s.start_activities).map(a => `<span class="pill pill-success">${UI.escapeHtml(a)}</span>`).join("")}
          </div>
          <div class="card-hint" style="margin-top:14px;">End activities</div>
          <div style="display:flex; flex-wrap:wrap; gap:6px; margin-top:6px;">
            ${Object.keys(s.end_activities).map(a => `<span class="pill pill-warn">${UI.escapeHtml(a)}</span>`).join("")}
          </div>
        </div>
      </div>

      <div class="grid grid-2" style="margin-top:16px;">
        <div class="card">
          <div class="card-head"><div><div class="card-title">Bottlenecks</div><div class="card-hint">Slowest average transitions</div></div></div>
          <table>
            <thead><tr><th>From</th><th>To</th><th>Avg hours</th></tr></thead>
            <tbody>
              ${s.top_bottlenecks.map(b => `
                <tr><td>${UI.escapeHtml(b.from)}</td><td>${UI.escapeHtml(b.to)}</td><td class="mono" style="color:var(--danger)">${b.avg_hours}h</td></tr>
              `).join("")}
            </tbody>
          </table>
        </div>
        <div class="card">
          <div class="card-head"><div><div class="card-title">Frequent paths</div><div class="card-hint">Most common end-to-end variants</div></div></div>
          ${s.frequent_paths.map(p => `
            <div class="result-block" style="margin-bottom:10px;">
              <div class="mono" style="font-size:12px; line-height:1.6; word-break:break-word;">${UI.escapeHtml(p.path)}</div>
              <div class="muted" style="font-size:11.5px; margin-top:6px;">${p.case_count} case${p.case_count === 1 ? "" : "s"}</div>
            </div>
          `).join("")}
        </div>
      </div>
    `);
  }

  return { render };
})();
