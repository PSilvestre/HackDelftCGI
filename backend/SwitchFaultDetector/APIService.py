import json, os
import time
import requests
from requests import Request, Session
from requests.auth import HTTPBasicAuth
import dateutil.parser
import urllib3

from martins_function import MartinsClass

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "detector.settings")
import django
django.setup()

from sfd.models import SwitchModel

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

TURN_AROUND_TIME_RIGHT= [
    "F1DPwz91T7MV00-ab1SR4aA0ZwGgAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDAxLk9NTE9PUFRJSkRSRUNIVFNfUkVMQUlT",
    "F1DPwz91T7MV00-ab1SR4aA0ZwhwAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDAyLk9NTE9PUFRJSkRSRUNIVFNfUkVMQUlT",
    "F1DPwz91T7MV00-ab1SR4aA0ZwnwAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDAzLk9NTE9PUFRJSkRSRUNIVFNfUkVMQUlT",
    "F1DPwz91T7MV00-ab1SR4aA0ZwuQAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDA0Lk9NTE9PUFRJSkRSRUNIVFNfUkVMQUlT",
    "F1DPwz91T7MV00-ab1SR4aA0ZwxwAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDA1Lk9NTE9PUFRJSkRSRUNIVFNfUkVMQUlT"
]

TURN_AROUND_TIME_LEFT = [
    "F1DPwz91T7MV00-ab1SR4aA0ZwGwAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDAxLk9NTE9PUFRJSkRMSU5LU19SRUxBSVM",
    "F1DPwz91T7MV00-ab1SR4aA0ZwhQAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDAyLk9NTE9PUFRJSkRMSU5LU19SRUxBSVM",
    "F1DPwz91T7MV00-ab1SR4aA0ZwnQAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDAzLk9NTE9PUFRJSkRMSU5LU19SRUxBSVM",
    "F1DPwz91T7MV00-ab1SR4aA0ZwtwAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDA0Lk9NTE9PUFRJSkRMSU5LU19SRUxBSVM",
    "F1DPwz91T7MV00-ab1SR4aA0ZwxgAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDA1Lk9NTE9PUFRJSkRMSU5LU19SRUxBSVM"
]

TIME_END_MOTOR_POWER_CONTROL_LEFT = [
    "F1DPwz91T7MV00-ab1SR4aA0ZwHQAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDAxLlRJSkRFSU5ETU9UT1JTVFJPT01DT05UUk9MRUxJTktT",
    "F1DPwz91T7MV00-ab1SR4aA0ZwiwAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDAyLlRJSkRFSU5ETU9UT1JTVFJPT01DT05UUk9MRUxJTktT",
    "F1DPwz91T7MV00-ab1SR4aA0ZwpgAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDAzLlRJSkRFSU5ETU9UT1JTVFJPT01DT05UUk9MRUxJTktT",
    "F1DPwz91T7MV00-ab1SR4aA0ZwvwAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDA0LlRJSkRFSU5ETU9UT1JTVFJPT01DT05UUk9MRUxJTktT",
    "F1DPwz91T7MV00-ab1SR4aA0ZwdAAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDA1LlRJSkRFSU5ETU9UT1JTVFJPT01DT05UUk9MRUxJTktT",
]

TIME_END_MOTOR_POWER_CONTROL_RIGHT = [
    "F1DPwz91T7MV00-ab1SR4aA0ZwHgAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDAxLlRJSkRFSU5ETU9UT1JTVFJPT01DT05UUk9MRVJFQ0hUUw",
    "F1DPwz91T7MV00-ab1SR4aA0ZwjAAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDAyLlRJSkRFSU5ETU9UT1JTVFJPT01DT05UUk9MRVJFQ0hUUw",
    "F1DPwz91T7MV00-ab1SR4aA0ZwpwAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDAzLlRJSkRFSU5ETU9UT1JTVFJPT01DT05UUk9MRVJFQ0hUUw",
    "F1DPwz91T7MV00-ab1SR4aA0ZwwAAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDA0LlRJSkRFSU5ETU9UT1JTVFJPT01DT05UUk9MRVJFQ0hUUw",
    "F1DPwz91T7MV00-ab1SR4aA0ZwdQAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDA1LlRJSkRFSU5ETU9UT1JTVFJPT01DT05UUk9MRVJFQ0hUUw"
]

TIME_STEERING_MOTOR_POWER_LEFT = [
    "F1DPwz91T7MV00-ab1SR4aA0ZwHwAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDAxLlRJSkRTVFVSSU5HTU9UT1JTVFJPT01MSU5LUw",
    "F1DPwz91T7MV00-ab1SR4aA0ZwjQAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDAyLlRJSkRTVFVSSU5HTU9UT1JTVFJPT01MSU5LUw",
    "F1DPwz91T7MV00-ab1SR4aA0ZwqAAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDAzLlRJSkRTVFVSSU5HTU9UT1JTVFJPT01MSU5LUw",
    "F1DPwz91T7MV00-ab1SR4aA0ZwwQAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDA0LlRJSkRTVFVSSU5HTU9UT1JTVFJPT01MSU5LUw",
    "F1DPwz91T7MV00-ab1SR4aA0ZwdgAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDA1LlRJSkRTVFVSSU5HTU9UT1JTVFJPT01MSU5LUw"
]
TIME_STEERING_MOTOR_POWER_RIGHT = [
    "F1DPwz91T7MV00-ab1SR4aA0ZwIAAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDAxLlRJSkRTVFVSSU5HTU9UT1JTVFJPT01SRUNIVFM",
    "F1DPwz91T7MV00-ab1SR4aA0ZwjgAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDAyLlRJSkRTVFVSSU5HTU9UT1JTVFJPT01SRUNIVFM",
    "F1DPwz91T7MV00-ab1SR4aA0ZwxQAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDAzLlRJSkRTVFVSSU5HTU9UT1JTVFJPT01SRUNIVFM",
    "F1DPwz91T7MV00-ab1SR4aA0ZwwgAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDA0LlRJSkRTVFVSSU5HTU9UT1JTVFJPT01SRUNIVFM",
    "F1DPwz91T7MV00-ab1SR4aA0ZwdwAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDA1LlRJSkRTVFVSSU5HTU9UT1JTVFJPT01SRUNIVFM"
]

OUT_OF_CONTROL_TIME = [
    "F1DPwz91T7MV00-ab1SR4aA0ZwIQAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDAxLlVJVENPTlRST0xFVElKRA",
    "F1DPwz91T7MV00-ab1SR4aA0ZwjwAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDAyLlVJVENPTlRST0xFVElKRA",
    "F1DPwz91T7MV00-ab1SR4aA0ZwqgAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDAzLlVJVENPTlRST0xFVElKRA",
    "F1DPwz91T7MV00-ab1SR4aA0ZwwwAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDA0LlVJVENPTlRST0xFVElKRA",
    "F1DPwz91T7MV00-ab1SR4aA0ZweAAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDA1LlVJVENPTlRST0xFVElKRA"
]

ENERGY_SURFACE_RIGHT = [
    "F1DPwz91T7MV00-ab1SR4aA0ZwEwAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDAxLkVORVJHSUUgT1BQRVJWTEFLVEUgUkVDSFRT",
    "F1DPwz91T7MV00-ab1SR4aA0ZwfQAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDAyLkVORVJHSUUgT1BQRVJWTEFLVEUgUkVDSFRT",
    "F1DPwz91T7MV00-ab1SR4aA0ZwlQAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDAzLkVORVJHSUUgT1BQRVJWTEFLVEUgUkVDSFR",
    "F1DPwz91T7MV00-ab1SR4aA0ZwrwAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDA0LkVORVJHSUUgT1BQRVJWTEFLVEUgUkVDSFRT",
    "F1DPwz91T7MV00-ab1SR4aA0ZwZAAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDA1LkVORVJHSUUgT1BQRVJWTEFLVEUgUkVDSFRT"
]

TURN_AROUND_TIME_LEFT_MOTOR = [
    "F1DPwz91T7MV00-ab1SR4aA0ZwGAAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDAxLk9NTE9PUFRJSkRMSU5LU19NT1RPUlNUUk9PTQ",
    "F1DPwz91T7MV00-ab1SR4aA0ZwhAAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDAyLk9NTE9PUFRJSkRMSU5LU19NT1RPUlNUUk9PTQ",
    "F1DPwz91T7MV00-ab1SR4aA0ZwnAAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDAzLk9NTE9PUFRJSkRMSU5LU19NT1RPUlNUUk9PTQ",
    "F1DPwz91T7MV00-ab1SR4aA0ZwtgAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDA0Lk9NTE9PUFRJSkRMSU5LU19NT1RPUlNUUk9PTQ",
    "F1DPwz91T7MV00-ab1SR4aA0ZwawAAAAT1NJSEFDS0FUSE9OXFdJU1NFTDA1Lk9NTE9PUFRJSkRMSU5LU19NT1RPUlNUUk9PTQ"
]

urllib3.disable_warnings()

def not_reset_data_struct():
    return {
        # "peak_current_left": {"webids": PEAK_CURRENT_LEFT, "latest_data": [[],[],[],[],[]]},
        # "peak_current_right": {"webids": PEAK_CURRENT_RIGHT, "latest_data": [[],[],[],[],[]]},
        # "turn_around_time_right": {"webids": TURN_AROUND_TIME_RIGHT, "latest_data": [[],[],[],[],[]]},
        # "turn_around_time_left": {"webids": TURN_AROUND_TIME_LEFT, "latest_data": [[],[],[],[],[]]},
        # "time_end_motor_Power_control_left": {"webids": TIME_END_MOTOR_POWER_CONTROL_LEFT, "latest_data": [[],[],[],[],[]]},
        "time_end_motor_Power_control_right": {"webids": TIME_END_MOTOR_POWER_CONTROL_RIGHT, "latest_data": [[],[],[],[],[]]},   # wel
        "time_steering_motor_power_left": {"webids": TIME_STEERING_MOTOR_POWER_LEFT, "latest_data": [[],[],[],[],[]]},      # wel
        "time_steering_motor_power_right": {"webids": TIME_STEERING_MOTOR_POWER_RIGHT, "latest_data": [[],[],[],[],[]]},  # goed
        # "out_of_control_time": {"webids": OUT_OF_CONTROL_TIME, "latest_data": [[],[],[],[],[]]}

        # todo: omlooptijdrechts relais
        # todo: flachtewatche

        "energy_surface_right": {"webids": ENERGY_SURFACE_RIGHT, "latest_data": [[],[],[],[],[]]},
        "turn_around_time_left_motor": {"webids": TURN_AROUND_TIME_LEFT_MOTOR, "latest_data": [[],[],[],[],[]]},
    }


def reset_data_struct():
    return {
        "motor": {"webids": MOTOR_VALUES_WEBIDS, "latest_data": [[],[],[],[],[]]},
        "control_left": {"webids": CONTROL_LEFT_WEBIDS, "latest_data": [[],[],[],[],[]]},
        "control_right": {"webids": CONTROL_RIGHT_WEBIDS, "latest_data": [[],[],[],[],[]]},
        "peak_current_left": {"webids": PEAK_CURRENT_LEFT, "latest_data": [[],[],[],[],[]]},
        "peak_current_right": {"webids": PEAK_CURRENT_RIGHT, "latest_data": [[],[],[],[],[]]},
        "turn_around_time_right": {"webids": TURN_AROUND_TIME_RIGHT, "latest_data": [[],[],[],[],[]]},
        "turn_around_time_left": {"webids": TURN_AROUND_TIME_LEFT, "latest_data": [[],[],[],[],[]]},
        "time_end_motor_Power_control_left": {"webids": TIME_END_MOTOR_POWER_CONTROL_LEFT, "latest_data": [[],[],[],[],[]]},
        "time_end_motor_Power_control_right": {"webids": TIME_END_MOTOR_POWER_CONTROL_RIGHT, "latest_data": [[],[],[],[],[]]},
        "time_steering_motor_power_left": {"webids": TIME_STEERING_MOTOR_POWER_LEFT, "latest_data": [[],[],[],[],[]]},
        "time_steering_motor_power_right": {"webids": TIME_STEERING_MOTOR_POWER_RIGHT, "latest_data": [[],[],[],[],[]]},
        "out_of_control_time": {"webids": OUT_OF_CONTROL_TIME, "latest_data": [[],[],[],[],[]]},

        "energy_surface_right": {"webids": ENERGY_SURFACE_RIGHT, "latest_data": [[],[],[],[],[]]},
        "turn_around_time_left_motor": {"webids": TURN_AROUND_TIME_LEFT_MOTOR, "latest_data": [[],[],[],[],[]]},
    }


MINIBATCH_SIZE = 50


def thread_pull_data_func(running):
    data = not_reset_data_struct()

    # preload old data to extract stats
    for attribute in data.keys():
        for switch in range(len(data[attribute]["webids"])):
            resp = requests.get(STREAM_QUERY_WITH_START_TIME.format(data[attribute]["webids"][switch], "-7d"),
                                auth=HTTPBasicAuth("Group09", "Hackathon09"), verify=False)
            jsondata = json.loads(resp.text)
            items = jsondata["Items"]
            for reading in range(len(items)):
                data[attribute]["latest_data"][switch].append(
                    (items[reading]["Value"], dateutil.parser.parse(items[reading]["Timestamp"])))

    print('make poo:')
    poo = MartinsClass(data)

    data = reset_data_struct()

    # loop for ever and pull new data in
    while (running[0]):
        #print('nu wachten op de batch')
        while all([len(data["motor"]["latest_data"][i]) < MINIBATCH_SIZE for i in range(5)]):
            for attribute in data.keys():
                for switch in range(len(data[attribute]["webids"])):
                    resp = requests.get(STREAM_QUERY_WITH_START_TIME.format(data[attribute]["webids"][switch], "-2m"),
                                        auth=HTTPBasicAuth("Group09", "Hackathon09"), verify=False)
                    jsondata = json.loads(resp.text)
                    items = jsondata["Items"]
                    for reading in range(len(items)):
                        data[attribute]["latest_data"][switch].append(
                            (items[reading]["Value"], dateutil.parser.parse(items[reading]["Timestamp"])))

            time.sleep(113.582789253790)            # i just want to sleep

        # We have enough data, call Martins function and reset
        results = poo.process_additional_data(data)
        print(results)

        for event in results:
            toSave = SwitchModel(switch_id=event["switch_id"], timestamp=event["timestamp"], description=event["description"], file_name=event["plot_url"], severity=event["severity"])
            toSave.save()
        # for event in results:
        #   toSave = SwitchModel(switch_id=, )

        data = reset_data_struct()

    print('de thread is done')
