import { Link } from "react-router-dom";
import Layout from "../components/Layout";
import { shipments } from "../data/mockData";

function Dashboard() {
  const total = shipments.length;

  const highRisk = shipments.filter(
    (shipment) => shipment.risk_level === "High"
  ).length;

  const onTime = shipments.filter(
    (shipment) => shipment.risk_level === "Low"
  ).length;

  return (
    <Layout>
      <div className="page">
        <h1 className="page-title">Welcome, Team!</h1>
        <p className="page-subtitle">
          Here's the latest shipment insights and recommendations.
        </p>

        <div className="cards">
          <div className="card">
            <div className="stat-label">Total Shipments</div>
            <div className="stat-value">{total}</div>
          </div>

          <div className="card">
            <div className="stat-label">At Risk of Delay</div>
            <div className="stat-value">{highRisk}</div>
          </div>

          <div className="card">
            <div className="stat-label">On Time</div>
            <div className="stat-value">{onTime}</div>
          </div>

          <div className="card">
            <div className="stat-label">Avg. Delay (days)</div>
            <div className="stat-value">2.3</div>
          </div>
        </div>

        <div className="dashboard-grid">
          <div className="section-card">
            <h2>Recent Shipments</h2>

            <div className="table-wrapper">
              <table>
                <thead>
                  <tr>
                    <th>Shipment ID</th>
                    <th>Product</th>
                    <th>Supplier</th>
                    <th>Risk</th>
                    <th>Status</th>
                    <th>Action</th>
                  </tr>
                </thead>

                <tbody>
                  {shipments.map((shipment) => (
                    <tr key={shipment.shipment_id}>
                      <td>{shipment.shipment_id}</td>
                      <td>{shipment.product}</td>
                      <td>{shipment.supplier}</td>

                      <td>
                        <span
                          className={`risk risk-${shipment.risk_level.toLowerCase()}`}
                        >
                          {shipment.risk_level}
                        </span>
                      </td>

                      <td>{shipment.status}</td>

                      <td>
                        <Link to={`/shipments/${shipment.shipment_id}`}>
                          <button className="view-btn">View</button>
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <div className="section-card">
            <h2>Suggested Alternatives</h2>

            <p>
              Select a shipment to inspect its possible alternatives.
            </p>

            <Link to="/shipments/SHP001">
              <button className="primary-btn">
                Open High-Risk Shipment
              </button>
            </Link>
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default Dashboard;