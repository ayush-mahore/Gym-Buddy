from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Workout(BaseModel):
    id: int
    exercise: str
    sets: int
    reps: int
    weight_kg: Optional[float] = None

workouts_db = []

@app.post("/workouts/", response_model=Workout)
def add_workout(workout: Workout):
    for w in workouts_db:
        if w.id == workout.id:
            raise HTTPException(status_code=400, detail="Workout already exists")
    workouts_db.append(workout)
    return workout

@app.get("/workouts/", response_model=list[Workout])
def get_all_workouts():
    return workouts_db

@app.get("/workouts/{workout_id}", response_model=Workout)
def get_workout(workout_id:int):
    for workout in workouts_db:
        if workout_id == workout.id:
            return workout
    raise HTTPException(status_code=404, detail="Workout not found")

@app.put("/workouts/{workout_id}", response_model=Workout)
def update_workout(workout_id: int, updated_workout: Workout):
    for index, workout in enumerate(workouts_db):
        if workout_id == workout.id:
            workouts_db[index] = updated_workout
            return updated_workout
    raise HTTPException(status_code=404, detail="Workout not found")

@app.delete("/workouts/{workout_id}")
def delete_workout(workout_id: int):
    for index, workout in enumerate(workouts_db):
        if workout_id == workout.id:
            del workouts_db[index]
            return {"message": f"Workout {workout_id} successfully deleted"}
    raise HTTPException(status_code=404, detail="Workout not found")