import re

COMMENT = re.compile('--\s?(.*)')
NAME    = re.compile('--\s?name:\s?([^\s]+)', re.I)

def parse_queries(lines):
    blank = {
        'doc': '',
        'sql': '',
        'name': None
    }

    query = blank.copy()
    for line in lines:
        name_match = NAME.match(line)
        if name_match:
            if query['name'] is not None:
                yield _clean(query)
                query = blank.copy()

            query['name'] = name_match.group(1)
            continue

        comment_match = COMMENT.match(line)
        if comment_match:
            query['doc'] += comment_match.group(1)
            continue

        query['sql'] += line

    if query['sql']:
        yield _clean(query)

def _clean(query):
    result = {k: (v or '').strip() for k, v in query.items()}
    if not result['sql'].endswith(';'):
        result['sql'] += ';'
    return result
