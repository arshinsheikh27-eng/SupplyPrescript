export const shipments = [
  {
    id: "SHP001",
    product: "Microchip",
    supplier: "Supplier A",
    risk: "High",
    status: "Predict"
  },
  {
    id: "SHP002",
    product: "Battery",
    supplier: "Supplier B",
    risk: "Low",
    status: "On Time"
  },
  {
    id: "SHP003",
    product: "Display",
    supplier: "Supplier C",
    risk: "Medium",
    status: "Predict"
  },
  {
    id: "SHP004",
    product: "Processor",
    supplier: "Supplier A",
    risk: "High",
    status: "Predict"
  },
  {
    id: "SHP005",
    product: "Camera",
    supplier: "Supplier D",
    risk: "Low",
    status: "On Time"
  }
];

export const delayRiskData = [
  { month: "Jan", high: 10, medium: 7, low: 3 },
  { month: "Feb", high: 13, medium: 8, low: 4 },
  { month: "Mar", high: 8, medium: 11, low: 5 },
  { month: "Apr", high: 14, medium: 9, low: 4 },
  { month: "May", high: 7, medium: 12, low: 6 },
  { month: "Jun", high: 11, medium: 8, low: 7 }
];

export const decisionData = [
  {
    name: "Successful",
    value: 70
  },
  {
    name: "Partially Successful",
    value: 20
  },
  {
    name: "Failed",
    value: 10
  }
];
