import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});
API.interceptors.response.use(
    (response) => response,
    (error) => {
      if (error.response?.status === 401) {
        localStorage.removeItem("token");
        window.location.href = "/login";
      }
  
      return Promise.reject(error);
    }
  );

API.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");

  console.log("Sending token:", token);

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

export default API;