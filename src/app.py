"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")


# In-memory activities store (module-level so all routes can access and modify it)
activities = {
    # Sports-related activities
    "soccer": {
        "name": "Soccer",
        "category": "sports",
        "description": "Outdoor team sport. Practice on Tuesdays and Thursdays.",
        "participants": [],
        "max_participants": 22
    },
    "basketball": {
        "name": "Basketball",
        "category": "sports",
        "description": "Indoor court, competitive team practices and games.",
        "participants": [],
        "max_participants": 12
    },
    "swimming": {
        "name": "Swimming",
        "category": "sports",
        "description": "Swim team with lap training and meets.",
        "participants": [],
        "max_participants": 20
    },
    # Artistic activities
    "drama": {
        "name": "Drama Club",
        "category": "artistic",
        "description": "Acting, stagecraft, and seasonal productions.",
        "participants": [],
        "max_participants": 30
    },
    "choir": {
        "name": "Choir",
        "category": "artistic",
        "description": "Vocal ensemble rehearsals and performances.",
        "participants": [],
        "max_participants": 50
    },
    "painting": {
        "name": "Painting",
        "category": "artistic",
        "description": "Open-studio painting sessions and exhibitions.",
        "participants": [],
        "max_participants": 25
    },
    # Intellectual activities
    "chess": {
        "name": "Chess Club",
        "category": "intellectual",
        "description": "Weekly meetings, puzzles, and interschool matches.",
        "participants": [],
        "max_participants": 30
    },
    "debate": {
        "name": "Debate Team",
        "category": "intellectual",
        "description": "Competitive debate practice and tournaments.",
        "participants": [],
        "max_participants": 24
    },
    "robotics": {
        "name": "Robotics Club",
        "category": "intellectual",
        "description": "Design and build robots for regional competitions.",
        "participants": [],
        "max_participants": 18
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Normalize email and validate student is not already signed up
    normalized_email = email.strip().lower()
    if normalized_email in [p.strip().lower() for p in activity["participants"]]:
        raise HTTPException(status_code=400, detail="Student is already signed up")

    # Optional: check capacity
    if "max_participants" in activity and len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="Activity is full")

    # Add student
    activity["participants"].append(normalized_email)
    return {"message": f"Signed up {normalized_email} for {activity_name}"}


@app.delete("/activities/{activity_name}/participants")
def remove_participant(activity_name: str, email: str):
    """Unregister a student from an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]
    normalized_email = email.strip().lower()

    # Find and remove participant
    for i, p in enumerate(activity["participants"]):
        if p.strip().lower() == normalized_email:
            activity["participants"].pop(i)
            return {"message": f"Removed {normalized_email} from {activity_name}"}

    raise HTTPException(status_code=404, detail="Participant not found")

