

// import { useState } from "react";

// import {
//   createConnector,
//   updateConnector
// } from "../../services/connectorService";

// function ConnectorFormModal({

//   isOpen,

//   connectorType,

//   editConnector,

//   onClose,

//   onSuccess

// }) {

  

//   const [form, setForm] = useState({

//     connector_name:
//       editConnector?.connector_name || "",

//     api_key: "",

//     keywords: "",

//     max_videos: 20,

//     max_comments: 100,

//     refresh_type: "manual",

//     schedule_frequency: "",

//     schedule_start_date: "",

//     schedule_start_time: ""

//   });
//   if (!isOpen) return null;

//   const handleChange = (
//     field,
//     value
//   ) => {

//     setForm({
//       ...form,
//       [field]: value
//     });

//   };

//   const handleSave = async () => {

//     const payload = {

//       connector_type:
//         connectorType,

//       connector_name:
//         form.connector_name,

//       refresh_type:
//         form.refresh_type,

//       schedule_frequency:
//         form.schedule_frequency,

//       schedule_start_date:
//         form.schedule_start_date,

//       schedule_start_time:
//         form.schedule_start_time,

//       config: {

//         api_key:
//           form.api_key,

//         keywords:
//           form.keywords,

//         max_videos:
//           Number(
//             form.max_videos
//           ),

//         max_comments:
//           Number(
//             form.max_comments
//           )

//       }

//     };

//     try {

//       if (editConnector) {

//         await updateConnector(
//           editConnector.connector_id,
//           payload
//         );

//       } else {

//         await createConnector(
//           payload
//         );

//       }

//       onSuccess();

//       onClose();

//     } catch (error) {

//       console.error(error);

//       alert("Save Failed");

//     }

//   };

//   return (

//     <div
//       style={{
//         position: "fixed",
//         inset: 0,
//         background:
//           "rgba(0,0,0,0.5)",
//         display: "flex",
//         justifyContent:
//           "center",
//         alignItems:
//           "center"
//       }}
//     >

//       <div
//         style={{
//           background: "#fff",
//           padding: "30px",
//           width: "700px"
//         }}
//       >

//         <h2>
//           {editConnector
//             ? "Edit Connector"
//             : "Create Connector"}
//         </h2>

//         <input
//           placeholder="Connector Name"
//           value={
//             form.connector_name
//           }
//           onChange={(e) =>
//             handleChange(
//               "connector_name",
//               e.target.value
//             )
//           }
//         />

//         <br />
//         <br />

//         <input
//           placeholder="API Key"
//           value={form.api_key}
//           onChange={(e) =>
//             handleChange(
//               "api_key",
//               e.target.value
//             )
//           }
//         />

//         <br />
//         <br />

//         <input
//           placeholder="Keywords"
//           value={form.keywords}
//           onChange={(e) =>
//             handleChange(
//               "keywords",
//               e.target.value
//             )
//           }
//         />

//         <br />
//         <br />

//         <input
//           type="number"
//           placeholder="Max Videos"
//           value={form.max_videos}
//           onChange={(e) =>
//             handleChange(
//               "max_videos",
//               e.target.value
//             )
//           }
//         />

//         <br />
//         <br />

//         <input
//           type="number"
//           placeholder="Max Comments"
//           value={form.max_comments}
//           onChange={(e) =>
//             handleChange(
//               "max_comments",
//               e.target.value
//             )
//           }
//         />

//         <br />
//         <br />

//         <select
//           value={
//             form.refresh_type
//           }
//           onChange={(e) =>
//             handleChange(
//               "refresh_type",
//               e.target.value
//             )
//           }
//         >

//           <option value="manual">
//             Manual
//           </option>

//           <option value="scheduled">
//             Scheduled
//           </option>

//         </select>

//         {form.refresh_type ===
//           "scheduled" && (
//           <>
//             <br />
//             <br />

//             <input
//               placeholder="daily"
//               value={
//                 form.schedule_frequency
//               }
//               onChange={(e) =>
//                 handleChange(
//                   "schedule_frequency",
//                   e.target.value
//                 )
//               }
//             />

//             <br />
//             <br />

//             <input
//               type="date"
//               onChange={(e) =>
//                 handleChange(
//                   "schedule_start_date",
//                   e.target.value
//                 )
//               }
//             />

//             <br />
//             <br />

//             <input
//               type="time"
//               onChange={(e) =>
//                 handleChange(
//                   "schedule_start_time",
//                   e.target.value
//                 )
//               }
//             />

//           </>
//         )}

//         <br />
//         <br />

//         <button
//           onClick={handleSave}
//         >
//           Save
//         </button>

//         <button
//           onClick={onClose}
//           style={{
//             marginLeft: "10px"
//           }}
//         >
//           Close
//         </button>

//       </div>

//     </div>

//   );

// }

// export default ConnectorFormModal;



















import { useState, useEffect } from "react";
import "../../styles/ConnectorFormModal.css";
import {
  createConnector,
  updateConnector
} from "../../services/connectorService";

import {
  CONNECTOR_CONFIGS
} from "../../config/connectorConfigs";

function ConnectorFormModal({

  isOpen,

  connectorType,

  editConnector,

  onClose,

  onSuccess

}) {

  const [form, setForm] = useState({

    connector_name: "",

    refresh_type: "manual",

    schedule_frequency: "",

    schedule_start_date: "",

    schedule_start_time: ""

  });

  useEffect(() => {

  if (!editConnector) return;

  let config = {};

  try {

    config =
      typeof editConnector.config_json === "string"
        ? JSON.parse(
            editConnector.config_json
          )
        : editConnector.config_json || {};

  } catch {

    config = {};

  }

  setForm({

      connector_name:
        editConnector.connector_name || "",

      refresh_type:
        editConnector.refresh_type || "manual",

      schedule_frequency:
        editConnector.schedule_frequency || "",

      schedule_start_date:
        editConnector.schedule_start_date || "",

      schedule_start_time:
        editConnector.schedule_start_time || "",

      ...config

    });

  }, [editConnector]);

  if (!isOpen) return null;

  const fields =
    CONNECTOR_CONFIGS[
      connectorType
    ] || [];

  const handleChange = (
    field,
    value
  ) => {

    setForm({
      ...form,
      [field]: value
    });

  };

  const handleSave = async () => {

    const config = {};

    fields.forEach((field) => {

      config[field.name] =
        form[field.name];

    });

    const payload = {

      connector_type:
        connectorType,

      connector_name:
        form.connector_name,

      refresh_type:
        form.refresh_type,

      schedule_frequency:
        form.schedule_frequency,

      schedule_start_date:
        form.schedule_start_date,

      schedule_start_time:
        form.schedule_start_time,

      config

    };

    try {

      if (editConnector) {

        await updateConnector(
          editConnector.connector_id,
          payload
        );

      } else {

        await createConnector(
          payload
        );

      }

      onSuccess();

      onClose();

    } catch (error) {

      console.error(error);

      alert("Save Failed");

    }

  };

  return (

  <div className="cfm-overlay">

      <div className="cfm-modal">

        <h2 className="cfm-title">

          {editConnector
            ? "Edit Connector"
            : `Create ${connectorType}`}

        </h2>

        <input
          className="cfm-input"
          placeholder="Connector Name"
          value={
            form.connector_name
          }
          onChange={(e) =>
            handleChange(
              "connector_name",
              e.target.value
            )
          }
          style={{
            width: "100%",
            padding: "10px"
          }}
        />

        <br />
        <br />

        {fields.map((field) => (

          <div
            key={field.name}
          >

            <input
              className="cfm-input"
              type={field.type}
              placeholder={field.label}
              value={
                form[field.name] || ""
              }
              onChange={(e) =>
                handleChange(
                  field.name,
                  e.target.value
                )
              }
            />

            <br />
            <br />

          </div>

        ))}

        <select
          className="cfm-select"
          value={
            form.refresh_type
          }
          onChange={(e) =>
            handleChange(
              "refresh_type",
              e.target.value
            )
          }
        >

          <option value="manual">
            Manual
          </option>

          <option value="scheduled">
            Scheduled
          </option>

        </select>

        <br />
        <br />

        {form.refresh_type ===
          "scheduled" && (

          <>

            <label>
              Frequency
            </label>

            <select
              className="cfm-select"
              value={
                form.schedule_frequency
              }
              onChange={(e) =>
                handleChange(
                  "schedule_frequency",
                  e.target.value
                )
              }
            >
              <option value="">
                Select Frequency
              </option>

              <option value="hourly">
                Hourly
              </option>

              <option value="daily">
                Daily
              </option>

              <option value="weekly">
                Weekly
              </option>

              <option value="monthly">
                Monthly
              </option>
            </select>

            <br />
            <br />

            <input
              className="cfm-input"
              type="date"
              value={
                form.schedule_start_date
              }
              onChange={(e) =>
                handleChange(
                  "schedule_start_date",
                  e.target.value
                )
              }
            />

            <br />
            <br />

            <input
              className="cfm-input"
              type="time"
              value={
                form.schedule_start_time
              }
              onChange={(e) =>
                handleChange(
                  "schedule_start_time",
                  e.target.value
                )
              }
            />

            <br />
            <br />

          </>

        )}

        <div className="cfm-actions">

          <button
            className="cfm-save-btn"
            onClick={handleSave}
          >
            Save
          </button>

          <button
            className="cfm-close-btn"
            onClick={onClose}
          >
            Cancel
          </button>

        </div>

      </div>

    </div>

  );

}

export default ConnectorFormModal;
