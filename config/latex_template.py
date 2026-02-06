
LATEX_TEMPLATE = r"""\documentclass[11pt,letterpaper]{{article}}

% Packages
\usepackage[utf8]{{inputenc}}
\usepackage[T1]{{fontenc}}
\usepackage{{geometry}}
\usepackage{{enumitem}}
\usepackage{{hyperref}}
\usepackage{{titlesec}}

% Page setup
\geometry{{top=0.75in, bottom=0.75in, left=0.75in, right=0.75in}}
\pagestyle{{empty}}
\setlist{{noitemsep, topsep=0pt}}

% Hyperlink setup
\hypersetup{{
    colorlinks=true,
    linkcolor=blue,
    urlcolor=blue,
    citecolor=blue
}}

% Section formatting
\titleformat{{\section}}
  {{\Large\bfseries}}{{}}{{0em}}{{}}[\titlerule]
\titlespacing*{{\section}}{{0pt}}{{8pt}}{{4pt}}

% Custom commands
\newcommand{{\name}}[1]{{\begin{{center}}{{\Huge\bfseries #1}}\end{{center}}}}
\newcommand{{\contact}}[1]{{\begin{{center}}#1\end{{center}}}}
\newcommand{{\job}}[4]{{%
  \noindent\textbf{{#1}} \hfill #2 \\
  \textit{{#3}} \hfill #4
}}

\begin{{document}}

% Header
\name{{{first_name} {last_name}}}
\contact{{
  {phone} $\mid$ 
  \href{{mailto:{email}}}{{{email}}} $\mid$ 
  \href{{https://linkedin.com/in/{linkedin}}}{{linkedin.com/in/{linkedin}}} $\mid$ 
  {location}
}}

\vspace{{0.2in}}

% Professional Summary
\section*{{Professional Summary}}
{summary}

% Skills
\section*{{Skills}}
{skills}

% Professional Experience
\section*{{Professional Experience}}
{experience}

\end{{document}}
"""