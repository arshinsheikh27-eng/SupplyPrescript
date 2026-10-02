import { useEffect, useState } from "react";

import Loading from "../components/Loading";
import ErrorMessage from "../components/ErrorMessage";

import { getOutcomes } from "../services/api";

function Outcomes() {
  const [outcomes, setOutcomes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadData() {
      try {
        const data = await getOutcomes();
        setOutcomes(data);
      } catch (err) {
        setError("Unable to load outcomes.");
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
          <h2>Outcomes</h2>
          <p>
            Compare predicted shipment risk with actual results.
          </p>
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
                <th>Predicted Risk</th>
                <th>Actual Delay</th>
                <th>Outcome Status</th>
              </tr>
            </thead>

            <tbody>
              {outcomes.map((outcome) => (
                <tr key={outcome.shipment_id}>
                  <td>{outcome.shipment_id}</td>

                  <td>
                    {(outcome.predicted_risk * 100).toFixed(0)}%
                  </td>

                  <td>
                    {outcome.actual_delay_days} days
                  </td>

                  <td>
                    {outcome.outcome_status}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default Outcomes;