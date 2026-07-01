import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../api";
import "../App.css";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

function Dashboard() {
  const navigate = useNavigate();

  const [results, setResults] = useState(null);
  const [history, setHistory] = useState([]);
  const [jdResult, setJdResult] = useState(null);
  const [analysis, setAnalysis] = useState(null);

  // NEW STATE
  const [resumeAnalysis, setResumeAnalysis] =
    useState(null);

  const [resumes, setResumes] = useState([]);
  const [selectedResume, setSelectedResume] =
    useState("");
  const [jobDescription, setJobDescription] =
    useState("");

  useEffect(() => {
    loadData();
  }, []);

  const logout = () => {
    localStorage.removeItem("token");
    window.location.href = "/login";
  };

  const loadData = async () => {
    try {
      // Load interview history
      const historyRes = await API.get("/interviews");
      setHistory(historyRes.data);

      // Load resumes
      const resumeRes = await API.get("/resumes");

console.log(
  "Resume API Response:",
  resumeRes.data
);

setResumes(resumeRes.data);

// NEW USER CHECK
if (resumeRes.data.length === 0) {
  alert(
    "No resume found. Please upload a resume first."
  );

  navigate("/upload-resume");
  return;
}

// Auto select first resume
const firstResumeId = resumeRes.data[0].id;

setSelectedResume(
  String(firstResumeId)
);

try {
  const analysisRes = await API.get(
    `/resume-analysis/${firstResumeId}`
  );

  setResumeAnalysis(
    analysisRes.data
  );
} catch (err) {
  console.log(err);
}

      // Latest interview result
      if (historyRes.data.length > 0) {
        const latestInterview =
          historyRes.data[
            historyRes.data.length - 1
          ];

        const interviewRes = await API.get(
          `/interview/${latestInterview.interview_id}/results`
        );

        setResults(interviewRes.data);

        try {
          const analysisRes =
            await API.get(
              `/interview/${latestInterview.interview_id}/weakness-analysis`
            );

          setAnalysis(
            analysisRes.data
          );

        } catch (err) {
          console.log(err);
        }
      }

    } catch (error) {
      console.log(error);
    }
  };

  const startInterview = async () => {
    if (!selectedResume) {
      alert("Please select a resume");
      return;
    }

    try {
      const response = await API.post(
        `/start-interview/${selectedResume}`
      );

      navigate(
        `/interview/${response.data.interview_id}`
      );

    } catch (error) {
      console.log(error);
      alert("Failed to start interview");
    }
  };

  const matchJD = async () => {

    if (!selectedResume) {
      alert("Please select a resume");
      return;
    }
  
    if (!jobDescription.trim()) {
      alert("Please enter Job Description");
      return;
    }
  
    try {
  
      const res = await API.post(
        "/match-jd",
        {
          resume_id: Number(selectedResume),
          job_description: jobDescription
        }
      );
  
      console.log(
        "JD Match Response:",
        res.data
      );
  
      setJdResult(res.data);
  
    } catch (err) {
  
      console.log(
        "JD Match Error:",
        err
      );
  
      if (err.response) {
        console.log(
          "Backend Error:",
          err.response.data
        );
      }
  
      alert("JD Matching Failed");
    }
  };

  const chartData = history.map(
    (item) => ({
      interview: `#${item.interview_id}`,
      score: item.average_score * 10,
    })
  );

  return (
    <div className="container">

      {/* Header */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <h1 className="title">
          🚀 InterviewAI Dashboard
        </h1>

        <button onClick={logout}>
          Logout
        </button>
      </div>

      {/* Score Cards */}
      {results && (
        <div className="cards">

          <div className="card">
            <h3>Overall Score</h3>
            <h2>{results.overall_score}%</h2>
          </div>

          <div className="card">
            <h3>Average Score</h3>
            <h2>{results.average_score}</h2>
          </div>

          <div className="card">
            <h3>Answered</h3>
            <h2>
              {results.questions_answered}/
              {results.questions_total}
            </h2>
          </div>

          {jdResult && (
            <div className="card">
              <h3>JD Match Score</h3>
              <h2>{jdResult.match_score}%</h2>
            </div>
          )}

        </div>
      )}

      {/* Resume + JD */}
      <div
  style={{
    textAlign: "center",
    marginTop: "30px",
    marginBottom: "30px"
  }}
>

  <button
    onClick={() =>
      navigate("/upload-resume")
    }

    style={{
      padding: "15px 30px",
      fontSize: "18px",
      borderRadius: "10px",
      cursor: "pointer"
    }}
  >
    📄 Upload New Resume
  </button>

</div>
      <div className="history-section">

        <h2>
          🎯 Resume vs Job Description
        </h2>

        <div className="history-card">

          <h3>Select Resume</h3>

          <select
  value={selectedResume}
  onChange={async (e) => {

    const id = e.target.value;

    setSelectedResume(id);

    try {

      const res = await API.get(
        `/resume-analysis/${id}`
      );

      setResumeAnalysis(
        res.data
      );

    } catch (err) {
      console.log(err);
    }
  }}
  style={{
    width: "100%",
    padding: "12px",
    borderRadius: "10px",
    marginBottom: "20px",
  }}
>

            <option value="">
              Select Resume
            </option>

            {resumes.map((resume) => (
              <option
                key={resume.id}
                value={String(resume.id)}
              >
                {resume.filename}
              </option>
            ))}

          </select>

          <p>
            Selected Resume ID:
            {" "}
            {selectedResume}
          </p>

          <textarea
            rows="6"
            placeholder="Paste Job Description here..."
            value={jobDescription}
            onChange={(e) =>
              setJobDescription(
                e.target.value
              )
            }
            style={{
              width: "100%",
              padding: "10px",
              borderRadius: "10px",
            }}
          />

          <br />
          <br />

          <button onClick={matchJD}>
            Analyze JD Match
          </button>

        </div>

      </div>

      {/* JD Results */}
      {jdResult && (
        <div className="history-section">

          <h2>
            🎯 JD Match Analysis
          </h2>

          <div className="history-card">

            <h3>Matching Skills</h3>

            <ul>
              {jdResult.matching_skills?.map(
                (skill, index) => (
                  <li key={index}>
                    {skill}
                  </li>
                )
              )}
            </ul>

          </div>

          <div className="history-card">

            <h3>Missing Skills</h3>

            <ul>
              {jdResult.missing_skills?.map(
                (skill, index) => (
                  <li key={index}>
                    {skill}
                  </li>
                )
              )}
            </ul>

          </div>

        </div>
      )}

{resumeAnalysis && (
  <div className="history-section">

    <h2>
      📄 Resume Analysis
    </h2>

    <div className="history-card">

      <h3>
        Resume Score:
        {" "}
        {resumeAnalysis.resume_score}/100
      </h3>

    </div>

    <div className="history-card">

      <h3>Strengths</h3>

      <ul>
        {resumeAnalysis.strengths?.map(
          (item, index) => (
            <li key={index}>
              {item}
            </li>
          )
        )}
      </ul>

    </div>

    <div className="history-card">

      <h3>Weaknesses</h3>

      <ul>
        {resumeAnalysis.weaknesses?.map(
          (item, index) => (
            <li key={index}>
              {item}
            </li>
          )
        )}
      </ul>

    </div>

    <div className="history-card">

      <h3>Suggestions</h3>

      <ul>
        {resumeAnalysis.suggestions?.map(
          (item, index) => (
            <li key={index}>
              {item}
            </li>
          )
        )}
      </ul>

    </div>

  </div>
)}

      {/* AI Coach */}
      {analysis && (
        <div className="history-section">

          <h2>
            🧠 AI Interview Coach
          </h2>

          <div className="history-card">

            <h3>Weak Topics</h3>

            <ul>
              {analysis.weak_topics?.map(
                (topic, index) => (
                  <li key={index}>
                    {topic}
                  </li>
                )
              )}
            </ul>

          </div>

          <div className="history-card">

            <h3>Strong Topics</h3>

            <ul>
              {analysis.strong_topics?.map(
                (topic, index) => (
                  <li key={index}>
                    {topic}
                  </li>
                )
              )}
            </ul>

          </div>

        </div>
      )}

      {/* Graph */}
      <div className="history-section">

        <h2>📈 Performance Trend</h2>

        <div className="history-card">

          <ResponsiveContainer
            width="100%"
            height={350}
          >
            <LineChart data={chartData}>
              <CartesianGrid
                strokeDasharray="3 3"
              />

              <XAxis dataKey="interview" />

              <YAxis />

              <Tooltip />

              <Line
                type="monotone"
                dataKey="score"
                stroke="#38bdf8"
                strokeWidth={3}
              />
            </LineChart>
          </ResponsiveContainer>

        </div>

      </div>

      {/* History */}
      <div className="history-section">

        <h2>📋 Interview History</h2>

        {history.map((item) => (
          <div
            className="history-card"
            key={item.interview_id}
          >
            <h3>
              Interview #{item.interview_id}
            </h3>

            <p>
              Questions Answered:
              {" "}
              {item.questions_answered}
            </p>

            <p>
              Average Score:
              {" "}
              {item.average_score}
            </p>
          </div>
        ))}

      </div>

      {/* Start Interview */}
      <div
        style={{
          textAlign: "center",
          marginTop: "40px",
        }}
      >
        <button
          onClick={startInterview}
          style={{
            padding: "15px 30px",
            fontSize: "18px",
            borderRadius: "10px",
            cursor: "pointer",
          }}
        >
          Start Mock Interview
        </button>
      </div>

    </div>
  );
}

export default Dashboard;