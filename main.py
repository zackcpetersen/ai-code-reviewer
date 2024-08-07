from dotenv import load_dotenv
from typing import Dict

from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from models.github_models import PRInfo
from prompts.code_review import system_instructions, review_instructions
from tools.post_comment import PostCommentTool
from wrappers.custom_github_api_wrapper import create_github_client

load_dotenv()


def run_code_review_agent(pr_link: str) -> Dict[str, any]:
    try:
        # Get the PR diff
        pr_info = parse_pr_link(pr_link)
        ghc = create_github_client(pr_info.owner, pr_info.repo)
        diff = ghc.get_pr_diff(pr_info.pr_number)

        # Set up the prompt
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    system_instructions,
                ),
                ("human", review_instructions),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        # Set up the agent
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        tools = [PostCommentTool(metadata={"github_client": ghc})]
        agent = create_openai_functions_agent(llm, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        # Prepare the input for the agent
        input_data = {
            "pr_info": pr_info.json(),
            "diff": diff,
        }

        # Invoke the agent
        result = agent_executor.invoke(input_data)
        return result
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}


def parse_pr_link(pull_request: str) -> PRInfo:
    # This is a simple implementation and may need to be more robust
    parts = pull_request.split("/")
    owner = parts[-4]
    repo = parts[-3]
    pr_number = int(parts[-1])
    return PRInfo(owner=owner, repo=repo, pr_number=pr_number)


if __name__ == "__main__":
    res = run_code_review_agent("https://github.com/zackcpetersen/portfolio/pull/10")
    print(res)
