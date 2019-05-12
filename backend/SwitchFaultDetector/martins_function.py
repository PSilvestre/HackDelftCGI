import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np

import datetime
import os
import pytz
import tempfile

muh_big_cache = {}
last_reported_timestamp = {}

next_random_detection = None
good_waveform = np.loadtxt(os.path.join(os.path.dirname(__file__), '../../good_waveform.csv'), delimiter=',')

RANDOM_DETECTION_PERIOD = 30

def data_for_period(table, start, origin, end):
    start_index = max(0, np.argmax(table[:,0] > start) - 1)

    bools = table[:,0] > end
    if not any(bools):
        end_index = table.shape[0]
    else:
        end_index = np.argmax(bools) + 2

    #     print('SPAN', start_index, end_index)
    cutout = np.copy(table[start_index:end_index])
    #t[:,0] = [(y - start).seconds for y in t[:,0]]
    #print(table.shape)
    t = np.zeros(cutout.shape)
    #print([(y - start) for y in cutout[:,0]])
    t[:,0] = [(y - origin).total_seconds() for y in cutout[:,0]]
    t[:,1] = cutout[:,1]
    #t = np.vstack([[(y - start).seconds for y in table[:,0]], table[:,1]])
    #print(t.shape)
    return t

def find_peak_before_time(switch_id, time):
    # to do that, iterate backwards until we get a peak and then a zero
    i = muh_big_cache[switch_id]['motor'].shape[0] - 1

    while i >= 0:
        # found the peak
        if muh_big_cache[switch_id]['motor'][i][1] is None:
            return None
        elif muh_big_cache[switch_id]['motor'][i][0] < time and muh_big_cache[switch_id]['motor'][i][1] > 10:
            break
        else:
            i -= 1

    while i >= 0:
        # found the zero
        if muh_big_cache[switch_id]['motor'][i][1] is None:
            return None
        elif muh_big_cache[switch_id]['motor'][i][1] < 0.3:
            break
        else:
            i -= 1

    if i >= 0:
        return i
    else:
        return None


def make_event_plot(starttime_in, switch_id):
    # find where the event proper starts (the starttime we get is in fact, time of detection)
    i = find_peak_before_time(switch_id, starttime_in)

    if i is not None:
        starttime_in = muh_big_cache[switch_id]['motor'][i][0]

    starttime = starttime_in - datetime.timedelta(seconds=0.5)
    endtime = starttime_in + datetime.timedelta(seconds=4)

    motorstroom_period = data_for_period(muh_big_cache[switch_id]['motor'], starttime, starttime_in, endtime)
    #motorstroom_period_ = motorstroom_period.tolist()
    #print(motorstroom_period)

    f = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    f.close()

    plt.plot(good_waveform[:,0], good_waveform[:,1], color=(0,0,0), alpha=0.3, linewidth=2)

    plt.plot(motorstroom_period[:,0], motorstroom_period[:,1], '--', color=(0.9, 0.2, 0.07), alpha=1, linewidth=2)
    plt.xlim([-0.5, 2])
    plt.grid()

    plt.savefig(f.name)

    return f.name

class MartinsClass:
    # calculate stats over historic past
    def __init__(self, data):
        muh_old_data_cache = {}
        self.attribute_mean = {}
        self.attribute_stddev = {}

        for key in data.keys():
            for switch_id in range(len(data[key]['latest_data'])):
                new_data = data[key]['latest_data'][switch_id]

                if switch_id not in muh_old_data_cache:
                    muh_old_data_cache[switch_id] = {}

                muh_len = len(new_data)
                muh_old_data_cache[switch_id][key] = np.empty((muh_len, 2), dtype=object)

                for i, (value, timestamp) in enumerate(new_data):
                    muh_old_data_cache[switch_id][key][i,:] = timestamp, value

                self.attribute_mean[(switch_id, key)] = np.mean(muh_old_data_cache[switch_id][key][:,1])
                self.attribute_stddev[(switch_id, key)] = np.std(muh_old_data_cache[switch_id][key][:,1])

        print('MEAN', self.attribute_mean)
        print('STD-DEV', self.attribute_stddev)

    def martins_actual_like_function(self, data):
        # data is a dict of attribute -> {"latest_data": list of list [0:num_switches] of tuple (float, datetime)}

        KEEP_LATEST = 100

        # we want to keep our own window of the last 30 seconds or so
        for key in data.keys():
            for switch_id in range(len(data[key]['latest_data'])):
                new_data = data[key]['latest_data'][switch_id]

                if not len(new_data):
                    continue

                # update cache
                if switch_id not in muh_big_cache:
                    muh_big_cache[switch_id] = {}
                if key not in muh_big_cache[switch_id]:
                    muh_big_cache[switch_id][key] = np.empty((KEEP_LATEST, 2), dtype=object)
                    muh_big_cache[switch_id][key][:,0] = datetime.datetime.fromtimestamp(0, tz=pytz.UTC)   # i hate you i hate you i hate you i hate y

                # push old data
                muh_big_cache[switch_id][key][:-len(new_data),:] = muh_big_cache[switch_id][key][len(new_data):,:]

                for i, (value, timestamp) in enumerate(new_data):
                    if KEEP_LATEST-len(new_data)+i >= 0:
                        muh_big_cache[switch_id][key][KEEP_LATEST-len(new_data)+i,:] = timestamp, value

        shit_to_return = []

        global next_random_detection

        # for switch_id in muh_big_cache.keys():
        #     # RANDOM DETECTION HACK
        #     # if next_random_detection is None or datetime.datetime.now() > next_random_detection:
        #     #     timestamp = muh_big_cache[switch_id]['motor'][-1,0]
        #     #     plot_url = make_event_plot(timestamp, switch_id)
        #     #     shit_to_return += [dict(timestamp=timestamp,
        #     #                             description='Whatever threshold was exceeded',
        #     #                             severity='warning',
        #     #                             plot_url=plot_url,
        #     #                             switch_id=switch_id)]
        #     #     next_random_detection = datetime.datetime.now() + datetime.timedelta(seconds=RANDOM_DETECTION_PERIOD)
        #     # END OF RANDOM DETECTION HACK

        # dumb detection for now
        for switch_id in muh_big_cache.keys():
            all_criteria = [
                ('time_end_motor_Power_control_right', lambda value: value > self.attribute_mean[(switch_id, 'time_end_motor_Power_control_right')] +
                                                                     3 * self.attribute_stddev[(switch_id, 'time_end_motor_Power_control_right')],
                 'magic value time_end_motor_Power_control_right is above another magic value'),
            ]

            for KEY_NAME, callback, message in all_criteria:
                if KEY_NAME in muh_big_cache[switch_id]:
                    my_last = last_reported_timestamp[(switch_id, KEY_NAME)] if (switch_id, KEY_NAME) in last_reported_timestamp else None

                    for i in range(len(muh_big_cache[switch_id][KEY_NAME])):
                        timestamp, value = muh_big_cache[switch_id][KEY_NAME][i]

                        if value is not None and (my_last is None or timestamp > my_last) and callback(value):
                            plot_url = make_event_plot(timestamp, switch_id)

                            shit_to_return += [dict(timestamp=timestamp,
                                                    description=message,
                                                    severity='warning',
                                                    plot_url=plot_url,
                                                    switch_id=switch_id)]

                            last_reported_timestamp[(switch_id, KEY_NAME)] = my_last = timestamp

        return shit_to_return

    def process_additional_data(self, data):
        #try:
        return self.martins_actual_like_function(data)
        #except Exception as ex:
        #    # print(ex)
        #    return []
