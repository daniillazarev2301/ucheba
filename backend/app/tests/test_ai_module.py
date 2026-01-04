from ai_module import TaskSolver


def test_task_solver_returns_answer():
    solver = TaskSolver()
    result = solver.solve({"subject": "математика", "question": "2+2"}, {})
    assert "answer" in result
    assert result["steps"]
