// import { useEffect, useState } from "react";

// import api from "../services/api";

// import ConnectorModal from "../components/connectors/ConnectorModal";

// function DataCenter() {

//   const [connectors, setConnectors] = useState([]);

//   const [showModal, setShowModal] = useState(false);

//   const loadConnectors = async () => {

//     try {

//       const response = await api.get(
//         "/connectors"
//       );

//       setConnectors(
//         response.data
//       );

//     } catch (error) {

//       console.error(error);

//     }

//   };

//   useEffect(() => {

//     loadConnectors();

//   }, []);

//   return (
//     <div>

//       <div
//         style={{
//           display: "flex",
//           justifyContent: "space-between",
//           alignItems: "center",
//           marginBottom: "20px"
//         }}
//       >
//         <h1>Data Center</h1>

//         <button
//           onClick={() => setShowModal(true)}
//           style={{
//             padding: "10px 20px",
//             cursor: "pointer"
//           }}
//         >
//           + Create Connector
//         </button>

//       </div>

//       <h2>Connected Connectors</h2>

//       {connectors.length === 0 ? (

//         <p>No connectors found</p>

//       ) : (

//         connectors.map((connector) => (

//           <div
//             key={connector.connector_id}
//             style={{
//               border: "1px solid #ddd",
//               padding: "15px",
//               marginTop: "10px",
//               borderRadius: "8px"
//             }}
//           >
//             <h3>
//               {connector.connector_name}
//             </h3>

//             <p>
//               Type: {connector.connector_type}
//             </p>

//             <p>
//               Status: {connector.status}
//             </p>

//           </div>

//         ))

//       )}

//       <ConnectorModal
//         isOpen={showModal}
//         onClose={() => setShowModal(false)}
//         onSelect={(connector) => {

//           console.log(
//             "Selected Connector:",
//             connector
//           );

//           setShowModal(false);

//         }}
//       />

//     </div>
//   );
// }

// export default DataCenter;







import { useEffect, useState } from "react";

import api from "../services/api";
import "../styles/DataCenter.css";
import ConnectorModal from "../components/connectors/ConnectorModal";
import ConnectorCard from "../components/connectors/ConnectorCard";
import ConnectorFormModal from "../components/connectors/ConnectorFormModal";

function DataCenter() {

  const [connectors, setConnectors] = useState([]);

  const [showModal, setShowModal] = useState(false);

  const [showForm, setShowForm] = useState(false);

  const [selectedType, setSelectedType] =
    useState(null);

  const [editConnector, setEditConnector] =
    useState(null);

  const loadConnectors = async () => {

    try {

      const response =
        await api.get(
            "/connectors/connectors"
        );

      setConnectors(
        response.data
      );

    } catch (error) {

      console.error(
        "Failed to load connectors",
        error
      );

    }

  };

  useEffect(() => {

    loadConnectors();

  }, []);

  return (

    <div>

      {/* Header */}

      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "20px"
        }}
      >

        <h1>Data Center</h1>

        <button
          onClick={() =>
            setShowModal(true)
          }
          style={{
            padding: "10px 20px",
            cursor: "pointer"
          }}
        >
          + Create Connector
        </button>

      </div>

      {/* Connector List */}

      <h2>
        Connected Connectors
      </h2>
      {/* <pre>
        {JSON.stringify(connectors, null, 2)}
      </pre> */}

      {connectors.length === 0 ? (

        <p>
          No connectors found
        </p>

      ) : (

        <div>

          {connectors.map(
            (connector) => (

              <ConnectorCard
                key={
                  connector.connector_id
                }

                connector={
                  connector
                }

                onRefresh={
                  loadConnectors
                }

                // onEdit={(item) => {

                //   setEditConnector(
                //     item
                //   );
                onEdit={(item) => {

                    console.log(item);

                    setEditConnector(item);

  

                  setSelectedType(
                    item.connector_type
                  );

                  setShowForm(
                    true
                  );

                }}
              />

            )
          )}

        </div>

      )}

      {/* Connector Type Selector */}

      <ConnectorModal

        isOpen={showModal}

        onClose={() =>
          setShowModal(false)
        }

        onSelect={(
          connectorType
        ) => {

          setSelectedType(
            connectorType
          );

          setEditConnector(
            null
          );

          setShowModal(
            false
          );

          setShowForm(
            true
          );

        }}
      />

      {/* Create / Edit Form */}

      <ConnectorFormModal

        isOpen={showForm}

        connectorType={
          selectedType
        }

        editConnector={
          editConnector
        }

        onClose={() => {

          setShowForm(
            false
          );

          setEditConnector(
            null
          );

          setSelectedType(
            null
          );

        }}

        onSuccess={() => {

          loadConnectors();

        }}
      />

    </div>

  );

}

export default DataCenter;