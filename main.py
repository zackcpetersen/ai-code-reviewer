import os
from dotenv import load_dotenv
from typing import Dict, Tuple

from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from models.github_models import PRInfo, GitHubClientCreds
from prompts.code_review import system_instructions, review_instructions
from tools.post_comment import PostCommentTool
from wrappers.custom_github_api_wrapper import create_github_client

load_dotenv()


def run_code_review_agent(
    pr_info: PRInfo, client_info: GitHubClientCreds
) -> Dict[str, any]:
    # Get the PR diff
    ghc = create_github_client(pr_info, client_info)
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


def validate_params() -> Tuple[PRInfo, GitHubClientCreds]:
    repo = os.environ["INPUT_GITHUB_REPO"]
    pr_number = int(os.environ["INPUT_GITHUB_PR_NUMBER"])

    app_id = os.environ["INPUT_GITHUB_APP_ID"]
    private_key = os.environ["INPUT_GITHUB_APP_PRIVATE_KEY"]
    base_branch = os.environ.get("INPUT_GITHUB_BASE_BRANCH")
    active_branch = os.environ.get("INPUT_GITHUB_ACTIVE_BRANCH")

    for env_var in [
        repo,
        pr_number,
        app_id,
        private_key,
        base_branch,
        active_branch,
    ]:
        if not env_var:
            raise ValueError(f"Missing required environment variable: {env_var}")

    owner, repo_name = repo.split('/', 1)
    pri = PRInfo(owner=owner, repo=repo_name, pr_number=pr_number)
    client_info = GitHubClientCreds(
        app_id=app_id,
        private_key=private_key,
        base_branch=base_branch,
        active_branch=active_branch,
    )
    return pri, client_info


if __name__ == "__main__":
    pri, ci = validate_params()
    res = run_code_review_agent(pri, ci)
    print(res.get("output"))
