import { useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../api";
import "../App.css";

function UploadResume() {

  const navigate = useNavigate();

  const [file, setFile] = useState(null);

  const uploadResume = async () => {

    if (!file) {
      alert("Please select a PDF file");
      return;
    }

    const formData = new FormData();

    formData.append("file", file);

    try {

      await API.post(
        "/upload-resume",
        formData,
        {
          headers: {
            "Content-Type":
              "multipart/form-data"
          }
        }
      );

      alert(
        "Resume uploaded successfully"
      );

      navigate("/");

    } catch (error) {

      console.log(error);

      alert(
        "Resume upload failed"
      );
    }
  };

  return (

    <div className="container">

      <h1>
        📄 Upload Resume
      </h1>

      <input
        type="file"
        accept=".pdf"
        onChange={(e) =>
          setFile(e.target.files[0])
        }
      />

      <br /><br />

      <button
        onClick={uploadResume}
      >
        Upload Resume
      </button>

    </div>

  );
}

export default UploadResume;