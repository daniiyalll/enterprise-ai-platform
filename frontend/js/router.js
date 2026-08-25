const Router = (() => {

  const routes = {
    "#/dashboard": {
      page: DashboardPage,
      roles: ["admin", "manager"]
    },

    "#/workflows": {
      page: WorkflowsPage,
      roles: ["admin", "manager", "employee"]
    },

    "#/decisions": {
      page: DecisionsPage,
      roles: ["admin", "manager"]
    },

    "#/mining": {
      page: MiningPage,
      roles: ["admin", "manager"]
    },

    "#/agents": {
      page: AgentsPage,
      roles: ["admin", "manager", "employee"]
    },

    "#/predict": {
      page: PredictPage,
      roles: ["admin", "manager", "employee"]
    },

    "#/copilot": {
      page: CopilotPage,
      roles: ["admin", "manager", "employee"]
    },

    "#/users": {
      page: UsersPage,
      roles: ["admin"]
    }
  };


  /* ============================================================
     PAGE BACKGROUND
     ============================================================ */

  function setPageBackground(hash) {
    // Remove any existing page-* classes
    Array.from(document.body.classList).filter(c => c.startsWith("page-")).forEach(c => document.body.classList.remove(c));

    // Map explicit page classes for each route so each page can have its own background
    switch (hash) {
      case "#/dashboard":
        document.body.classList.add("page-dashboard");
        break;
      case "#/workflows":
        document.body.classList.add("page-workflows");
        break;
      case "#/decisions":
        document.body.classList.add("page-decisions");
        break;
      case "#/mining":
        document.body.classList.add("page-mining");
        break;
      case "#/agents":
        document.body.classList.add("page-agents");
        break;
      case "#/predict":
        document.body.classList.add("page-predict");
        break;
      case "#/copilot":
        document.body.classList.add("page-copilot");
        break;
      case "#/users":
        document.body.classList.add("page-users");
        break;
      default:
        // fallback to intelligence-style background
        document.body.classList.add("page-intelligence");
    }

  }


  /* ============================================================
     DEFAULT ROUTE
     ============================================================ */

  function defaultRouteFor(role) {

    if (role === "admin" || role === "manager") {
      return "#/dashboard";
    }

    return "#/workflows";

  }


  /* ============================================================
     ROUTER
     ============================================================ */

  function go() {

    let hash = window.location.hash || "";


    /* ----------------------------------------------------------
       NOT LOGGED IN
       ---------------------------------------------------------- */

    if (!Session.isLoggedIn()) {

      // Remove any page-specific classes while on auth pages
      Array.from(document.body.classList).filter(c => c.startsWith("page-")).forEach(c => document.body.classList.remove(c));

      // Login page
      if (hash === "#/signup") {
        LoginPage.render("signup");
        return;
      }

      // Default to login
      LoginPage.render("login");
      return;

    }


    /* ----------------------------------------------------------
       DEFAULT / LOGIN / SIGNUP ROUTES
       ---------------------------------------------------------- */

    if (
      !hash ||
      hash === "#/login" ||
      hash === "#/signup" ||
      hash === "#/"
    ) {

      hash = defaultRouteFor(Session.role());

      window.location.hash = hash;

      return;

    }


    /* ----------------------------------------------------------
       FIND ROUTE
       ---------------------------------------------------------- */

    const route = routes[hash];


    if (!route) {

      window.location.hash = defaultRouteFor(Session.role());

      return;

    }


    /* ----------------------------------------------------------
       ROLE ACCESS
       ---------------------------------------------------------- */

    if (!route.roles.includes(Session.role())) {

      UI.toast(
        "You don't have access to that section",
        "error"
      );

      window.location.hash = defaultRouteFor(Session.role());

      return;

    }


    /* ----------------------------------------------------------
       SET PAGE BACKGROUND
       ---------------------------------------------------------- */

    setPageBackground(hash);


    /* ----------------------------------------------------------
       RENDER PAGE
       ---------------------------------------------------------- */

    route.page.render();

  }


  /* ============================================================
     HASH CHANGE
     ============================================================ */

  window.addEventListener("hashchange", go);


  return {
    go
  };

})();