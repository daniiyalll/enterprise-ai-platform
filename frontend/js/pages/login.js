const LoginPage = (() => {

  function render(mode = "login") {
    document.getElementById("app").innerHTML = `
      <div class="auth-screen">
        <div class="auth-tape"></div>
        <div class="auth-box">
          <div class="auth-brand">
            <div class="brand-mark">
              <img src="assets/logo.svg" alt="CortexFlow" class="brand-logo" />
            </div>
            <div>
              <div class="brand-name">CortexFlow</div>
              <div class="brand-sub">Workflow Intelligence</div>
            </div>
          </div>
          ${mode === "login" ? loginForm() : signupForm()}
        </div>
      </div>
    `;
    if (mode === "login") bindLogin(); else bindSignup();
  }

  function loginForm() {
    return `
      <div class="auth-title">Sign in</div>
      <div class="auth-sub">Enter your credentials to access the platform.</div>
      <div id="authError"></div>
      <form id="loginForm">
        <div class="field">
          <label>Username</label>
          <input type="text" name="username" autocomplete="username" required />
        </div>
        <div class="field">
          <label>Password</label>
          <input type="password" name="password" autocomplete="current-password" required />
        </div>
        <button class="btn btn-primary btn-block" type="submit" id="loginSubmit">Sign in</button>
      </form>
      <div class="auth-switch">No account? <button id="toSignup">Request access</button></div>
      <div class="auth-switch" style="margin-top:4px;">
        <button id="editApiBase" style="color:var(--muted);">API: ${UI.escapeHtml(window.API_BASE)}</button>
      </div>
    `;
  }

  function signupForm() {
    return `
      <div class="auth-title">Request access</div>
      <div class="auth-sub">Sign-up requires an invite secret key from your admin.</div>
      <div id="authError"></div>
      <form id="signupForm">
        <div class="field-row">
          <div class="field">
            <label>Username</label>
            <input type="text" name="username" required />
          </div>
          <div class="field">
            <label>Role</label>
            <select name="role" required>
              <option value="employee">Employee</option>
              <option value="manager">Manager</option>
              <option value="admin">Admin</option>
            </select>
          </div>
        </div>
        <div class="field">
          <label>Email</label>
          <input type="email" name="email" required />
        </div>
        <div class="field">
          <label>Password</label>
          <input type="password" name="password" autocomplete="new-password" required />
        </div>
        <div class="field">
          <label>Signup secret key</label>
          <input type="password" name="secret_key" required />
        </div>
        <button class="btn btn-primary btn-block" type="submit" id="signupSubmit">Create account</button>
      </form>
      <div class="auth-switch">Already have an account? <button id="toLogin">Sign in</button></div>
    `;
  }

  function showError(msg) {
    document.getElementById("authError").innerHTML = `<div class="error-box">${UI.escapeHtml(msg)}</div>`;
  }

  function bindLogin() {
    document.getElementById("toSignup").addEventListener("click", () => render("signup"));
    document.getElementById("editApiBase").addEventListener("click", (e) => {
      e.preventDefault();
      const val = prompt("Backend API base URL", window.API_BASE);
      if (val) {
        window.localStorage.setItem("api_base", val);
        window.API_BASE = val;
        UI.toast("API base updated");
      }
    });
    document.getElementById("loginForm").addEventListener("submit", async (e) => {
      e.preventDefault();
      const btn = document.getElementById("loginSubmit");
      const data = Object.fromEntries(new FormData(e.target));
      btn.disabled = true; btn.textContent = "Signing in…";
      try {
        const res = await Api.form("/auth/login", data, { auth: false });
        const claims = decodeJwt(res.access_token);
        Session.set({ username: claims.sub, role: claims.role }, res.access_token);
        UI.toast(`Welcome back, ${claims.sub}`, "success");
        window.location.hash = "#/dashboard";
        Router.go();
      } catch (err) {
        showError(err.message);
      } finally {
        btn.disabled = false; btn.textContent = "Sign in";
      }
    });
  }

  function bindSignup() {
    document.getElementById("toLogin").addEventListener("click", () => render("login"));
    document.getElementById("signupForm").addEventListener("submit", async (e) => {
      e.preventDefault();
      const btn = document.getElementById("signupSubmit");
      const data = Object.fromEntries(new FormData(e.target));
      btn.disabled = true; btn.textContent = "Creating…";
      try {
        await Api.post("/auth/signup", data, { auth: false });
        UI.toast("Account created — sign in now", "success");
        render("login");
      } catch (err) {
        showError(err.message);
      } finally {
        btn.disabled = false; btn.textContent = "Create account";
      }
    });
  }

  return { render };
})();
