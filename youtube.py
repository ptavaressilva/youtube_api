# -*- coding: utf-8 -*-
import pandas as pd
import datetime
import pickle
import time


def get_data(n_days_to_get):
    today = datetime.datetime.today()

    start_date_list = [(today - datetime.timedelta(days=x)).strftime("%Y-%m-%d")
                       for x in range(n_days_to_get, 0, -1)]
    end_date_list = [(today - datetime.timedelta(days=x-1)).strftime("%Y-%m-%d")
                     for x in range(n_days_to_get, 0, -1)]

    print('Start date: {}\nEnd date: {}'.format(
        start_date_list[0], end_date_list[-1]))

    youtube_analytics = pickle.load(open("api_client.pkl", "rb"))

    rows = []

    for start_date, end_date in zip(start_date_list, end_date_list):
        request = youtube_analytics.reports().query(
            endDate=end_date,
            ids="channel==MINE",
            metrics="views,comments,likes,dislikes,estimatedMinutesWatched,averageViewDuration",
            startDate=start_date
        )
        start_time = time.time()
        result = request.execute()
        end_time = time.time()
        print('Got data in range {} --> {}. Took {:.2f}s'.format(start_date,
                                                                 end_date, end_time - start_time))
        rows.append(result['rows'])

    rows_with_date = [[date]+i[0]
                      for i, date in zip(rows, start_date_list) if i != []]

    df = pd.DataFrame(rows_with_date, columns=['date', 'views', 'comments', 'likes',
                                               'dislikes', 'estimatedMinutesWatched', 'averageViewDuration'])

    df.set_index('date', inplace=True)

    return df
