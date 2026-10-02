import { NavLink } from "react-router-dom";

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="logo">
        <h2>SupplyPrescript</h2>
        <p>Shipment Intelligence</p>
      </div>

      <nav className="sidebar-nav">
        <NavLink
          to="/"
          className={({ isActive }) =>
            isActive ? "nav-link active" : "nav-link"
          }
        >
          Dashboard
        </NavLink>

        <NavLink
          to="/shipments"
          className={({ isActive }) =>
            isActive ? "nav-link active" : "nav-link"
          }
        >
          Shipments
        </NavLink>

        <NavLink
          to="/decisions"
          className={({ isActive }) =>
            isActive ? "nav-link active" : "nav-link"
          }
        >
          Decision History
        </NavLink>

        <NavLink
          to="/outcomes"
          className={({ isActive }) =>
            isActive ? "nav-link active" : "nav-link"
          }
        >
          Outcomes
        </NavLink>

        <NavLink
          to="/analytics"
          className={({ isActive }) =>
            isActive ? "nav-link active" : "nav-link"
          }
        >
          Analytics
        </NavLink>
      </nav>
    </aside>
  );
}

export default Sidebar;