import json

from langchain.tools import tool


@tool('JSON_parser')
def json_output_parser(response: str, graph_id: str = ''):
    """Use this tool to create a valid JSON output after generating the response. This function receives the response and graph_id values, the graph_id parameter is optional. A string json formatted output is returned. No need to use this again if no errors returned."""

    return json.dumps({'response': response, 'graph_id': graph_id})
