import React, { useEffect, useState } from "react";
import api from "../api";

const PlansPage: React.FC = () => {
  const [plans, setPlans] = useState([]);

  useEffect(() => {
    const load = async () => {
      const response = await api.get("/plans/");
      setPlans(response.data);
    };
    load();
  }, []);

  const handleSelect = async (planId: number) => {
    await api.post("/subscriptions/select/", { plan_id: planId });
    alert("Тариф активирован");
  };

  return (
    <div>
      <h2>Тарифы</h2>
      <ul>
        {plans.map((plan: any) => (
          <li key={plan.id}>
            {plan.name} - {plan.price} ₽
            <button onClick={() => handleSelect(plan.id)}>Выбрать</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default PlansPage;
