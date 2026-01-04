class TaskSolver:
    def solve(self, payload, user_profile):
        subject = payload.get("subject", "")
        question = payload.get("question", "")
        steps = [
            f"Определить предмет: {subject}",
            "Проанализировать условие",
            "Составить план решения",
            "Выполнить вычисления",
        ]
        answer = f"Ответ сформирован для вопроса: {question[:50]}..."
        return {"steps": steps, "answer": answer, "profile": user_profile}
