from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool, wiki_tool, save_tool

load_dotenv()

#Set up Prompt Template

class ResearchResponse(BaseModel):
    topic: str                  # generate a topic that is of type str
    summary: str                # generate summary that is of type str
    sources: list[str]          # generate a list of string sources
    tools_used: list[str]       # tools used

llm = ChatOpenAI(model="gpt-4")

parser = PydanticOutputParser(pydantic_object=ResearchResponse)  # Allows us to take output of llm and parse is into the model to use as a regular python object

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",  #info to the llm that tells it what is is supposed to so
            """
            You are a research assistanct that will help gereate a research paper.
            Answer the user query and use neccessary tools.
            Format the JSON keys in all lowercase snake_case.
            Wrap the output in this format and provide no other text\n{format_instructions}
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
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


query = input("What can I help you research? ")
raw_response = agent_executor.invoke({"query": query}) # must invoke with prompt variable "query." "chat_history" and "agent_scartch[ad are added automatically by agent_executor"

try:
  structured_response = parser.parse(raw_response.get("output"))
  print(structured_response)
except Exception as e:
  print("Error Parsing Respose: ", e, "Raw Response: ", raw_response)
