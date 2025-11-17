from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool, wiki_tool, save_tool

load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

llm = ChatOpenAI(model="gpt-4")
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a research assistant that will help generate a research paper.
            Answer the user query and use necessary tools.
            Format the JSON keys in all lowercase snake_case.
            Wrap the output in this format and provide no other text\n{format_instructions}
            IMPORTANT: Only use save_text_to_file tool when the user explicitly says "save" or "save to file".
            NEVER automatically save the research results.
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}")
    ]
).partial(format_instructions=parser.get_format_instructions())

tools = [search_tool, wiki_tool,save_tool]
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

def format_research_output(topic: str, summary: str, sources: list, tools_used: list) -> str:
  """Format the research output in a standard, readable format."""
  output = f"Topic: {topic}\n\n"
  output += f"{summary}\n\n"
  output += "Sources:\n"
  for source in sources:
    output += f"- {source}\n"
  output += f"\nTools used: {', '.join(tools_used)}"
  return output

def format_for_saving(topic: str, summary: str) -> str:
  """Format for research input used only when saving to a file. Excludes sources and tools."""
  return f"Topic: {topic}\n\n{summary}"

query = input("What can I help you research? ")
raw_response = agent_executor.invoke({"query": query})

try:
  structured_response = parser.parse(raw_response.get("output"))

  print("\n" + "="*60)
  formatted_output = format_research_output(
      topic=structured_response.topic,
      summary=structured_response.summary,
      sources=structured_response.sources,
      tools_used=structured_response.tools_used
  )
  print(formatted_output)
  print("="*60)

  save_choice = input("\nDo you want to save this research to a file? (y/n): ")
  if save_choice.lower() in ['y','yes']:
    save_result = save_tool.func(format_for_saving(structured_response.topic, structured_response.summary))
    print("Your result has been saved to research_output.txt in the current directory.")
except Exception as e:
  print("Error Parsing Response: ", e)
  print("Raw Response: ", raw_response)
