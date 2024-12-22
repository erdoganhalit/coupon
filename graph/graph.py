from tools.tools import COUPON_CRAWLER_TOOL, COUPON_TRY_TOOL
from langchain_openai import ChatOpenAI
from typing import Annotated, Any, Literal, Union
from pydantic import BaseModel
from langchain_core.messages import (AIMessage, AnyMessage, ToolCall, ToolMessage, SystemMessage)
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

# Configuration defaults
from config.config import (
    TOOL_CALLER_MODEL_NAME,
    ANSWER_GENERATOR_MODEL_NAME,
    TOOL_CALLER_TEMPERATURE,
    ANSWER_GENERATOR_TEMPERATURE,
    TOOL_CALLER_SYSTEM_MESSAGE,
    ANSWER_GENERATOR_SYSTEM_MESSAGE,
)

class CouponCodesGraph:
    def __init__(
        self,
        tool_caller_model: str = TOOL_CALLER_MODEL_NAME,
        tool_caller_temperature: float = TOOL_CALLER_TEMPERATURE,
        answer_generator_model: str = ANSWER_GENERATOR_MODEL_NAME,
        answer_generator_temperature: float = ANSWER_GENERATOR_TEMPERATURE,
        tool_caller_system_message: str = TOOL_CALLER_SYSTEM_MESSAGE,
        answer_generator_system_message: str = ANSWER_GENERATOR_SYSTEM_MESSAGE
    ):
        """
        Initializes the CouponCodesGraph with LLM configurations for tool caller and answer generator.

        Args:
            tool_caller_model (str): Model name for the tool caller LLM.
            tool_caller_temperature (float): Temperature value for the tool caller LLM.
            answer_generator_model (str): Model name for the answer generator LLM.
            answer_generator_temperature (float): Temperature value for the answer generator LLM.
            tool_caller_system_message (str): System message for the tool caller node.
            answer_generator_system_message (str): System message for the answer generator node.
        """
        # Initialize LLMs
        self.tool_caller_llm = ChatOpenAI(model=tool_caller_model, temperature=tool_caller_temperature)
        self.answer_generator_llm = ChatOpenAI(model=answer_generator_model, temperature=answer_generator_temperature)

        # System messages
        self.tool_caller_system_message = tool_caller_system_message
        self.answer_generator_system_message = answer_generator_system_message

        # Tools setup
        self.coupon_tools = [COUPON_CRAWLER_TOOL, COUPON_TRY_TOOL]
        self.coupon_tools_node = ToolNode(tools=self.coupon_tools)

        # Bind tools to tool caller LLM
        self.llm_with_tools = self.tool_caller_llm.bind_tools(tools=self.coupon_tools, strict=True)

        # Define graph state and builder
        class State(TypedDict):
            messages: Annotated[list, add_messages]

        self.graph_builder = StateGraph(State)

        # Build the graph
        self._build_graph()

        self.graph = self.compile_graph()

    def _build_graph(self):
        """Builds the state graph with nodes and edges."""
        # Add nodes
        self.graph_builder.add_node("tool_caller", self._tool_caller)
        self.graph_builder.add_node("coupon_tools", self.coupon_tools_node)
        self.graph_builder.add_node("answer_generator", self._answer_generator)

        # Add edges
        self.graph_builder.add_conditional_edges("tool_caller", self._coupon_tools_condition)
        self.graph_builder.add_edge("coupon_tools", "answer_generator")

        # Set entry and finish points
        self.graph_builder.set_entry_point("tool_caller")
        self.graph_builder.set_finish_point("answer_generator")

    def _coupon_tools_condition(
        self,
        state: Union[list[AnyMessage], dict[str, Any], BaseModel],
        messages_key: str = "messages",
    ) -> Literal["coupon_tools", "__end__"]:
        """
        Conditional function to determine whether to proceed to coupon tools or end.

        Args:
            state: The current state of the graph.
            messages_key: The key for retrieving messages from the state.

        Returns:
            Literal["coupon_tools", "__end__"]: Next node identifier.
        """
        if isinstance(state, list):
            ai_message = state[-1]
        elif isinstance(state, dict) and (messages := state.get(messages_key, [])):
            ai_message = messages[-1]
        elif messages := getattr(state, messages_key, []):
            ai_message = messages[-1]
        else:
            raise ValueError(f"No messages found in input state to tool_edge: {state}")
        if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
            return "coupon_tools"
        return "__end__"

    def _tool_caller(self, state: dict):
        """
        Node function to handle tool caller logic.

        Args:
            state: The current state of the graph.

        Returns:
            dict: Updated state with messages.
        """
        system_message = SystemMessage(content=self.tool_caller_system_message)
        state["messages"].insert(-1, system_message)
        response = self.llm_with_tools.invoke(state["messages"])
        return {"messages": [response]}

    def _answer_generator(self, state: dict):
        """
        Node function to handle answer generation logic.

        Args:
            state: The current state of the graph.

        Returns:
            dict: Updated state with messages.
        """
        system_message = SystemMessage(content=self.answer_generator_system_message)
        state["messages"].append(system_message)
        return {"messages": [self.answer_generator_llm.invoke(state["messages"])]}

    def compile_graph(self):
        """
        Compiles and returns the state graph.

        Returns:
            StateGraph: Compiled graph instance.
        """
        return self.graph_builder.compile()
    
    def stream_graph_updates(self, user_input: str, state: dict):
        state["messages"].append(("user", user_input))
        
        for event in self.graph.stream(state):
            print("-----New Event-----")
            for value in event.values():
                #print("Assistant:", [value["messages"][i].content for i in range(len(value["messages"]))] )
                assistant_messages = value["messages"]
                state["messages"].extend(assistant_messages)  # Keep assistant messages in the state
                for message in assistant_messages:
                    print("Assistant:", message.content)

