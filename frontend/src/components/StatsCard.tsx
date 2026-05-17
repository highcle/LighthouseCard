interface Props {
  label: string;
  value: string | number;
  sub?: string;
  color?: string;
}

export default function StatsCard({ label, value, sub, color = "ocean" }: Props) {
  return (
    <div className={`bg-${color}-50 border border-${color}-200 rounded-xl p-4 text-center`}>
      <p className={`text-3xl font-bold text-${color}-700`}>{value}</p>
      {sub && <p className={`text-sm text-${color}-600 mt-0.5`}>{sub}</p>}
      <p className="text-xs text-gray-500 mt-1">{label}</p>
    </div>
  );
}
