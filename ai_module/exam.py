class ExamPreparator:
    def prepare(self, subjects, user_profile):
        materials = [f"Конспект по теме: {subject}" for subject in subjects]
        tests = [
            {"question": f"Что вы знаете о {subject}?", "options": ["A", "B", "C"], "answer": "A"}
            for subject in subjects
        ]
        return {"materials": materials, "tests": tests, "profile": user_profile}
