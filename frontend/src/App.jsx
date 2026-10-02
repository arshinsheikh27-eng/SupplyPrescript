import { Routes, Route } from "react-router-dom";

import Sidebar from "./components/Sidebar";
import Navbar from "./components/Navbar";

import Dashboard from "./pages/Dashboard";
import Shipments from "./pages/Shipments";
import ShipmentDetails from "./pages/ShipmentDetails";
import Alternatives from "./pages/Alternatives";
import DecisionHistory from "./pages/DecisionHistory";
import Outcomes from "./pages/Outcomes";
import Analytics from "./pages/Analytics";

import "./App.css";

function App() {
  return (
    <div className="app">
      <Sidebar />

      <div className="main-area">
        <Navbar />

        <main className="page-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />

            <Route path="/shipments" element={<Shipments />} />

            <Route
              path="/shipments/:shipmentId"
              element={<ShipmentDetails />}
            />

            <Route
              path="/shipments/:shipmentId/alternatives"
              element={<Alternatives />}
            />

            <Route
              path="/decisions"
              element={<DecisionHistory />}
            />

            <Route
              path="/outcomes"
              element={<Outcomes />}
            />

            <Route
              path="/analytics"
              element={<Analytics />}
            />
          </Routes>
        </main>
      </div>
    </div>
  );
}

export default App;