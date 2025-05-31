import os
import requests
from dotenv import load_dotenv
from agno.tools import tool

# Load environment variables from .env file
load_dotenv()

GITLAB_API_URL = "https://gitlab.com/api/v4"
PERSONAL_ACCESS_TOKEN = os.getenv("GITLAB_TOKEN")
PROJECT_ID = os.getenv("GITLAB_PROJECT_ID")
headers = {"PRIVATE-TOKEN": PERSONAL_ACCESS_TOKEN}


def request(method, endpoint, params=None, json=None):
    url = f"{GITLAB_API_URL}/projects/{PROJECT_ID}{endpoint}"
    if params is None:
        params = {}
    response = requests.request(method, url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


@tool(
    name="get_git_merge_requests",  # Custom name for the tool (otherwise the function name is used)
    description="Fetches merge requests from the GitLab project, including their title, description, state, approval info, and other metadata.",  # Custom description (otherwise the function docstring is used)
    show_result=False,  # Show result after function call
    stop_after_tool_call=False,  # Return the result immediately after the tool call and stop the agent                     # Hook to run before and after execution
    requires_confirmation=False,  # Requires user confirmation before execution
    cache_results=False,  # Cache TTL in seconds (1 hour)
)
def get_git_merge_requests():
    """
    Fetch merge requests from the GitLab project using the GitLab API.

    This function queries the GitLab API to retrieve all merge requests for the current project.
    Each merge request is returned with detailed information including:

    - `id`: Unique identifier of the merge request.
    - `title`: Title of the merge request.
    - `description`: Description of the merge request.
    - `state`: Current state (e.g., "opened", "merged", "closed").
    - `created_at`: Creation timestamp.
    - `updated_at`: Last update timestamp.
    - `merged_by_name`: Name of the user who merged the MR, if applicable.
    - `source_branch`: Source branch of the merge request.
    - `work_in_progress`: Boolean indicating if it's marked as WIP.
    - `merge_status`: Mergeability status (e.g., "can_be_merged").
    - `time_stats`: Dictionary containing estimated and spent time in both seconds and human-readable formats.
        - `time_estimate`
        - `total_time_spent`
        - `human_time_estimate`
        - `human_total_time_spent`
    - `approved`: Boolean flag or field indicating if the MR is approved (if supported in your custom setup).
    - `approved_by_ids`: List of user IDs who approved the MR (if available).

    Returns:
        list[dict]: A list of dictionaries, each containing detailed metadata for a merge request.
    """
    response = request("GET", "/merge_requests")
    res = []
    for mr in response:
        mrDetail = {
            "comments_id": mr.get("iid"),
            "title": mr.get("title"),
            "description": mr.get("description"),
            "state": mr.get("state"),  # e.g., "opened", "merged", "closed"
            "created_at": mr.get("created_at"),
            "updated_at": mr.get("updated_at"),
            "merged_by_name": mr.get("merged_by", {}).get("name")
            if mr.get("merged_by")
            else None,
            "source_branch": mr.get("source_branch"),
            "work_in_progress": mr.get("work_in_progress"),
            "merge_status": mr.get(
                "merge_status"
            ),  # e.g., "can_be_merged", "cannot_be_merged"
            "time_stats": {
                "time_estimate": mr.get("time_stats", {}).get("time_estimate"),
                "total_time_spent": mr.get("time_stats", {}).get("total_time_spent"),
                "human_time_estimate": mr.get("time_stats", {}).get(
                    "human_time_estimate"
                ),
                "human_total_time_spent": mr.get("time_stats", {}).get(
                    "human_total_time_spent"
                ),
            },
            "approved": mr.get("approved"),
            "approved_by_ids": mr.get("approved_by_ids"),
        }
        res.append(mrDetail)
    return res


@tool(
    name="get_git_merge_request_comments",
    description="Fetches all comments (notes) for a specific merge request in the GitLab project.",
    show_result=False,
    stop_after_tool_call=False,
    requires_confirmation=False,
    cache_results=False,
)
def get_git_merge_request_comments(mr_id: int):
    """
    Retrieve all comments (also called notes) for a given merge request in the GitLab project.

    This function uses the GitLab API to fetch all user-submitted comments (notes) associated
    with a specific merge request, identified by its internal ID (`iid`).

    Args:
        mr_id (int): The internal ID (`iid`) of the merge request to retrieve comments for.

    Returns:
        list[dict]: A list of comment dictionaries, each containing:
            - merge_request_id (int): The ID of the merge request.
            - body (str): The content of the comment.
            - created_at (str): Timestamp when the comment was created (ISO 8601 format).
            - updated_at (str): Timestamp of the last update to the comment (if any).

    Note:
        - This does not include system-generated notes or discussion threads.
        - Use the `/discussions` endpoint if you want full threaded conversations.
    """
    notes = request("GET", f"/merge_requests/{mr_id}/notes")
    all_comments = []
    for note in notes:
        comment = {
            "merge_request_id": mr_id,
            "author": note.get("author", {}).get("name"),
            "body": note.get("body"),
            "created_at": note.get("created_at"),
            "updated_at": note.get("updated_at"),
        }
        all_comments.append(comment)

    return all_comments
