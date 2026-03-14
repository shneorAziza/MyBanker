from typing import Literal
from app.tools.definitions import get_user_balance_tool, financial_knowledge_tool
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from app.agents.state import AgentState

# הגדרת המודל עם הכלים
tools = [financial_knowledge_tool, get_user_balance_tool]
model = ChatOpenAI(model="gpt-4o-mini", temperature=0).bind_tools(tools)

# צומת המודל
def call_model(state: AgentState):
    response = model.invoke(state["messages"])
    return {"messages": [response]}

# פונקציית ניתוב - האם להמשיך לכלים או לסיים?
def should_continue(state: AgentState) -> Literal["tools", "__end__"]:
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return "__end__"

# בניית הגרף
workflow = StateGraph(AgentState)

# הוספת צמתים
workflow.add_node("agent", call_model)
workflow.add_node("tools", ToolNode(tools))

# הגדרת זרימה
workflow.set_entry_point("agent")

# קצוות מותנים: מה עושים אחרי ה-agent?
workflow.add_conditional_edges(
    "agent",
    should_continue,
)

# קצה רגיל: אחרי הכלים תמיד חוזרים ל-agent כדי שינתח את התוצאה
workflow.add_edge("tools", "agent")

app_graph = workflow.compile()