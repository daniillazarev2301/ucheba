import React, { useState } from "react";
import api from "../api";

const ExamPage: React.FC = () => {
  const [subjects, setSubjects] = useState("");
  const [materials, setMaterials] = useState<string[]>([]);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    const response = await api.post("/exam/prepare", { subjects: subjects.split(",") });
    setMaterials(response.data.materials);
  };

  return (
    <div>
      <h2>Подготовка к экзамену</h2>
      <form onSubmit={handleSubmit}>
        <input
          placeholder="Дисциплины через запятую"
          value={subjects}
          onChange={(e) => setSubjects(e.target.value)}
        />
        <button type="submit">Подготовить</button>
      </form>
      <ul>
        {materials.map((material, index) => (
          <li key={index}>{material}</li>
        ))}
      </ul>
    </div>
  );
};

export default ExamPage;
