# Azure Functions HTTP trigger entry point for mcp-reddit
import azure.functions as func
import logging
from mcp_reddit.reddit_fetcher import mcp

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        # Example: run a tool or handle request
        # You may want to parse req.get_json() and call mcp.run() or a specific tool
        return func.HttpResponse("Reddit MCP Function is running.", status_code=200)
    except Exception as e:
        logging.error(f"Error: {e}")
        return func.HttpResponse(f"Error: {e}", status_code=500)
