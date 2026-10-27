import axios from "axios";

const API_URL =
  import.meta.env.VITE_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const getShipments = async () => {
  const response = await api.get("/shipments");
  return response.data;
};

export const getShipment = async (shipmentId) => {
  const response = await api.get(`/shipments/${shipmentId}`);
  return response.data;
};

export const getPrediction = async (shipmentId) => {
  const response = await api.get(
    `/shipments/${shipmentId}/prediction`
  );

  return response.data;
};

export const getAlternatives = async (shipmentId) => {
  const response = await api.get(
    `/shipments/${shipmentId}/alternatives`
  );

  return response.data;
};

export const saveDecision = async (shipmentId, data) => {
  const response = await api.post(
    `/shipments/${shipmentId}/decisions`,
    data
  );

  return response.data;
};

export const getDecisions = async (shipmentId) => {
  const response = await api.get(
    `/shipments/${shipmentId}/decisions`
  );

  return response.data;
};

export default api;