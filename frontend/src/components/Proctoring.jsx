import { useEffect, useRef, useState } from "react";

function Proctoring() {
  const videoRef = useRef(null);

  const [warning, setWarning] =
    useState("");

  useEffect(() => {
    startVideo();
  }, []);

  const startVideo = async () => {
    try {
      const stream =
        await navigator.mediaDevices.getUserMedia({
          video: true,
        });

      videoRef.current.srcObject = stream;
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <div
      style={{
        marginTop: "30px",
      }}
    >
      <h2>📷 Proctoring</h2>

      <video
        ref={videoRef}
        autoPlay
        muted
        width="300"
        height="220"
        style={{
          borderRadius: "10px",
        }}
      />

      {warning && (
        <h3 style={{ color: "red" }}>
          {warning}
        </h3>
      )}
    </div>
  );
}

export default Proctoring;