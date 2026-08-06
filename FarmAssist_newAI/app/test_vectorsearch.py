from vector_search import semantic_search



questions = [

    "I am a farmer in Theni. Where can I store vegetables?",

    "How can farmers get better price for crops?",

    "I want to start an agriculture business. Is there any support?",

    "Where can I sell my vegetables directly?"

]



for question in questions:


    print("\n")
    print("="*70)

    print(
        "QUESTION:"
    )

    print(question)


    print("\nRESULTS:")
    

    results = semantic_search(
        question,
        top_k=3
    )


    for r in results:


        print("\nType:",
              r["type"])

        print(
            "Score:",
            r["score"]
        )

        print(
            r["content"][:300],
            "..."
        )

