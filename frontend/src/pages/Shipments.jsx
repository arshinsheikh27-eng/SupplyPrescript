import { useEffect, useState } from "react";

import ShipmentTable from "../components/ShipmentTable";
import Loading from "../components/Loading";
import ErrorMessage from "../components/ErrorMessage";

import { getShipments } from "../services/api";

function Shipments() {
  const [shipments, setShipments] = useState([]);
  const [filter, setFilter] = useState("All");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadData() {
      try {
        const data = await getShipments();
        setShipments(data);
      } catch (err) {
        setError("Unable to load shipments.");
      } finally {
        setLoading(false);
      }
    }

    loadData();
  }, []);

  const filteredShipments =
    filter === "All"
      ? shipments
      : shipments.filter(
          (shipment) => shipment.risk_level === filter
        );

  return (
    <div>
      <div className="page-header">
        <div>
          <h2>Shipments</h2>
          <p>Review shipment records and predicted delay risk.</p>
        </div>
      </div>

      <div className="filter-container">
        {["All", "High", "Medium", "Low"].map((item) => (
          <button
            key={item}
            className={
              filter === item
                ? "filter-button active"
                : "filter-button"
            }
            onClick={() => setFilter(item)}
          >
            {item}
          </button>
        ))}
      </div>

      {loading && <Loading />}

      {error && <ErrorMessage message={error} />}

      {!loading && !error && (
        <ShipmentTable shipments={filteredShipments} />
      )}
    </div>
  );
}

export default Shipments;