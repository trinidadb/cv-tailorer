LATEX_TEMPLATE = r"""\documentclass[11pt,a4paper,sans]{moderncv}

% ModernCV theme
\moderncvstyle{classic}
\moderncvcolor{blue}

% Character encoding
\usepackage[utf8]{inputenc}

% Adjust page margins
\usepackage[scale=0.85]{geometry}

% Personal data
\name{{{first_name}}}{{{last_name}}}
\phone[mobile]{{{phone}}}
\email{{{email}}}
\social[linkedin]{{{linkedin}}}
\address{{{location}}}

\begin{document}

\makecvtitle

% Professional Summary
\section{Professional Summary}
{summary}

% Skills
\section{Skills}
{skills}

% Professional Experience
\section{Professional Experience}
{experience}

\end{document}
"""
