import { useEffect, useState } from "react";

import StatCard from "../components/StatCard";
import Loading from "../components/Loading";

import { getShipments } from "../services/api";

function Analytics() {
  const [shipments, setShipments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      const data = await getShipments();
      setShipments(data);
      setLoading(false);
    }

    loadData();
  }, []);

  if (loading) {
    return <Loading />;
  }

  const highRisk = shipments.filter(
    (item) => item.risk_level === "High"
  ).length;

  const mediumRisk = shipments.filter(
    (item) => item.risk_level === "Medium"
  ).length;

  const lowRisk = shipments.filter(
    (item) => item.risk_level === "Low"
  ).length;

  return (
    <div>
      <div className="page-header">
        <div>
          <h2>Analytics</h2>
          <p>
            Summary of current shipment risk distribution.
          </p>
        </div>
      </div>

      <div className="stats-grid">
        <StatCard
          title="Total Shipments"
          value={shipments.length}
          description="Available shipment records"
        />

        <StatCard
          title="High Risk"
          value={highRisk}
          description="High predicted risk"
        />

        <StatCard
          title="Medium Risk"
          value={mediumRisk}
          description="Medium predicted risk"
        />

        <StatCard
          title="Low Risk"
          value={lowRisk}
          description="Low predicted risk"
        />
      </div>

      <div className="content-section">
        <h3>Risk Distribution</h3>

        <div className="risk-bars">
          <div>
            <span>High Risk</span>
            <div className="bar">
              <div
                style={{
                  width: `${(highRisk / shipments.length) * 100}%`,
                }}
              />
            </div>
          </div>

          <div>
            <span>Medium Risk</span>
            <div className="bar">
              <div
                style={{
                  width: `${(mediumRisk / shipments.length) * 100}%`,
                }}
              />
            </div>
          </div>

          <div>
            <span>Low Risk</span>
            <div className="bar">
              <div
                style={{
                  width: `${(lowRisk / shipments.length) * 100}%`,
                }}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Analytics;