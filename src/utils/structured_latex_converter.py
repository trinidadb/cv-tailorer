"""
LaTeX Converter - Converts structured TailoredResume (Pydantic) to LaTeX format
Works with the structured output from GeminiClient using the TailoredResume schema.
"""
from src.config.constants import ValidLanguages
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

    def __init__(self, language: ValidLanguages = ValidLanguages.EN):
        self.english = (language == ValidLanguages.EN)

    def clean(self, text: str) -> str:
        """Escape special LaTeX characters in a string."""
        return text.translate(LATEX_SPECIAL_CHARS)

    COMPANY_SUFFIXES_EN = {
        0: "| Research & Consulting Organization",
        1: "| USA's Largest Financial Services Provider",
    }

    COMPANY_SUFFIXES_ES = {
        0: "| Empresa de consultoria e investigación",
        1: "| Empresa líder global en servicios financieros",
    }

    def _build_education_en(self) -> str:
        return r"""
\noindent\textbf{Master in Smart Systems} \hfill \textit{Spain}\\
\textit{University of Salamanca} \hfill 10/2023 -- 10/2024\\
\textit{GPA: 9.0/10}
\begin{itemize}
  \item Specialization: Machine Learning, Deep Learning, Statistics, Data Mining, Data Science, Data Visualization, Econometrics
  \item Thesis: ``Application of Convolutional Neural Networks in bioacoustics analysis''
\end{itemize}
\vspace{0.1in}

\noindent\textbf{Electronic Engineering} \hfill \textit{Argentina}\\
\textit{Catholic University of Argentina (UCA)} \hfill 03/2016 -- 07/2022\\
\text{GPA: 8.9/10}
\begin{itemize}
  \item Quantitative curriculum including Applied Mathematics, Operations Research, Statistics, Systems Engineering
  \item Thesis: ``Image stabilizer system -- application of the Kalman Filter using dual-core DSP''
\end{itemize}
"""

    def _build_education_es(self) -> str:
        return r"""
\noindent\textbf{Master en Sistemas Inteligentes} \hfill \textit{Spain}\\
\textit{University of Salamanca} \hfill 10/2023 -- 10/2024\\
\textit{GPA: 9.0/10}
\begin{itemize}
  \item Especialización: Machine Learning, Deep Learning, Estadística, Data Mining, Data Science, Data Visualization, Econometrics
  \item Tesis: ``Aplicación de redes CNN en el analisis de señales bioacústicas (abejas)''
\end{itemize}
\vspace{0.1in}

\noindent\textbf{Ingeniería Electrónica} \hfill \textit{Argentina}\\
\textit{Pontificia Universidad Católica Argentina (UCA)} \hfill 03/2016 -- 07/2022\\
\text{GPA: 8.9/10}
\begin{itemize}
  \item Plan de estudios cuantitativo que incluye matemáticas aplicadas, investigación operativa, estadística e ingeniería de sistemas
  \item Tesis: ``Sistema estabilizador de imagen: aplicación del filtro de Kalman utilizando DSP de doble núcleo''
\end{itemize}
"""

    def _build_awards_en(self) -> str:
        return r"""
\begin{itemize}
  \item Winner -- Argentine Association of Control's National Thesis Contest (2023)
  \item Recognition from Microchip Technology and MC Electronics for thesis excellence (2023)
  \item PRIUNES Scholarship to study at the Catholic University of Argentina (2016)
\end{itemize}
"""

    def _build_awards_es(self) -> str:
        return r"""
\begin{itemize}
  \item Ganadora del Concurso Nacional de Tesis de la Asociación Argentina de Control Automático (2023)
  \item Reconocimiento de Microchip Technology y MC Electronics por excelencia de la tesis (2023)
  \item Beca PRIUNES para el estudio en la Universidad Católica Argentina (2016)
\end{itemize}
"""

    def _build_courses_en(self) -> str:
        return r"""
\begin{itemize}
  \item AWS Certified Cloud Practitioner (2025)
  \item Generative AI with Large Language Models Specialization -- DeepLearning.AI & AWS (2025)
  \item Artificial neural networks: current models and the deep learning paradigm (2024)
  \item Introduction and Advanced Topics on Machine Learning (2022)
  \item Leading Digital Transformation - MIT with Santander Scholarship (2020)
  \item PMP Candidate - Project Management Professional (in progress)
\end{itemize}
"""

    def _build_experience(self, experience: list) -> str:
        """Render the professional experience entries."""
        lines = []
        for idx, entry in enumerate(experience):
            company   = self.clean(entry.company)
            location  = self.clean(entry.location)
            job_title = self.clean(entry.job_title)
            start     = self.clean(entry.start_date)
            end       = self.clean(entry.end_date)

            # Append hardcoded company suffix if defined
            suffix = self.COMPANY_SUFFIXES_EN.get(idx, "") if self.english else self.COMPANY_SUFFIXES_ES
            company_display = f"{company} {suffix}" if suffix else company

            # Company + location on one line, dates flush-right
            lines.append(
                rf"\noindent\textbf{{{job_title}}} \hfill \textit{{{location}}}\\"
            )
            lines.append(
                rf"\textit\textbf{{{{{company_display}}}}} \hfill {start} -- {end}\\"
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
        education   = self._build_education_en() if self.english else self._build_education_es()
        courses     = self._build_courses_en()
        awards      = self._build_awards_en()  if self.english else self._build_awards_es()

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
\section*{{{'Profile' if self.english else 'Perfil'}}}
{summary}

% ── Professional Experience ───────────────────────────────────────────
\section*{{{'Professional Experience' if self.english else 'Experiencia'}}}
{experience}

% ── Education ────────────────────────────────────────────────────────
\section*{{{'Education' if self.english else 'Educación'}}}
{education}

% ── Education ────────────────────────────────────────────────────────
\section*{{{'Certifications & Courses' if self.english else 'Cursos y Certificaciones'}}}
{courses}

% ── Awards \& Recognition ─────────────────────────────────────────────
\section*{{{'Awards \& Recognitions' if self.english else 'Premios \& Reconocimientos'}}}
{awards}
\end{{document}}

% ── Skills ───────────────────────────────────────────────────────────
\section*{{Skills}}
{skills}
"""
        return doc