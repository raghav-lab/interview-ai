import { useEffect, useState } from "react";
import API from "../api";
import {
  useParams,
  useNavigate,
} from "react-router-dom";
import "../App.css";

function Interview() {
    const { interviewId } = useParams();

   
  const navigate = useNavigate();

  const [questions, setQuestions] = useState([]);
  const [current, setCurrent] = useState(0);
  const [answer, setAnswer] = useState("");
  const [feedback, setFeedback] = useState(null);
  const [loading, setLoading] = useState(false);

  const [isListening, setIsListening] =
    useState(false);

  const [timeLeft, setTimeLeft] = useState(120);

  // Load questions
  useEffect(() => {
    loadQuestions();
  }, []);

  // Tab switching detection
  useEffect(() => {
    const handleVisibility = () => {
      if (document.hidden) {
        alert(
          "⚠️ Tab switching detected during interview!"
        );
      }
    };

    document.addEventListener(
      "visibilitychange",
      handleVisibility
    );

    return () =>
      document.removeEventListener(
        "visibilitychange",
        handleVisibility
      );
  }, []);

  // Auto speak question
  useEffect(() => {
    if (questions.length > 0) {
      setTimeout(() => {
        speakQuestion(
          questions[current].question
        );
      }, 1000);
    }
  }, [current, questions]);

  // Timer
  useEffect(() => {
    if (!questions.length) return;

    if (timeLeft === 0) {
      if (current < questions.length - 1) {
        nextQuestion();
      } else {
        navigate(`/results/${questions[current].interview_id}`);
      }
      return;
    }

    const timer = setTimeout(() => {
      setTimeLeft((prev) => prev - 1);
    }, 1000);

    return () => clearTimeout(timer);
  }, [timeLeft, current, questions]);

  const loadQuestions = async () => {
    try {
      console.log(
        "Interview ID:",
        interviewId
      );
  
      const res = await API.get(
        `/interview/${interviewId}/questions`
      );
  
      console.log(
        "Questions received:",
        res.data
      );
  
      setQuestions(res.data);
  
    } catch (err) {
      console.log("FULL ERROR:", err);
  
      if (err.response) {
        console.log(
          "Backend Error:",
          err.response.data
        );
  
        console.log(
          "Status:",
          err.response.status
        );
      }
  
      alert("Failed to load questions");
    }
  };

  const submitAnswer = async () => {
    try {
      setLoading(true);

      const res = await API.post(
        "/submit-answer",
        {
          question_id: questions[current].id,
          answer,
        }
      );

      setFeedback(res.data.evaluation);
    } catch (err) {
      console.log(err);
      alert("Evaluation failed.");
    } finally {
      setLoading(false);
    }
  };

  const nextQuestion = () => {
    window.speechSynthesis.cancel();

    setCurrent(current + 1);
    setAnswer("");
    setFeedback(null);
    setTimeLeft(120);
  };

  // Voice Answer
  const startListening = () => {
    const SpeechRecognition =
      window.SpeechRecognition ||
      window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert(
        "Speech Recognition not supported in this browser."
      );
      return;
    }

    const recognition =
      new SpeechRecognition();

    recognition.lang = "en-US";
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onstart = () =>
      setIsListening(true);

    recognition.onend = () =>
      setIsListening(false);

    recognition.onresult = (event) => {
      const transcript =
        event.results[0][0].transcript;

      setAnswer(
        (prev) => prev + " " + transcript
      );
    };

    recognition.start();
  };

  // AI Voice Question
  const speakQuestion = (text) => {
    if (!window.speechSynthesis) {
      alert(
        "Speech synthesis not supported."
      );
      return;
    }

    // stop previous speech
    window.speechSynthesis.cancel();

    const utterance =
      new SpeechSynthesisUtterance(text);

    utterance.lang = "en-US";
    utterance.rate = 0.9;
    utterance.pitch = 1;
    utterance.volume = 1;

    // Delay helps Chrome/Safari
    setTimeout(() => {
      window.speechSynthesis.speak(
        utterance
      );
    }, 100);
  };

  if (!questions.length)
    return (
      <div className="container">
        <h2>Loading Questions...</h2>
      </div>
    );

  const progress =
    ((current + 1) / questions.length) * 100;

  const minutes = Math.floor(timeLeft / 60);
  const seconds = timeLeft % 60;

  return (
    <div className="container">
      <h1>🎤 Mock Interview</h1>

      <h3>
        Question {current + 1}/
        {questions.length}
      </h3>

      {/* Progress */}
      <div
        style={{
          width: "100%",
          background: "#ddd",
          borderRadius: "10px",
          marginBottom: "20px",
        }}
      >
        <div
          style={{
            width: `${progress}%`,
            height: "20px",
            background: "#38bdf8",
            borderRadius: "10px",
          }}
        />
      </div>

      {/* Timer */}
      <h2>
        ⏱️ {minutes}:
        {seconds < 10
          ? `0${seconds}`
          : seconds}
      </h2>

      <button
        onClick={() =>
          navigate(`/results/${interviewId}`)
        }
      >
        📊 View Results Anytime
      </button>

      <div className="history-card">
        <p>{questions[current].question}</p>

        <button
          onClick={() =>
            speakQuestion(
              questions[current].question
            )
          }
          style={{
            marginTop: "10px",
          }}
        >
          🔊 Repeat Question
        </button>
      </div>

      <textarea
        rows="8"
        value={answer}
        onChange={(e) =>
          setAnswer(e.target.value)
        }
        placeholder="Type or speak your answer..."
        style={{
          width: "100%",
          padding: "15px",
          borderRadius: "10px",
          marginTop: "20px",
        }}
      />

      <br />
      <br />

      <button onClick={startListening}>
        {isListening
          ? "🎙️ Listening..."
          : "🎙️ Speak Answer"}
      </button>

      {"  "}

      <button
        onClick={submitAnswer}
        disabled={loading}
      >
        {loading
          ? "🤖 Evaluating..."
          : "Submit Answer"}
      </button>

      {feedback && (
        <div
          className="history-card"
          style={{ marginTop: "30px" }}
        >
          <h2>AI Feedback</h2>

          <h3>
            ⭐ Score:
            {feedback.score}/10
          </h3>

          <h3>✅ Strengths</h3>

          <ul>
            {feedback.strengths?.map(
              (item, index) => (
                <li key={index}>{item}</li>
              )
            )}
          </ul>

          <h3>❌ Weaknesses</h3>

          <ul>
            {feedback.weaknesses?.map(
              (item, index) => (
                <li key={index}>{item}</li>
              )
            )}
          </ul>

          <h3>
            💡 Improved Answer
          </h3>

          <p>
            {feedback.improved_answer}
          </p>

          {current <
          questions.length - 1 ? (
            <button
              onClick={nextQuestion}
            >
              Next Question →
            </button>
          ) : (
            <button
              onClick={() =>
                navigate(
                  `/results/${interviewId}`
                )
              }
            >
              View Final Results
            </button>
          )}
        </div>
      )}
    </div>
  );
}

export default Interview;