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


class Task:
    def __init__(self, name: str, category: str, duration_minutes: int, priority: int):
        self.name = name
        self.category = category
        self.duration_minutes = duration_minutes
        self.priority = priority  # 1 = low, 5 = high

    def __repr__(self) -> str:
        pass

    def __lt__(self, other: "Task") -> bool:
        pass


class DailyPlan:
    def __init__(self, scheduled: list[Task], skipped: list[Task], total_duration: int):
        self.scheduled = scheduled
        self.skipped = skipped
        self.total_duration = total_duration

    def explain(self) -> str:
        pass

    def summary(self) -> str:
        pass


class Scheduler:
    def __init__(self, pet: Pet, tasks: list[Task], available_minutes: int):
        self.pet = pet
        self.tasks = tasks
        self.available_minutes = available_minutes

    def generate_plan(self) -> DailyPlan:
        pass

    def _sort_tasks(self) -> list[Task]:
        pass
