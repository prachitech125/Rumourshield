import requests

BASE_URL = "https://factchecktools.googleapis.com/v1alpha1/claims:search"

def search_fact_checks(query: str, api_key: str, page_size: int = 5):
    
    params = {
        "query": query,
        "key": api_key,
        "pageSize": page_size
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
