""" 
Basic Http Request Implementations in Single File. 
Credits: Tim H./TimsyMagnus in his free time.
"""

import http.client
import json
from pprint import pprint
import urllib
import os
from datetime import datetime


def send_get_request(host, path, is_https=False):
    """ Send a GET request to the host with given path, return the response as string """
    if is_https:
        conn = http.client.HTTPSConnection(host)
    else:
        conn = http.client.HTTPConnection(host)
    conn.request("GET", path)
    response = conn.getresponse()
    return response.read()


def send_get_json_request(host, path, is_https=False):
    """ Send a GET request to the host with given path that returns a JSON object """
    response = send_get_request(host, path, is_https)
    return json.loads(response)


def send_get_json_request_collection(host, base_path, collection_param_name, collection, is_https=False):
    collection_param = ",".join(collection)
    base_path = f"{base_path}?{collection_param_name}={collection_param}"
    base_path = urllib.parse.quote(base_path, safe='/:?=')
    return send_get_json_request(host, base_path, is_https)


def send_and_save_json_request_param(host, path_with_param, param, folder_name, is_https=False, is_cwd=True):
    path = f"{path_with_param}={param}"
    json_response = send_get_json_request(host, path, is_https)
    if is_cwd:
        file_name = f"{os.getcwd()}/{folder_name}/{param}.json"
        # print("File Name: ", file_name)
    else:
        file_name = f"{folder_name}/{param}.json"
    with open(file_name, 'w') as file:
        # pprint(json_response)
        json.dump(json_response, file)


def send_and_save_json_request(host, path, value, folder_name, is_https=False, is_cwd=True):
    path = f"{path}/{value}"
    json_response = send_get_json_request(host, path, is_https)
    if is_cwd:
        file_name = f"{os.getcwd()}\\{folder_name}\\{value}.json"
        # print("File Name: ", file_name)
    else:
        file_name = f"{folder_name}\\{value}.json"
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    with open(file_name, 'w') as file:
        # pprint(json_response)
        json.dump(json_response, file, indent=4)


def send_and_save_collection_json_result_multi(host, path, collection, folder_name, is_https=False, is_cwd=True):
    """ Save all the results to individual results named after the request value. """
    for item in collection:
        send_and_save_json_request(host, path, item, folder_name, is_https, is_cwd)


def send_and_save_collection_json_result_obj(host, path, collection, folder_name, file_name=None, is_https=False,
                                             is_cwd=True):
    """ Save all the results in a single json object where the request is key and return object is the value. """
    total_result = {}
    file_name = file_name if file_name else folder_name
    for item in collection:
        result = send_get_json_request(host, f"{path}/{item}", is_https)
        total_result[item] = result
    if is_cwd:
        file_name = f"{os.getcwd()}\\{folder_name}\\{file_name}.json"
    else:
        file_name = f"{folder_name}\\{file_name}.json"
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    with open(file_name, 'w') as file:
        json.dump(total_result, file, indent=4)


def send_and_save_collection_json_result_list(host, path, collection, folder_name, file_name=None,
                                              request_value_in_result=True, is_https=False, is_cwd=True):
    """ Save all the result json objects in a list/array and save to file. """
    total_result = []
    file_name = file_name if file_name else folder_name
    for item in collection:
        result = send_get_json_request(host, f"{path}/{item}", is_https)
        if request_value_in_result:
            item_result = result
        else:
            item_result = {"requestValue": item, "result": result}
        total_result.append(item_result)
    if is_cwd:
        file_name = f"{os.getcwd()}\\{folder_name}\\{file_name}.json"
    else:
        file_name = f"{folder_name}\\{file_name}.json"
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    with open(file_name, 'w') as file:
        json.dump(total_result, file, indent=4)


def output_in_as(output):
    pass


global output_in_as_g
output_in_as_g = output_in_as


def test_01():
    host = "api.zippopotam.us"
    path = "/us/63119"
    output_in_as_g(send_get_json_request(host, path))


def test_02():
    collection = ["ABCD", "1234", "XYZ"]
    result = send_get_json_request_collection("some-fake-url-sdkfheu.com", "/us", 'testcodes', collection)
    output_in_as_g(result)


def test_04():
    host = "api.zippopotam.us"
    path = "/us"
    send_and_save_json_request(host, path, "63119", "zip_codes")


def test_05():
    host = "api.zippopotam.us"
    path = "/us/63119"
    result = send_get_json_request(host, path)
    dumps_result = json.dumps(result, indent=4)
    output_in_as_g(dumps_result)


def test_06():
    host = "api.zippopotam.us"
    path = "/us"
    collection = ["63119", "63122", "63127"]
    send_and_save_collection_json_result_multi(host, path, collection, 'ZipCodes')


def test_07():
    host = "api.zippopotam.us"
    path = "/us"
    collection = ["63119", "63122", "63127"]
    send_and_save_collection_json_result_obj(host, path, collection, 'ZipCodesObbjects', 'ZipCodesObjects')


def test_08():
    host = "api.zippopotam.us"
    path = "/us"
    collection = ["63119", "63122", "63127"]
    send_and_save_collection_json_result_list(host, path, collection, 'ZipCodesList', 'ListOfZipCodes')


def test_09():
    host = "api.zippopotam.us"
    path = "/us"
    collection = ["63119", "63122", "63127"]
    send_and_save_collection_json_result_list(host, path, collection, 'ZipCodesListHasRequest', 'ListOfZipCodeResults',
                                              request_value_in_result=True)


def test_10():
    json_str = """
        {
            "post code": "63119",
            "country": "United States",
            "country abbreviation": "US",
            "places": [
                {
                    "place name": "Saint Louis",
                    "longitude": "-90.3481",
                    "state": "Missouri",
                    "state abbreviation": "MO",
                    "latitude": "38.5893"
                }
            ]
        }
        """
    try:
        data = json.loads(json_str, object_hook=PostalCode.json_object_hook)
        output_in_as_g(data)
    except Exception as e:
        output_in_as_g(f"Exception: {e}")


def test_11():
    postal_code = PostalCode(post_code="63119", country="United States", country_abbreviation="US", places=[
        Place(place_name="Saint Louis", longitude="-90.3481", state="Missouri", state_abbreviation="MO",
              latitude="38.5893")])
    output_in_as_g(postal_code)


def test_12():
    json_str = """
            {
                "post code": "63119",
                "country": "United States",
                "country abbreviation": "US",
                "places": [
                    {
                        "place name": "Saint Louis",
                        "longitude": "-90.3481",
                        "state": "Missouri",
                        "state abbreviation": "MO",
                        "latitude": "38.5893"
                    }
                ]
            }
            """
    try:
        data = json.loads(json_str, object_hook=PostalCode.json_object_hook)
        output = json.dumps(data.to_dict(), indent=4)
        # pprint(output)
        output_in_as_g(output)
    except Exception as e:
        print(f"Exception: {e}")


def run_all_tests(comment_line_length=76, use_output_file=False, output_file_name="output.txt", new_output_file=False):
    global output_in_as_g
    if use_output_file and new_output_file:
        if os.path.exists(output_file_name):
            print("Removing Existing Output File")
            os.remove(output_file_name)

    def output_as(output):
        if type(output) is not str and type(output) is not dict:
            output = json.dumps(output.to_dict(), indent=4)
        elif type(output) is dict:
            output = json.dumps(output, indent=4)
        if use_output_file:
            with open(output_file_name, 'a') as file:
                file.write(output)
        else:
            print(output)

    output_in_as_g = output_as
    tests = [test_01, test_02, test_04, test_05, test_06, test_07, test_08, test_09, test_10, test_11, test_12]
    stars = "*" * comment_line_length
    output_as(f"\n\nStarting New Test Run\n" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + f"\n{stars}\n")
    for test in tests:
        try:
            stars_short = "*" * int((comment_line_length - (len(test.__name__) + 11)) / 2)
            # output_as(f"{stars}\n")
            output_as(f"{stars_short} {test.__name__} Starting {stars_short}\n")
            test()
            output_as(f"\n{stars_short} {test.__name__} Complete {stars_short}\n\n")
            # output_as(f"{stars}\n")
        except Exception as e:
            output_as(f"Exception: {e}")
            stars_short = "*" * int((comment_line_length - (len(test.__name__) + 9)) / 2)
            output_as(f"\n{stars_short} {test.__name__} Failed {stars_short}\n\n")
            # output_as(f"{stars}\n")
            continue


class Place:
    def __init__(self, place_name, longitude, state, state_abbreviation, latitude):
        self.place_name = place_name
        self.longitude = longitude
        self.state = state
        self.state_abbreviation = state_abbreviation
        self.latitude = latitude

    def __str__(self):
        return json.dumps(self.__dict__, default=lambda o: o.__dict__, indent=4)

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        return {
            'place_name': self.place_name,
            'longitude': self.longitude,
            'state': self.state,
            'state_abbreviation': self.state_abbreviation,
            'latitude': self.latitude
        }

    @classmethod
    def from_dict(cls, data):
        data['place_name'] = data.pop('place name')
        data['state_abbreviation'] = data.pop('state abbreviation')
        return cls(**data)


class PostalCode:
    def __init__(self, post_code, country, country_abbreviation, places):
        self.post_code = post_code
        self.country = country
        self.country_abbreviation = country_abbreviation
        self.places = places

    def __str__(self):
        return json.dumps(self.__dict__, default=lambda o: o.__dict__, indent=4)

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        return {
            'post_code': self.post_code,
            'country': self.country,
            'country_abbreviation': self.country_abbreviation,
            'places': [place.to_dict() for place in self.places]
        }

    @classmethod
    def from_dict(cls, data):
        data['post_code'] = data.pop('post code')
        data['country_abbreviation'] = data.pop('country abbreviation')
        data['places'] = [Place.from_dict(place) for place in data['places']]
        result = cls(**data)
        return result

    @classmethod
    def json_object_hook(cls, dict_obj):
        if 'post code' in dict_obj:
            return PostalCode.from_dict(dict_obj)
        return dict_obj


if __name__ == "__main__":
    run_all_tests(76, True, "output.txt", new_output_file=True)