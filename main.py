from pawpal_system import Owner, Pet, Task, Scheduler

# Create an owner with 60 minutes available
owner = Owner("Nathan", available_minutes=60, preferences=["morning walks"])

# Create two pets
dog = Pet("Buddy", species="Dog", owner=owner)
cat = Pet("Whiskers", species="Cat", owner=owner)

# Tasks for Buddy the dog
dog_tasks = [
    Task("Morning walk", category="exercise", duration_minutes=30, priority=5),
    Task("Feed breakfast", category="feeding", duration_minutes=10, priority=4),
    Task("Brush coat", category="grooming", duration_minutes=20, priority=2),
    Task("Play fetch", category="enrichment", duration_minutes=25, priority=3),
]

# Tasks for Whiskers the cat
cat_tasks = [
    Task("Feed wet food", category="feeding", duration_minutes=5, priority=5),
    Task("Clean litter box", category="hygiene", duration_minutes=10, priority=4),
    Task("Interactive toy play", category="enrichment", duration_minutes=15, priority=3),
]

# Schedule for Buddy
print(f"=== Today's Schedule for {dog.name} ({dog.species}) ===")
print(f"Owner: {owner.name} | Available time: {owner.available_minutes} min\n")

dog_scheduler = Scheduler(dog, dog_tasks, owner.available_minutes)
dog_plan = dog_scheduler.generate_plan()

print(dog_plan.explain())
print(f"\n>> {dog_plan.summary()}\n")

# Schedule for Whiskers
print(f"=== Today's Schedule for {cat.name} ({cat.species}) ===")
print(f"Owner: {owner.name} | Available time: {owner.available_minutes} min\n")

cat_scheduler = Scheduler(cat, cat_tasks, owner.available_minutes)
cat_plan = cat_scheduler.generate_plan()

print(cat_plan.explain())
print(f"\n>> {cat_plan.summary()}")
