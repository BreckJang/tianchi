from __future__ import division
import os
import numpy as np
import pandas as pd
from pandas import Series, DataFrame, read_csv
import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime
from glob import glob
from os import path
from datetime import datetime, timedelta

os.chdir('D://tianchi//p2_music')

def get_song_predict(in_fl, out_fl, songs):
    result = read_csv(in_fl, header=None, index_col=0)
    result[result  < 0] = 0
    result = pd.merge(result, songs[['song_id', 'artist_id']], how='left', left_index=True, right_on='song_id')
    result.drop('song_id', axis=1).groupby('artist_id').sum().to_csv(out_fl, header=None)
    return

def get_user_predict(infl, outfl):
    result = read_csv(infl, header=None, index_col=0)
    result[result < 0] = 0
    result.groupby(level=0).sum().to_csv(outfl, header=None)
    return

def get_user_song_average():
    input_file_1 = 'song_predict.csv'
    input_file_2 = 'user_predict.csv'
    output_file = 'average_predict.csv'
    tmp_1 = read_csv(input_file_1, header=None, index_col=0)
    tmp_2 = read_csv(input_file_2, header=None, index_col=0)
    result = (tmp_1 + tmp_2) / 2
    result.to_csv(output_file, header=None)
    return

def for_submit(input_file):
    output_file = 'mars_tianchi_artist_plays_predict.csv'
    start = datetime(2015, 8, 31)
    predict_day_num = 61
    names = [(start + timedelta(i)).strftime('%Y%m%d') for i in xrange(predict_day_num)]
    result = pd.read_csv(input_file, names= ['artist_id'] + names, index_col='artist_id')
    result = result.drop( '20150831', axis=1)
    result = result.stack().astype(int)
    answer = result.reset_index().reindex(columns=['artist_id', 0, 'level_1'])
    answer.to_csv(output_file, header=None, index=None)
    return

if __name__ == '__main__':
    part2_songs_index = ['song_id', 'artist_id', 'publist_time', 'song_init_plays', 'language', 'gender']
    part2_songs = pd.read_csv('part2_mars_tianchi_songs.csv', names=part2_songs_index)

    get_song_predict('song_predict_tmp.csv', 'song_predict.csv', part2_songs)
    get_user_predict('user_predict_tmp.csv', 'user_predict.csv')
    get_user_song_average()
    
    input_file = 'average_predict.csv'
    for_submit(input_file)
