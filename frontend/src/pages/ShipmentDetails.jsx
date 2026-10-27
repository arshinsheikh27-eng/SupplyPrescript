import { useParams } from "react-router-dom";
import { useState } from "react";

import Layout from "../components/Layout";
import { shipments, alternatives } from "../data/mockData";

function ShipmentDetails() {
  const { id } = useParams();

  const shipment = shipments.find(
    (item) => item.shipment_id === id
  );

  const [selectedAlternative, setSelectedAlternative] = useState("");

  if (!shipment) {
    return (
      <Layout>
        <div className="page">
          <h1>Shipment Not Found</h1>
        </div>
      </Layout>
    );
  }

  const shipmentAlternatives = alternatives[id] || [];

  return (
    <Layout>
      <div className="page">
        <h1>Shipment Details</h1>

        <div className="section-card">
          <h2>{shipment.shipment_id}</h2>

          <div className="detail-grid">
            <div className="detail-item">
              <strong>Product</strong>
              {shipment.product}
            </div>

            <div className="detail-item">
              <strong>Supplier</strong>
              {shipment.supplier}
            </div>

            <div className="detail-item">
              <strong>Origin</strong>
              {shipment.origin}
            </div>

            <div className="detail-item">
              <strong>Destination</strong>
              {shipment.destination}
            </div>

            <div className="detail-item">
              <strong>Planned Delivery</strong>
              {shipment.planned_delivery_date}
            </div>

            <div className="detail-item">
              <strong>Risk</strong>
              <span
                className={`risk risk-${shipment.risk_level.toLowerCase()}`}
              >
                {shipment.risk_level}
              </span>
            </div>
          </div>
        </div>

        <div className="section-card">
          <h2>Prediction</h2>

          <p>
            Estimated delay probability:
            <strong>
              {" "}
              {(shipment.delay_probability * 100).toFixed(0)}%
            </strong>
          </p>

          <p>
            Current risk category:
            <strong> {shipment.risk_level}</strong>
          </p>

          <p>
            This is currently a prototype prediction and should be replaced
            with the team's actual model output.
          </p>
        </div>

        <div className="section-card">
          <h2>Suggested Alternatives</h2>

          {shipmentAlternatives.length === 0 ? (
            <p>No feasible alternative found.</p>
          ) : (
            shipmentAlternatives.map((alternative) => (
              <div
                className={`alternative ${
                  selectedAlternative === alternative.alternative_id
                    ? "selected"
                    : ""
                }`}
                key={alternative.alternative_id}
              >
                <label>
                  <input
                    type="radio"
                    name="alternative"
                    value={alternative.alternative_id}
                    checked={
                      selectedAlternative === alternative.alternative_id
                    }
                    onChange={() =>
                      setSelectedAlternative(
                        alternative.alternative_id
                      )
                    }
                  />

                  <div>
                    <strong>{alternative.action}</strong>

                    <div>
                      Estimated time: {alternative.estimated_time}
                    </div>

                    <div>
                      Estimated cost: ₹
                      {alternative.estimated_cost.toLocaleString()}
                    </div>
                  </div>
                </label>
              </div>
            ))
          )}

          <button className="primary-btn">
            Save Decision
          </button>
        </div>
      </div>
    </Layout>
  );
}

export default ShipmentDetails;