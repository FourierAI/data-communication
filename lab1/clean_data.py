import argparse


def filter_average_time(content):
    return ('t=' not in content) and ('M/M' not in content) and ('' != content)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-F",
        "--file_path",
        help="file_path",
        default='',
        type=str)
    args = parser.parse_args()

    file_path = args.file_path

    with open(file_path) as file:
        content = file.read()
        list_value = content.splitlines()

        list_value = list(filter(filter_average_time, list_value))

        for content in list_value:
            print(content)
