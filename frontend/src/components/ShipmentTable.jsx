import { Link } from "react-router-dom";
import RiskBadge from "./RiskBadge";

function ShipmentTable({ shipments }) {
  return (
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
                <RiskBadge level={shipment.risk_level} />
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
  );
}

export default ShipmentTable;