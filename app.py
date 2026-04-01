import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.markdown("A pet care planning assistant that helps you schedule daily tasks based on time and priority.")

# Fix number_input +/- buttons staying highlighted after click
st.components.v1.html("""
<script>
const doc = window.parent.document;
doc.addEventListener('mouseup', function() {
    if (doc.activeElement && doc.activeElement.tagName === 'BUTTON') {
        doc.activeElement.blur();
    }
});
</script>
""", height=0)

# --- Step 2: Session state initialization ---
# Store Owner and pets in session_state so they persist across reruns

if "owner" not in st.session_state:
    st.session_state.owner = None
if "pets" not in st.session_state:
    st.session_state.pets = []
if "selected_pet" not in st.session_state:
    st.session_state.selected_pet = None

# --- Owner setup ---
st.subheader("Owner Info")

col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Owner name", value="Jordan")
with col2:
    available_minutes = st.number_input("Available minutes today", min_value=5, max_value=480, value=60)

if st.button("Set Owner"):
    st.session_state.owner = Owner(owner_name, available_minutes)
    st.session_state.pets = []
    st.session_state.selected_pet = None

if st.session_state.owner:
    st.success(f"Owner: {st.session_state.owner.name} | {st.session_state.owner.available_minutes} min available")
else:
    st.info("Set your owner info above to get started.")
    st.stop()

st.divider()

# --- Add a pet ---
st.subheader("Add a Pet")

col1, col2 = st.columns(2)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["Dog", "Cat", "Bird", "Fish", "Other"])

if st.button("Add Pet"):
    new_pet = Pet(pet_name, species, st.session_state.owner)
    st.session_state.pets.append(new_pet)

if st.session_state.pets:
    pet_names = [f"{p.name} ({p.species})" for p in st.session_state.pets]
    selected_index = st.selectbox("Select a pet", range(len(pet_names)), format_func=lambda i: pet_names[i])
    st.session_state.selected_pet = st.session_state.pets[selected_index]
else:
    st.info("Add a pet above.")
    st.stop()

st.divider()

# --- Add tasks to the selected pet ---
pet = st.session_state.selected_pet
st.subheader(f"Tasks for {pet.name}")

PRIORITY_MAP = {"Low": 1, "Medium": 3, "High": 5}

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_name = st.text_input("Task name", value="Morning walk")
with col2:
    category = st.selectbox("Category", ["Exercise", "Feeding", "Medication", "Grooming", "Enrichment", "Hygiene"])
with col3:
    duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
with col4:
    priority_label = st.selectbox("Priority", ["High", "Medium", "Low"])

if st.button("Add Task"):
    new_task = Task(task_name, category.lower(), int(duration), PRIORITY_MAP[priority_label])
    pet.add_task(new_task)

if pet.tasks:
    st.write("Current tasks:")
    task_data = [
        {"Task": t.name, "Category": t.category, "Duration (min)": t.duration_minutes, "Priority": t.priority}
        for t in pet.tasks
    ]
    st.table(task_data)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# --- Generate schedule ---
st.subheader("Build Schedule")

if st.button("Generate Schedule"):
    if not pet.tasks:
        st.warning("Add at least one task before generating a schedule.")
    else:
        scheduler = Scheduler(pet, pet.tasks, st.session_state.owner.available_minutes)
        plan = scheduler.generate_plan()

        st.markdown(f"**{plan.summary()}**")
        st.code(plan.explain())
