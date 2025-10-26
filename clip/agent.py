from google.adk.agents.llm_agent import Agent
import clip.tools.github as github

root_agent = Agent(
    model='gemini-2.5-flash',
    name='clip',
    description='A helpful assistant for user questions.',
    instruction='You are a paper clip, dramatic and charismatic. Answer user questions to the best of your knowledge',
    tools=[github.get_pull_request,
           github.get_pull_request_files]
)
