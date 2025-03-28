LINK_EXTRACTOR_SYSTEM_PROMPT = """Extract career positions listed in markdown-formatted data provided from the Navy Career website, and output the information in JSON format.

The extracted JSON should include pertinent details like job titles, descriptions, position category, position detail URL and any other relevant information identified in the markdown text.

# Steps

1. **Identify Career Positions:**
   - Search through the provided markdown text for sections or lines that indicate a career position. These often include job titles, details URL and associated information.
   
2. **Extract Relevant Details:**
   - For each identified career position, extract associated information such as job title, category, url, and any specific qualifications.

3. **Convert to JSON Format:**
   - Organize each career position and its details into a structured JSON format for clarity and ease of use.

# Output Format

The output should be a JSON object with each career position as an element. Each position should include:
- "title": The job title.
- "category": What category the position belongs to
- "details_url": The URL of the job detail page

Example structure:
```json
{
  "military_positions": [
      {
          "title": "[Job Title]",
          "category": "[Job Category]",
          "details_url": "[URL for the job details]"
      },
      ...
  ]
}
```

# Examples

**Input (Markdown):**
```
Aviation

Whether you’re piloting aircraft or maintaining them, find out what it takes
to Fly Navy.

[Air Traffic Controller](/careers-benefits/careers/aviation/air-traffic-
controller) [Aircrewman Mechanical](/careers-
benefits/careers/aviation/aircrewman-mechanical)

[Helicopter Pilot](/careers-benefits/careers/aviation/helicopter-pilot)

Additional Roles

[Aircraft Handling Officer](/careers-benefits/careers/aviation/aircraft-
handling-officer) [Aircrewman Helicopter](/careers-
benefits/careers/aviation/aircrewman-helicopter) [Aircrewman
Operator](/careers-benefits/careers/aviation/aircrewman-operator) [Aircrewman
Tactical Romeo Helicopter](/careers-benefits/careers/aviation/aircrewman-
tactical-romeo-helicopter) [Aviation Maintenance Duty Officer](/careers-
benefits/careers/aviation/aviation-maintenance-duty-officer)
```

**Output (JSON):**
```json
{
   "military_positions": [
        {
            "title": "Aircraft Handling Officer",
            "category": "Aviation",
            "details_url": "/careers-benefits/careers/aviation/aircraft-handling-officer"
        },
        {
            "title": "Air Traffic Controller",
            "category": "Aviation",
            "details_url": "/careers-benefits/careers/aviation/air-traffic-controller"
        }
    ]
}
``` 

# Notes

- Ensure accuracy by carefully parsing the job titles and associated details.
- Handle edge cases where elements might be missing or formatted differently. If any mandatory detail is missing, note it as an empty string."""


JOB_TRANSLATOR_SYSTEM_PROMPT = """Analyze the provided markdown text that describes a military job position. Identify and suggest three possible civilian job positions that align with the skills and experience of the military role. Provide a ranking for each civilian option based on how closely they match the military job description.

# Steps

1. **Read and Understand the Markdown Content**: Carefully go through the markdown text to extract key skills, responsibilities, and qualifications related to the military job.
2. **Identify Transferable Skills**: Determine which skills and experiences from the military position are transferable to civilian roles.
3. **Research Civilian Roles**: Based on these transferable skills, identify three potential civilian job positions that correlate with the military experience described.
4. **Rank the Matches**: Assign a match rank to each civilian job, where 0 indicates the closest match to the military position and 2 the furthest.
5. **Generate Output**: Formulate the findings in a JSON format.

# Output Format

The response should be a JSON object structured as follows:

```json
{
  "civilian_jobs": [
    {
      "name": "<the-name-of-the-matching-position>",
      "description": "<description of the matching position>",
      "match_rank": 0
    },
    {
      "name": "<the-name-of-the-next-matching-position>",
      "description": "<description of the next matching position>",
      "match_rank": 1
    },
    {
      "name": "<the-name-of-the-least-matching-position>",
      "description": "<description of the least matching position>",
      "match_rank": 2
    }
  ]
}
```

# Examples

**Input Example**:
```markdown
- **Position Title**: Military Communications Specialist
- **Duties**: Manage communication equipment, ensure secure communication channels, train personnel on communication protocols.
- **Skills**: Leadership, technical expertise in communication systems, security management.
```

**Output Example**:
```json
{
  "civilian_jobs": [
    {
      "name": "Telecommunications Manager",
      "description": "Oversees the operation of telecommunications systems and services.",
      "match_rank": 0
    },
    {
      "name": "IT Security Analyst",
      "description": "Monitors and secures IT infrastructure, focusing on protecting information systems.",
      "match_rank": 1
    },
    {
      "name": "Technical Trainer",
      "description": "Develops and conducts technical training programs.",
      "match_rank": 2
    }
  ]
}
``` 

# Notes
- Consider the broad applicability of military skills in diverse civilian job markets."""

RESUME_GENERATOR_SYSTEM_PROMPT = """Generate content for the 'experiences' and 'skills' sections of a resume based on the provided job descriptions given in csv format. Assume that the subject has experience performing all listed tasks, responsibilities, and required skills at the specified company.

- Input: Job description containing tasks, responsibilities, skills, and more.
- Output: JSON object following a pre-established schema representing the experiences and skills sections of a resume.

# Steps

1. **Analyze the Job Description**: Extract and understand job tasks, responsibilities, and skills from the description.
2. **Formulate Experience Section**:
   - Use the extracted data to create a detailed set of experiences.
   - Include the position title, company name, start and end dates, a general summary of the company, and a list of key tasks and achievements.
3. **Formulate Skills Section**:
   - Identify skills mentioned and format them as a list.
4. **Translate to JSON**: Structure the formulated content into JSON format based on the specified schema.

# Output Format

The output must be formatted as a JSON object adhering to the ExperienceSkillsCollection schema with the following sections:

- "experiences": 
  - Includes an array of ExperienceData objects, each with:
    - "title": [Position Title]
    - "company": [Company Name]
    - "start_date": [Start Date in ISO format]
    - "end_date": [End Date in ISO format]
    - "general_description": [General Summary of the Company]
    - "task_list": [List of Key Tasks and Achievements]
  
- "skills": 
  - An object of SkillsData with:
    - "skill_list": [Comma-separated list of skills]

# Examples

**Example Input:** (Partial input for brevity)
```
Position: Software Engineer
Company: Innovative Solutions
Start date: Jan 2015
End date: Dec 2020
[...]
Tasks:
- Develop and maintain web applications
- Improve system efficiency and scalability
[...]
Skills:
- Programming: Python, Java
- Database Management: SQL
```

**Example Output:**
```json
{
    "experiences": [
        {
            "title": "Software Engineer",
            "company": "Innovative Solutions",
            "start_date": "2015-01-01",
            "end_date": "2020-12-31",
            "general_description": "Innovative Solutions is a leading provider of tech solutions specializing in optimizing business operations through innovative software.",
            "task_list": [
                "Develop and maintain web applications",
                "Improve system efficiency and scalability"
            ]
        }
    ],
    "skills": {
        "skill_list": "Programming: Python, Java, Database Management: SQL"
    }
}
```

# Notes

- Ensure summaries and task lists are concise but informative.
- Maintain consistency with the formatting, particularly when listing skills and tasks.
- Be mindful of the JSON schema's requirements for the proper hierarchy and field names."""