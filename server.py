from fastapi import FastAPI, Request, HTTPException
from salesforce_client import SalesforceClient

app = FastAPI()

@app.get("/")
def root():
    return {"message": "MCP server running"}

@app.get("/schema")
def get_schema():
    return {
        "tools": [
            {
                "name": "query_salesforce",
                "description": "Run a SOQL query on Salesforce and return the results.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "soql": {
                            "type": "string",
                            "description": "SOQL query to run"
                        }
                    },
                    "required": ["soql"]
                }
            }
        ]
    }

@app.post("/call-tool")
async def call_tool(request: Request):
    try:
        if request.headers.get("content-length") == "0":
            return {"message": "Empty body received for connector test."}

        data = await request.json()
        tool = data.get("tool")
        params = data.get("params", {})

        if tool == "query_salesforce":
            soql = params.get("soql")
            if not soql:
                return {"error": "Missing SOQL query"}
            client = SalesforceClient()
            return client.query(soql)

        return {"error": f"Unknown tool: {tool}"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad request: {str(e)}")
