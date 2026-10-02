import axios from "axios";
import {
  shipments,
  alternatives,
  decisions,
  outcomes,
} from "./mockData";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export async function getShipments() {
  if (!API_BASE_URL) {
    return shipments;
  }

  const response = await api.get("/shipments");
  return response.data;
}

export async function getShipment(shipmentId) {
  if (!API_BASE_URL) {
    return shipments.find(
      (shipment) => shipment.shipment_id === shipmentId
    );
  }

  const response = await api.get(`/shipments/${shipmentId}`);
  return response.data;
}

export async function getPrediction(shipmentId) {
  if (!API_BASE_URL) {
    const shipment = shipments.find(
      (item) => item.shipment_id === shipmentId
    );

    return {
      shipment_id: shipmentId,
      delay_probability: shipment?.delay_probability ?? 0,
      risk_level: shipment?.risk_level ?? "Unknown",
    };
  }

  const response = await api.get(
    `/shipments/${shipmentId}/prediction`
  );

  return response.data;
}

export async function getAlternatives(shipmentId) {
  if (!API_BASE_URL) {
    return alternatives[shipmentId] || [];
  }

  const response = await api.get(
    `/shipments/${shipmentId}/alternatives`
  );

  return response.data;
}

export async function saveDecision(
  shipmentId,
  selectedAlternative,
  userNote = ""
) {
  if (!API_BASE_URL) {
    return {
      shipment_id: shipmentId,
      selected_action: selectedAlternative,
      decision_timestamp: new Date().toISOString(),
      user_note: userNote,
      status: "Saved",
    };
  }

  const response = await api.post(
    `/shipments/${shipmentId}/decisions`,
    {
      selected_action: selectedAlternative,
      user_note: userNote,
    }
  );

  return response.data;
}

export async function getDecisions() {
  if (!API_BASE_URL) {
    return decisions;
  }

  const response = await api.get("/decisions");
  return response.data;
}

export async function getOutcomes() {
  if (!API_BASE_URL) {
    return outcomes;
  }

  const response = await api.get("/outcomes");
  return response.data;
}

export default api;