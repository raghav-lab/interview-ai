import { useState } from "react";
import axios from "axios";
import { useNavigate, Link } from "react-router-dom";

function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const login = async () => {
    try {
      const res = await axios.post(
        "http://127.0.0.1:8000/login",
        {
          email,
          password,
        }
      );

      localStorage.setItem(
        "token",
        res.data.access_token
      );

      alert("Login Successful");

      navigate("/");
    } catch (err) {
      console.log(err);
      alert("Invalid Credentials");
    }
  };

  return (
    <div className="container">
      <h1>Login</h1>

      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) =>
          setEmail(e.target.value)
        }
      />

      <br /><br />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) =>
          setPassword(e.target.value)
        }
      />

      <br /><br />

      <button onClick={login}>
        Login
      </button>

      <br /><br />

      <Link to="/register">
        Create Account
      </Link>
    </div>
  );
}

export default Login;