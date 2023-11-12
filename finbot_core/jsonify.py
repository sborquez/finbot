import argparse
import json
import re
from typing import Union
from pathlib import Path


def convert_protobuff(description_file):
    with open(description_file) as f:
        content = f.read()
        # remove all occurrences streamed comments (/*COMMENT */) from string
        content = re.sub(re.compile("/\*.*?\*/", re.DOTALL ), "", content)
        # remove all occurrence single-line comments (//COMMENT\n ) from string
        content = re.sub(re.compile("//.*?\n"), "", content)
        # remove identation
        content = re.sub(re.compile("( ){2}"), "", content)
    description = []
    for c in content:
        if c == '\n':
            continue
        description.append(c)
    description = ''.join(description)
    return description

SCHEMA_TYPES = {
    'protobuf': ('PROTOCOL_BUFFER', convert_protobuff),
}

def convert(description_file: Union[str, Path], schema_type: str, output_file: Union[str, Path]):
    if schema_type not in SCHEMA_TYPES:
        raise ValueError(f'schema_type not supported.', schema_type)
    type_, convert_func = SCHEMA_TYPES.get(schema_type, (None, None))
    json_definition = {
        "definition": convert_func(description_file),
        "type": type_
    }
    with open(output_file, 'w') as json_file:
        json.dump(json_definition, json_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert schema description into a json.')
    parser.add_argument('-f', '--description_file', help='Schema definition file.', required=True)
    parser.add_argument('-t','--schema_type', help='Schema type.', default='protobuf')
    parser.add_argument('-o','--output_file', help='Schema output json file.')
    args = vars(parser.parse_args())
    convert(**args)