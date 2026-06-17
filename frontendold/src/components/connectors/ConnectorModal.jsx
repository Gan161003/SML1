// // function ConnectorModal({
// //   isOpen,
// //   onClose,
// //   onSelect
// // }) {

// //   if (!isOpen) return null;

// //   const connectors = [
// //     "reddit",
// //     "youtube",
// //     "instagram",
// //     "newsapi",
// //     "googlenews",
// //     "campaignindia"
// //   ];

// //   return (
// //     <div
// //       style={{
// //         position: "fixed",
// //         top: 0,
// //         left: 0,
// //         width: "100%",
// //         height: "100%",
// //         background: "rgba(0,0,0,0.5)",
// //         display: "flex",
// //         justifyContent: "center",
// //         alignItems: "center",
// //         zIndex: 1000
// //       }}
// //     >
// //       <div
// //         style={{
// //           background: "#fff",
// //           width: "700px",
// //           padding: "30px",
// //           borderRadius: "10px"
// //         }}
// //       >
// //         <h2>Select Connector</h2>

// //         <div
// //           style={{
// //             display: "grid",
// //             gridTemplateColumns: "repeat(3, 1fr)",
// //             gap: "15px",
// //             marginTop: "20px"
// //           }}
// //         >
// //           {connectors.map((connector) => (
// //             <button
// //               key={connector}
// //               onClick={() => onSelect(connector)}
// //               style={{
// //                 padding: "20px",
// //                 cursor: "pointer"
// //               }}
// //             >
// //               {connector}
// //             </button>
// //           ))}
// //         </div>

// //         <button
// //           onClick={onClose}
// //           style={{
// //             marginTop: "20px",
// //             padding: "10px 20px"
// //           }}
// //         >
// //           Close
// //         </button>

// //       </div>
// //     </div>
// //   );
// // }

// // export default ConnectorModal;














// function ConnectorModal({
//   isOpen,
//   onClose,
//   onSelect
// }) {

//   if (!isOpen) return null;

//   const connectors = [

//   "youtube",

//   "reddit",

//   "instagram_account",

//   "instagram_hashtag",

//   "newsapi",

//   "googlenews",

//   "campaignindia",

//   "rss_reviews"

// ];

//   return (
//     <div
//       style={{
//         position: "fixed",
//         top: 0,
//         left: 0,
//         width: "100%",
//         height: "100%",
//         background: "rgba(0,0,0,0.5)",
//         display: "flex",
//         justifyContent: "center",
//         alignItems: "center",
//         zIndex: 1000
//       }}
//     >
//       <div
//         style={{
//           background: "#fff",
//           width: "700px",
//           padding: "30px",
//           borderRadius: "10px"
//         }}
//       >
//         <h2>Select Connector</h2>

//         <div
//           style={{
//             display: "grid",
//             gridTemplateColumns: "repeat(3, 1fr)",
//             gap: "15px",
//             marginTop: "20px"
//           }}
//         >
//           {connectors.map((connector) => (
//             <button
//               key={connector}
//               onClick={() => onSelect(connector)}
//               style={{
//                 padding: "20px",
//                 cursor: "pointer"
//               }}
//             >
//               {connector}
//             </button>
//           ))}
//         </div>

//         <button
//           onClick={onClose}
//           style={{
//             marginTop: "20px",
//             padding: "10px 20px"
//           }}
//         >
//           Close
//         </button>

//       </div>
//     </div>
//   );
// }

// export default ConnectorModal;












import {
  FaInstagram,
  FaYoutube,
  FaReddit,
  FaRss,
  FaNewspaper,
  FaGoogle
} from "react-icons/fa";

const getPlatformIcon = (type) => {

  const connector =
    String(type || "")
      .toLowerCase();

  if (
    connector.includes("instagram")
  ) {
    return (
      <FaInstagram
        color="#E4405F"
      />
    );
  }

  if (
    connector.includes("youtube")
  ) {
    return (
      <FaYoutube
        color="#FF0000"
      />
    );
  }

  if (
    connector.includes("reddit")
  ) {
    return (
      <FaReddit
        color="#FF4500"
      />
    );
  }

  if (
    connector.includes("rss")
  ) {
    return (
      <FaRss
        color="#F97316"
      />
    );
  }

  if (
    connector.includes("news")
  ) {
    return (
      <FaNewspaper
        color="#2563EB"
      />
    );
  }

  if (
    connector.includes("google")
  ) {
    return (
      <FaGoogle
        color="#4285F4"
      />
    );
  }

  return "🔗";
};

function ConnectorModal({
  isOpen,
  onClose,
  onSelect
}) {

  if (!isOpen) return null;

  const connectors = [

    "youtube",

    "reddit",

    "instagram_account",

    "instagram_hashtag",

    "newsapi",

    "googlenews",

    "campaignindia",

    "rss_reviews"

  ];

  return (

    <div
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        width: "100%",
        height: "100%",
        background:
          "rgba(0,0,0,0.5)",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        zIndex: 1000
      }}
    >

      <div
        style={{
          background: "#fff",
          width: "750px",
          padding: "30px",
          borderRadius: "12px",
          boxShadow:
            "0 10px 30px rgba(0,0,0,0.15)"
        }}
      >

        <h2
          style={{
            margin: 0,
            marginBottom: "20px"
          }}
        >
          Select Connector
        </h2>

        <div
          style={{
            display: "grid",
            gridTemplateColumns:
              "repeat(2, 1fr)",
            gap: "15px"
          }}
        >

          {connectors.map(
            (connector) => (

              <button
                key={connector}
                onClick={() =>
                  onSelect(
                    connector
                  )
                }
                style={{
                  display: "flex",
                  alignItems:
                    "center",

                  gap: "12px",

                  padding: "16px",

                  border:
                    "1px solid #e5e7eb",

                  borderRadius:
                    "10px",

                  background:
                    "#fff",

                  cursor:
                    "pointer",

                  textAlign:
                    "left",

                  fontSize:
                    "14px",

                  fontWeight:
                    "500"
                }}
              >

                <span
                  style={{
                    width:
                      "36px",

                    height:
                      "36px",

                    display:
                      "flex",

                    alignItems:
                      "center",

                    justifyContent:
                      "center",

                    fontSize:
                      "22px",

                    flexShrink:
                      0
                  }}
                >
                  {getPlatformIcon(
                    connector
                  )}
                </span>

                <span>
                  {connector
                    .replaceAll(
                      "_",
                      " "
                    )
                    .replace(
                      /\b\w/g,
                      (char) =>
                        char.toUpperCase()
                    )}
                </span>

              </button>

            )
          )}

        </div>

        <div
          style={{
            display: "flex",
            justifyContent:
              "flex-end",

            marginTop:
              "20px"
          }}
        >

          <button
            onClick={onClose}
            style={{
              padding:
                "10px 20px",

              border:
                "none",

              borderRadius:
                "8px",

              background:
                "#1d2d50",

              color:
                "white",

              cursor:
                "pointer"
            }}
          >
            Close
          </button>

        </div>

      </div>

    </div>

  );

}

export default ConnectorModal;