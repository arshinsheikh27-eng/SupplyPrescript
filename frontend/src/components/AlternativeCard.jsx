import { formatCurrency } from "../utils/formatters";

function AlternativeCard({
  alternative,
  selected,
  onSelect,
}) {
  return (
    <div
      className={
        selected
          ? "alternative-card selected"
          : "alternative-card"
      }
    >
      <div className="alternative-header">
        <h3>{alternative.action}</h3>

        <span className="status-badge">
          {alternative.status}
        </span>
      </div>

      <div className="alternative-details">
        <div>
          <span>Estimated Time</span>
          <strong>{alternative.estimated_time}</strong>
        </div>

        <div>
          <span>Estimated Cost</span>
          <strong>
            {formatCurrency(alternative.estimated_cost)}
          </strong>
        </div>
      </div>

      <button
        className="primary-button"
        onClick={() => onSelect(alternative)}
      >
        {selected ? "Selected" : "Select Action"}
      </button>
    </div>
  );
}

export default AlternativeCard;