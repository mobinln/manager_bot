import os
import requests
from dotenv import load_dotenv
from agno.tools import tool

# Load environment variables from .env file
load_dotenv()

GITLAB_API_URL = "https://gitlab.com/api/v4"
PERSONAL_ACCESS_TOKEN = os.getenv("GITLAB_TOKEN")
PROJECT_ID = os.getenv("GITLAB_PROJECT_ID")
headers = {
    "PRIVATE-TOKEN": PERSONAL_ACCESS_TOKEN
}
def request(method, endpoint, params=None, json=None):
    url = f"{GITLAB_API_URL}/projects/{PROJECT_ID}{endpoint}"
    if params is None:
        params = {}
    response = requests.request(method,url, headers=headers,params=params)
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
    response = request("GET","/merge_requests")
    res=[]
    for mr in response:
        mrDetail={
            "id":mr.get("id"),
            "title": mr.get("title"),
            "description": mr.get("description"),
            "state": mr.get("state"),  # e.g., "opened", "merged", "closed"
            "created_at": mr.get("created_at"),
            "updated_at": mr.get("updated_at"),
            "merged_by_name": mr.get("merged_by", {}).get("name") if mr.get("merged_by") else None,
            "source_branch": mr.get("source_branch"),
            "work_in_progress": mr.get("work_in_progress"),
            "merge_status": mr.get("merge_status"),  # e.g., "can_be_merged", "cannot_be_merged"
            "time_stats": {
                "time_estimate": mr.get("time_stats", {}).get("time_estimate"),
                "total_time_spent": mr.get("time_stats", {}).get("total_time_spent"),
                "human_time_estimate": mr.get("time_stats", {}).get("human_time_estimate"),
                "human_total_time_spent": mr.get("time_stats", {}).get("human_total_time_spent")
            },
            "approved": mr.get('approved'),
            "approved_by_ids":mr.get('approved_by_ids'),
        }
        res.append(mrDetail)
    return res    
# if __name__ == "__main__":
#     print(get_git_merge_requests())