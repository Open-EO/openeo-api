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

    # Group by tag in a dict
    errors = {}
    tags = []
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
            if tag not in tags:
                tags.append(tag)
                errors[tag] = {}
            errors[tag][key] = val

    tags.sort()

    # Create table of contents
    html = ""
    html += "<h3>Categories</h3>"
    html += "<ul>"
    for tag in tags:
        html += "<li><a href='#" + slugify(tag) + "'>" + tag + "</a></li>"
    html += "</ul>"

    # Generate tables with errors
    for tag in tags:
        html += "<a name='" + slugify(tag) + "'></a>"
        html += "<h3>" + tag + "</h3>"
        html += "<table>"
        html += "<tr>"
        html += "<th>openEO Error Code</th>"
        html += "<th>Description</th>"
        html += "<th>Message</th>"
        html += "<th>HTTP Status Code</th>"
        html += "</tr>"
        for key in sorted(errors[tag].keys()):
            error = errors[tag][key]
            html += "<tr>"
            html += "<td>" + error['name'] + "</td>"
            html += "<td>" + error['description'] + "</td>"
            html += "<td>" + error['message'] + "</td>"
            html += "<td>" + str(error['http']) + "</td>"
            html += "</tr>"
        html += "</table>"

    return html

def slugify(title):
    return title.lower().replace(' ', '_')