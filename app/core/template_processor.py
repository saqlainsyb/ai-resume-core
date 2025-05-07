import re
from typing import Dict, Any
from fastapi import HTTPException
from app.api.v1.endpoints.resumes.utils import escape_latex

class TemplateProcessor:
    """Processes LaTeX templates with dynamic placeholders and loops."""
    
    def __init__(self, template_content: str):
        self.template = template_content
        self.loop_pattern = re.compile(r'%REPEAT_(\w+)%(.*?)%END_REPEAT%', re.DOTALL)

    def _escape_value(self, value: Any) -> str:
        """Escape LaTeX special characters in a value."""
        if isinstance(value, str):
            return escape_latex(value)
        return str(value)

    def _process_loop(self, loop_name: str, loop_content: str, data: list) -> str:
        """Process a single loop section (e.g., EXPERIENCE, PROJECTS)."""
        result = []
        for item in data:
            temp_content = loop_content
            if not isinstance(item, dict):
                raise HTTPException(status_code=400, detail=f"Invalid data format for {loop_name}: expected a dictionary")
            for key, value in item.items():
                if key == "details" or key == "notes":
                    # Handle lists (e.g., responsibilities, project details, education notes)
                    if not isinstance(value, list):
                        raise HTTPException(status_code=400, detail=f"Invalid {key} format in {loop_name}: expected a list")
                    items = [f"\\resumeItem{{{self._escape_value(v)}}}" for v in value]
                    temp_content = temp_content.replace(f"{{{key}}}", "\n        ".join(items))
                else:
                    # Handle scalar fields (e.g., role, company)
                    temp_content = temp_content.replace(f"{{{key}}}", self._escape_value(value))
            result.append(temp_content)
        return "\n".join(result)

    def render(self, data: Dict[str, Any]) -> str:
        """Render the template with provided data."""
        rendered = self.template
        # Preprocess skills to convert strings to lists
        if "skills" in data:
            skills_dict = {
                "Languages": data["skills"]["languages"].split(", ") if data["skills"]["languages"] else [],
                "Frameworks": data["skills"]["frameworks"].split(", ") if data["skills"]["frameworks"] else [],
                "Frontend Technologies": data["skills"]["frontend"].split(", ") if data["skills"]["frontend"] else [],
                "Databases": data["skills"]["databases"].split(", ") if data["skills"]["databases"] else [],
                "Developer Tools": data["skills"]["tools"].split(", ") if data["skills"]["tools"] else [],
                "Methodologies": data["skills"]["methodologies"].split(", ") if data["skills"]["methodologies"] else []
            }
            data["skills"] = skills_dict

        # Process loops (EXPERIENCE, PROJECTS, EDUCATION, but skip SKILLS)
        for match in self.loop_pattern.finditer(rendered):
            loop_name, loop_content = match.group(1), match.group(2)
            if loop_name == "SKILLS":
                continue  # Skip SKILLS loop, handle it separately below
            loop_data = data.get(loop_name.lower(), [])
            if not isinstance(loop_data, list):
                raise HTTPException(status_code=400, detail=f"Invalid data for {loop_name}: expected a list")
            processed_content = self._process_loop(loop_name, loop_content.strip(), loop_data)
            rendered = rendered.replace(match.group(0), processed_content)

        # Process skills separately (dictionary format)
        if "skills" in data:
            skills_content = []
            for category, items in data["skills"].items():
                escaped_items = ", ".join(self._escape_value(item) for item in items)
                # Double escape backslashes for LaTeX commands in regex
                skills_content.append(f"\\\\textbf{{{self._escape_value(category)}}}: {{{escaped_items}}}")
            skills_section = "\n".join(skills_content)
            # Replace the SKILLS loop placeholder explicitly
            try:
                rendered = re.sub(r'%REPEAT_SKILLS%.*?%END_REPEAT%', skills_section, rendered, flags=re.DOTALL)
            except re.PatternError as e:
                raise HTTPException(status_code=400, detail=f"Regex error in skills replacement: {str(e)}")

        # Process scalar placeholders (name, email, phone, linkedin, github, summary)
        # For scalar fields (non-URLs)
        scalar_fields = ["name", "email", "phone", "summary"]
        for key in scalar_fields:
            if key in data:
                value = data[key] or ""
                rendered = rendered.replace(f"{{{key}}}", self._escape_value(value))

        # Proper LaTeX-wrapped links
        linkedin_url = data.get("linkedin", "")
        if linkedin_url:
            # Display clean text (e.g. just the username or domain)
            display_text = linkedin_url.replace("https://", "").replace("www.", "")
            rendered = rendered.replace(
                "{linkedin}",
                f"\\href{{{linkedin_url}}}{{\\underline{{{display_text}}}}}"
            )

        github_url = data.get("github", "")
        if github_url:
            display_text = github_url.replace("https://", "").replace("www.", "")
            rendered = rendered.replace(
                "{github}",
                f"\\href{{{github_url}}}{{\\underline{{{display_text}}}}}"
            )



        return rendered