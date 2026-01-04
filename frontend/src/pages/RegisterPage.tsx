import React, { useState } from "react";
import api from "../api";

const RegisterPage: React.FC = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    const response = await api.post("/auth/register", { email, password });
    localStorage.setItem("token", response.data.access);
    setMessage("Регистрация выполнена");
  };

  return (
    <div>
      <h2>Регистрация</h2>
      <form onSubmit={handleSubmit}>
        <input placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input
          placeholder="Пароль"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit">Создать аккаунт</button>
      </form>
      <p>{message}</p>
    </div>
  );
};

export default RegisterPage;
