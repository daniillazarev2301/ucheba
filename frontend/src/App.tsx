import React from "react";
import { Route, Routes, Link } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import DashboardPage from "./pages/DashboardPage";
import TaskPage from "./pages/TaskPage";
import WorkPage from "./pages/WorkPage";
import PresentationPage from "./pages/PresentationPage";
import ExamPage from "./pages/ExamPage";
import PlansPage from "./pages/PlansPage";
import PaymentPage from "./pages/PaymentPage";
import AdminPage from "./pages/AdminPage";

const App: React.FC = () => {
  return (
    <div>
      <header>
        <nav>
          <Link to="/">Личный кабинет</Link> | <Link to="/tasks">Задачи</Link> |{" "}
          <Link to="/work">Работы</Link> | <Link to="/presentations">Презентации</Link> |{" "}
          <Link to="/exam">Экзамены</Link> | <Link to="/plans">Тарифы</Link> |{" "}
          <Link to="/admin">Админ</Link>
        </nav>
      </header>
      <Routes>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/tasks" element={<TaskPage />} />
        <Route path="/work" element={<WorkPage />} />
        <Route path="/presentations" element={<PresentationPage />} />
        <Route path="/exam" element={<ExamPage />} />
        <Route path="/plans" element={<PlansPage />} />
        <Route path="/payment" element={<PaymentPage />} />
        <Route path="/admin" element={<AdminPage />} />
      </Routes>
    </div>
  );
};

export default App;
