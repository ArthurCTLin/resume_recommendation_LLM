from sentence_transformers import util

def compute_similarity(resume_embeds, jd_embeds):
    expected_sections = ["Experience & Achievements", "Skills & Competencies", "Culture Fit", "Personal Traits", "Education"]

    similarity_scores = {}

    for section in expected_sections:
        if section in resume_embeds and section in jd_embeds:
            similarity_scores[section] = float(util.cos_sim(resume_embeds[section], jd_embeds[section]))
        else:
            resume_values = list(resume_embeds.values())
            jd_values = list(jd_embeds.values())

            if len(resume_values) == len(jd_values):
                resume_section_idx = expected_sections.index(section)
                similarity_scores[section] = float(util.cos_sim(resume_values[resume_section_idx], jd_values[resume_section_idx]))

    return similarity_scores
