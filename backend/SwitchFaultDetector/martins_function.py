import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np

import datetime
import tempfile

muh_big_cache = {}
last_reported_timestamp = {}

next_random_detection = None

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

def make_event_plot(starttime_in, switch_id):
    f = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    f.close()

    starttime = starttime_in - datetime.timedelta(seconds=3)
    endtime = starttime_in + datetime.timedelta(seconds=3)

    motorstroom_period = data_for_period(muh_big_cache[switch_id]['motor'], starttime, starttime_in, endtime)
    #motorstroom_period_ = motorstroom_period.tolist()
    #print(motorstroom_period)

    # TODO: plot expected waveform in grey

    plt.plot(motorstroom_period[:,0], motorstroom_period[:,1], color=(0,0,0), linewidth=3)
    plt.xlim([-3, 3])

    plt.savefig(f.name)

    return f.name

def martins_actual_function(data):
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
                muh_big_cache[switch_id][key][:,0] = datetime.datetime.fromtimestamp(0)

            # push old data
            muh_big_cache[switch_id][key][:-len(new_data),:] = muh_big_cache[switch_id][key][len(new_data):,:]

            for i, (value, timestamp) in enumerate(new_data):
                if KEEP_LATEST-len(new_data)+i >= 0:
                    muh_big_cache[switch_id][key][KEEP_LATEST-len(new_data)+i,:] = timestamp, value

    shit_to_return = []

    global next_random_detection

    for switch_id in muh_big_cache.keys():
        # RANDOM DETECTION HACK
        if next_random_detection is None or datetime.datetime.now() > next_random_detection:
            timestamp = muh_big_cache[switch_id]['motor'][-1,0]
            plot_url = make_event_plot(timestamp, switch_id)
            shit_to_return += [dict(timestamp=timestamp,
                                    description='Whatever threshold was exceeded',
                                    severity='warning',
                                    plot_url=plot_url,
                                    switch_id=switch_id)]
            next_random_detection = datetime.datetime.now() + datetime.timedelta(seconds=10)
        # END OF RANDOM DETECTION HACK

        # KEY_NAME = 'TODO'
        # THRESHOLD = 1000
        # TIME_TRAVEL = datetime.timedelta(seconds=3)

        # # dumb detection for now
        # if KEY_NAME in muh_cache:
        #     my_last = last_reported_timestamp[KEY_NAME] if KEY_NAME in last_reported_timestamp or None

        #     for i in range(len(muh_cache[KEY_NAME])):
        #         value, timestamp = muh_cache[KEY_NAME][i]

        #         if (my_last is None or timestamp > my_last) and value > THRESHOLD:
        #             plot_url = make_event_plot(timestamp - TIME_TRAVEL)

        #             shit_to_return += [dict(timestamp=timestamp,
        #                                     description='Whatever threshold was exceeded',
        #                                     severity='warning',
        #                                     plot_url=plot_url)]

        #             last_reported_timestamp[KEY_NAME] = my_last = timestamp

    return shit_to_return

def martins_function(data):
    try:
        return martins_actual_function(data)
    except:
        return []
