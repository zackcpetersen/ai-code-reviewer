from langchain.pydantic_v1 import BaseModel, Field


class PRInfo(BaseModel):
    owner: str = Field(description="The owner of the repository")
    repo: str = Field(description="The name of the repository")
    pr_number: int = Field(description="The pull request number")


class PostCommentInput(PRInfo):
    comment: str = Field(description="Comment to post on the pull request")


class GitHubClientCreds(BaseModel):
    app_id: str = Field(description="The GitHub App ID")
    private_key: str = Field(description="The private key for the GitHub App")
    base_branch: str = Field(description="The base branch for the PR")
    active_branch: str = Field(description="The active branch for the PR")
