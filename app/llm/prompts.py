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