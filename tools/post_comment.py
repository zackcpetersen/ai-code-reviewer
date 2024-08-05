import os

from langchain_community.utilities.github import GitHubAPIWrapper
from langchain_core.tools import tool

from models.github_models import PostCommentInput


@tool(args_schema=PostCommentInput)
def post_pr_comment(owner: str, repo: str, pr_number: int, comment: str) -> str:
    """Post a comment on a GitHub pull request"""

    app_id = os.environ["GITHUB_APP_ID"]
    private_key = os.environ["GITHUB_APP_PRIVATE_KEY"]
    base_branch = os.environ.get("GITHUB_BASE_BRANCH")
    active_branch = os.environ.get("GITHUB_BRANCH")

    formatted_req = f"{pr_number}\n\n{comment}"

    api_wrapper = GitHubAPIWrapper(
        github_repository=f"{owner}/{repo}",
        github_app_id=app_id,
        github_app_private_key=private_key,
        active_branch=active_branch,
        github_base_branch=base_branch,
    )
    resp = api_wrapper.comment_on_issue(formatted_req)
    return resp
