import json

from langchain.tools import tool


@tool('JSON_parser')
def json_output_parser(response: str, graph_id: str = ''):
    """Use this tool to create a valid JSON output after generating the response and as last step. This function receives the response and graph_id values, the graph_id parameter is optional. A string json formatted output is returned. No need to use this again if no errors returned.
    **Use the exact format returned as output for the user**"""

    return json.dumps({'response': response, 'graph_id': graph_id})
