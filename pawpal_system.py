class Owner:
    def __init__(self, name: str, available_minutes: int, preferences: list[str] = None):
        self.name = name
        self.available_minutes = available_minutes
        self.preferences = preferences or []


class Pet:
    def __init__(self, name: str, species: str, owner: Owner):
        self.name = name
        self.species = species
        self.owner = owner
        self.tasks: list["Task"] = []

    def add_task(self, task: "Task"):
        # Append a task to this pet's task list
        self.tasks.append(task)


class Task:
    def __init__(self, name: str, category: str, duration_minutes: int, priority: int):
        self.name = name
        self.category = category
        self.duration_minutes = duration_minutes
        self.priority = priority  # 1 = low, 5 = high
        self.completed = False

    def mark_complete(self):
        # Mark this task as done
        self.completed = True

    def __repr__(self) -> str:
        # Return a readable string showing key task details
        return f"Task({self.name!r}, category={self.category!r}, duration={self.duration_minutes}min, priority={self.priority})"

    def __lt__(self, other: "Task") -> bool:
        # Higher priority number = more important, so sort descending
        return self.priority > other.priority


class DailyPlan:
    def __init__(self, scheduled: list[Task], skipped: list[Task], total_duration: int):
        self.scheduled = scheduled
        self.skipped = skipped
        self.total_duration = total_duration

    def explain(self) -> str:
        # Build a detailed breakdown of scheduled/skipped tasks with reasoning
        lines = []
        lines.append("Scheduled tasks (in order):")
        for i, task in enumerate(self.scheduled, 1):
            lines.append(
                f"  {i}. {task.name} ({task.duration_minutes}min, priority {task.priority}) "
                f"— scheduled because priority {task.priority}/5 fit within remaining time"
            )
        if self.skipped:
            lines.append("\nSkipped tasks (not enough time):")
            for task in self.skipped:
                lines.append(
                    f"  - {task.name} ({task.duration_minutes}min, priority {task.priority})"
                )
        lines.append(f"\nTotal scheduled time: {self.total_duration} minutes")
        return "\n".join(lines)

    def summary(self) -> str:
        # Return a one-line overview of the plan
        scheduled_count = len(self.scheduled)
        skipped_count = len(self.skipped)
        return (
            f"{scheduled_count} task(s) scheduled ({self.total_duration}min), "
            f"{skipped_count} task(s) skipped"
        )


class Scheduler:
    def __init__(self, pet: Pet, tasks: list[Task], available_minutes: int):
        self.pet = pet
        self.tasks = tasks
        self.available_minutes = available_minutes

    def generate_plan(self) -> DailyPlan:
        # Greedily schedule tasks by priority until time runs out
        sorted_tasks = self._sort_tasks()
        scheduled = []
        skipped = []
        remaining_time = self.available_minutes

        for task in sorted_tasks:
            if task.duration_minutes <= remaining_time:
                scheduled.append(task)
                remaining_time -= task.duration_minutes
            else:
                skipped.append(task)

        total_duration = self.available_minutes - remaining_time
        return DailyPlan(scheduled, skipped, total_duration)

    def _sort_tasks(self) -> list[Task]:
        # Sort tasks using __lt__ so highest priority comes first
        return sorted(self.tasks)
