import {
  LayoutDashboard,
  PackagePlus,
  GitBranch,
  BarChart3,
  FileText,
  Settings,
  Truck
} from "lucide-react";

function Sidebar() {
  return (
    <aside className="sidebar">

      <div className="logo">
        <Truck size={24} />
        <span>
          Supply<span>Prescript</span>
        </span>
      </div>

      <nav>

        <a className="nav-item active">
          <LayoutDashboard size={18} />
          Dashboard
        </a>

        <a className="nav-item">
          <PackagePlus size={18} />
          New Shipment
        </a>

        <a className="nav-item">
          <GitBranch size={18} />
          Decisions
        </a>

        <a className="nav-item">
          <BarChart3 size={18} />
          Results
        </a>

        <a className="nav-item">
          <FileText size={18} />
          Reports
        </a>

      </nav>

      <div className="sidebar-bottom">
        <a className="nav-item">
          <Settings size={18} />
          Settings
        </a>
      </div>

    </aside>
  );
}

export default Sidebar;