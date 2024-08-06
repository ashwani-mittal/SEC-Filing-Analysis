import re

def filter_xml_content(xml_data, keys):
    results = []
    regex_patterns = [re.compile(key, re.IGNORECASE) for key in keys]
    def search_dict(d):
        if isinstance(d, dict):
            for k, v in d.items():
                if any(pattern.search(k) for pattern in regex_patterns):
                    results.append((k, v))
                if isinstance(v, dict):
                    search_dict(v)
                elif isinstance(v, list):
                    for item in v:
                        search_dict(item)
        elif isinstance(d, list):
            for item in d:
                search_dict(item)

    search_dict(xml_data)
    return results

