from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from typing import Any, List
from state import State
from langgraph.graph import StateGraph, START, END
from tools import tool_mapping
from langgraph.prebuilt import ToolNode, tools_condition, create_react_agent
from langchain_openai import ChatOpenAI
from models import UserConfiguration


load_dotenv()


# def create_agent(system_prompt: str, tools: List[str]):
#     tool_list = [tool_mapping[key] for key in tools if key in tool_mapping]
#     llm_with_tools = llm.bind_tools(tool_list)

#     def chatbot(state: State):
#         return {"messages": llm_with_tools.invoke(state["messages"])}
    
#     graph_builder = StateGraph(State)
#     graph_builder.add_node("chatbot", chatbot)

#     tool_node = ToolNode(tools=tool_list)
#     graph_builder.add_node("tools", tool_node)
#     graph_builder.add_conditional_edges(
#         "chatbot", 
#         tools_condition
#     )
#     graph_builder.add_edge("tools", "chatbot")
#     graph_builder.add_edge(START, "chatbot")

#     graph = graph_builder.compile()

#     return graph

class Agent:
    def __init__(self, config: UserConfiguration):
        self.username = config.USERNAME
        self.system_message = config.SYSTEM_MESSAGE
        self.model = config.MODEL
        self.tools = config.TOOLS
        self.temperature = config.TEMPERATURE
        self.presence_penalty = config.PRESENCE_PENALTY
        self.freq_penalty = config.FREQUENCY_PENALTY
        self.top_p = config.TOP_P
        self.logits_bias = config.LOGIT_BIAS
        self.max_tokens = config.MAX_TOKENS
    def create_react_agent(self):
        tool_list = [tool_mapping[key] for key in self.tools if key in tool_mapping]
        if self.model == "GPT-4o":
            llm = ChatOpenAI(
                model=self.model, 
                temperature=self.temperature, 
                presence_penalty=self.presence_penalty, 
                frequency_penalty=self.freq_penalty, 
                logit_bias=self.logits_bias, 
                top_p=self.top_p, 
                max_tokens=self.max_tokens)
        graph = create_react_agent(model=llm, tools=tool_list, state_modifier=self.system_message)
        return graph