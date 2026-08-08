const WorkflowsPage = (() => {
  let cache = [];

  async function render() {
    UI.shell("#/workflows", "Workflows", "Create, track, and manage business workflows", `<div class="loading">Loading workflows</div>`);
    await load();
  }

  async function load() {
    try {
      cache = await Api.get("/workflows/");
      draw();
    } catch (err) {
      UI.setContent(`<div class="error-box">${UI.escapeHtml(err.message)}</div>`);
    }
  }

  function draw() {
    const canWrite = Session.hasAny("admin", "manager");
    const canDelete = Session.hasAny("admin");

    UI.setContent(`
      <div class="card">
        <div class="card-head">
          <div>
            <div class="card-title">All workflows</div>
            <div class="card-hint">${cache.length} total</div>
          </div>
          ${canWrite ? `<button class="btn btn-primary btn-sm" id="newWfBtn">+ New workflow</button>` : ""}
        </div>
        <div class="table-wrap">
          ${cache.length ? table(canWrite, canDelete) : empty()}
        </div>
      </div>
    `);

    if (canWrite) {
      document.getElementById("newWfBtn").addEventListener("click", () => openModal());
      document.querySelectorAll("[data-edit]").forEach(b =>
        b.addEventListener("click", () => openModal(cache.find(w => w.id == b.dataset.edit))));
    }
    if (canDelete) {
      document.querySelectorAll("[data-del]").forEach(b =>
        b.addEventListener("click", () => remove(b.dataset.del)));
    }
  }

  function table(canWrite, canDelete) {
    return `
      <table>
        <thead><tr>
          <th>ID</th><th>Name</th><th>Description</th><th>Status</th><th>Active</th><th></th>
        </tr></thead>
        <tbody>
          ${cache.map(w => `
            <tr>
              <td class="mono">#${w.id}</td>
              <td><strong>${UI.escapeHtml(w.name)}</strong></td>
              <td class="muted">${UI.escapeHtml(w.description)}</td>
              <td>${UI.statusPill(w.status)}</td>
              <td>${w.is_active ? '<span class="pill pill-success">yes</span>' : '<span class="pill pill-muted">no</span>'}</td>
              <td>
                ${canWrite ? `<button class="btn btn-ghost btn-sm" data-edit="${w.id}">Edit</button>` : ""}
                ${canDelete ? `<button class="btn btn-ghost btn-sm" data-del="${w.id}" style="color:var(--danger)">Delete</button>` : ""}
              </td>
            </tr>
          `).join("")}
        </tbody>
      </table>
    `;
  }

  function empty() {
    return `<div class="empty"><div class="glyph">▤</div>No workflows yet. Create one to get started.</div>`;
  }

  function openModal(existing) {
    const isEdit = !!existing;
    const wrap = document.createElement("div");
    wrap.className = "modal-bg";
    wrap.innerHTML = `
      <div class="modal">
        <div class="modal-head">
          <div class="card-title">${isEdit ? "Edit workflow" : "New workflow"}</div>
          <button class="modal-close" id="closeModal">✕</button>
        </div>
        <div id="modalError"></div>
        <form id="wfForm">
          <div class="field">
            <label>Name</label>
            <input name="name" required value="${isEdit ? UI.escapeHtml(existing.name) : ""}" />
          </div>
          <div class="field">
            <label>Description</label>
            <textarea name="description" rows="3" required>${isEdit ? UI.escapeHtml(existing.description) : ""}</textarea>
          </div>
          ${isEdit ? `
          <div class="field-row">
            <div class="field">
              <label>Status</label>
              <select name="status">
                ${["pending", "active", "approved", "rejected", "cancelled"].map(s =>
                  `<option value="${s}" ${existing.status === s ? "selected" : ""}>${s}</option>`).join("")}
              </select>
            </div>
            <div class="field">
              <label>Active</label>
              <select name="is_active">
                <option value="true" ${existing.is_active ? "selected" : ""}>Yes</option>
                <option value="false" ${!existing.is_active ? "selected" : ""}>No</option>
              </select>
            </div>
          </div>` : ""}
          <button class="btn btn-primary btn-block" type="submit">${isEdit ? "Save changes" : "Create workflow"}</button>
        </form>
      </div>
    `;
    document.body.appendChild(wrap);
    document.getElementById("closeModal").addEventListener("click", () => wrap.remove());
    wrap.addEventListener("click", (e) => { if (e.target === wrap) wrap.remove(); });

    document.getElementById("wfForm").addEventListener("submit", async (e) => {
      e.preventDefault();
      const fd = Object.fromEntries(new FormData(e.target));
      try {
        if (isEdit) {
          fd.is_active = fd.is_active === "true";
          await Api.put(`/workflows/${existing.id}`, fd);
          UI.toast("Workflow updated", "success");
        } else {
          await Api.post("/workflows/", fd);
          UI.toast("Workflow created", "success");
        }
        wrap.remove();
        load();
      } catch (err) {
        document.getElementById("modalError").innerHTML = `<div class="error-box">${UI.escapeHtml(err.message)}</div>`;
      }
    });
  }

  async function remove(id) {
    if (!confirm(`Delete workflow #${id}? This cannot be undone.`)) return;
    try {
      await Api.del(`/workflows/${id}`);
      UI.toast("Workflow deleted", "success");
      load();
    } catch (err) {
      UI.toast(err.message, "error");
    }
  }

  return { render };
})();
