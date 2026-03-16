from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever

model = OllamaLLM(model="llama3")

template = """
You are an expert in answering questions about restaurant reviews.
Here are some relevant reviews: {reviews}
Here is the question to answer: {question}
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

def ask_question(question: str) -> str:
    reviews = retriever.invoke(question)
    result = chain.invoke({"reviews": reviews, "question": question})
    return result

if __name__ == "__main__":
    while True:
        print("\n-------------------------------")
        question = input("Ask your question (q to quit): ")
        print()
        if question.lower() == "q":
            break
        print(ask_question(question))