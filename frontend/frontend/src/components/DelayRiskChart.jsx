import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from "recharts";

import { delayRiskData } from "../data/mockData";

function DelayRiskChart() {
  return (
    <div className="panel">

      <h3>Delay Risk Trend</h3>

      <ResponsiveContainer width="100%" height={280}>

        <LineChart data={delayRiskData}>

          <CartesianGrid strokeDasharray="3 3" />

          <XAxis dataKey="month" />

          <YAxis />

          <Tooltip />

          <Legend />

          <Line
            type="monotone"
            dataKey="high"
            stroke="#ef4444"
            name="High"
          />

          <Line
            type="monotone"
            dataKey="medium"
            stroke="#f59e0b"
            name="Medium"
          />

          <Line
            type="monotone"
            dataKey="low"
            stroke="#10b981"
            name="Low"
          />

        </LineChart>

      </ResponsiveContainer>

    </div>
  );
}

export default DelayRiskChart;
