function StatCard({ title, value, icon, iconClass }) {
  return (
    <div className="stat-card">

      <div>
        <p>{title}</p>
        <h2>{value}</h2>
      </div>

      <div className={`stat-icon ${iconClass}`}>
        {icon}
      </div>

    </div>
  );
}

export default StatCard;
