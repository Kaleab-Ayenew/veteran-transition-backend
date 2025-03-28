from app.resume_generator import resume_schema

def generate_resume_markdown(data: resume_schema.FullResumeData):
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


    
    




