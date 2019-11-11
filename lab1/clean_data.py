def filter_average_time(content):
    return ('t=' not in content) and ('M/M' not in content) and ('' != content)


with open('mm2.out') as file:
    content = file.read()
    list_value = content.splitlines()

    list_value = list(filter(filter_average_time, list_value))

    for content in list_value:
        print(content)

