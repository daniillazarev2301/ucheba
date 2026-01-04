import React, { useState } from "react";
import api from "../api";

const PresentationPage: React.FC = () => {
  const [topic, setTopic] = useState("");
  const [slides, setSlides] = useState(5);
  const [fileUrl, setFileUrl] = useState("");

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    const response = await api.post("/presentation/create", { topic, slides });
    setFileUrl(response.data.file_url);
  };

  return (
    <div>
      <h2>Презентации</h2>
      <form onSubmit={handleSubmit}>
        <input placeholder="Тема" value={topic} onChange={(e) => setTopic(e.target.value)} />
        <input
          type="number"
          value={slides}
          onChange={(e) => setSlides(Number(e.target.value))}
        />
        <button type="submit">Создать</button>
      </form>
      {fileUrl && <a href={fileUrl}>Скачать презентацию</a>}
    </div>
  );
};

export default PresentationPage;
