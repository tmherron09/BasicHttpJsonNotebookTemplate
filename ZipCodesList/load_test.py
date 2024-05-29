import os
import json
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from basic_http_calls import PostalCode
from pprint import pprint


def load_json_file_to_notebook(file_path, object_hook=None):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    if object_hook is not None:
        with open(file_path, 'r') as f:
            data = json.load(f, object_hook=object_hook)
    else:
        with open(file_path, 'r') as f:
            data = json.load(f)
    return data


def load_json_file_to_notebook_v2(folder_name, file_path, is_cwd=True, object_hook=None):
    # file_dir = os.path.dirname(__file__)
    cwd = os.getcwd()
    if is_cwd:
        if not os.path.exists(f"{cwd}/{folder_name}"):
            raise FileNotFoundError(f"File not found: {cwd}/{folder_name}/{file_path}")
        if object_hook is not None:
            with open(os.path.join(cwd ,folder_name, file_path), 'r') as f:
                data = json.load(f, object_hook=object_hook)
        else:
            with open(os.path.join(cwd, folder_name, file_path), 'r') as f:
                data = json.load(f)
    else:
        if not os.path.exists(f"{folder_name}"):
                raise FileNotFoundError(f"File not found: {folder_name}/{file_path}")
        if object_hook is not None:
            with open(os.path.join(folder_name, file_path), 'r') as f:
                data = json.load(f, object_hook=object_hook)
        else:
            with open(os.path.join(folder_name, file_path), 'r') as f:
                data = json.load(f)
    return data
    

def test_01():
    data = load_json_file_to_notebook_v2("ZipCodesList", "ListOfZipCodes.json", is_cwd=True, object_hook=PostalCode.json_object_hook)
    pprint(data)

if __name__ == "__main__":
    # print(os.path.dirname(__file__))
    test_01()