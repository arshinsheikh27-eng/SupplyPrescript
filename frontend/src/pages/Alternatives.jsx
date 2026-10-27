import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";

import AlternativeCard from "../components/AlternativeCard";
import Loading from "../components/Loading";
import ErrorMessage from "../components/ErrorMessage";

import {
  getAlternatives,
  getShipment,
  saveDecision,
} from "../services/api";

function Alternatives() {
  const { shipmentId } = useParams();

  const [shipment, setShipment] = useState(null);
  const [alternatives, setAlternatives] = useState([]);

  const [selected, setSelected] = useState(null);

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  useEffect(() => {
    async function loadData() {
      try {
        const shipmentData = await getShipment(shipmentId);
        const alternativeData =
          await getAlternatives(shipmentId);

        setShipment(shipmentData);
        setAlternatives(alternativeData);
      } catch (err) {
        setError("Unable to load alternatives.");
      } finally {
        setLoading(false);
      }
    }

    loadData();
  }, [shipmentId]);

  async function handleSaveDecision() {
    if (!selected) {
      setError("Please select an action first.");
      return;
    }

    try {
      setSaving(true);
      setError("");
      setSuccess("");

      await saveDecision(
        shipmentId,
        selected.action
      );

      setSuccess(
        "Decision saved successfully."
      );
    } catch (err) {
      setError("Unable to save the decision.");
    } finally {
      setSaving(false);
    }
  }

  if (loading) {
    return <Loading />;
  }

  if (error && !shipment) {
    return <ErrorMessage message={error} />;
  }

  return (
    <div>
      <div className="page-header">
        <div>
          <h2>Alternative Actions</h2>

          <p>
            Shipment: {shipment?.shipment_id}
          </p>
        </div>

        <Link
          to={`/shipments/${shipmentId}`}
          className="secondary-button"
        >
          Back to Shipment
        </Link>
      </div>

      {error && (
        <ErrorMessage message={error} />
      )}

      {success && (
        <div className="success-message">
          {success}
        </div>
      )}

      {alternatives.length === 0 ? (
        <div className="empty-state">
          No feasible alternative found.
        </div>
      ) : (
        <>
          <div className="alternatives-grid">
            {alternatives.map((alternative) => (
              <AlternativeCard
                key={alternative.alternative_id}
                alternative={alternative}
                selected={
                  selected?.alternative_id ===
                  alternative.alternative_id
                }
                onSelect={setSelected}
              />
            ))}
          </div>

          {selected && (
            <div className="decision-box">
              <h3>Selected Action</h3>

              <p>
                You selected:
                <strong>
                  {" "}{selected.action}
                </strong>
              </p>

              <button
                className="primary-button"
                onClick={handleSaveDecision}
                disabled={saving}
              >
                {saving
                  ? "Saving..."
                  : "Confirm & Save Decision"}
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default Alternatives;