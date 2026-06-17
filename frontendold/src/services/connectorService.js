import api from "./api";

export const getConnectors = () =>
  api.get("/connectors/connectors");

export const createConnector = (payload) =>
  api.post("/connectors/connectors", payload);

export const updateConnector = (id, payload) =>
  api.put(
    `/connectors/connectors/${id}`,
    payload
  );

export const deleteConnector = (id) =>
  api.delete(
    `/connectors/connectors/${id}`
  );

export const runConnector = (id) =>
  api.post(
    `/connectors/connectors/${id}/run`
  );