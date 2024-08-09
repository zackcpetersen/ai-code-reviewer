from langchain_community.utilities.github import GitHubAPIWrapper
from models.github_models import PRInfo, GitHubClientCreds


class CustomGitHubAPIClient(GitHubAPIWrapper):
    def get_pr_diff(self, pr_number: int) -> str:
        """Get the diff of a GitHub pull request"""
        files = self.github_repo_instance.get_pull(pr_number).get_files()
        # Convert files to a string representation of the diff
        diff = "\n".join(
            [f"File: {file.filename}\nChanges:\n{file.patch}" for file in files]
        )
        # Remove curly braces to avoid issues with f-strings
        return diff

    def comment_onissue(self, comment_query: str) -> str:
        # In the future, could improve this to make comments on specific files/lines of the PR
        # https://docs.github.com/en/rest/pulls/comments?apiVersion=2022-11-28#create-a-review-comment-for-a-pull-request
        # self.github_repo_instance.get_pull(pr_number).create_review_comment(
        #     body="", commit="", path="", line=0
        # )

        # For now, just post a comment on the PR as a whole
        return self.comment_on_issue(comment_query)


def create_github_client(
    pr_info: PRInfo, client_info: GitHubClientCreds
) -> CustomGitHubAPIClient:
    wrapped = CustomGitHubAPIClient(
        github_repository=f"{pr_info.owner}/{pr_info.repo}",
        github_app_id=client_info.app_id,
        github_app_private_key=client_info.private_key,
        active_branch=client_info.active_branch,
        github_base_branch=client_info.base_branch,
    )

    return wrapped
