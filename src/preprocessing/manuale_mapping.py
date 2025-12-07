
from urllib import response
from datapizza.core.clients.models import ClientResponse

def mapping_category_technique(response: ClientResponse) -> dict:
    """
    Map categories to their techniques from the extraction response.

    Args:
        response (ClientResponse): The response object containing structured data.

    Returns:
        dict: A dictionary mapping category names to their techniques.
    """
    
    all_techniques = {}
    for category in response.structured_data[0].categories:
        all_techniques[category.category_name] = category.techniques
    return all_techniques

