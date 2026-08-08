const Router = (() => {

  const routes = {
    "#/dashboard": { page: DashboardPage, roles: ["admin", "manager"] },
    "#/workflows": { page: WorkflowsPage, roles: ["admin", "manager", "employee"] },
    "#/decisions": { page: DecisionsPage, roles: ["admin", "manager"] },
    "#/mining": { page: MiningPage, roles: ["admin", "manager"] },
    "#/agents": { page: AgentsPage, roles: ["admin", "manager", "employee"] },
    "#/predict": { page: PredictPage, roles: ["admin", "manager", "employee"] },
    "#/copilot": { page: CopilotPage, roles: ["admin", "manager", "employee"] },
    "#/users": { page: UsersPage, roles: ["admin"] },
  };

  function defaultRouteFor(role) {
    if (role === "admin" || role === "manager") return "#/dashboard";
    return "#/workflows";
  }

  function go() {
    let hash = window.location.hash || "";

    if (!Session.isLoggedIn()) {
      if (hash === "#/signup") { LoginPage.render("signup"); return; }
      LoginPage.render("login");
      return;
    }

    if (!hash || hash === "#/login" || hash === "#/signup" || hash === "#/") {
      hash = defaultRouteFor(Session.role());
      window.location.hash = hash;
      return;
    }

    const route = routes[hash];
    if (!route) {
      window.location.hash = defaultRouteFor(Session.role());
      return;
    }

    if (!route.roles.includes(Session.role())) {
      UI.toast("You don't have access to that section", "error");
      window.location.hash = defaultRouteFor(Session.role());
      return;
    }

    route.page.render();
  }

  window.addEventListener("hashchange", go);

  return { go };
})();
