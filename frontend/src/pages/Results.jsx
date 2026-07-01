import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import jsPDF from "jspdf";
import html2canvas from "html2canvas";
import API from "../api";
import "../App.css";

function Results() {
  const { interviewId } = useParams();

  const [results, setResults] = useState(null);

  useEffect(() => {
    loadResults();
  }, []);

  const loadResults = async () => {
    try {
      const res = await API.get(
        `/interview/${interviewId}/results`
      );

      console.log("Results:", res.data);

      setResults(res.data);

    } catch (err) {
      console.log(err);
      alert("Failed to load results");
    }
  };

  const downloadPDF = async () => {
    const input = document.getElementById("report");

    const canvas = await html2canvas(input);

    const imgData =
      canvas.toDataURL("image/png");

    const pdf = new jsPDF(
      "p",
      "mm",
      "a4"
    );

    const pdfWidth =
      pdf.internal.pageSize.getWidth();

    const pdfHeight =
      (canvas.height * pdfWidth) /
      canvas.width;

    pdf.addImage(
      imgData,
      "PNG",
      0,
      0,
      pdfWidth,
      pdfHeight
    );

    pdf.save(
      "Interview_Report.pdf"
    );
  };

  if (!results) {
    return (
      <div className="container">
        <h2>Loading Results...</h2>
      </div>
    );
  }

  return (
    <div className="container">

      <div id="report">

        <h1>
          🎉 Interview Results
        </h1>

        <div className="cards">

          <div className="card">
            <h3>Overall Score</h3>
            <h2>
              {results.overall_score}%
            </h2>
          </div>

          <div className="card">
            <h3>Average Score</h3>
            <h2>
              {results.average_score}
            </h2>
          </div>

          <div className="card">
            <h3>
              Questions Answered
            </h3>

            <h2>
              {
                results.questions_answered
              }
              /
              {results.questions_total}
            </h2>
          </div>

        </div>

        <div className="history-card">

          <h2>
            📊 Performance Summary
          </h2>

          <p>
            Questions Answered:
            <strong>
              {" "}
              {
                results.questions_answered
              }
            </strong>
          </p>

          <p>
            Average Score:
            <strong>
              {" "}
              {results.average_score}/10
            </strong>
          </p>

          <p>
            Overall Performance:
            <strong>
              {" "}
              {results.overall_score}%
            </strong>
          </p>

        </div>

      </div>

      <br />

      <button
        onClick={downloadPDF}
        style={{
          padding: "12px 25px",
          borderRadius: "10px",
          marginRight: "15px",
          cursor: "pointer",
        }}
      >
        📄 Download PDF Report
      </button>

      <Link to="/">
        <button
          style={{
            padding: "12px 25px",
            borderRadius: "10px",
            cursor: "pointer",
          }}
        >
          Back to Dashboard
        </button>
      </Link>

    </div>
  );
}

export default Results;