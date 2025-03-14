from pydantic import Field

from app.agent.toolcall import ToolCallAgent
from app.prompt.manus import NEXT_STEP_PROMPT, SYSTEM_PROMPT
from app.tool import Terminate, ToolCollection
from app.tool.browser_use_tool import BrowserUseTool
from app.tool.file_saver import FileSaver
from app.tool.google_search import GoogleSearch
from app.tool.python_execute import PythonExecute
from app.tool.exa_ai import ExaAi
from app.tool.ask_human import AskHuman
from app.tool.finder import Finder
from app.config import config
from app.tool.bing_search import BingSearch


def get_search_agent():
    search_agent_config = config.default.get("search_agent")
    if search_agent_config == "ExaAi":
        search_agent = ExaAi()
    elif search_agent_config == "BingSearch":
        search_agent = BingSearch()
    else:
        search_agent = GoogleSearch()
    return search_agent


class Manus(ToolCallAgent):
    """
    A versatile general-purpose agent that uses planning to solve various tasks.

    This agent extends PlanningAgent with a comprehensive set of tools and capabilities,
    including Python execution, web browsing, file operations, and information retrieval
    to handle a wide range of user requests.
    """

    name: str = "Manus"
    description: str = (
        "A versatile agent that can solve various tasks using multiple tools"
    )

    system_prompt: str = SYSTEM_PROMPT
    next_step_prompt: str = NEXT_STEP_PROMPT

    # Add general-purpose tools to the tool collection
    available_tools: ToolCollection = Field(
        default_factory=lambda: ToolCollection(
            PythonExecute(),
            get_search_agent(),
            BrowserUseTool(),
            FileSaver(),
            AskHuman(),
            Terminate(),
            Finder()
        )
    )
