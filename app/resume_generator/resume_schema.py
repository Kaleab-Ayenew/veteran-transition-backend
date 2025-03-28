from pydantic import BaseModel



class ResumePersonalData(BaseModel):
    name: str
    email: str
    phone_number: str
    website: str | None = None
    address: str


class ExperienceData(BaseModel):
    title: str
    company: str
    start_date: str # Start date in ISO format
    end_date: str # End date in ISO format
    general_description: str # A general description of what the person did in that position
    task_list: list[str] # A bullet point list of the tasks performed under that position


class ProjectData(BaseModel):
    project_name: str
    project_summary: str # One sentence summary of the project
    project_details: list[str] # A bullet point list of the tasks performed under that project
    project_date: str

class EducationData(BaseModel):
    institution: str
    field_of_study: str # The field of study for that degree
    degree_level: str # The degree level of the company
    gpa: str # The GPA for that degree

class SkillsData(BaseModel):
    skill_list: list[str] # A bullet point(Comma separated) list of skills

class ExperienceSkillsCollection(BaseModel):
    experiences: list[ExperienceData] # A list of experiences
    skills: SkillsData # A list of skills

class FullResumeData(BaseModel):
    personal_data: ResumePersonalData
    experiences: list[ExperienceData]
    projects: list[ProjectData]
    education: list[EducationData]
    skills: SkillsData


if __name__ == "__main__":
    print(ExperienceSkillsCollection.model_json_schema()["$defs"])