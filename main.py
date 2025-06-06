from aicore import create_ai_core_client
from flask import Flask, request
import json
import tools
import os
from langchain_core.messages import SystemMessage
from langgraph.graph import START, StateGraph, MessagesState
from langgraph.prebuilt import tools_condition, ToolNode
from gen_ai_hub.proxy.langchain.init_models import init_llm

# 1. Initialize Flask App
# app = Flask(__name__)

port = int(os.environ.get('PORT', 3000))
with open('./credentials.json', 'r') as creds:
    credentials = json.load(creds)

create_ai_core_client(credentials)

model = 'gpt-4o'
llm = init_llm(model, temperature=0., max_tokens=256)



tools = [tools.get_salesorder_details, tools.get_email_address, tools.sendmail]
llm_with_tools = llm.bind_tools(tools)
sys_msg = SystemMessage(content="""
You are a helfpul assistant tasked with answering questions about different topics. 
Your name is 'SAP BTP AI Agent'. Keep your answers short. After giving a response, do not ask for additional requests. 
Only use information that is provided to you by the different tools you are given.""")

def assistant(state: MessagesState):
   return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
   "assistant",
   # If the latest message (result) from assistant is a tool call -> tools_condition routes to Tools
   # If the latest message (result) from assistant is not a tool call -> tools_condition routes to END
   tools_condition,
)
builder.add_edge("tools", "assistant")
graph = builder.compile()

# @app.route('/', methods=['GET'])
# @app.route('/')
def processing():
    user_input = "what is the status of salesorder 1112 and can you send an email to Fabian with status of the salesorder 1112?"
        
    # Get user request from the paylod
    # payload = request.get_json()
    # user_input = payload['user_input']

    # Pass the request to the AI agent
    agent_outcome = graph.invoke({"messages": [("user", user_input)]})

    # The agent's response
    btpaiagent_response = agent_outcome['messages'][-1].to_json()['kwargs']['content']

    text = json.dumps({'btpaiagent_response': btpaiagent_response})
    print(f"${text}")
    return json.dumps({'btpaiagent_response': btpaiagent_response})

if __name__ == '__main__':
    processing()
	# app.run(host='0.0.0.0', port=port)
