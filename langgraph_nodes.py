import langgraph as lg
from model import summarize_text

class FetchSupplierNode(lg.Node):
    def __init__(self, db_connection):
        super().__init__()
        self.db_connection = db_connection

    # def run(self, input_data):
    #     supplier_data = fetch_supplier_data(self.db_connection)
    #     return {"supplier_data": supplier_data}
    
    
class SummarizeSupplierNode(lg.Node):
    def __init__(self, summarizer):
        super().__init__()
        self.summarizer = summarizer

    def run(self, input_data):
        supplier_info = input_data["supplier_data"]
        summaries = [summarize_text(info[1]) for info in supplier_info]
        return {"summaries": summaries}


