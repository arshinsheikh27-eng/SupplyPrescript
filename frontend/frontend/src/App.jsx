import {
  Truck,
  AlertTriangle,
  CheckCircle,
  Clock
} from "lucide-react";

import Sidebar from "./components/Sidebar";
import Header from "./components/Header";
import StatCard from "./components/StatCard";

import "./App.css";

function App() {
  return (
    <div className="app">

      <Sidebar />

      <main className="main-content">

        <Header />

        <section className="stats-grid">

          <StatCard
            title="Total Shipments"
            value="24"
            icon={<Truck />}
            iconClass="blue"
          />

          <StatCard
            title="At Risk of Delay"
            value="6"
            icon={<AlertTriangle />}
            iconClass="red"
          />

          <StatCard
            title="On Time"
            value="18"
            icon={<CheckCircle />}
            iconClass="green"
          />

          <StatCard
            title="Avg. Delay (days)"
            value="2.3"
            icon={<Clock />}
            iconClass="purple"
          />

        </section>

      </main>

    </div>
  );
}

export default App;