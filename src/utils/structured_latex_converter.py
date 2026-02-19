"""
LaTeX Converter - Converts structured TailoredResume (Pydantic) to LaTeX format
Works with the structured output from GeminiClient using the TailoredResume schema.
"""

from src.config.schemas import PersonalInfo

LATEX_SPECIAL_CHARS = str.maketrans({
    "&":  r"\&",
    "%":  r"\%",
    "$":  r"\$",
    "#":  r"\#",
    "_":  r"\_",
    "{":  r"\{",
    "}":  r"\}",
    "~":  r"\textasciitilde{}",
    "^":  r"\textasciicircum{}",
    # Typographic quotes → LaTeX equivalents
    "\u2018": "`",
    "\u2019": "'",
    "\u201C": "``",
    "\u201D": "''",
    # Dashes
    "\u2013": "--",
    "\u2014": "---",
    # Bullet (just in case)
    "\u2022": r"$\bullet$",
})


class StructuredLaTeXConverter:
    """
    Converts a TailoredResume Pydantic object into a compilable LaTeX document.
    No regex parsing needed — data comes in clean from the structured LLM output.
    """

    def clean(self, text: str) -> str:
        """Escape special LaTeX characters in a string."""
        return text.translate(LATEX_SPECIAL_CHARS)

    def _build_experience(self, experience: list) -> str:
        """Render the professional experience entries."""
        lines = []
        for entry in experience:
            company   = self.clean(entry.company)
            location  = self.clean(entry.location)
            job_title = self.clean(entry.job_title)
            start     = self.clean(entry.start_date)
            end       = self.clean(entry.end_date)

            # Company + location on one line, dates flush-right
            lines.append(
                rf"\noindent\textbf{{{job_title}}} \hfill \textit{{{location}}}\\"
            )
            lines.append(
                rf"\textit{{{company}}} \hfill {start} -- {end}\\"
            )
            lines.append(r"\vspace{2pt}")

            # Bullet tasks
            lines.append(r"\begin{itemize}")
            for task in entry.tasks:
                lines.append(rf"  \item {self.clean(task)}")
            lines.append(r"\end{itemize}")
            lines.append(r"\vspace{0.12in}")
            lines.append("")  # blank line between entries

        return "\n".join(lines)

    def _build_skills(self, skills: list) -> str:
        """Render the skills section as category: skill1, skill2, ... lines."""
        lines = []
        for entry in skills:
            category   = self.clean(entry.category_name)
            skill_list = ", ".join(self.clean(s) for s in entry.skills)
            lines.append(rf"\noindent\underline{{\textbf{{{category}:}}}} {skill_list}")
            lines.append("")  # blank line between categories
        return "\n".join(lines)

    def convert(self, resume, personal_info: PersonalInfo = None) -> str:
        """
        Convert a TailoredResume Pydantic object to a LaTeX string.

        Args:
            resume:        TailoredResume instance (structured LLM output).
            personal_info: Optional dict with keys: name, email, phone,
                           location, linkedin, github. Falls back to
                           placeholder values when not provided.
        Returns:
            A complete LaTeX document as a string.
        """
        info = personal_info or PersonalInfo()
        name     = self.clean(info.name or "Your Name")
        email    = self.clean(info.email or "youremail@example.com")
        location = self.clean(info.location or "Your Location")
        linkedin = self.clean(info.linkedin or "yourlinkedin")
        github   = self.clean(info.github or "yourgithub")

        headline    = self.clean(resume.headline)
        summary     = self.clean(resume.professional_summary)
        experience  = self._build_experience(resume.professional_experience)
        skills      = self._build_skills(resume.skills)

        doc = rf"""\documentclass[11pt,letterpaper]{{article}}

% Packages
\usepackage[utf8]{{inputenc}}
\usepackage[T1]{{fontenc}}
\usepackage{{geometry}}
\usepackage{{enumitem}}
\usepackage{{hyperref}}
\usepackage{{titlesec}}
\usepackage{{amsmath}}

% Page setup
\geometry{{top=0.75in, bottom=0.75in, left=0.75in, right=0.75in}}
\pagestyle{{empty}}
\setlist{{noitemsep, topsep=2pt, parsep=0pt, leftmargin=*}}

% Hyperlink setup
\hypersetup{{
    colorlinks=true,
    linkcolor=blue,
    urlcolor=blue
}}

% Section formatting
\titleformat{{\section}}
  {{\Large\bfseries}}{{}}{{0em}}{{}}[\titlerule]
\titlespacing*{{\section}}{{0pt}}{{10pt}}{{6pt}}

\begin{{document}}

% ── Header ───────────────────────────────────────────────────────────
\begin{{center}}
{{\huge\bfseries {name}}}
\end{{center}}

% ── Headline ─────────────────────────────────────────────────────────
\begin{{center}}
\large\text{{{headline}}}
\end{{center}}

% ── Contact Infomation ─────────────────────────────────────────────────────────
\begin{{center}}
\contact{{
\textit{{
  \href{{mailto:{email}}}{{{email}}} $\mid$
  {location} $\mid$ 
  \href{{https://linkedin.com/in/{linkedin}}}{{linkedin.com/in/{linkedin}}} $\mid$ 
  \href{{https://github.com/{github}}}{{github.com/{github}}}
}}}}
\end{{center}}

\vspace{{0.1in}}

% ── Professional Summary ──────────────────────────────────────────────
\section*{{Professional Summary}}
{summary}

% ── Professional Experience ───────────────────────────────────────────
\section*{{Professional Experience}}
{experience}
% ── Skills ───────────────────────────────────────────────────────────
\section*{{Skills}}
{skills}
\end{{document}}
"""
        return doc
