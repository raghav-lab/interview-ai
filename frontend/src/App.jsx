import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

function App() {
  const [results, setResults] = useState(null);
  const [history, setHistory] = useState([]);
  const [jdResult, setJdResult] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const interviewRes = await axios.get(
        "http://127.0.0.1:8000/interview/1/results"
      );

      const historyRes = await axios.get(
        "http://127.0.0.1:8000/interviews"
      );

      const jdRes = await axios.post(
        "http://127.0.0.1:8000/match-jd",
        {
          resume_id: 1,
          job_description:
            "Looking for a Full Stack Developer with React, FastAPI, PostgreSQL, Docker, AWS and CI/CD experience.",
        }
      );

      setResults(interviewRes.data);
      setHistory(historyRes.data);
      setJdResult(jdRes.data);
    } catch (error) {
      console.error(error);
    }
  };

  const chartData = history.map((item) => ({
    interview: `#${item.interview_id}`,
    score: item.average_score * 10,
  }));

  return (
    <div className="container">
      <h1 className="title">🚀 InterviewAI Dashboard</h1>

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

      {jdResult && (
        <div className="history-section">
          <h2>🎯 Skill Gap Analysis</h2>

          <div className="history-card">
            <h3>Missing Skills</h3>

            <ul>
              {jdResult.missing_skills?.map((skill, index) => (
                <li key={index}>{skill}</li>
              ))}
            </ul>
          </div>

          <div className="history-card">
            <h3>Matching Skills</h3>

            <ul>
              {jdResult.matching_skills?.map((skill, index) => (
                <li key={index}>{skill}</li>
              ))}
            </ul>
          </div>
        </div>
      )}

      <div className="history-section">
        <h2>📈 Performance Trend</h2>

        <div className="history-card">
          <ResponsiveContainer width="100%" height={350}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
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
              Questions Answered: {item.questions_answered}
            </p>

            <p>
              Average Score: {item.average_score}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;