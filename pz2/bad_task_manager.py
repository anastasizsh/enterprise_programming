class BadTaskManager:
    def __init__(self):
        self.tasks = []

    def create_task(self, title: str, description: str, assignee_name: str, assignee_email: str):
        if not title or not title.strip():
            raise ValueError("Title is required")

        task_id = len(self.tasks) + 1
        task = {
            "id": task_id,
            "title": title.strip(),
            "description": description,
            "assignee": assignee_name,
            "email": assignee_email,
            "status": "Created"
        }
        self.tasks.append(task)

        with open("tasks.txt", "a", encoding="utf-8") as file:
            file.write(f"[{task_id}] {task['title']} -> {assignee_name}\n")

        print(f"Sending email to {assignee_email}: Task '{title}' assigned.")
        return task