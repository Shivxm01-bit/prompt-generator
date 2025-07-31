import random

prompt_templates = {
    "Customer Support": [
        "You are a helpful customer support agent. Respond kindly to the user's question: \"{user_input}\"",
        "Politely help the customer resolve: \"{user_input}\""
    ],
    "HR Bot": [
        "You are an HR assistant. Answer this employee's query: \"{user_input}\"",
        "Respond as a friendly HR bot to: \"{user_input}\""
    ],
    "Educational Assistant": [
        "You are a tutor. Explain the concept of: \"{user_input}\"",
        "Teach the user about: \"{user_input}\""
    ],
    "Healthcare Assistant": [
        "You are a virtual health assistant. Give initial advice for: \"{user_input}\"",
        "Help the patient understand symptoms like: \"{user_input}\""
    ]
}

def generate_prompt(domain, user_input):
    template = random.choice(prompt_templates[domain])
    return template.replace("{user_input}", user_input)

def suggest_improvements(domain, user_input, filled_prompt):
    return [
        filled_prompt + "\n- Keep your answer concise and polite.",
        f"Act like an expert in {domain.lower()}. Answer: \"{user_input}\" in a step-by-step manner.",
        f"You are an AI assistant. Based on the following query: \"{user_input}\", provide a detailed yet friendly response."
    ]

def similarity_scores(base_prompt, suggestions):
    def simple_similarity(a, b):
        set_a = set(a.lower().split())
        set_b = set(b.lower().split())
        return round(len(set_a & set_b) / len(set_a | set_b), 2) if set_a | set_b else 0.0

    return [simple_similarity(base_prompt, s) for s in suggestions]

if __name__ == "__main__":
    domain = "Educational Assistant"
    user_input = "What is machine learning?"

    print("Running Demo Prompt Generator...")
    base_prompt = generate_prompt(domain, user_input)
    print("\n🎯 Generated Prompt:")
    print(base_prompt)

    suggestions = suggest_improvements(domain, user_input, base_prompt)
    print("\n✨ Improved Prompt Suggestions:")
    for i, s in enumerate(suggestions):
        print(f"\nOption {i+1}:")
        print(s)

    print("\n🧠 Similarity Scores:")
    scores = similarity_scores(base_prompt, suggestions)
    for i, score in enumerate(scores):
        print(f"Similarity to Option {i+1}: {score}")