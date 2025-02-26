import json

def readjson(path):
    f = open(path, 'r')
    data = json.load(f)
    f.close()
    return data

def http_parser_request(html_string):
    
    map = dict()
    html_string = html_string.split('\r\n')
    
    map['body'] = ''

    first = True
    is_body = False

    for i in (html_string):
        if (first):
            i = i.split(' ')
            map['Method'] = i[0]
            map['Path'] = i[1]
            map['Version'] = i[2]
            first = False

        elif not is_body:
            if (i == ''):
                is_body = True
            else:
                i = i.split(':')
                map[i[0]] = i[1]

        else:
            map['body'] += i +'\n'

    return map

def http_parser_reply(html_string):
    
    map = dict()
    html_string = html_string.split('\r\n')
    
    map['body'] = ''

    first = True
    is_body = False

    for i in (html_string):
        if (first):
            i = i.split(' ')
            map['Version'] = i[0]
            map['Status Code'] = i[1]
            map['Status Message'] = i[2]
            first = False

        elif not is_body:
            if (i == ''):
                is_body = True
            else:
                i = i.split(':')
                map[i[0]] = i[1]

        else:
            map['body'] += i +'\n'

    return map