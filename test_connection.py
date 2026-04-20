import os
import httpx
from dotenv import load_dotenv

# Forensic Connection Test (GraphQL Edition)
# Verifies that the Vault Distiller can reach the NEW Buffer GraphQL API

load_dotenv()

ACCESS_TOKEN = os.getenv("BUFFER_ACCESS_TOKEN")
API_ENDPOINT = "https://api.buffer.com"

async def test_connection():
    print(f"--- Forensic GraphQL Connection Test ---")
    print(f"Target: {API_ENDPOINT}")
    
    if not ACCESS_TOKEN:
        print("ERROR: BUFFER_ACCESS_TOKEN not found in .env")
        return

    # The query from the Buffer docs
    query = """
    query GetOrganizations {
      account {
        organizations {
          id
        }
      }
    }
    """

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                API_ENDPOINT,
                json={"query": query},
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                if "errors" in data:
                    print(f"FAILURE: GraphQL Errors returned.")
                    print(data["errors"])
                else:
                    print(f"SUCCESS: Connected to Buffer GraphQL API.")
                    print(f"Response Data: {data}")
            else:
                print(f"FAILURE: Status Code {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"EXCEPTION: {str(e)}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_connection())
