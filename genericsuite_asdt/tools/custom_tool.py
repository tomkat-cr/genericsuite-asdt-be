from crewai_tools import tool
# from crewai_tools import BaseTool


# class MyCustomTool(BaseTool):
#     name: str = "Name of my tool"
#     description: str = (
#         "Clear description for what this tool is useful for, you agent" + \
#         " will need this information to use it."
#     )

#     def _run(self, argument: str) -> str:
#         # Implementation goes here
#         return "this is an example of a tool output, ignore it and move" + \
#                " along."


@tool("Tool Name")
def my_simple_tool(question: str) -> str:
    """Tool description for clarity."""
    # Tool logic here
    return "Tool output"
