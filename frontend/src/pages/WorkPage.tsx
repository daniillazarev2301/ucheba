import React, { useState } from "react";
import api from "../api";

const WorkPage: React.FC = () => {
  const [topic, setTopic] = useState("");
  const [pages, setPages] = useState(1);
  const [fileUrl, setFileUrl] = useState("");

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    const response = await api.post("/work/create", { topic, pages });
    setFileUrl(response.data.file_url);
  };

  return (
    <div>
      <h2>Генерация работ</h2>
      <form onSubmit={handleSubmit}>
        <input placeholder="Тема" value={topic} onChange={(e) => setTopic(e.target.value)} />
        <input
          type="number"
          value={pages}
          onChange={(e) => setPages(Number(e.target.value))}
        />
        <button type="submit">Создать</button>
      </form>
      {fileUrl && <a href={fileUrl}>Скачать работу</a>}
    </div>
  );
};

export default WorkPage;
