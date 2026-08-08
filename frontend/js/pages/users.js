const UsersPage = (() => {
  let cache = [];

  async function render() {
    UI.shell("#/users", "Users", "Manage roles across the platform (admin only)", `<div class="loading">Loading users</div>`);
    await load();
  }

  async function load() {
    try {
      cache = await Api.get("/users/");
      draw();
    } catch (err) {
      UI.setContent(`<div class="error-box">${UI.escapeHtml(err.message)}</div>`);
    }
  }

  function draw() {
    UI.setContent(`
      <div class="card">
        <div class="card-head"><div><div class="card-title">All users</div><div class="card-hint">${cache.length} accounts</div></div></div>
        <div class="table-wrap">
          <table>
            <thead><tr><th>ID</th><th>Username</th><th>Email</th><th>Role</th><th></th></tr></thead>
            <tbody>
              ${cache.map(u => `
                <tr>
                  <td class="mono">#${u.id}</td>
                  <td><strong>${UI.escapeHtml(u.username)}</strong></td>
                  <td class="muted">${UI.escapeHtml(u.email)}</td>
                  <td>${roleSelect(u)}</td>
                  <td><button class="btn btn-ghost btn-sm" data-save="${u.id}">Save</button></td>
                </tr>
              `).join("")}
            </tbody>
          </table>
        </div>
      </div>
    `);

    document.querySelectorAll("[data-save]").forEach(btn => {
      btn.addEventListener("click", async () => {
        const id = btn.dataset.save;
        const role = document.getElementById(`role_${id}`).value;
        btn.disabled = true; btn.textContent = "Saving…";
        try {
          await Api.put(`/users/${id}/role?role=${encodeURIComponent(role)}`);
          UI.toast("Role updated", "success");
        } catch (err) {
          UI.toast(err.message, "error");
        } finally {
          btn.disabled = false; btn.textContent = "Save";
        }
      });
    });
  }

  function roleSelect(u) {
    const roles = ["admin", "manager", "employee"];
    return `
      <select id="role_${u.id}">
        ${roles.map(r => `<option value="${r}" ${u.role === r ? "selected" : ""}>${r}</option>`).join("")}
      </select>
    `;
  }

  return { render };
})();
