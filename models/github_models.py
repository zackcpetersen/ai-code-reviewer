from langchain.pydantic_v1 import BaseModel, Field


class PRInfo(BaseModel):
    owner: str = Field(description="The owner of the repository")
    repo: str = Field(description="The name of the repository")
    pr_number: int = Field(description="The pull request number")


class PostCommentInput(PRInfo):
    comment: str = Field(description="Comment to post on the pull request")
