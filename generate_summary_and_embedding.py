import re
from model import load_model 
from sentence_transformers import SentenceTransformer

def generate_summary(text, text_type='resume', llm=None):
    assert text_type in ["resume", "job_description"]

    label = "résumé" if text_type == "resume" else "job description"

    system_prompt = f"""
                You are a professional HR specialist.
                Please help the user analyze {label} and summarize them into readable and structured paragraphs.
                Summarize the {label} into five clearly labeled sections:
                - Experience & Achievements
                - Skills & Competencies
                - Culture Fit
                - Personal Traits
                - Education

                Each section should be written in natural, human-readable paragraphs suitable for comparison.

                **Experience & Achievements**: Focus on the key responsibilities, accomplishments, and results demonstrated in the {label}. Summarize the most impactful experiences and achievements that illustrate the candidate’s or position's value, including any major contributions, leadership, or problem-solving. Highlight any quantifiable results or outcomes.

                **Skills & Competencies**: List and explain the key technical and soft skills required or demonstrated in the {label}. Highlight how these skills were applied in practical contexts, and ensure they are tied to real-world achievements or job functions.

                **Culture Fit**:
                - For JD: Summarize the key cultural aspects and work environment requirements described in the job description. This could include the need for innovation, teamwork, adaptability, flexibility, and remote work capabilities.
                - For Resume: Summarize the candidate’s work preferences, including ideal work environments, preferred working styles (e.g., remote, hybrid), and any personal values or principles that align with the company culture.

                **Personal Traits**:
                - For JD: Identify any specific personality traits or behavioral characteristics that the job description emphasizes. This could include things like leadership potential, communication skills, ability to work under pressure, creativity, adaptability, and any other personal qualities the company values.
                - For Resume: Summarize the candidate's self-described personality traits or any references to their behavior, character, and how they approach challenges. This could include their ability to collaborate, take initiative, handle conflict, or lead teams.

                **Education**:
                - For JD: Summarize any specific educational requirements or qualifications listed in the job description. This could include the necessary degree, certifications, or other academic credentials.
                - For Resume: Summarize the candidate’s educational background, including degrees, relevant coursework, academic honors, or other achievements. Highlight how the education relates to the position or demonstrates key qualifications.


                Each section should be clearly defined and written in a way that makes it easy for a reader to compare key elements across different résumés or job descriptions.

                Please ensure that the sections are structured, informative, and concise. Avoid bullet points or lists, and focus on clarity and coherence in your writing.
                """

    user_input = f"""
                Please analyze the following {label} and provide summaries in paragraph form.

                {label.capitalize()}:
                """ + text

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input},
    ]

    output = llm(messages, max_new_tokens=1024)[0]["generated_text"][-1]["content"].strip()
    return output

def extract_section_text(summary_text):
    sections = re.split(r"\*\*([A-Za-z& ]+)\*\*", summary_text)
    section_dict = {}
    for i in range(1, len(sections)-1, 2):
        section_title = sections[i].strip()
        section_content = sections[i+1].strip()
        section_dict[section_title] = re.sub(r"^.*:\s*", "", section_content)
    return section_dict

def generate_summary_and_embedding(text, text_type="resume", model_id="sentence-transformers/all-MiniLM-L6-v2", llm_model=None, pipe=None):
    if pipe is None:
        pipe = load_model(model_path=llm_model)
    embedder = SentenceTransformer(model_id)

    summary = generate_summary(text, text_type, llm=pipe)
    section_texts = extract_section_text(summary)

    embeddings = {
        section: embedder.encode(content, convert_to_tensor=True)
        for section, content in section_texts.items()
    }

    return embeddings, section_texts
