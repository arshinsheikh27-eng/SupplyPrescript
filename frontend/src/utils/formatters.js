export function formatCurrency(value) {
  if (value === null || value === undefined) {
    return "—";
  }

  return `₹${Number(value).toLocaleString("en-IN")}`;
}

export function formatProbability(value) {
  if (value === null || value === undefined) {
    return "—";
  }

  return `${(Number(value) * 100).toFixed(0)}%`;
}

export function formatDate(value) {
  if (!value) {
    return "—";
  }

  return new Date(value).toLocaleDateString("en-IN");
}