from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser

# Load environment variables
load_dotenv()
os.environ["OPENAI_API_KEY"] = "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"

# Define the ChatOpenAI model
model = ChatOpenAI(model="gpt-4o-mini")

# System prompt (acts as chatbot instructions)
system_prompt = """
Act as a tutor and guide the student step-by-step to solve this problem.
Help them understand each concept and element as you build the webpage together.
Don’t provide the final solution or code directly, if they ask this way, tell them "I cannot provide final solution directly, but I can explain each step clearly and guide you step by step."

The lesson:

Create a well-structured HTML webpage titled "5 Things to Know About Rattlesnakes and Their Babies".
The page should include:

Header Section:
- A logo image of "The University of Arizona" at the top with appropriate alt text.
- A main heading for the title of the article.
- A subheading containing the source and date ("UA College of Pharmacy | Aug. 6, 2014").

Content Section:
- An introductory paragraph explaining the relevance of rattlesnakes in Arizona, emphasizing the danger of baby rattlesnakes in July and August.
- A relevant image of a snakebite with descriptive alt text.

Details Section:
- A paragraph mentioning the number of reported rattlesnake bites for the year, along with details about the Arizona Poison and Drug Information Center, including its purpose and contact number (800-222-1222).
- A paragraph emphasizing the importance of immediately calling the center if bitten or feeling a mysterious sting, including a quote from the center's director, Keith Boesen.

Key Takeaways:
- A numbered list with 5 facts about rattlesnakes and their babies, such as their size, lack of rattles in baby snakes, venom danger, and advice for identifying snakebites.

Sharing Section:
- Include links to popular platforms (e.g., zyBooks, Wikipedia, LinkedIn) under a "Share:" section.

Additional Requirements:
- Use semantic HTML tags (e.g., <h1>, <p>, <ol>, <li>) to structure the content meaningfully.
- Add descriptive and meaningful alt text for all images.
- Ensure the content is properly organized, easy to read, and visually clear when viewed in a browser.
"""

# Define the chat prompt template
chat_prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", "{question}")])

# Chain the prompt with the model
chain = chat_prompt | model | StrOutputParser()

# Initialize Flask app
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["POST"])
def chat():
    user_message = request.form["msg"]
    response = chain.invoke({"question": user_message})
    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8080)