import os
from openai import OpenAI

def llm_evaluate(question: str, gt_answer:str, llm_answer:str, engine:str="Qwen2.5-72B-Instruct") -> bool:
    prompt = \
f"""Please act as an evaluator to determine whether the model's response matches or includes the correct answer. I will provide both the correct answer and the model's response. 
Please reply with either [Match] or [No Match], and briefly explain the reasoning behind your judgment.
There are some examples:
- Question: {{What time is the meeting?}}, Correct Answer: {{3:00PM}}, Model Response: {{The meeting is scheduled for 15:00.}}
- [Match]
- Question: {{What is Mike's total cost?}}, Correct Answer: {{9}}, Model Response: {{The total cost of Mike is 9.001}}
- [Match]
- Question: {{When is he scheduled to attend the meeting?}}, Correct Answer: {{01/12}}, Model Response: {{He will attend this meeting on the morning of January 12th.}}
- [Match]
- Question: {{What is the price?}}, Correct Answer: {{$9374}}, Model Response: {{None}}
- [No Match] Model Response is None.

- Question: {{{question}}}, Correct Answer: {{{gt_answer}}}, Model Response: {{{llm_answer}}}
- """

    if engine == "Qwen2.5-72B-Instruct":
        evaluator = OpenAI(
            base_url=os.getenv("QWEN2_BASE"), api_key=os.getenv("QWEN2_KEY")
        )
    elif engine == "deepseek-chat":
        evaluator = OpenAI(
            base_url="https://api.deepseek.com", api_key=os.getenv("DEEPSEEK_API_KEY")
        )
    else:
        raise ValueError
    
    try:
        response_content = evaluator.chat.completions.create(
            model=engine,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=100,
        ).choices[0].message.content
    except Exception as e:
        print(f"""- Question: {{{question}}}, Correct Answer: {{{gt_answer}}}, Model Response: {{{llm_answer}}}\n- {{RESPONSE_ERROR}}:{{{e}}}""")
        return False

    print(f"""- Question: {{{question}}}, Correct Answer: {{{gt_answer}}}, Model Response: {{{llm_answer}}}\n- {{{response_content}}}""")
    if response_content.count("[Match]"): return True
    return False
