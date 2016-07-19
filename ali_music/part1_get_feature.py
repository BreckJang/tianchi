# python 2.7.11
# author: Cheff YU && Zhiyuan XIONG
# July.7th, 2016

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

def get_song_dayly_play(outfl, actions, songs):
    play_df = actions[actions['action_type'] == 1][['song_id', 'action_type', 'ds']]
    dayly_play_amount = play_df.groupby(['song_id', 'ds'])['action_type'].count().unstack()
    amounts = DataFrame(dayly_play_amount, index=songs['song_id'])
    amounts.fillna(0).to_csv(outfl, header=None)
    return

def get_user_action(actions ,of):
    user_action_tmp = actions.groupby(['user_id', 'action_type'])[['ds']].count().unstack()
    user_action_tmp.columns = user_action_tmp.columns.droplevel()
    user_action_tmp = user_action_tmp.fillna(0)
    user_action_tmp.sort_values(by=1).to_csv(of, header=None)
    return

def get_user_frequency(infl, outfl, actions, songs):
    user_play_frequency = pd.read_csv(infl, names=['user_id', 'play', 'download', 'favorite'], skiprows=[0])
    user_play_frequency = user_play_frequency.reindex(columns=['user_id', 'play'])
    action_tmp = actions[actions['action_type'] == 1]
    action_tmp = action_tmp.drop(['gmt_create'], axis=1)
    action_tmp = pd.merge(action_tmp, user_play_frequency, how='left', on='user_id')
    action_tmp = pd.merge(action_tmp, songs[['song_id', 'artist_id']], how='left', on='song_id')
    action_tmp = action_tmp.groupby(['play', 'artist_id', 'ds'])['action_type'].sum()
    action_tmp.unstack(fill_value=0).to_csv(outfl, header=None)
    return


if __name__ == '__main__':
    part2_songs_index = ['song_id', 'artist_id', 'publist_time', 'song_init_plays', 'language', 'gender']
    part2_songs = pd.read_csv('part2_mars_tianchi_songs.csv', names=part2_songs_index)
    part2_actions_index = ['user_id', 'song_id', 'gmt_create', 'action_type', 'ds']
    part2_actions = pd.read_csv('part2_mars_tianchi_user_actions.csv', names=part2_actions_index)

    get_song_dayly_play('part2_song_dayly_play.csv', part2_actions, part2_songs)

    get_user_action(part2_actions, 'part2_user_actions.csv')
    get_user_frequency('part2_user_actions.csv', 'part2_user_frequency.csv', part2_actions, part2_songs)




