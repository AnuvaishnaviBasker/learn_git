from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

print("Initializing the AI Chef with Memory... (Please wait)")

# 1. Setup Model
model = ChatOllama(model="llama3.2", temperature=0.7)

# 2. Setup Prompt Template with a MessagesPlaceholder
# This placeholder is where LangChain will inject the past conversation history!
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a master chef. You remember what ingredients the user has already mentioned and help them build a cohesive recipe idea step by step. Keep answers under 3 sentences."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}")  # Changed from '{ingredient}' to general '{input}'
])

# 3. Base Chain
base_chain = prompt_template | model | StrOutputParser()

# 4. Memory Management Setup
# We create a dictionary to hold session history objects
history_store = {}

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in history_store:
        history_store[session_id] = InMemoryChatMessageHistory()
    return history_store[session_id]

# 5. WRAP THE CHAIN WITH MEMORY
# This intercepts calls, grabs old history, runs the chain, and saves the new response.
conversational_chain = RunnableWithMessageHistory(
    base_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

print("\n--- AI Chef Terminal with Memory Ready! ---")
print("Try telling the chef your first ingredient, then build on top of it!")
print("Type 'exit' to quit.")
print("-" * 45)

# 6. Interactive Loop
while True:
    user_input = input("\nYou: ").strip()
    
    if user_input.lower() in ['exit', 'quit']:
        print("\nGoodbye! Happy cooking! 👋")
        break
        
    if not user_input:
        continue
        
    print("Chef is thinking...")
    
    # Run the conversational chain
    # We pass a config dictionary specifying a 'session_id' so it tracks this specific chat
    result = conversational_chain.invoke(
        {"input": user_input},
        config={"configurable": {"session_id": "cooking_session_1"}}
    )
    
    print(f"\nChef:\n{result}")