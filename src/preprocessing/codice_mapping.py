from collections import defaultdict
from datapizza.core.clients.models import ClientResponse

def mapping_licences(response: ClientResponse) -> dict:
    """
    Map licences to their techniques from the extraction response.
    Args:
        response (ClientResponse): The response object containing structured data.
    Returns:
        dict: A dictionary mapping licence names to their levels and associated techniques.
    """

    licence_to_techniques = defaultdict(lambda: defaultdict(list))

    extracted_data = response.structured_data[0]

    for category in extracted_data.categories:
        for technique in category.techniques:
            technique_name = technique.technique_name
            for licence in technique.licences:
                licence_name = licence.licence_name
                licence_level = licence.licence_level
                
                if technique_name not in licence_to_techniques[licence_name][licence_level]:
                    licence_to_techniques[licence_name][licence_level].append(technique_name)

    # Convert nested defaultdict to regular dict for cleaner serialization
    licence_to_techniques_dict = {
        licence_name: dict(levels) 
        for licence_name, levels in licence_to_techniques.items()
    }

    return licence_to_techniques_dict