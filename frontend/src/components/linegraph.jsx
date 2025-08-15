import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

export default function LineGraph({ data }) {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart
        data={data}
        margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" /> {/* X-axis shows date */}
        <YAxis domain={[0, 100]} />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="score" stroke="#82ca9d" />
      </LineChart>
    </ResponsiveContainer>
  );
}
