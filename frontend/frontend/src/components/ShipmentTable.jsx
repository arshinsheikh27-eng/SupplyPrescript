import { shipments } from "../data/mockData";

function ShipmentTable() {
  return (
    <div className="panel">

      <div className="panel-header">
        <h3>Recent Shipments</h3>
        <button>View All</button>
      </div>

      <table>

        <thead>
          <tr>
            <th>Shipment ID</th>
            <th>Product</th>
            <th>Supplier</th>
            <th>Delay Risk</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>

        <tbody>

          {shipments.map((shipment) => (

            <tr key={shipment.id}>

              <td>{shipment.id}</td>

              <td>{shipment.product}</td>

              <td>{shipment.supplier}</td>

              <td>
                <span className={`risk ${shipment.risk.toLowerCase()}`}>
                  {shipment.risk}
                </span>
              </td>

              <td>{shipment.status}</td>

              <td>
                <button>View</button>
              </td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>
  );
}

export default ShipmentTable;