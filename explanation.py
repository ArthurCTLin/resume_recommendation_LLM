def result_explanation(cv, jd):
    
    system_prompt = f"""
                You are a professional HR specialist.
                
                """

    user_input = f"""
                According to the following Resume and Job description, please explain why is this applicant suitable or unsuitable for this position in paragraph form.
                Job Description:
                {jd}
                RESUME:
                {cv}
                """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input},
    ]
    
    return messages
