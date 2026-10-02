function RiskBadge({ risk }) {
  const normalizedRisk = risk?.toLowerCase();

  return (
    <span className={`risk-badge ${normalizedRisk}`}>
      {risk || "Unknown"}
    </span>
  );
}

export default RiskBadge;