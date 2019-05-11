import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import datetime
import tempfile

muh_cache = {}
last_reported_timestamp = {}

next_random_detection = None

RANDOM_DETECTION_PERIOD = 30

def make_event_plot(start_time):
    f = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    f.close()

    # TODO: plot expected waveform in grey
    plt.plot([0, 1, 2], [0, 2, 0])

    # TODO: plot actual waveform

    # TODO: dump plot to file
    plt.savefig(f.name)

    return f.name

def martins_function(data):
    # data is a dict of attribute -> {"latest_data": list of tuple (float, datetime)}

    KEEP_LATEST = 100

    # we want to keep our own window of the last 30 seconds or so
    for key in data.keys():
        # update cache
        if key not in muh_cache:
            muh_cache[key] = []

        muh_cache[key] += data[key]['latest_data']

        # drop stale data
        # TODO: use a time interval instead of fixed number of entries
        muh_cache[key] = muh_cache[key][-KEEP_LATEST:]

    shit_to_return = []

    global next_random_detection

    # RANDOM DETECTION HACK
    if next_random_detection is None or datetime.datetime.now() > next_random_detection:
        timestamp = datetime.datetime.now()
        plot_url = make_event_plot(timestamp)
        shit_to_return += [dict(timestamp=timestamp,
                                         description='Whatever threshold was exceeded',
                                         severity='warning',
                                         plot_url=plot_url,
                                switch_id=1)]
        next_random_detection = datetime.datetime.now() + datetime.timedelta()
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
