from flask import Flask, jsonify, request
from langgraph_nodes import FetchSupplierNode, SummarizeSupplierNode
from database import connect_to_mysql, fetch_supplier_data
from model import summarizer

app = Flask(__name__)

db_conn = connect_to_mysql()
fetch_supplier_node = FetchSupplierNode(db_conn)
summarize_supplier_node = SummarizeSupplierNode(summarizer)

# Set up LangGraph
from langgraph import Graph
graph = Graph()
graph.add_node(fetch_supplier_node)
graph.add_node(summarize_supplier_node)
graph.connect(fetch_supplier_node, summarize_supplier_node)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('user_input', '')
    
    if 'supplier' in user_input.lower():
        graph_result = graph.run({})
        summarized_supplier_data = graph_result["summaries"]
        return jsonify({"response": summarized_supplier_data})
    else:
        return jsonify({"response": "I can only provide supplier information. Try asking about suppliers."})

if __name__ == "__main__":
    app.run(debug=True)
