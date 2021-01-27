import sys, os, math
from datetime import datetime, timedelta
from api.chat_replay_downloader import get_chat_replay, ChatReplayDownloader

def search(link, search_terms, analysis_interval, start_time, end_time):

    analysis_interval = int(analysis_interval)
    start_time = int(start_time)
    end_time = int(end_time)

    search_terms = search_terms.lower()
    search_terms = search_terms.split(',')
    for index, search_term in enumerate(search_terms):
        search_terms[index] = search_term.lower()

    print('search terms -> ' + str(search_terms))

    block_print()
    youtube_messages = get_chat_replay(link, start_time = start_time, end_time = end_time)
    enable_print()

    for index, message in enumerate(youtube_messages):
        youtube_messages[index]['message'] = message['message'].lower()

    duration = youtube_messages[-1]['time_in_seconds']

    buckets = []
    bucket_num = math.ceil(duration/(analysis_interval)) - 1

    next_lower_bound = 0
    next_upper_bound = analysis_interval

    buckets.append({
        'lower_bound': next_lower_bound,
        'lower_timestamp': str(timedelta(seconds=next_lower_bound)),
        'upper_bound': next_upper_bound,
        'upper_timestamp': str(timedelta(seconds=next_upper_bound)),
        'count': 0
    })

    for i in range(bucket_num):
        next_lower_bound = next_lower_bound + analysis_interval + 1
        next_upper_bound = next_lower_bound + analysis_interval
        buckets.append({
            'lower_bound': next_lower_bound,
            'lower_timestamp': str(timedelta(seconds=next_lower_bound)),
            'upper_bound': next_upper_bound,
            'upper_timestamp': str(timedelta(seconds=next_upper_bound)),
            'count': 0
        })

    for search_term in search_terms:
        for bucket in buckets:
            lower_bound = bucket['lower_bound']
            upper_bound = bucket['upper_bound']
            # print(lower_bound)
            # print(upper_bound)
            for message in youtube_messages:
                time_in_seconds = message['time_in_seconds']
                within_bucket_range = lower_bound <= time_in_seconds <= upper_bound
                if within_bucket_range:
                    if search_term in message['message']:
                        print(message)
                        bucket['count'] = bucket['count'] + 1
                # else:
                    # print(str(time_in_seconds <= upper_bound) + str(time_in_seconds >= lower_bound) + str(lower_bound) + ' ' + str(upper_bound) + str(message))
                    # pass

    # print(buckets)
    return buckets


# datetime.now().strftime("%H:%M:%S")

# Disable
def block_print():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enable_print():
    sys.stdout = sys.__stdout__