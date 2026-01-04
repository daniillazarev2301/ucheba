import React, { useState } from "react";
import api from "../api";

const TaskPage: React.FC = () => {
  const [subject, setSubject] = useState("");
  const [question, setQuestion] = useState("");
  const [result, setResult] = useState("");

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    const response = await api.post("/task/solve", { subject, question });
    setResult(response.data.answer);
  };

  return (
    <div>
      <h2>Решение задач</h2>
      <form onSubmit={handleSubmit}>
        <input placeholder="Предмет" value={subject} onChange={(e) => setSubject(e.target.value)} />
        <textarea
          placeholder="Вопрос"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />
        <button type="submit">Отправить</button>
      </form>
      <p>{result}</p>
    </div>
  );
};

export default TaskPage;
