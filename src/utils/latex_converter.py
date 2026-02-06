"""
LaTeX Converter - Converts text resume to LaTeX format
Built specifically for the CV Tailor output format
"""

import re


class LaTeXConverter:
    """Converts plain text resume to LaTeX format"""
    
    def __init__(self):
        pass
    
    def text_to_latex(self, resume_text: str, personal_info: dict = None) -> str:
        """
        Convert a plain text resume to LaTeX format
        
        Args:
            resume_text: The tailored resume in text format
            personal_info: Not used - we use defaults
            
        Returns:
            LaTeX formatted resume
        """
        # Parse sections from the text
        headline = self._extract_headline(resume_text)
        summary = self._extract_summary(resume_text)
        experience = self._extract_experience(resume_text)
        skills = self._extract_skills(resume_text)
        
        # Build the complete LaTeX document
        latex_doc = self._build_latex_document(headline, summary, experience, skills)
        
        return latex_doc
    
    def _extract_headline(self, text: str) -> str:
        """Extract the headline section"""
        match = re.search(r"\*\*HEADLINE:\*\*\s*\n(.+?)(?=\n\n|\*\*SKILLS.)", text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return "Your Professional Title"

    def _extract_summary(self, text: str) -> str:
        """Extract the professional summary"""
        match = re.search(r"\*\*PROFESSIONAL SUMMARY:\*\*\s*\n(.+?)(?=\n\n|\*\*PROFESSIONAL EXPERIENCE)", text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return ""

    def _extract_experience(self, text: str) -> str:
        """Extract the professional experience section"""
        match = re.search(r"\*\*PROFESSIONAL EXPERIENCE:\*\*\s*\n(.+?)(?=\*\*SKILLS)", text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return ""

    def _extract_skills(self, text: str) -> str:
        """Extract the skills section"""
        match = re.search(r'\*\*SKILLS:\*\*\s*\n(.+?)$', text, re.DOTALL)
        print("SKILLS")
        print(match.group(1).strip())
        if match:
            return match.group(1).strip()
        return ""

    def _clean_text(self, text: str) -> str:
        """Clean and escape text for LaTeX"""
        # Remove ** bold markers (we'll handle them separately)
        # Escape special LaTeX characters
        text = text.replace('&', r'\&')
        text = text.replace('%', r'\%')
        text = text.replace('$', r'\$')
        text = text.replace('#', r'\#')
        text = text.replace('_', r'\_')
        text = text.replace('{', r'\{')
        text = text.replace('}', r'\}')
        text = text.replace('~', r'\textasciitilde{}')
        text = text.replace('^', r'\textasciicircum{}')

        # Handle special unicode characters
        text = text.replace('–', '--')  # en dash
        text = text.replace('—', '---')  # em dash
        text = text.replace(''', "'")   # smart quote
        text = text.replace(''', "'")   # smart quote
        text = text.replace('"', '``')  # smart quote
        text = text.replace('"', "''")  # smart quote
        text = text.replace('•', r'$\bullet$')  # bullet
        
        return text
    
    def _format_experience_section(self, experience_text: str) -> str:
        """Format the experience section for LaTeX"""
        if not experience_text:
            return ""

        # Split by company (each starts with **)
        companies = re.split(r'\n\s*\n(?=\s*\*\*[A-Z])', experience_text)

        latex_output = ""
        for company_block in companies:
            company_block = re.sub(r'^\s+', '', company_block, flags=re.MULTILINE)
            if not company_block.strip():
                continue

            lines = company_block.strip().split('\n')

            # First line: **Company Name** | Description
            if lines:
                company_line = lines[0].replace('**', '') if lines[0].startswith('**') else lines
                parts = [p.strip() for p in company_line.split('|')]
                company_name = parts[0] if parts else ""
                company_desc = parts[1] if len(parts) > 1 else ""

                latex_output += f"\\noindent\\textbf{{{self._clean_text(company_name)}}}"
                if company_desc:
                    latex_output += f" | \\textit{{{self._clean_text(company_desc)}}}"
                latex_output += "\\\\\n"

            # Second line: **Job Title** | Dates
            if len(lines) > 1:
                title_line = lines[1].replace('**', '') if lines[0].startswith('**') else lines
                parts = [p.strip() for p in title_line.split('|')]
                job_title = parts[0] if parts else ""
                dates = parts[1] if len(parts) > 1 else ""

                latex_output += f"\\textit{{{self._clean_text(job_title)}}}"
                if dates:
                    latex_output += f" \\\\\n\\hfill {self._clean_text(dates)}"
                latex_output += "\\\\\n"

            # Bullet points (start with *)
            bullets = [line for line in lines[2:] if line.strip().startswith('*')]

            if bullets:
                latex_output += "\\begin{itemize}\n"
                for bullet in bullets:
                    # Remove the leading *
                    bullet_text = bullet.strip()[1:].strip()
                    latex_output += f"  \\item {self._clean_text(bullet_text)}\n"
                latex_output += "\\end{itemize}\n"

            latex_output += "\\vspace{0.15in}\n\n"

        return latex_output

    def _format_skills_section(self, skills_text: str) -> str:
        """Format the skills section for LaTeX"""
        if not skills_text:
            return ""
        skills_text = re.sub(r'^\s+', '', skills_text, flags=re.MULTILINE)
        # Skills are in format: **Category:** skill1, skill2, skill3
        categories = re.findall(r'\*\*([^:]+):\*\*([^\n]+)', skills_text)

        latex_output = ""

        for category, skills in categories:
            category_clean = self._clean_text(category.strip())
            skills_clean = self._clean_text(skills.strip())

            latex_output += f"\\noindent\\textbf{{{category_clean}:}} {skills_clean}\n\n"

        return latex_output

    def _build_latex_document(self, headline: str, summary: str, experience: str, skills: str) -> str:
        """Build the complete LaTeX document"""
        
        doc = r"""\documentclass[11pt,letterpaper]{article}

% Packages
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{geometry}
\usepackage{enumitem}
\usepackage{hyperref}
\usepackage{titlesec}

% Page setup
\geometry{top=0.75in, bottom=0.75in, left=0.75in, right=0.75in}
\pagestyle{empty}
\setlist{noitemsep, topsep=2pt, parsep=0pt, leftmargin=*}

% Hyperlink setup
\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    urlcolor=blue
}

% Section formatting
\titleformat{\section}
  {\Large\bfseries}{}{0em}{}[\titlerule]
\titlespacing*{\section}{0pt}{10pt}{6pt}

\begin{document}

% Header
\begin{center}
{\Huge\bfseries Your Name}
\end{center}

\begin{center}
your\_email@example.com $\mid$ +1-XXX-XXX-XXXX $\mid$ Your Location $\mid$ LinkedIn: your\_profile $\mid$ GitHub: your\_profile
\end{center}

\vspace{0.1in}

% Headline
\begin{center}
\textit{"""
        
        doc += self._clean_text(headline)
        
        doc += r"""}
\end{center}

\vspace{0.1in}

% Professional Summary
\section*{Professional Summary}
"""
        
        doc += self._clean_text(summary) + "\n\n"
        
        doc += r"""% Professional Experience
\section*{Professional Experience}
"""
        
        doc += self._format_experience_section(experience)
        
        doc += r"""% Skills
\section*{Skills}
"""
        
        doc += self._format_skills_section(skills)
        
        doc += r"""
\end{document}"""
        
        return doc