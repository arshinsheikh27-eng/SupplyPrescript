function RiskBadge({ level }) {
  return (
    <span className={`risk risk-${level.toLowerCase()}`}>
      {level}
    </span>
  );
}

export default RiskBadge;