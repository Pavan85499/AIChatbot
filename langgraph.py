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
