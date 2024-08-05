import os
from dotenv import load_dotenv
from typing import Dict

from github import Github
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from models.github_models import PRInfo
from tools.post_comment import post_pr_comment

load_dotenv()


def run_code_review_agent(token: str, pr_link: str) -> Dict[str, any]:
    try:
        pr_info = parse_pr_link(pr_link)
        diff = get_pr_diff(token=token, pr_info=pr_info)

        # TODO
        #  set code review comments on specific lines in the diff - /Users/zackpetersen/.local/share/virtualenvs/ai_code_reviewer-C5KEYmZo/lib/python3.11/site-packages/github/PullRequest.py create_comment()
        #    going to need LLM to specify line numbers and files to comment on
        system_instructions = """
            As an expert code reviewer, analyze the following code changes:
            1. Identify potential bugs, security issues, and performance problems.
            2. Suggest improvements in code style, readability, and maintainability.
            3. Highlight violations of best practices or coding standards.
            4. Provide constructive feedback with explanations.
            5. If there are no significant issues, you may state that the code looks good.
            """

        review_instructions = """
        Review the following code changes. If you have meaningful feedback, post a comment using the 
        `post_pr_comment` tool.
        
        pr info: 
        {pr_info}
        
        diff: 
        {diff}
        """
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
        tools = [post_pr_comment]
        agent = create_openai_functions_agent(llm, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        # Prepare the input for the agent
        input_data = {
            "pr_info": pr_info.json(),
            "diff": diff,
        }

        result = agent_executor.invoke(input_data)
        return result
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}


def get_pr_diff(token: str, pr_info: PRInfo) -> str:
    client = Github(token)
    files = (
        client.get_repo(f"{pr_info.owner}/{pr_info.repo}")
        .get_pull(pr_info.pr_number)
        .get_files()
    )
    # Convert files to a string representation of the diff
    diff = "\n".join(
        [f"File: {file.filename}\nChanges:\n{file.patch}" for file in files]
    )
    # Remove curly braces to avoid issues with f-strings
    diff = diff.replace("{", "{{").replace("}", "}}")
    return diff


def parse_pr_link(pull_request: str) -> PRInfo:
    # This is a simple implementation and might need to be more robust
    parts = pull_request.split("/")
    owner = parts[-4]
    repo = parts[-3]
    pr_number = int(parts[-1])
    return PRInfo(owner=owner, repo=repo, pr_number=pr_number)


if __name__ == "__main__":
    github_token = os.environ["GITHUB_TOKEN"]
    pr = "https://github.com/zackcpetersen/portfolio/pull/10"
    res = run_code_review_agent(github_token, pr)
    print(res)
