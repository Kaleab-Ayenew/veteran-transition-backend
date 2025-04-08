import json
from app.llm.open_ai import LLMClient
from app.llm import prompts
from app.db import db_utils, models
from app.resume_generator import resume_schema, resume_utils
from app.scraping.scraping_ant import AntScraper
from app.resume_generator import resume_generator, resume_schema
from bs4 import BeautifulSoup
import requests
import sys



class ResumeGeneratorAgent:
    def __init__(self, position_name: str, 
                 personal_data: resume_schema.ResumePersonalData, 
                 education_data: resume_schema.EducationData,
                 project_data: resume_schema.ProjectData):
        self.llm_client = LLMClient(model="gpt-4o-mini",
                                    history=[{"role":"system", "content": prompts.RESUME_GENERATOR_SYSTEM_PROMPT}])
        
        self.onetonline_base_url = "https://www.onetonline.org"
        self.position_name = position_name
        self.personal_data = personal_data
        self.education_data = education_data
        self.project_data = project_data
        self.job_url = self._get_position_detail_page_url()
        self.full_resume_data = None

    def extract_experience_and_skills(self) -> resume_schema.ExperienceSkillsCollection:
        csv_job_data = self._extract_csv_tables()
        llm_response = self.llm_client.send_message(
            input=[{
                "role": "user",
                "content": csv_job_data
            }],
            response_format="json_schema",
            json_schema=resume_schema.ExperienceSkillsCollection
        )
        return llm_response
    
    def _extract_csv_tables(self):
        print("[*] Extracting CSV tables")
        scraper = AntScraper(
        scrap_url=self.job_url,
        extract_type="general"
         )
        job_page_html = scraper.get_content()
        soup = BeautifulSoup(job_page_html, "html.parser")
        h2_reports = soup.select("h2.report")
        header_urls = [(h2.find(string=True, recursive=False).strip(), h2.find_all("a")[1]["href"]) for h2 in h2_reports if len(h2.find_all("a")) >= 2]

        csv_tables = []
        for h,u in header_urls:
            csv = requests.get(self.onetonline_base_url+u).text
            content = f"## {h} ##\n\n{csv}"
            csv_tables.append(content)
        return "\n\n=========\n\n".join(csv_tables)
    
    def _get_position_detail_page_url(self):
        search_url = f"{self.onetonline_base_url}/find/result?s={self.position_name}"
        scraper = AntScraper(
            scrap_url=search_url,
            extract_type="general"
            )
        page_html = scraper.get_content()
        soup = BeautifulSoup(page_html, "html.parser")
        position_code = soup.find("table").find("tbody").find("tr").find("td").text
        detail_page_url = f"{self.onetonline_base_url}/link/details/{position_code}"
        return detail_page_url

    def generate_resume_markdown(self, data: resume_schema.FullResumeData):
        personal_data = f"""# {data.personal_data.name}

    - <{data.personal_data.email}>
    - {data.personal_data.phone_number}
    - {data.personal_data.address}
    """
        exp_list = []
        for e in data.experiences:
            task_list = [f"- {tl}" for tl in e.task_list]
            str_task_list = "\n".join(task_list)
            exp_text = f"### <span>{e.title}, {e.company}</span> <span>{e.start_date} -- {e.end_date}</span>\n\n{e.general_description}\n\n{str_task_list}" 
            exp_list.append(exp_text)
        experience_list_text = "\n\n".join(exp_list)

        experience_data = f"""## Experience

{experience_list_text}
    """
        pr_list = []
        for p in data.projects:
            project_details = [f"- {pd}" for pd in p.project_details]
            str_pr_task_list = "\n".join(project_details)
            pr_text = f"### <span>{p.project_name}</span> <span>{p.project_date}</span>\n\n{p.project_summary}\n\n{str_pr_task_list}"
            pr_list.append(pr_text)
        pr_list_text = "\n\n".join(pr_list)
        project_data = f"""## Projects

{pr_list_text}
    """

        edu_list = []
        for e in data.education:
            edu_text = f"### <span>{e.institution}, {e.degree_level} {e.field_of_study}</span>\n\n- GPA: {e.gpa}"
            edu_list.append(edu_text)
        edu_list_text = "\n\n".join(edu_list)
        education_data = f"""## Education

{edu_list_text}
    """
        skill_list = [f"- {s}" for s in data.skills.skill_list]
        skill_list_text = "\n".join(skill_list)
        skills_text = f"""## Skills

{skill_list_text}
"""
        final_resume_md = f"{personal_data}\n\n{experience_data}\n\n{project_data}\n\n{education_data}\n\n{skills_text}"
        return final_resume_md
    
    def get_full_resume_data(self):
        if self.full_resume_data is not None:
            return self.full_resume_data
        exp_skills = self.extract_experience_and_skills()
        self.full_resume_data = resume_schema.FullResumeData(
            personal_data=self.personal_data,
            experiences=exp_skills.experiences,
            projects=[self.project_data],
            education=[self.education_data],
            skills=exp_skills.skills
        )
        return self.full_resume_data
    
    def generate_pdf_resume(self) -> str:
        full_resume_data = self.get_full_resume_data()
        resume_markdown = self.generate_resume_markdown(full_resume_data)
        resume_html = resume_generator.make_html(resume_markdown)
        pdf_path = resume_generator.write_pdf(html=resume_html, prefix="_".join(self.personal_data.name.split(" ") + ["Resume"])+".pdf")
        print(f"[*] Resume pdf saved successfully.\nPath: {pdf_path}")
        return pdf_path




if __name__ == "__main__":
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

    resume_agent = ResumeGeneratorAgent("Hazardous Materials Technician", personal_data, education_data, project_data)
    exp_skills = resume_agent.generate_pdf_resume()
