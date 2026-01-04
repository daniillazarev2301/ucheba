import React, { useEffect, useState } from "react";
import api from "../api";

const DashboardPage: React.FC = () => {
  const [tasks, setTasks] = useState([]);
  const [subscriptions, setSubscriptions] = useState([]);

  useEffect(() => {
    const load = async () => {
      const taskResponse = await api.get("/tasks/");
      const subscriptionResponse = await api.get("/subscriptions/");
      setTasks(taskResponse.data);
      setSubscriptions(subscriptionResponse.data);
    };
    load();
  }, []);

  return (
    <div>
      <h2>Личный кабинет</h2>
      <h3>История задач</h3>
      <ul>
        {tasks.map((task: any) => (
          <li key={task.id}>{task.subject}</li>
        ))}
      </ul>
      <h3>Подписка</h3>
      <ul>
        {subscriptions.map((sub: any) => (
          <li key={sub.id}>{sub.status}</li>
        ))}
      </ul>
    </div>
  );
};

export default DashboardPage;
