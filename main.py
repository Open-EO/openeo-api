import json
from pprint import pprint

def declare_variables(variables, macro):
    """
    This is the hook for the functions

    - variables: the dictionary that contains the variables
    - macro: a decorator function, to declare a macro.
    """

    macro(build_error_list, 'error_codes')


def build_error_list():
    with open('errors.json') as f:
        data = json.load(f)

    errors = {}
    for key, val in data.items():
        val['name'] = key
        if 'description' not in val or val['description'] is None:
            val['description'] = ""
        if 'message' not in val or val['message'] is None:
            raise Exception("No message specified for error: " + key)
        if 'http' not in val or val['http'] is None:
            raise Exception("No HTTP status code specified for error: " + key)
        if 'tags' not in val or val['tags'] is None or not val['tags']:
            raise Exception("No tags specified for error: " + key)
        for tag in val['tags']:
            if tag in errors:
                errors[tag].append(val)
            else:
                errors[tag] = [val]

    html = ""
    for tag, error in errors.items():
        html += "<h3>" + tag.replace('_', ' ').title() + "</h3>"
        html += "<table>"
        html += "<tr>"
        html += "<th>openEO Error Code</th>"
        html += "<th>openEO Error Name</th>"
        html += "<th>Description</th>"
        html += "<th>Message</th>"
        html += "<th>HTTP Status Code</th>"
        html += "</tr>"
        for val in error:
            html += "<tr>"
            html += "<td>" + str(val['code']) + "</td>"
            html += "<td>" + val['name'] + "</td>"
            html += "<td>" + val['description'] + "</td>"
            html += "<td>" + val['message'] + "</td>"
            html += "<td>" + str(val['http']) + "</td>"
            html += "</tr>"
        html += "</table>"

    return html
