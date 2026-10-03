import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer
} from "recharts";

import { decisionData } from "../data/mockData";

function DecisionOutcomeChart() {

  const colors = [
    "#10b981",
    "#f59e0b",
    "#ef4444"
  ];

  return (
    <div className="panel">

      <h3>Decision Outcomes</h3>

      <ResponsiveContainer width="100%" height={280}>

        <PieChart>

          <Pie
            data={decisionData}
            dataKey="value"
            nameKey="name"
            innerRadius={55}
            outerRadius={85}
          >

            {decisionData.map((entry, index) => (
              <Cell
                key={index}
                fill={colors[index]}
              />
            ))}

          </Pie>

          <Tooltip />

          <Legend />

        </PieChart>

      </ResponsiveContainer>

    </div>
  );
}

export default DecisionOutcomeChart;