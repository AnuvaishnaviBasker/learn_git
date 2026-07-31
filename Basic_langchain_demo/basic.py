from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

print("Initializing the AI Chef Application... (Please wait)")

# 1. Setup the core components
model = ChatOllama(model="llama3.2", temperature=0.7)

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a master chef. Give a short, energetic 1-sentence cooking tip for the ingredient provided."),
    ("user", "What should I do with {ingredient}?")
])

# 2. Assemble the chain
chef_chain = prompt_template | model | StrOutputParser()

print("\n--- AI Chef Terminal Ready! ---")
print("Type an ingredient to get a pro tip, or type 'exit' to quit.")
print("-" * 32)

# 3. Interactive Loop
while True:
    # Get user input and clean up any accidental trailing spaces
    user_input = input("\nEnter an ingredient: ").strip()
    
    # Check for the exit command
    if user_input.lower() in ['exit', 'quit']:
        print("\nThanks for cooking with me! Goodbye! 👋")
        break
        
    # Skip empty entries if the user just presses Enter
    if not user_input:
        print("Please type an actual ingredient!")
        continue
        
    print("Chef is thinking...")
    
    # Run the chain dynamically with whatever the user typed
    result = chef_chain.invoke({"ingredient": user_input})
    
    print(f"\nChef's Tip:\n{result}")