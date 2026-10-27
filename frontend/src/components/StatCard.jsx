function StatCard({ title, value }) {
  return (
    <div className="card">
      <div className="stat-label">{title}</div>
      <div className="stat-value">{value}</div>
    </div>
  );
}

export default StatCard;