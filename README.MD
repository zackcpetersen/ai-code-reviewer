# AI Code Reviewer GitHub Action

This GitHub Action provides an AI-powered code review for your pull requests. It uses OpenAI's GPT model to analyze code changes and provide meaningful feedback.

## What it does

The AI Code Reviewer:

1. Retrieves the diff of a specified pull request
2. Analyzes the code changes using an AI model
3. Identifies potential issues, suggests improvements, and provides constructive feedback
4. Posts comments directly on the pull request with its findings

## How to use

To use this action in your workflow, add the following step to your `.github/workflows/main.yml` file:

```yaml
- name: AI Code Review
  uses: your-username/ai-code-reviewer@v1
  with:
    github_repo: ${{ github.repository }}
    github_pr_number: ${{ github.event.pull_request.number }}
    github_base_branch: ${{ github.base_ref }}
    github_active_branch: ${{ github.head_ref }}
    github_app_id: ${{ secrets.GITHUB_APP_ID }}
    github_app_private_key: ${{ secrets.GITHUB_APP_PRIVATE_KEY }}
  env:
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
    LANGCHAIN_TRACING_V2: ${{ secrets.LANGCHAIN_TRACING_V2 }}
    LANGCHAIN_API_KEY: ${{ secrets.LANGCHAIN_API_KEY }}
    LANGCHAIN_PROJECT: ${{ secrets.LANGCHAIN_PROJECT }}
```

## Inputs

| Input | Description | Required |
|-------|-------------|----------|
| `github_repo` | The GitHub repository in the format `owner/repo` | Yes |
| `github_pr_number` | The pull request number | Yes |
| `github_base_branch` | The base branch of the pull request (default: main) | Yes |
| `github_active_branch` | The active branch of the pull request | Yes |
| `github_app_id` | The GitHub App ID | Yes |
| `github_app_private_key` | The GitHub App private key | Yes |

## Environment Variables

The action requires the following environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key
- `LANGCHAIN_TRACING_V2`: Boolean flag to enable LangSmith tracing
- `LANGCHAIN_API_KEY`: LangChain API key for LangSmith tracing
- `LANGCHAIN_PROJECT`: LangSmith project to associate for tracing

## Setup

1. Create a GitHub App and install it in your repository. Make note of the App ID and generate a private key.
2. Add the following secrets to your GitHub repository:
   - `GITHUB_APP_ID`: Your GitHub App ID
   - `GITHUB_APP_PRIVATE_KEY`: Your GitHub App private key
   - `OPENAI_API_KEY`: Your OpenAI API key
   - (Optional) `LANGCHAIN_TRACING_V2`, `LANGCHAIN_API_KEY`, and `LANGCHAIN_PROJECT` for LangSmith tracing
3. Add the workflow file to your repository as shown in the "How to use" section.

## How it works

1. The action is triggered when a pull request is opened or updated.
2. It retrieves the diff of the pull request using the GitHub API.
3. The diff is then analyzed by an AI model (GPT-4) using the LangChain framework.
4. The AI generates a code review based on the changes, identifying potential issues and suggesting improvements.
5. The review comments are posted directly on the pull request using the GitHub API.

## Customization

You can customize the review process by modifying the `prompts/code_review.py` file. This file contains the system instructions and review instructions for the AI model.

## Limitations

- The AI only has access to the diff of the pull request, not the entire codebase.
- The quality of the review depends on the OpenAI model used and the provided instructions.
