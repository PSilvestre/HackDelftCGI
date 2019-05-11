import json
import time
import requests
from requests import Request, Session
from requests.auth import HTTPBasicAuth
import dateutil.parser
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

STREAM_QUERY = "https://168.63.5.124/piwebapi/streams/{}/recorded"
STREAM_QUERY_WITH_START_TIME = "https://168.63.5.124/piwebapi/streams/{}/recorded?startTime={}"
STREAM_QUERY_WITH_START_END_TIME = "https://168.63.5.124/piwebapi/streams/{}/recorded?startTime={}&endTime={}"

MOTOR_VALUES_WEBIDS = ["F1DPwz91T7MV00-ab1SR4aA0ZwJwAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDAxLk1PVE9SU1RST09N",
                       "F1DPwz91T7MV00-ab1SR4aA0ZwggAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDAyLk1PVE9SU1RST09N",
                       "F1DPwz91T7MV00-ab1SR4aA0ZwmgAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDAzLk1PVE9SU1RST09N",
                       "F1DPwz91T7MV00-ab1SR4aA0ZwtAAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDA0Lk1PVE9SU1RST09N",
                       "F1DPwz91T7MV00-ab1SR4aA0ZwaQAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDA1Lk1PVE9SU1RST09N"]

CONTROL_LEFT_WEBIDS = ["F1DPwz91T7MV00-ab1SR4aA0ZwJAAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDAxLlNUVVJJTkcgTElOS1M",
                       "F1DPwz91T7MV00-ab1SR4aA0ZwiAAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDAyLlNUVVJJTkcgTElOS1M",
                       "F1DPwz91T7MV00-ab1SR4aA0ZwowAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDAzLlNUVVJJTkcgTElOS1M",
                       "F1DPwz91T7MV00-ab1SR4aA0ZwvAAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDA0LlNUVVJJTkcgTElOS1M",
                       "F1DPwz91T7MV00-ab1SR4aA0ZwcQAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDA1LlNUVVJJTkcgTElOS1M"]

CONTROL_RIGHT_WEBIDS = ["F1DPwz91T7MV00-ab1SR4aA0ZwJQAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDAxLlNUVVJJTkcgUkVDSFRT",
                        "F1DPwz91T7MV00-ab1SR4aA0ZwiQAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDAyLlNUVVJJTkcgUkVDSFRT",
                        "F1DPwz91T7MV00-ab1SR4aA0ZwpAAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDAzLlNUVVJJTkcgUkVDSFRT",
                        "F1DPwz91T7MV00-ab1SR4aA0ZwvQAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDA0LlNUVVJJTkcgUkVDSFRT",
                        "F1DPwz91T7MV00-ab1SR4aA0ZwcgAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDA1LlNUVVJJTkcgUkVDSFRT"]

PEAK_CURRENT_LEFT = [
    "F1DPwz91T7MV00-ab1SR4aA0ZwEgAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDAxLkVORVJHSUUgT1BQRVJWTEFLVEUgTElOS1M",
    "F1DPwz91T7MV00-ab1SR4aA0ZwfgAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDAyLklOU0NIQUtFTFBJRUtMSU5LUw",
    "F1DPwz91T7MV00-ab1SR4aA0ZwlgAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDAzLklOU0NIQUtFTFBJRUtMSU5LUw",
    "F1DPwz91T7MV00-ab1SR4aA0ZwsAAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDA0LklOU0NIQUtFTFBJRUtMSU5LUw",
    "F1DPwz91T7MV00-ab1SR4aA0ZwZQAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDA1LklOU0NIQUtFTFBJRUtMSU5LUw"
]

PEAK_CURRENT_RIGHT = [
    "F1DPwz91T7MV00-ab1SR4aA0ZwFQAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDAxLklOU0NIQUtFTFBJRUtSRUNIVFM",
    "F1DPwz91T7MV00-ab1SR4aA0ZwfwAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDAyLklOU0NIQUtFTFBJRUtSRUNIVFM",
    "F1DPwz91T7MV00-ab1SR4aA0ZwlwAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDAzLklOU0NIQUtFTFBJRUtSRUNIVFM",
    "F1DPwz91T7MV00-ab1SR4aA0ZwsQAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDA0LklOU0NIQUtFTFBJRUtSRUNIVFM",
    "F1DPwz91T7MV00-ab1SR4aA0ZwZgAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDA1LklOU0NIQUtFTFBJRUtSRUNIVFM"
]


def reset_data_struct(data):
    data = {
        "motor": {"webids": MOTOR_VALUES_WEBIDS, "latest_data": []},
        "control_left": {"webids": CONTROL_LEFT_WEBIDS, "latest_data": []},
        "control_right": {"webids": CONTROL_RIGHT_WEBIDS, "latest_data": []},
        "peak_current_left": {"webids": PEAK_CURRENT_LEFT, "latest_data": []},
        "peak_current_right": {"webids": PEAK_CURRENT_RIGHT, "latest_data": []},
    }


data = {
    "motor": {"webids": MOTOR_VALUES_WEBIDS, "latest_data": []},
    "control_left": {"webids": CONTROL_LEFT_WEBIDS, "latest_data": []},
    "control_right": {"webids": CONTROL_RIGHT_WEBIDS, "latest_data": []},
    "peak_current_left": {"webids": PEAK_CURRENT_LEFT, "latest_data": []},
    "peak_current_right": {"webids": PEAK_CURRENT_RIGHT, "latest_data": []},
}

reset_data_struct(data)

MINIBATCH_SIZE = 100


def thread_pull_data():
    while (True):
        print([x for x in data.keys()])
        while data["motor"]["latest_data"] < MINIBATCH_SIZE:
            print(list(len(data[x]["latest_data"]) for x in data.keys()))
            for attribute in data.keys():
                for switch in range(len(data[attribute]["webids"])):
                    resp = requests.get(STREAM_QUERY_WITH_START_TIME.format(data[attribute]["webids"][switch], "-10m"),
                                        auth=HTTPBasicAuth("Group09", "Hackathon09"), verify=False)
                    jsondata = json.loads(resp.text)
                    print("got response")
                    items = jsondata["Items"]
                    for reading in range(len(items)):
                        data[attribute]["latest_data"].append(
                            (items[reading]["Value"], dateutil.parser.parse(items[reading]["Timestamp"])))

            time.sleep(61)

    # We have enough data, call Martins function and reset
    reset_data_struct(data)


thread_pull_data()
