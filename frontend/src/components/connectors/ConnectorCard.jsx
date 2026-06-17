import {
  runConnector,
  deleteConnector
} from "../../services/connectorService";

function ConnectorCard({
  connector,
  onRefresh,
  onEdit
}) {

  const handleRun = async () => {

    try {

      const response =
        await runConnector(
          connector.connector_id
        );

      alert(
        JSON.stringify(
          response.data,
          null,
          2
        )
      );

      onRefresh();

    } catch (error) {

      console.error("RUN ERROR:",error);

      alert(error.message);

    }

  };
 

  const handleDelete = async () => {

    const confirmed =
      window.confirm(
        "Delete connector?"
      );

    if (!confirmed) return;

    try {

      await deleteConnector(
        connector.connector_id
      );

      onRefresh();

    } catch (error) {

      console.error(error);

      alert("Delete Failed");

    }

  };

  return (

    <div
      style={{
        border: "1px solid #ddd",
        borderRadius: "10px",
        padding: "15px",
        marginBottom: "10px"
      }}
    >

      <h3>
        {connector.connector_name}
      </h3>

      <p>
        Type:
        {" "}
        {connector.connector_type}
      </p>

      <p>
        Status:
        {" "}
        {connector.status}
      </p>

      <p>
        Refresh:
        {" "}
        {connector.refresh_type}
      </p>

      <p>
        Last Run:
        {" "}
        {connector.last_run || "-"}
      </p>

      <div
        style={{
          display: "flex",
          gap: "10px"
        }}
      >

        <button onClick={handleRun}>
          Run Now
        </button>

        <button
          onClick={() =>
            onEdit(connector)
          }
        >
          Edit
        </button>

        <button
          onClick={handleDelete}
        >
          Delete
        </button>

      </div>

    </div>

  );

}

export default ConnectorCard;