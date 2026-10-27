import { useEffect, useState } from "react";

import Loading from "../components/Loading";
import ErrorMessage from "../components/ErrorMessage";

import { getDecisions } from "../services/api";

function DecisionHistory() {
  const [decisions, setDecisions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadData() {
      try {
        const data = await getDecisions();
        setDecisions(data);
      } catch (err) {
        setError("Unable to load decision history.");
      } finally {
        setLoading(false);
      }
    }

    loadData();
  }, []);

  return (
    <div>
      <div className="page-header">
        <div>
          <h2>Decision History</h2>
          <p>Previously selected shipment actions.</p>
        </div>
      </div>

      {loading && <Loading />}

      {error && <ErrorMessage message={error} />}

      {!loading && !error && (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Shipment ID</th>
                <th>Selected Action</th>
                <th>Decision Time</th>
                <th>Status</th>
              </tr>
            </thead>

            <tbody>
              {decisions.map((decision, index) => (
                <tr key={index}>
                  <td>{decision.shipment_id}</td>
                  <td>{decision.selected_action}</td>
                  <td>{decision.decision_timestamp}</td>
                  <td>{decision.status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default DecisionHistory;