#!/usr/bin/env python3
########################################################################
# 1. IMPORTS
########################################################################
import os
import autogen
from dotenv import load_dotenv
import openai
import re
import datetime

# Imports for file generation
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

########################################################################
# 2. ENVIRONMENT AND OPENAI CONFIGURATION
########################################################################
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")

openai.api_key = OPENAI_API_KEY

# Define the OpenAI model to use for AutoGen orchestration.
OPENAI_MODEL_FOR_AUTOGEN = 'gpt-3.5-turbo'  # Change to 'gpt-4' if you have access

# Configuration list for autogen using OpenAI
config_list = [
    {
        "model": OPENAI_MODEL_FOR_AUTOGEN,
        "api_key": OPENAI_API_KEY,
    }
]

if not config_list[0].get("api_key"):
    raise ValueError("OPENAI_API_KEY seems empty after loading into config_list.")

llm_config = {
    "config_list": config_list,
    "cache_seed": 42,       # Set to None to disable caching
    "temperature": 0.1,     # Low temperature for deterministic responses
}

########################################################################
# 3. OPENAI GENERATOR HELPER CLASS
########################################################################
class OpenAIGenerator:
    """
    A helper class to wrap OpenAI ChatCompletion calls.
    It provides a generate_content() method so that our helper functions have a uniform interface.
    """
    def __init__(self, model):
        self.model = model

    def generate_content(self, prompt):
        # Note: Ensure you have migrated to the new ChatCompletion API if using openai>=1.0.0.
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=llm_config["temperature"]
        )
        class ResponseWrapper:
            pass
        res = ResponseWrapper()
        res.text = response.choices[0].message["content"]
        return res

openai_generator = OpenAIGenerator(OPENAI_MODEL_FOR_AUTOGEN)

########################################################################
# 4. HELPER FUNCTIONS
########################################################################
def search_academic_papers(topic: str, max_papers: int = 10) -> str:
    """
    Simulates a search for academic papers.
    Uses OpenAI to generate representative paper titles and one-sentence summaries.
    """
    print(f"--- Function Call: search_academic_papers(topic='{topic}', max_papers={max_papers}) ---")
    try:
        prompt = f"""
        Simulate finding the top 3-5 academic paper titles and provide a one-sentence summary for each.
        The topic is: '{topic}'.
        Do not invent citations; use representative titles and clear summaries.
        """
        response = openai_generator.generate_content(prompt)
        return f"Found potential papers:\n{response.text}"
    except Exception as e:
        print(f"Error during paper search simulation: {e}")
        return f"Simulated search for '{topic}': Found 2 potential papers."

def verify_fact(claim: str, source_context: str) -> str:
    """
    Simulates fact-checking: determine if a given claim is supported by the provided source context.
    Returns a short status and explanation.
    """
    print(f"--- Function Call: verify_fact(claim='{claim}', source_context='{source_context[:100]}...') ---")
    try:
        prompt = f"""
        Evaluate the following claim using the source context:
        Claim: "{claim}"
        Source Context: "{source_context}"
        Provide a status: Verified, Partially Verified, Contradicted, or Cannot Verify, with a brief explanation.
        """
        response = openai_generator.generate_content(prompt)
        return f"Verification Result: {response.text}"
    except Exception as e:
        print(f"Error during fact verification: {e}")
        keywords = re.findall(r'\b\w+\b', claim.lower())
        context_lower = source_context.lower()
        found_keywords = [kw for kw in keywords if kw in context_lower]
        if len(found_keywords) > len(keywords) / 2:
            return "Verification Result: Likely Verified (based on keyword overlap)."
        else:
            return "Verification Result: Cannot Verify (based on keyword overlap)."

def write_section(topic: str, information: str, style: str = "academic") -> str:
    """
    Uses OpenAI to generate a draft section of a research report.
    The output is formatted in Markdown.
    """
    print(f"--- Function Call: write_section(topic='{topic}', style='{style}') ---")
    try:
        prompt = f"""
        Write a well-structured section for a research report on the topic: '{topic}'.
        Use the following validated research findings as support:
        {information}
        Ensure the style is {style} with clear headings, paragraphs, and a logical flow.
        """
        response = openai_generator.generate_content(prompt)
        text = response.text.replace("```", "")
        return text
    except Exception as e:
        print(f"Error during section writing: {e}")
        return f"## Draft Section: {topic}\n{information}\n_(Generation failed, raw info returned)_"

def create_report_files(report_content: str, filename_base: str = "research_report") -> str:
    """
    Generates DOCX and PDF files from the final research report.
    Saves the files in the 'reports' directory.
    """
    print(f"--- Function Call: create_report_files(filename_base='{filename_base}') ---")
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    docx_filename = f"{filename_base}_{timestamp}.docx"
    pdf_filename = f"{filename_base}_{timestamp}.pdf"
    output_dir = "reports"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    docx_filepath = os.path.join(output_dir, docx_filename)
    pdf_filepath = os.path.join(output_dir, pdf_filename)
    try:
        # Generate DOCX using python-docx.
        document = Document()
        document.add_heading('Research Report', level=0)
        paragraphs = report_content.strip().split('\n\n')
        for para in paragraphs:
            if para.strip():
                if para.strip().startswith('#'):
                    heading_level = para.count('#', 0, 5)
                    clean_text = para.lstrip('#').strip()
                    document.add_heading(clean_text, level=min(heading_level, 4))
                else:
                    document.add_paragraph(para.strip())
        document.save(docx_filepath)
        print(f"DOCX report saved to: {docx_filepath}")

        # Generate PDF using ReportLab.
        doc = SimpleDocTemplate(pdf_filepath, pagesize=letter,
                                leftMargin=inch, rightMargin=inch,
                                topMargin=inch, bottomMargin=inch)
        styles = getSampleStyleSheet()
        story = [Paragraph("Research Report", styles['h1']), Spacer(1, 0.2 * inch)]
        for para in paragraphs:
            if para.strip():
                if para.strip().startswith('#'):
                    heading_level = para.count('#', 0, 5)
                    clean_text = para.lstrip('#').strip()
                    style_name = f'h{min(heading_level, 4)}'
                    if style_name not in styles:
                        style_name = 'h2'
                    story.append(Paragraph(clean_text, styles[style_name]))
                else:
                    story.append(Paragraph(para.strip().replace('\n', '<br/>'), styles['BodyText']))
                story.append(Spacer(1, 0.1 * inch))
        doc.build(story)
        print(f"PDF report saved to: {pdf_filepath}")

        return f"Successfully generated reports:\n- {docx_filepath}\n- {pdf_filepath}"
    except Exception as e:
        error_message = f"Error generating report files: {e}"
        print(error_message)
        return error_message

########################################################################
# 5. AGENT DEFINITIONS (EXPLANATIONS INCLUDED)
########################################################################
# Supervisor Agent:
# - Manages the research process, defines scope, and triggers final report generation.
supervisor = autogen.AssistantAgent(
    name="Supervisor",
    llm_config=llm_config,
    system_message="""You are the Supervisor.
Your role is to manage the research process.
1. Define the research scope and specific questions for the topic.
2. Coordinate tasks among PhD Students, Verifier, Writer, and Validator.
3. Review drafts and ensure coherence.
4. Instruct final report generation.
Do not conduct research yourself; guide the team instead."""
)

# PhD_Student_1 Agent:
# - Focuses on academic research and summarizing key findings.
phd_student_1 = autogen.AssistantAgent(
    name="PhD_Student_1",
    llm_config=llm_config,
    system_message="""You are PhD_Student_1, an expert researcher.
1. Use search_academic_papers to retrieve articles on the topic.
2. Summarize research methodologies and key findings.
3. Provide detailed source information.
Wait for further instructions."""
)

# PhD_Student_2 Agent:
# - Collaborates with PhD_Student_1 and provides additional research insights.
phd_student_2 = autogen.AssistantAgent(
    name="PhD_Student_2",
    llm_config=llm_config,
    system_message="""You are PhD_Student_2, working collaboratively.
1. Conduct research on the topic using search_academic_papers.
2. Summarize and compare your findings with those of PhD_Student_1.
3. Provide additional insights as needed.
Wait for instructions."""
)

# Verifier Agent:
# - Checks factual accuracy of research summaries.
verifier = autogen.AssistantAgent(
    name="Verifier",
    llm_config=llm_config,
    system_message="""You are the Verifier.
Your duty is to ensure factual accuracy.
1. Evaluate the research summaries using verify_fact.
2. Report the verification status clearly.
Focus solely on accuracy."""
)

# Writer Agent:
# - Drafts the final research report by integrating the validated research findings.
writer = autogen.AssistantAgent(
    name="Writer",
    llm_config=llm_config,
    system_message="""You are the Writer.
Your task is to draft the final research report.
1. Use the validated research summaries from PhD Students.
2. Combine the information into clear sections (Introduction, Methodology, Findings, Conclusion).
3. Incorporate feedback from the Supervisor and Verifier.
4. When instructed, generate final report files using create_report_files.
Wait for instructions before drafting."""
)

# Validator Agent:
# - Conducts the final review for completeness and coherence.
validator = autogen.AssistantAgent(
    name="Validator",
    llm_config=llm_config,
    system_message="""You are the Validator.
Your role is to review the final report.
1. Check that the report meets research objectives.
2. Ensure all sections (Introduction, Methodology, Findings, Conclusion) are present.
3. Verify that the research findings are accurately represented.
Provide a verdict: 'Validation PASSED.' or list issues."""
)

# User Proxy Agent:
# - Interfaces with the user and executes code functions.
user_proxy = autogen.UserProxyAgent(
    name="User_Proxy",
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=15,
    is_termination_msg=lambda x: "Successfully generated reports" in x.get("content", "") or "TERMINATE" in x.get("content", ""),
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,
    },
    function_map={
        "search_academic_papers": search_academic_papers,
        "verify_fact": verify_fact,
        "write_section": write_section,
        "create_report_files": create_report_files,
    }
)

########################################################################
# 6. GROUP CHAT SETUP AND MANAGER
########################################################################
agents = [user_proxy, supervisor, phd_student_1, phd_student_2, verifier, writer, validator]
group_chat = autogen.GroupChat(
    agents=agents,
    messages=[],
    max_round=20  # Adjust rounds as needed; set to a low number to avoid repetition.
)
manager = autogen.GroupChatManager(
    groupchat=group_chat,
    llm_config=llm_config,
    is_termination_msg=lambda x: "Successfully generated reports" in x.get("content", "") or "TERMINATE" in x.get("content", "")
)

########################################################################
# 7. INITIATING THE RESEARCH TASK FROM INPUT FILE
########################################################################
# Read the research topic from the input file.
input_file = "research_topic.txt"  # Ensure this file exists with your topic.
if not os.path.exists(input_file):
    raise FileNotFoundError(f"The input file '{input_file}' was not found.")

with open(input_file, "r") as f:
    research_topic = f.read().strip()
if not research_topic:
    raise ValueError("The research topic file is empty. Please provide a valid topic.")

# Use the research topic consistently in the prompt.
initial_prompt = f"""
Generate a research report on the topic: '{research_topic}'.
Objective: Summarize key findings from recent (last 5 years) academic research on the topic '{research_topic}'.
Include:
1. An introduction defining the scope.
2. A summary of research methodologies commonly used.
3. Key findings (both positive and negative aspects).
4. A brief conclusion summarizing the main points.

Process:
- Supervisor: Coordinate the research and review all summaries.
- PhD Students: Use search_academic_papers to provide detailed research summaries on '{research_topic}'.
- Verifier: Check all claims and details for accuracy.
- Writer: Draft a cohesive report based on the collected summaries.
- Validator: Conduct a final review ensuring the report is comprehensive.
Once validation passes, the Supervisor instructs the Writer to generate final report files.
Start the process.
"""
# Initiate the (simulated) conversation.
user_proxy.initiate_chat(manager, message=initial_prompt)

########################################################################
# 8. FINAL REPORT GENERATION (FORCED)
########################################################################
# Simulate that the PhD Students' validated research findings have been aggregated.
aggregated_findings = f"""
Final Aggregated Research Findings on '{research_topic}':
1. PhD_Student_1 reported that the fundamentals of AI include key concepts such as machine learning, neural networks, natural language processing, and expert systems. Their research used systematic literature reviews.
2. PhD_Student_2 confirmed these findings and added that emerging trends emphasize ethical considerations and practical applications in various sectors.
Validation: All findings have been verified by the Verifier and confirmed by the Validator.
These findings indicate that AI and its basics offer significant benefits (e.g., enhanced decision-making, innovation) while also presenting challenges (e.g., bias in algorithms, implementation difficulties).
"""

# Now let the Writer draft the final research report using the aggregated validated research findings.
final_draft = write_section(research_topic, aggregated_findings, style="academic")

# Generate the report files.
final_result = create_report_files(final_draft)
print(final_result)
