import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  Truck,
  ClipboardList,
  BarChart3,
  Settings,
} from "lucide-react";

function Layout({ children }) {
  return (
    <div className="app">
      <aside className="sidebar">
        <div className="logo">
          <Truck size={22} />
          <span>SupplyPrescript</span>
        </div>

        <nav>
          <NavLink to="/">
            <LayoutDashboard size={18} />
            Dashboard
          </NavLink>

          <NavLink to="/">
            <Truck size={18} />
            Shipments
          </NavLink>

          <NavLink to="/decisions">
            <ClipboardList size={18} />
            Decisions
          </NavLink>

          <NavLink to="/outcomes">
            <BarChart3 size={18} />
            Results
          </NavLink>
        </nav>

        <div className="sidebar-bottom">
          <NavLink to="/outcomes">
            <Settings size={18} />
            Settings
          </NavLink>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <span>SupplyPrescript</span>

          <div className="team-user">
            <div className="avatar">S</div>
            <span>Team</span>
          </div>
        </header>

        {children}
      </main>
    </div>
  );
}

export default Layout;