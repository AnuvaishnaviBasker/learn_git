from vector_search import semantic_search
from ollama import chat


def ask_farmassist(
    question: str
):


    results = semantic_search(
        question,
        top_k=1
    )

    if not results:
        return "Sorry, I could not find any relevant information."


    context = results[0]["content"]


    print("\nCONTEXT SENT TO LLM:")
    print(context)
    print("\n")


    prompt = f"""

You are FarmAssist AI, an agriculture assistant for Tamil Nadu farmers.

Rules:

1. Answer ONLY using the provided context.
2. Do NOT invent information.
3. Do NOT assume facilities, cold storage, warehouses, subsidies, timings, or locations unless explicitly mentioned in the context.
4. If the information is not available in the context, say:

"Based on the available knowledge base, I could not find this information."

5. Keep answers simple and clear.

Context:

{context}


Farmer Question:

{question}


Answer:
"""


    response = chat(
        model="llama3.2:latest",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )


    return response["message"]["content"]



if __name__ == "__main__":

    print("\n🌾 FarmAssist AI")
    print("Type 'exit' to quit\n")


    while True:

        question = input("Farmer: ")


        if question.lower() == "exit":
            break


        response = ask_farmassist(
            question
        )


        print("\nFarmAssist:\n")
        print(response)
