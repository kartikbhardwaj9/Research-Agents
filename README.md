# AI Research Report Generator

This repository contains a Python-based multi-agent research report generator. The system uses OpenAI's GPT models (via the new ChatCompletion API) to simulate a group discussion among agents (Supervisor, PhD Students, Verifier, Writer, Validator, and a User Proxy) that collectively produce a comprehensive research report on a topic specified by the user through an input file.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Overview

This project simulates a collaborative research process in which multiple agents interact to gather, verify, and draft a research report. The final report is automatically saved in both DOCX and PDF formats in the `reports` folder. The topic for the research report is dynamically read from an input file named `research_topic.txt`.

## Features

- **Multi-Agent Simulation:**  
  Multiple agents (Supervisor, two PhD Students, Verifier, Writer, Validator) work together to produce a research report.
- **Dynamic Input Topic:**  
  The research topic is read from a file (`research_topic.txt`), ensuring the report is based on user-specified topics.
- **OpenAI Integration:**  
  Uses OpenAI's GPT-3.5-turbo (or GPT-4 if available) to simulate research activities and generate report sections.
- **Report File Generation:**  
  The final research report is output as both DOCX and PDF files in the `reports` directory.
- **Automated Finalization:**  
  The system forces final report generation after a set number of conversation rounds to avoid infinite loops.

## Prerequisites

- **Python 3.8 or higher**  
- A valid **OpenAI API key**
- Required Python packages:
  - `openai`
  - `python-dotenv`
  - `autogen` (or the version compatible with your usage)
  - `python-docx`
  - `reportlab`
  - Other dependencies as needed (e.g., `re`, `datetime`)

## Installation

1. **Clone this repository:**

   ```bash
   git clone https://github.com/your-username/ai-research-report-generator.git
   cd ai-research-report-generator
Create and activate a virtual environment (optional but recommended):

bash
Copy
python -m venv venv
source venv/bin/activate   # On Windows use: venv\Scripts\activate
Install the required dependencies:

bash
Copy
pip install -r requirements.txt
If you do not have a requirements.txt, you can install the packages manually:

bash
Copy
pip install openai python-dotenv python-docx reportlab autogen
Set up environment variables:

Create a .env file in the root directory with the following content:

env
Copy
OPENAI_API_KEY=your_openai_api_key_here
Prepare the research topic input file:

Create a file named research_topic.txt in the root directory and add your desired research topic. For example:

txt
Copy
Ai and its basics
Project Structure
bash
Copy
ai-research-report-generator/
├── app.py                 # Main script containing the multi-agent simulation and final report generation
├── research_topic.txt     # Input file with the research topic
├── .env                   # Environment variables (contains OPENAI_API_KEY)
├── reports/               # Generated report files (DOCX and PDF)
├── README.md              # This file
└── requirements.txt       # List of dependencies (optional)
Configuration
OpenAI API Key:
Set in .env file as OPENAI_API_KEY.

Model Selection:
In app.py, the variable OPENAI_MODEL_FOR_AUTOGEN can be set to either 'gpt-3.5-turbo' or 'gpt-4' (if you have access).

Conversation Rounds:
The max_round for the group chat is set to 15 to avoid indefinite looping. You can adjust this value in the Group Chat Setup section.

Temperature:
The system uses a low temperature (0.1) for deterministic responses. This value is set in the llm_config dictionary.

Usage
Ensure the prerequisites are met (Python version, dependencies installed, .env and research_topic.txt in place).

Run the main script:

bash
Copy
python app.py
Output:

The script will simulate the agents’ conversation (limited to a single round or the specified number of rounds).

The final aggregated research findings will be used to generate the report.

The final report is saved as a DOCX and PDF file in the reports folder.

Check the console for the paths of the generated files.

How It Works
Initialization:
The script loads the OpenAI API key from the environment and sets up a global configuration for the GPT model.

Helper Functions:
Functions such as search_academic_papers, verify_fact, write_section, and create_report_files use OpenAI's GPT model to simulate research activities and generate formatted report sections and files.

Agent Definitions:
Several agents are defined:

Supervisor: Orchestrates the research process.

PhD_Student_1 & PhD_Student_2: Simulate research activities by providing summaries based on the input topic.

Verifier: Checks the accuracy of the research summaries.

Writer: Drafts the final research report using the aggregated findings.

Validator: Conducts the final review of the report.

User Proxy: Initiates the process and executes file generation.

Group Chat Simulation:
The agents are added to a group chat managed by GroupChatManager. The conversation rounds are limited to prevent indefinite looping.

Final Report Generation:
After simulating the research process, the validated aggregated research findings are passed to the Writer. The final report is generated via write_section and then saved as both DOCX and PDF using create_report_files.

Troubleshooting
OpenAI Migration Error:
If you see an error message about openai.ChatCompletion not being supported, either run the openai migrate command or pin your OpenAI package to an older version using:

bash
Copy
pip install openai==0.28
Refer to the OpenAI Python migration guide for more details.

Missing Environment Variables:
Ensure your .env file is present in the project root and includes a valid OPENAI_API_KEY.

No Output Files:
If no files appear in the reports folder, check the console output for error messages. Ensure the folder has proper write permissions and that the research topic file exists.

Conversation Looping:
The group chat is limited to a small number of rounds (max_round is set to 15). Adjust this value if needed, but note that the final report generation is forced after the conversation.

License
This project is licensed under the MIT License. See the LICENSE file for details.

pgsql
Copy

---

### Final Notes

- Modify the `README.md` as necessary to align with any changes made to the project.
- Ensure that all necessary files (such as the `.env` and `research_topic.txt`) are created before running the project.
- The README serves to explain the setup, configuration, usage, and troubleshooting steps in detail.

Save this file as `README.md` in your repository root, and it will guide users on how to run the project and understand its functionality.




Search

Deep research


ChatGPT can make mistakes. Check important info.
