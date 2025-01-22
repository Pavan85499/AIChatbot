from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# from langgraph import Agent
# from langgraph import Agent, Task
# from langchain.llms import OpenAI
# from transformers import GPT2LMHeadModel, GPT2Tokenizer

import langgraph as lg
from langgraph import nodes, edges
import random

# Define the chatbot flow using LangGraph
class SimpleChatBot:
    def __init__(self):
        # Create a LangGraph instance
        self.graph = lg.Graph()

        # Create nodes (representing conversation steps)
        self.node_greeting = nodes.TextNode("Hello! How can I help you today?")
        self.node_ask_name = nodes.TextNode("What is your name?")
        self.node_respond_name = nodes.TextNode("Nice to meet you, {name}!")
        self.node_farewell = nodes.TextNode("Goodbye! Have a great day!")

        # Create edges (defining the transitions between nodes)
        self.graph.add_edge(edges.TextEdge(self.node_greeting, self.node_ask_name, input_text="Hi"))
        self.graph.add_edge(edges.TextEdge(self.node_ask_name, self.node_respond_name, input_text="{name}"))
        self.graph.add_edge(edges.TextEdge(self.node_respond_name, self.node_farewell, input_text="bye"))
        
    def run(self):
        print(self.node_greeting.text)  # Start with the greeting
        current_node = self.node_greeting
        
        while True:
            user_input = input("> ").strip().lower()
            
            # Find the next node based on user input
            next_node = None
            for edge in self.graph.edges(current_node):
                if user_input in edge.input_text.lower():
                    next_node = edge.target_node
                    break

            if next_node:
                if next_node == self.node_respond_name:
                    # If we're asking for the name, get the name from the user and pass it to the response
                    name = user_input.capitalize()
                    print(next_node.text.format(name=name))
                else:
                    print(next_node.text)
                current_node = next_node

            # If the user says "bye", end the chat
            if current_node == self.node_farewell:
                break

if __name__ == "__main__":
    bot = SimpleChatBot()
    bot.run()

# Initialize the Flask app
app = Flask(__name__)

# Set up the database URI (SQLite example)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'  # For SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable tracking modifications (optional)

# Initialize the database
db = SQLAlchemy(app)

# Define a model (this represents a table in the database)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# Route to retrieve information from the database
@app.route('/')
def home():
    # Query the database for all users
    users = User.query.all()  # This fetches all users from the User table
    return render_template('index.html', users=users)

# Create the database and tables (if they don't exist yet)
with app.app_context():
    db.create_all()

# @app.route('/')
# def index():
   
#    return render_template("index.html")

if __name__ == '__main__':
   app.run(debug = True)
   































# @app.route('/query', methods=['POST'])
# def query():
#     user_input = request.json['query']
#     response = agent.run(user_input)
#     return jsonify({"response": response})

# if __name__ == '__main__':
#     app.run(debug=True)

# Initialize agent
# agent = ProductQueryAgent()

# Define the LLM model
# llm = OpenAI(model="text-davinci-003")

# Define agent workflow
# class ProductQueryAgent(Agent):
#     def define_tasks(self):
#         self.add_task("query_database", Task(query_database))
#         self.add_task("summarize_data", Task(summarize_data))

    # def query_database(self, user_input):
        # SQL query to the database
        # if "price" in user_input:
        #     return "SELECT price FROM products WHERE product_name LIKE '%{}%'".format(user_input.split()[-1])
        # return ""

    # def summarize_data(self, data):
        # Summarize or format data with the LLM
        # return llm.generate(f"Summarize this data: {data}")


# -------------Data Base Connector----------------
# def fetch_product_price(product_name):
#     conn = mysql.connector.connect(
#         host="localhost", user="root", password="password", database="product_supplier"
#     )
#     cursor = conn.cursor()
#     query = f"SELECT price FROM products WHERE product_name LIKE '%{product_name}%'"
#     cursor.execute(query)
#     result = cursor.fetchone()
#     conn.close()
#     return result[0] if result else None

# ---------------LLM Summarizer----------------
# def summarize_data(data):
#     tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
#     model = GPT2LMHeadModel.from_pretrained("gpt2")

#     inputs = tokenizer.encode(data, return_tensors="pt")
#     outputs = model.generate(inputs, max_length=100, num_return_sequences=1)
#     return tokenizer.decode(outputs[0], skip_special_tokens=True)