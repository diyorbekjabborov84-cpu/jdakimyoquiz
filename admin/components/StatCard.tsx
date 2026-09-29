interface StatCardProps {
  title: string;
  value: number | string;
  icon: string;
  description: string;
}

export default function StatCard({ title, value, icon, description }: StatCardProps) {
  return (
    <div className="stat-card">
      <div className="stat-header">
        <span>{title}</span>
        <span className="stat-icon">{icon}</span>
      </div>
      <div className="stat-value">{value}</div>
      <div className="stat-desc">{description}</div>
    </div>
  );
}
