import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Owner, Pet, Task


def test_mark_complete_changes_status():
    """Verify that calling mark_complete() changes the task's status to True."""
    task = Task("Morning walk", category="exercise", duration_minutes=30, priority=5)
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    """Verify that adding a task to a Pet increases that pet's task count."""
    owner = Owner("Nathan", available_minutes=60)
    pet = Pet("Buddy", species="Dog", owner=owner)
    assert len(pet.tasks) == 0

    pet.add_task(Task("Feed breakfast", category="feeding", duration_minutes=10, priority=4))
    assert len(pet.tasks) == 1

    pet.add_task(Task("Evening walk", category="exercise", duration_minutes=30, priority=5))
    assert len(pet.tasks) == 2
