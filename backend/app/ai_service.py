from ai_module import ExamPreparator, PresentationGenerator, TaskSolver, TextWorkGenerator


task_solver = TaskSolver()
text_generator = TextWorkGenerator()
presentation_generator = PresentationGenerator()
exam_preparator = ExamPreparator()


def solve_task(payload, user_profile):
    return task_solver.solve(payload, user_profile)


def generate_text_work(topic, pages, user_profile):
    return text_generator.generate(topic=topic, pages=pages, user_profile=user_profile)


def generate_presentation(topic, slides, user_profile):
    return presentation_generator.generate(topic=topic, slides=slides, user_profile=user_profile)


def prepare_exam(subjects, user_profile):
    return exam_preparator.prepare(subjects=subjects, user_profile=user_profile)
