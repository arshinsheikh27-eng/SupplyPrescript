import ShipmentTable from "./components/ShipmentTable";
import SuggestedAlternatives from "./components/SuggestedAlternatives";
import DelayRiskChart from "./components/DelayRiskChart";
import DecisionOutcomeChart from "./components/DecisionOutcomeChart";

import {
  Truck,
  AlertTriangle,
  CheckCircle,
  Clock,
} from "lucide-react";

import Sidebar from "./components/Sidebar";
import Header from "./components/Header";
import StatCard from "./components/StatCard";

import "./App.css";

function App() {
  return (
    <div className="app">

      {/* Sidebar */}
      <Sidebar />

      {/* Main Dashboard */}
      <main className="main-content">

        {/* Header */}
        <Header />

        {/* Statistics Cards */}
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

        {/* Shipment Information */}
        <section className="dashboard-grid">
          <ShipmentTable />
          <SuggestedAlternatives />
        </section>

        {/* Charts */}
        <section className="charts-grid">
          <DelayRiskChart />
          <DecisionOutcomeChart />
        </section>

      </main>
    </div>
  );
}

export default App;
