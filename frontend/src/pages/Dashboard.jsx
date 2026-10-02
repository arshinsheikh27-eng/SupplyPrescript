import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import StatCard from "../components/StatCard";
import ShipmentTable from "../components/ShipmentTable";
import Loading from "../components/Loading";
import ErrorMessage from "../components/ErrorMessage";

import { getShipments } from "../services/api";

function Dashboard() {
  const [shipments, setShipments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadShipments() {
      try {
        const data = await getShipments();
        setShipments(data);
      } catch (err) {
        setError("Unable to load shipment data.");
      } finally {
        setLoading(false);
      }
    }

    loadShipments();
  }, []);

  const highRisk = shipments.filter(
    (shipment) => shipment.risk_level === "High"
  ).length;

  const mediumRisk = shipments.filter(
    (shipment) => shipment.risk_level === "Medium"
  ).length;

  const lowRisk = shipments.filter(
    (shipment) => shipment.risk_level === "Low"
  ).length;

  return (
    <div>
      <div className="page-header">
        <div>
          <h2>Dashboard</h2>
          <p>
            Monitor shipment delay risk and review possible actions.
          </p>
        </div>

        <Link to="/shipments" className="primary-button">
          View Shipments
        </Link>
      </div>

      {loading && <Loading />}

      {error && <ErrorMessage message={error} />}

      {!loading && !error && (
        <>
          <div className="stats-grid">
            <StatCard
              title="Total Shipments"
              value={shipments.length}
              description="Current shipment records"
            />

            <StatCard
              title="High Risk"
              value={highRisk}
              description="Shipments requiring attention"
            />

            <StatCard
              title="Medium Risk"
              value={mediumRisk}
              description="Shipments to monitor"
            />

            <StatCard
              title="Low Risk"
              value={lowRisk}
              description="Lower predicted risk"
            />
          </div>

          <section className="content-section">
            <div className="section-header">
              <h3>Shipment Overview</h3>
            </div>

            <ShipmentTable shipments={shipments} />
          </section>
        </>
      )}
    </div>
  );
}

export default Dashboard;