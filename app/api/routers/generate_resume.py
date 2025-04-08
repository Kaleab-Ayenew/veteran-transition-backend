from fastapi import APIRouter, HTTPException
from app.config import settings
from app.db import db_utils, models
from app.llm.resume_generator_agent import ResumeGeneratorAgent
from app.resume_generator import resume_schema
import pathlib


router = APIRouter(prefix="/resume")


@router.post("/generate/{military_position_id}")
def generate_resume(military_position_id: str, civilian_position_number: int | None = None):
    military_position = db_utils.get_one_row(
        models.MilitaryPosition,
        (models.MilitaryPosition.id == military_position_id,)
    )

    # Check if the military position exists
    if not military_position:
        raise HTTPException(status_code=404, detail="We couldn't find a military position with the given ID.")

    # Retrive the civilian position
    civilian_positions = db_utils.get_one_row(
        models.CivilianPosition,
        (models.CivilianPosition.military_position == military_position_id,)
    )

    if not civilian_positions:
        raise HTTPException(status_code=400, detail=f"We couldn't find the civilian translation for military position: '{military_position.name}' with id: '{military_position_id}'.")
    parsed_civilian_position = civilian_positions.get_civilian_options()
    chosen_civilian_position = parsed_civilian_position["civilian_jobs"][civilian_position_number]["name"] if civilian_position_number else parsed_civilian_position["civilian_jobs"][0]["name"]

    # Prepare dummy personal data
    personal_data = resume_schema.ResumePersonalData(
        name="John Doe",
        email="john.doe@email.com",
        phone_number="+12345678901",
        address="Los Angels, CA"
    )
    project_data = resume_schema.ProjectData(
        project_name="Project 1",
        project_summary="A one sentence summary of project number 1",
        project_details=["Project detail 1", "Project detail 2", "Project detail 3"],
        project_date="Dec 2020"
    )

    education_data = resume_schema.EducationData(
        institution="UCLA",
        field_of_study="Computer Science",
        degree_level="BS",
        gpa="3.9"
    )
    resume_agent = ResumeGeneratorAgent(
        position_name=chosen_civilian_position,
        personal_data=personal_data,
        education_data=education_data,
        project_data=project_data
    )

    pdf_path = resume_agent.generate_pdf_resume()
    filename = pathlib.Path(pdf_path).name
    download_path = f"{settings.BACKEND_BASE_URL}/static/{filename}"
    return {"resume_url": download_path}



