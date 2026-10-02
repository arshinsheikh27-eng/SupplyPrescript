import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

import RiskBadge from "../components/RiskBadge";
import Loading from "../components/Loading";
import ErrorMessage from "../components/ErrorMessage";

import {
  getShipment,
  getPrediction,
} from "../services/api";

function ShipmentDetails() {
  const { shipmentId } = useParams();

  const [shipment, setShipment] = useState(null);
  const [prediction, setPrediction] = useState(null);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadData() {
      try {
        const shipmentData = await getShipment(shipmentId);
        const predictionData = await getPrediction(shipmentId);

        setShipment(shipmentData);
        setPrediction(predictionData);
      } catch (err) {
        setError("Unable to load shipment details.");
      } finally {
        setLoading(false);
      }
    }

    loadData();
  }, [shipmentId]);

  if (loading) {
    return <Loading />;
  }

  if (error) {
    return <ErrorMessage message={error} />;
  }

  if (!shipment) {
    return <ErrorMessage message="Shipment not found." />;
  }

  return (
    <div>
      <div className="page-header">
        <div>
          <h2>Shipment {shipment.shipment_id}</h2>
          <p>
            Review shipment information and predicted delay risk.
          </p>
        </div>

        <Link
          to={`/shipments/${shipment.shipment_id}/alternatives`}
          className="primary-button"
        >
          View Alternatives
        </Link>
      </div>

      <div className="details-grid">
        <div className="detail-card">
          <h3>Shipment Information</h3>

          <div className="detail-row">
            <span>Shipment ID</span>
            <strong>{shipment.shipment_id}</strong>
          </div>

          <div className="detail-row">
            <span>Origin</span>
            <strong>{shipment.origin}</strong>
          </div>

          <div className="detail-row">
            <span>Destination</span>
            <strong>{shipment.destination}</strong>
          </div>

          <div className="detail-row">
            <span>Planned Delivery</span>
            <strong>{shipment.planned_delivery_date}</strong>
          </div>
        </div>

        <div className="detail-card">
          <h3>Prediction</h3>

          <div className="prediction-value">
            <RiskBadge
              risk={
                prediction?.risk_level ||
                shipment.risk_level
              }
            />
          </div>

          <p>
            Predicted delay probability:
          </p>

          <h2>
            {(
              (prediction?.delay_probability ??
                shipment.delay_probability) * 100
            ).toFixed(0)}
            %
          </h2>

          <p className="muted">
            This risk result is based on the current
            prediction response. Replace mock values with
            the actual model response during integration.
          </p>
        </div>
      </div>
    </div>
  );
}

export default ShipmentDetails;