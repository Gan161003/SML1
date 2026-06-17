// // import { useEffect, useState } from "react";
// // import { FaCog } from "react-icons/fa";

// // import api from "../services/api";
// // import "../styles/DataCenter.css";

// // import ConnectorModal from "../components/connectors/ConnectorModal";
// // import ConnectorFormModal from "../components/connectors/ConnectorFormModal";

// // function DataCenter() {

// //   const [connectors, setConnectors] = useState([]);

// //   const [showModal, setShowModal] =
// //     useState(false);

// //   const [showForm, setShowForm] =
// //     useState(false);

// //   const [selectedType, setSelectedType] =
// //     useState(null);

// //   const [editConnector, setEditConnector] =
// //     useState(null);

// //   const [menuOpen, setMenuOpen] =
// //     useState(null);

// //   const loadConnectors = async () => {

// //     try {

// //       const response =
// //         await api.get(
// //           "/connectors/connectors"
// //         );

// //       setConnectors(
// //         response.data || []
// //       );

// //     } catch (error) {

// //       console.error(
// //         "Failed to load connectors",
// //         error
// //       );

// //     }

// //   };

// //   useEffect(() => {

// //     loadConnectors();

// //   }, []);

// //   const getPlatformIcon = (
// //     connectorType
// //   ) => {

// //     const type =
// //       String(
// //         connectorType || ""
// //       ).toLowerCase();

// //     if (
// //       type.includes("youtube")
// //     )
// //       return "🎥";

// //     if (
// //       type.includes("instagram")
// //     )
// //       return "📸";

// //     if (
// //       type.includes("reddit")
// //     )
// //       return "🔴";

// //     if (
// //       type.includes("news")
// //     )
// //       return "📰";

// //     if (
// //       type.includes("rss")
// //     )
// //       return "📡";

// //     if (
// //       type.includes("google")
// //     )
// //       return "🌐";

// //     return "🔗";

// //   };

// //   return (

// //     <div className="data-center-page">

// //       {/* HEADER */}

// //       <div className="dc-header">

// //         <h1>Data Center</h1>

// //         <button
// //           className="connect-btn"
// //           onClick={() => setShowModal(true)}
// //         >
// //           Connect
// //         </button>

// //       </div>

// //       <h2 className="section-title">
// //         Connected Connectors
// //       </h2>


// //       {/* LIST */}

// //       {connectors.length === 0 ? (

// //         <div className="empty-state">

// //           <h3>
// //             No Connectors Found
// //           </h3>

// //           <p>
// //             Create your first connector
// //             to start collecting data.
// //           </p>

// //         </div>

// //       ) : (





  
       

// //         <div className="connector-list">

// //           {connectors.map((connector) => (

// //             <div
// //               key={connector.connector_id}
// //               className="connector-card"
// //             >
              

// //               <div className="connector-top">

// //                 <div className="connector-title">

// //                   <span className="connector-icon">

// //                     {getPlatformIcon(
// //                       connector.connector_type
// //                     )}

// //                   </span>

// //                   {connector.connector_name}

// //                 </div>

// //                 <div className="connector-settings">

// //                   <button
// //                     className="gear-button"
// //                     onClick={() =>
// //                       setMenuOpen(
// //                         menuOpen === connector.connector_id
// //                           ? null
// //                           : connector.connector_id
// //                       )
// //                     }
// //                   >
// //                     <FaCog />
// //                   </button>

// //                   {menuOpen === connector.connector_id && (

// //                     <div className="dropdown-menu">

// //                       <button>
// //                         ▶ Run Now
// //                       </button>

// //                       <button
// //                         onClick={() => {

// //                           setEditConnector(
// //                             connector
// //                           );

// //                           setSelectedType(
// //                             connector.connector_type
// //                           );

// //                           setShowForm(
// //                             true
// //                           );

// //                           setMenuOpen(
// //                             null
// //                           );

// //                         }}
// //                       >
// //                         ✏ Edit
// //                       </button>

// //                       <button>
// //                         🗑 Delete
// //                       </button>

// //                     </div>

// //                   )}

// //                 </div>

// //               </div>

// //               <div className="connector-bottom">

// //                 <span>
// //                   Type:
// //                   {" "}
// //                   {connector.connector_type}
// //                 </span>

// //                 <span>
// //                   Schedule:
// //                   {" "}
// //                   {connector.schedule || "Manual"}
// //                 </span>

// //                 <span>
// //                   Last Run:
// //                   {" "}
// //                   {connector.last_run || "Never"}
// //                 </span>

// //               </div>

// //             </div>

// //           ))}

// //         </div>

          















            

    

// //       )}

// //       {/* CONNECTOR TYPE MODAL */}

// //       <ConnectorModal

// //         isOpen={showModal}

// //         onClose={() =>
// //           setShowModal(false)
// //         }

// //         onSelect={(
// //           connectorType
// //         ) => {

// //           setSelectedType(
// //             connectorType
// //           );

// //           setEditConnector(
// //             null
// //           );

// //           setShowModal(
// //             false
// //           );

// //           setShowForm(
// //             true
// //           );

// //         }}
// //       />

// //       {/* CREATE / EDIT */}

// //       <ConnectorFormModal

// //         isOpen={showForm}

// //         connectorType={
// //           selectedType
// //         }

// //         editConnector={
// //           editConnector
// //         }

// //         onClose={() => {

// //           setShowForm(
// //             false
// //           );

// //           setEditConnector(
// //             null
// //           );

// //           setSelectedType(
// //             null
// //           );

// //         }}

// //         onSuccess={() => {

// //           loadConnectors();

// //         }}
// //       />

// //     </div>

// //   );

// // }

// // export default DataCenter;













































// import {
//   useEffect,
//   useState,
//   useRef
// } from "react";
// import { FaCog } from "react-icons/fa";
// import {
//   FaInstagram,
//   FaYoutube,
//   FaReddit,
//   FaRss,
//   FaNewspaper,
//   FaGoogle
// } from "react-icons/fa";
// import api from "../services/api";
// import "../styles/DataCenter.css";

// import ConnectorModal from "../components/connectors/ConnectorModal";
// import ConnectorFormModal from "../components/connectors/ConnectorFormModal";

  
// function DataCenter() {
//   // const menuRef = useRef(null);
//   const [connectors, setConnectors] = useState([]);
//   const [showModal, setShowModal] = useState(false);
//   const [showForm, setShowForm] = useState(false);
//   const [selectedType, setSelectedType] = useState(null);
//   const [editConnector, setEditConnector] = useState(null);
//   const [menuOpen, setMenuOpen] = useState(null);

//   const loadConnectors = async () => {
//     try {
//       const response = await api.get(
//         "/connectors/connectors"
//       );

//       setConnectors(
//         response.data || []
//       );
//     } catch (error) {
//       console.error(
//         "Failed to load connectors",
//         error
//       );
//     }
//   };

//   useEffect(() => {
//     loadConnectors();
//   }, []);
//   // useEffect(() => {

//   // const handleClickOutside = (
//   //   event
//   // ) => {

//   //   if (
//   //     menuRef.current &&
//   //     !menuRef.current.contains(
//   //       event.target
//   //     )
//   //   ) {
//   //     setMenuOpen(null);
//   //   }

//   // };

// //   document.addEventListener(
// //     "mousedown",
// //     handleClickOutside
// //   );

// //   return () => {

// //     document.removeEventListener(
// //       "mousedown",
// //       handleClickOutside
// //     );

// //   };

// // }, []);

//   const getPlatformIcon = (
//     connectorType
//   ) => {

//     const type = String(
//       connectorType || ""
//     ).toLowerCase();

//     if (
//       type.includes("instagram")
//     ) {
//       return (
//         <FaInstagram
//           color="#E4405F"
//         />
//       );
//     }

//     if (
//       type.includes("youtube")
//     ) {
//       return (
//         <FaYoutube
//           color="#FF0000"
//         />
//       );
//     }

//     if (
//       type.includes("reddit")
//     ) {
//       return (
//         <FaReddit
//           color="#FF4500"
//         />
//       );
//     }

//     if (
//       type.includes("news")
//     ) {
//       return (
//         <FaNewspaper
//           color="#2563eb"
//         />
//       );
//     }

//     if (
//       type.includes("rss")
//     ) {
//       return (
//         <FaRss
//           color="#f97316"
//         />
//       );
//     }

//     if (
//       type.includes("google")
//     ) {
//       return (
//         <FaGoogle
//           color="#4285F4"
//         />
//       );
//     }

//     return "🔗";
//   };

//   return (
//     <div className="data-center-page">
//       {/* HEADER */}

//       <div className="dc-header">
//         <h1>Data Center</h1>

//         <button
//           className="connect-btn"
//           onClick={() =>
//             setShowModal(true)
//           }
//         >
//           Connect
//         </button>
//       </div>

//       {/* LIST */}

//       {connectors.length === 0 ? (
//         <div className="empty-state">
//           <h3>
//             No Connectors Found
//           </h3>

//           <p>
//             Create your first connector
//             to start collecting data.
//           </p>
//         </div>
//       ) : (
//         <div className="connector-list">
//           {connectors.map(
//             (connector) => (
//               <div
//                 key={
//                   connector.connector_id
//                 }
//                 className="connector-card"
//               >
//                 {/* LEFT SIDE */}

//                 <div className="connector-content">
//                   <div className="connector-title">
//                     <span className="connector-icon">
//                       {getPlatformIcon(
//                         connector.connector_type
//                       )}
//                     </span>

//                     <span>
//                       {
//                         connector.connector_name
//                       }
//                     </span>
//                   </div>

//                   <div className="connector-bottom">
//                     <span>
//                       Type:{" "}
//                       {
//                         connector.connector_type
//                       }
//                     </span>

//                     <span>
//                       Schedule:{" "}
//                       {connector.schedule ||
//                         "Manual"}
//                     </span>

//                     <span>
//                       Last Run:{" "}
//                       {connector.last_run ||
//                         "Never"}
//                     </span>
//                   </div>
//                 </div>

//                 {/* RIGHT SIDE */}
//                 {/* RIGHT SIDE */}

//                 <div className="connector-settings">

//                   <button
//                     className="gear-button"
//                     onClick={() =>
//                       setMenuOpen(
//                         menuOpen === connector.connector_id
//                           ? null
//                           : connector.connector_id
//                       )
//                     }
//                   >
//                     <FaCog />
//                   </button>

//                   {menuOpen === connector.connector_id && (

//                     <div className="dropdown-menu">

//                       <button
//                         onClick={() => {

//                           console.log(
//                             "Run:",
//                             connector.connector_id
//                           );

//                           setMenuOpen(null);

//                         }}
//                       >
//                         Run Now
//                       </button>

//                       <button
//                         onClick={() => {

//                           console.log(
//                             "Edit:",
//                             connector
//                           );

//                           setEditConnector(
//                             connector
//                           );

//                           setSelectedType(
//                             connector.connector_type
//                           );

//                           setShowForm(true);

//                           setMenuOpen(null);

//                         }}
//                       >
//                         Edit
//                       </button>

//                       <button
//                         onClick={() => {

//                           if (
//                             !window.confirm(
//                               `Delete ${connector.connector_name}?`
//                             )
//                           ) {
//                             return;
//                           }

//                           console.log(
//                             "Delete:",
//                             connector.connector_id
//                           );

//                           setMenuOpen(null);

//                         }}
//                       >
//                         Delete
//                       </button>

//                     </div>

//                   )}

//                 </div>

//                 </div>









//       {/* CONNECTOR TYPE MODAL */}

//       <ConnectorModal
//         isOpen={showModal}
//         onClose={() =>
//           setShowModal(false)
//         }
//         onSelect={(
//           connectorType
//         ) => {
//           setSelectedType(
//             connectorType
//           );

//           setEditConnector(null);

//           setShowModal(false);

//           setShowForm(true);
//         }}
//       />

//       {/* FORM MODAL */}

//       <ConnectorFormModal
//         isOpen={showForm}
//         connectorType={selectedType}
//         editConnector={editConnector}
//         onClose={() => {
//           setShowForm(false);

//           setEditConnector(null);

//           setSelectedType(null);
//         }}
//         onSuccess={() => {
//           loadConnectors();
//         }}
//       />
//     </div>
//   );
// }

// export default DataCenter;





















import {
  useEffect,
  useState,
  useRef
} from "react";

import { FaCog } from "react-icons/fa";

import {
  FaInstagram,
  FaYoutube,
  FaReddit,
  FaRss,
  FaNewspaper,
  FaGoogle
} from "react-icons/fa";
import ConnectorHistoryModal from "../components/ConnectorHistoryModal";
import api from "../services/api";
import "../styles/DataCenter.css";
import ConnectorModal from "../components/connectors/ConnectorModal";
import ConnectorFormModal from "../components/connectors/ConnectorFormModal";
import {
  runConnector,
  deleteConnector
} from "../services/connectorService";
function DataCenter() {
  const dropdownRef = useRef(null);

  const [connectors, setConnectors] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [selectedType, setSelectedType] = useState(null);
  const [editConnector, setEditConnector] = useState(null);
  const [menuOpen, setMenuOpen] = useState(null);
  const [
    showHistory,
    setShowHistory
  ] = useState(false);

  const [
    selectedConnector,
    setSelectedConnector
  ] = useState(null);

  const loadConnectors = async () => {

    try {

      const response = await api.get(
        "/connectors/connectors"
      );

      setConnectors(
        response.data || []
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
  useEffect(() => {

  const handleClickOutside = (
      event
    ) => {

      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(
          event.target
        )
      ) {
        setMenuOpen(null);
      }

    };

    document.addEventListener(
      "mousedown",
      handleClickOutside
    );

    return () => {

      document.removeEventListener(
        "mousedown",
        handleClickOutside
      );

    };

  }, []);

  const getPlatformIcon = (
    connectorType
  ) => {

    const type = String(
      connectorType || ""
    ).toLowerCase();

    if (
      type.includes("instagram")
    ) {
      return (
        <FaInstagram
          color="#E4405F"
        />
      );
    }

    if (
      type.includes("youtube")
    ) {
      return (
        <FaYoutube
          color="#FF0000"
        />
      );
    }

    if (
      type.includes("reddit")
    ) {
      return (
        <FaReddit
          color="#FF4500"
        />
      );
    }

    if (
      type.includes("news")
    ) {
      return (
        <FaNewspaper
          color="#2563eb"
        />
      );
    }

    if (
      type.includes("rss")
    ) {
      return (
        <FaRss
          color="#f97316"
        />
      );
    }

    if (
      type.includes("google")
    ) {
      return (
        <FaGoogle
          color="#4285F4"
        />
      );
    }

    return "🔗";
  };

  return (

    <div className="data-center-page">

      {/* HEADER */}

      <div className="dc-header">

        <h1>Data Center</h1>

        <button
          className="connect-btn"
          onClick={() =>
            setShowModal(true)
          }
        >
          Connect
        </button>

      </div>

      {/* LIST */}

      {connectors.length === 0 ? (

        <div className="empty-state">

          <h3>
            No Connectors Found
          </h3>

          <p>
            Create your first connector
            to start collecting data.
          </p>

        </div>

      ) : (

        <div className="connector-list">

          {connectors.map(
            (connector) => (

              <div
                key={
                  connector.connector_id
                }
                className="connector-card"
                onClick={() => {

                  setSelectedConnector(
                    connector
                  );

                  setShowHistory(
                    true
                  );

                }}
              >

                {/* LEFT SIDE */}

                <div className="connector-content">

                  <div className="connector-title">

                    <span className="connector-icon">

                      {getPlatformIcon(
                        connector.connector_type
                      )}

                    </span>

                    <span>

                      {
                        connector.connector_name
                      }

                    </span>

                  </div>

                  <div className="connector-bottom">

                    <span>
                      Type:{" "}
                      {
                        connector.connector_type
                      }
                    </span>

                    <span>
                      Schedule:{" "}
                      {
                        connector.schedule ||
                        "Manual"
                      }
                    </span>

                    <span>
                      Last Run:{" "}
                      {
                        connector.last_run ||
                        "Never"
                      }
                    </span>

                  </div>

                </div>

                {/* RIGHT SIDE */}

                <div
                  className="connector-settings"
                  ref={
                    menuOpen === connector.connector_id
                      ? dropdownRef
                      : null
                  }
                >

                  <button
                    className="gear-button"
                    onClick={(e) => {

                      e.stopPropagation();

                      setMenuOpen(
                        menuOpen ===
                          connector.connector_id
                          ? null
                          : connector.connector_id
                      );

                    }}
                  >
                    <FaCog />
                  </button>

                  {menuOpen ===
                    connector.connector_id && (

                    <div className="dropdown-menu" onClick={(e) => e.stopPropagation() }>


                      <button
                          onClick={async (e) => {

                            e.stopPropagation();

                            setMenuOpen(null);

                          setMenuOpen(null);

                          try {

                            const response =
                              await runConnector(
                                connector.connector_id
                              );

                            console.log(
                              "RUN RESPONSE:",
                              response.data
                            );

                            if (
                              response.data.status ===
                              "success"
                            ) {

                              alert(
                                "Connector executed successfully"
                              );

                            } else {

                              alert(
                                `Failed: ${
                                  response.data.message
                                }`
                              );

                            }

                            loadConnectors();

                          } catch (error) {

                            console.error(
                              error
                            );

                            alert(
                              "Run Failed"
                            );

                          }

                        }}
                      >
                        Run Now
                      </button>

                      <button
                          onClick={(e) => {

                            e.stopPropagation();

                            console.log(
                              "Edit:",
                              connector
                            );

                          setEditConnector(
                            connector
                          );

                          setSelectedType(
                            connector.connector_type
                          );

                          setShowForm(
                            true
                          );

                          setMenuOpen(
                            null
                          );

                        }}
                      >
                        Edit
                      </button>

     
                      <button
                    
                          onClick={async () => {

                            setMenuOpen(null);

                            const confirmed =
                              window.confirm(
                                `Delete ${connector.connector_name}?`
                              );

                            if (!confirmed)
                              return;

                            try {

                              await deleteConnector(
                                connector.connector_id
                              );

                              loadConnectors();

                            } catch (error) {

                              console.error(error);

                              alert(
                                "Delete Failed"
                              );

                            }

                          }}
                        >
                          Delete
                        </button>

                    </div>

                  )}

                </div>

              </div>

            )
          )}

        </div>

      )}

      {/* CONNECTOR TYPE MODAL */}

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

      {/* FORM MODAL */}

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
      <ConnectorHistoryModal

        isOpen={
          showHistory
        }

        connector={
          selectedConnector
        }

        onClose={() =>
          setShowHistory(false)
        }

      />

    </div>

  );

}

export default DataCenter;