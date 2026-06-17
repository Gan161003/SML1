// // import { useEffect, useState } from "react";
// // import api from "../services/api";

// // function ConnectorHistoryModal({
// //   isOpen,
// //   connector,
// //   onClose
// // }) {

// //   const [history, setHistory] =
// //     useState([]);

// //   useEffect(() => {

// //     if (
// //       !isOpen ||
// //       !connector
// //     ) {
// //       return;
// //     }

// //     loadHistory();

// //   }, [
// //     isOpen,
// //     connector
// //   ]);

// //   const loadHistory = async () => {

// //     try {

// //       const response =
// //         await api.get(
// //           `/connectors/connectors/${connector.connector_id}/history`
// //         );

// //       setHistory(
// //         response.data || []
// //       );

// //     } catch (error) {

// //       console.error(error);

// //     }

// //   };

// //   if (
// //     !isOpen ||
// //     !connector
// //   ) {
// //     return null;
// //   }

// //   return (

// //     <div className="history-overlay">

// //       <div className="history-modal">

// //         <div className="history-header">

// //           <h2>History</h2>

// //           <button
// //             onClick={onClose}
// //           >
// //             ✕
// //           </button>

// //         </div>

// //         <table className="history-table">

// //           <thead>

// //             <tr>

// //               <th>Name</th>

// //               <th>Run Time</th>

// //               <th>Status</th>

// //             </tr>

// //           </thead>

// //           <tbody>

// //             {history.map(
// //               (
// //                 item,
// //                 index
// //               ) => (

// //                 <tr
// //                   key={index}
// //                 >

// //                   <td>
// //                     {
// //                       item.connector_name
// //                     }
// //                   </td>

// //                   <td>
// //                     {
// //                       item.run_time
// //                     }
// //                   </td>

// //                   <td>
// //                     {
// //                       item.status
// //                     }
// //                   </td>

// //                 </tr>

// //               )
// //             )}

// //           </tbody>

// //         </table>

// //       </div>

// //     </div>

// //   );

// // }

// // export default ConnectorHistoryModal;





// import { useEffect, useState } from "react";
// import api from "../services/api";
// import "../styles/ConnectorHistoryModal.css";

// function ConnectorHistoryModal({
//   isOpen,
//   connector,
//   onClose
// }) {

//   const [history, setHistory] =
//     useState([]);

//   useEffect(() => {

//     if (
//       !isOpen ||
//       !connector
//     ) {
//       return;
//     }

//     loadHistory();

//   }, [
//     isOpen,
//     connector
//   ]);

//   const loadHistory = async () => {

//     try {

//       const response =
//         await api.get(
//           `/connectors/connectors/${connector.connector_id}/history`
//         );

//       setHistory(
//         response.data || []
//       );

//     } catch (error) {

//       console.error(error);

//     }

//   };

//   if (
//     !isOpen ||
//     !connector
//   ) {
//     return null;
//   }

//   return (

//     <div
//       className="history-overlay"
//       onClick={onClose}
//     >

//       <div
//         className="history-modal"
//         onClick={(e) =>
//           e.stopPropagation()
//         }
//       >

//         <div className="history-header">

//           <h2>
//             {connector.connector_name}
//             {" "}
//             History
//           </h2>

//           <button
//             className="close-btn"
//             onClick={onClose}
//           >
//             ✕
//           </button>

//         </div>

//         <table className="history-table">

//           <thead>

//             <tr>

//               <th>Name</th>

//               <th>Run Time</th>

//               <th>Status</th>

//             </tr>

//           </thead>

//           <tbody>

//             {history.length > 0 ? (

//               history.map(
//                 (
//                   item,
//                   index
//                 ) => (

//                   <tr key={index}>

//                     <td>
//                       {
//                         item.connector_name
//                       }
//                     </td>

//                     <td>
//                       {
//                         item.run_time
//                       }
//                     </td>

//                     <td
//                       className={
//                         String(
//                           item.status
//                         )
//                         .toLowerCase()
//                         .includes(
//                           "failed"
//                         )
//                           ? "failed-status"
//                           : "success-status"
//                       }
//                     >
//                       {
//                         item.status
//                       }
//                     </td>

//                   </tr>

//                 )
//               )

//             ) : (

//               <tr>

//                 <td
//                   colSpan="3"
//                   className="no-history"
//                 >
//                   No History Found
//                 </td>

//               </tr>

//             )}

//           </tbody>

//         </table>

//       </div>

//     </div>

//   );

// }

// export default ConnectorHistoryModal;




















import { useEffect, useState } from "react";
import api from "../services/api";
import "../styles/ConnectorHistoryModal.css";

function ConnectorHistoryModal({
  isOpen,
  connector,
  onClose
}) {

  const [history, setHistory] =
    useState([]);

  useEffect(() => {

    if (
      !isOpen ||
      !connector
    ) {
      return;
    }

    loadHistory();

  }, [
    isOpen,
    connector
  ]);

  const loadHistory = async () => {

    try {

      const response =
        await api.get(
          `/connectors/connectors/${connector.connector_id}/history`
        );

      setHistory(
        response.data || []
      );

    } catch (error) {

      console.error(error);

    }

  };

  if (
    !isOpen ||
    !connector
  ) {
    return null;
  }

  return (

    <div
      className="history-overlay"
      onClick={onClose}
    >

      <div
        className="history-modal"
        onClick={(e) =>
          e.stopPropagation()
        }
      >

        <div className="history-header">

          <h2>
            {connector.connector_name}
            {" "}
            History
          </h2>

          <button
            className="history-close"
            onClick={onClose}
          >
            ✕
          </button>

        </div>

        <div className="history-table-wrapper">

          <table className="history-table">

            <thead>

              <tr>

                <th>Name</th>

                <th>Run Time</th>

                <th>Status</th>

              </tr>

            </thead>

            <tbody>

              {history.length === 0 ? (

                <tr>

                  <td
                    colSpan="3"
                    className="no-history"
                  >
                    No History Found
                  </td>

                </tr>

              ) : (

                history.map(
                  (
                    item,
                    index
                  ) => (

                    <tr
                      key={index}
                    >

                      <td>
                        {
                          item.connector_name
                        }
                      </td>

                      <td>
                        {
                          item.run_time
                        }
                      </td>

                      <td>

                        <span
                          className={
                            item.status
                              ?.toLowerCase()
                              .includes(
                                "failed"
                              )
                              ? "status-failed"
                              : "status-success"
                          }
                          title={
                            item.status
                          }
                        >
                          {
                            item.status
                          }
                        </span>

                      </td>

                    </tr>

                  )
                )

              )}

            </tbody>

          </table>

        </div>

      </div>

    </div>

  );

}

export default ConnectorHistoryModal;