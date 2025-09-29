import json

from langchain.tools import tool


@tool('JSON_parser')
def json_output_parser(response: str, graph: str = ''):
    """Use this tool to create a valid JSON output after generating the response. This function receives the response and graph values, the graph parameter is optional. A string json format output is returned. No need to use this again if no errors returned."""

    return json.dumps({'response': response, 'graph': graph})
