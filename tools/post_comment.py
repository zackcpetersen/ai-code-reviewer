import os
from typing import Optional, Type, Any

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import tool, BaseTool

from models.github_models import PostCommentInput
from langchain.pydantic_v1 import BaseModel


class PostCommentTool(BaseTool):
    name: str = "post_pr_comment"
    description: str = "Post a comment on a GitHub pull request"
    args_schema: Type[BaseModel] = PostCommentInput

    def _run(
        self,
        owner: str,
        repo: str,
        pr_number: int,
        comment: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        formatted_req = f"{pr_number}\n\n{comment}"
        resp = self.metadata.get("github_client").comment_onissue(formatted_req)
        return resp
