import React from "react";

export default function DummyUI() {
  const imageUrl =
    "https://www.pulsarplatform.com/wp-content/uploads/2023/08/sentiment-analysis-img-3-1024x710.png";

  return (
    <img
      src={imageUrl}
      alt="UI Mockup"
      style={{
        width: "100%",
        height: "calc(100vh - 64px)", // subtract header height
        objectFit: "cover",
        display: "block",
      }}
    />
  );
}

