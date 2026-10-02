import { Link } from "react-router-dom";
import RiskBadge from "./RiskBadge";

function ShipmentTable({ shipments }) {
  return (
    <div className="table-container">
      <table>
        <thead>
          <tr>
            <th>Shipment ID</th>
            <th>Origin</th>
            <th>Destination</th>
            <th>Planned Delivery</th>
            <th>Risk</th>
            <th>Probability</th>
            <th>Action</th>
          </tr>
        </thead>

        <tbody>
          {shipments.map((shipment) => (
            <tr key={shipment.shipment_id}>
              <td>{shipment.shipment_id}</td>
              <td>{shipment.origin}</td>
              <td>{shipment.destination}</td>
              <td>{shipment.planned_delivery_date}</td>

              <td>
                <RiskBadge risk={shipment.risk_level} />
              </td>

              <td>
                {(shipment.delay_probability * 100).toFixed(0)}%
              </td>

              <td>
                <Link
                  className="view-button"
                  to={`/shipments/${shipment.shipment_id}`}
                >
                  View
                </Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ShipmentTable;