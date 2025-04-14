Absolutely! Here's the **perfectly formatted** `README.md` just like you asked:

---

# AI Research Report Generator

This project is a Python-based multi-agent simulation that generates a detailed research report on a topic you provide. Agents collaborate to gather information, verify facts, draft the report, and export it to DOCX and PDF formats automatically.

---

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Troubleshooting](#troubleshooting)
- [License](#license)
- [Final Notes](#final-notes)

---

## Features

- **Multi-Agent Collaboration:** Supervisor, PhD Students, Verifier, Writer, and Validator agents simulate a real research workflow.
- **Dynamic Research Topics:** Specify any research topic via an input file (`research_topic.txt`).
- **OpenAI GPT Integration:** Use GPT-3.5-turbo (or GPT-4) for content generation, summarization, and verification.
- **Automatic Report Generation:** Creates structured reports in both DOCX and PDF formats inside a `reports/` folder.
- **Error Handling and Forced Termination:** Ensures conversation does not loop indefinitely.

---

## Prerequisites

- **Python 3.8+**
- **OpenAI API Key**
- Packages:
  - `openai`
  - `python-dotenv`
  - `python-docx`
  - `reportlab`
  - `autogen`

---

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-username/ai-research-report-generator.git
   cd ai-research-report-generator
   ```

2. **Create and Activate a Virtual Environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate        # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies:**

   If you have a `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

   Or install manually:

   ```bash
   pip install openai python-dotenv python-docx reportlab autogen
   ```

4. **Set Up Environment Variables:**

   Create a `.env` file in the root directory:

   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

5. **Prepare the Research Topic Input File:**

   Create a file named `research_topic.txt` with the topic:

   ```txt
   Ai and its basics
   ```

---

## Project Structure

```bash
ai-research-report-generator/
├── app.py               # Main script with agent orchestration and report generation
├── research_topic.txt   # Input file specifying the research topic
├── .env                 # Environment variables (API key)
├── reports/             # Output directory for generated reports
├── README.md            # Project documentation
└── requirements.txt     # List of dependencies (optional)
```

---

## Configuration

- **OpenAI API Key:**  
  Set your API key in the `.env` file.

- **Model Selection:**  
  You can change the model by setting the `OPENAI_MODEL_FOR_AUTOGEN` variable in `app.py` to `'gpt-3.5-turbo'` or `'gpt-4'`.

- **Conversation Rounds:**  
  The group chat is limited to `max_round = 15` to prevent infinite loops. You can adjust this in `app.py`.

- **Temperature Setting:**  
  The OpenAI API call uses a low temperature (`0.1`) for more deterministic and factual responses.

---

## Usage

1. Ensure Python, all dependencies, `.env`, and `research_topic.txt` are properly set up.

2. Run the main script:

   ```bash
   python app.py
   ```

3. **Output:**
   - The script will simulate a multi-agent conversation.
   - Final validated research findings will be compiled.
   - The final research report will be saved in **DOCX** and **PDF** formats inside the `reports/` folder.

4. **Check the Console:**
   - The console will display the paths where the reports are saved.

---

## How It Works

1. **Initialization:**
   - Loads your OpenAI API key.
   - Configures the GPT model and helper functions.

2. **Helper Functions:**
   - `search_academic_papers`: Simulates academic research.
   - `verify_fact`: Fact-checks research claims.
   - `write_section`: Structures and writes report sections.
   - `create_report_files`: Exports the final document.

3. **Agent Definitions:**
   - **Supervisor:** Manages the workflow.
   - **PhD Students:** Search and summarize papers.
   - **Verifier:** Checks factual accuracy.
   - **Writer:** Drafts the final report.
   - **Validator:** Final review for completeness.
   - **User Proxy:** Controls the overall process and triggers code functions.

4. **Group Chat Simulation:**
   - Agents collaborate through `GroupChatManager`.
   - Conversation is limited to 15 rounds for efficiency.

5. **Final Report Generation:**
   - Aggregated findings are passed to the Writer.
   - The report is generated and saved in both `.docx` and `.pdf` formats.

---

## Troubleshooting

- **OpenAI Migration Error:**

  If you get an error about `openai.ChatCompletion` not being supported:

  ```bash
  pip install openai==0.28
  ```

  Or run:

  ```bash
  openai migrate
  ```

- **Missing Environment Variables:**

  Ensure `.env` exists and contains a valid `OPENAI_API_KEY`.

- **No Output Files:**

  Make sure the `reports/` folder exists and is writable.

  Ensure the `research_topic.txt` file has valid content.

- **Conversation Looping:**

  If the simulation loops endlessly, adjust `max_round` or manually terminate after report generation.

---

## License

This project is licensed under the MIT License.  
See the [LICENSE](LICENSE) file for more information.

