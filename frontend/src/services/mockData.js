export const shipments = [
  {
    shipment_id: "SHP-1001",
    origin: "Hyderabad",
    destination: "Mumbai",
    planned_delivery_date: "2026-10-05",
    actual_delivery_date: null,
    delay_days: null,
    delay_label: "Delayed",
    delay_probability: 0.82,
    risk_level: "High",
  },
  {
    shipment_id: "SHP-1002",
    origin: "Bangalore",
    destination: "Chennai",
    planned_delivery_date: "2026-10-04",
    actual_delivery_date: null,
    delay_days: null,
    delay_label: "On Time",
    delay_probability: 0.22,
    risk_level: "Low",
  },
  {
    shipment_id: "SHP-1003",
    origin: "Delhi",
    destination: "Pune",
    planned_delivery_date: "2026-10-07",
    actual_delivery_date: null,
    delay_days: null,
    delay_label: "At Risk",
    delay_probability: 0.64,
    risk_level: "Medium",
  },
  {
    shipment_id: "SHP-1004",
    origin: "Kolkata",
    destination: "Hyderabad",
    planned_delivery_date: "2026-10-08",
    actual_delivery_date: null,
    delay_days: null,
    delay_label: "Delayed",
    delay_probability: 0.91,
    risk_level: "High",
  },
];

export const alternatives = {
  "SHP-1001": [
    {
      alternative_id: "ALT-01",
      action: "Current shipping plan",
      estimated_cost: 4200,
      estimated_time: "3 days",
      status: "Baseline",
    },
    {
      alternative_id: "ALT-02",
      action: "Priority shipping",
      estimated_cost: 5800,
      estimated_time: "2 days",
      status: "Feasible",
    },
    {
      alternative_id: "ALT-03",
      action: "Alternative route",
      estimated_cost: 4700,
      estimated_time: "2.5 days",
      status: "Feasible",
    },
  ],

  "SHP-1002": [
    {
      alternative_id: "ALT-04",
      action: "Current shipping plan",
      estimated_cost: 3000,
      estimated_time: "2 days",
      status: "Baseline",
    },
  ],

  "SHP-1003": [
    {
      alternative_id: "ALT-05",
      action: "Priority shipping",
      estimated_cost: 5200,
      estimated_time: "2 days",
      status: "Feasible",
    },
    {
      alternative_id: "ALT-06",
      action: "Alternative route",
      estimated_cost: 4400,
      estimated_time: "2.5 days",
      status: "Feasible",
    },
  ],

  "SHP-1004": [
    {
      alternative_id: "ALT-07",
      action: "Priority shipping",
      estimated_cost: 6200,
      estimated_time: "2 days",
      status: "Feasible",
    },
  ],
};

export const decisions = [
  {
    shipment_id: "SHP-1001",
    selected_action: "Priority shipping",
    decision_timestamp: "2026-10-01 10:30",
    status: "Saved",
  },
];

export const outcomes = [
  {
    shipment_id: "SHP-1001",
    predicted_risk: 0.82,
    actual_delay_days: 1,
    outcome_status: "Completed",
  },
];