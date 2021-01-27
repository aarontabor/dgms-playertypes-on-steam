#!/usr/bin/python

import ast
from collections import defaultdict
import csv
import numpy
import pandas as pd
import re
import sys
csv.field_size_limit(sys.maxsize)

user_files = 'users-1.csv users-2.csv users-3.csv users-4.csv users-5.csv users-6.csv'.split()

desired_field_order = 'profile_url dgms_habit dgms_moral dgms_agency dgms_narrative dgms_escapism dgms_pastime dgms_performance dgms_social dgms_habit_bin dgms_moral_bin dgms_agency_bin dgms_narrative_bin dgms_escapism_bin dgms_pastime_bin dgms_performance_bin dgms_social_bin age gender gender_other ethnicity education subject employment income marital gamer_identity enjoy_action enjoy_adventure enjoy_casual enjoy_fps enjoy_mmorpg enjoy_moba enjoy_platformer enjoy_puzzle enjoy_rpg enjoy_simulation enjoy_sports enjoy_strategy game_ban_count owned_count owned_games owned_action owned_adventure owned_casual owned_fps owned_mmorpg owned_moba owned_multiplayer owned_platformer owned_puzzle owned_rpg owned_simulation owned_sports owned_strategy owned_action_normalized owned_adventure_normalized owned_casual_normalized owned_fps_normalized owned_mmorpg_normalized owned_moba_normalized owned_multiplayer_normalized owned_platformer_normalized owned_puzzle_normalized owned_rpg_normalized owned_simulation_normalized owned_sports_normalized owned_strategy_normalized playtime_count playtime_action playtime_adventure playtime_casual playtime_fps playtime_mmorpg playtime_moba playtime_multiplayer playtime_platformer playtime_puzzle playtime_rpg playtime_simulation playtime_sports playtime_strategy playtime_action_normalized playtime_adventure_normalized playtime_casual_normalized playtime_fps_normalized playtime_mmorpg_normalized playtime_moba_normalized playtime_multiplayer_normalized playtime_platformer_normalized playtime_puzzle_normalized playtime_rpg_normalized playtime_simulation_normalized playtime_sports_normalized playtime_strategy_normalized recently_played_count recently_played_games recently_played_action recently_played_adventure recently_played_casual recently_played_fps recently_played_mmorpg recently_played_moba recently_played_multiplayer recently_played_platformer recently_played_puzzle recently_played_rpg recently_played_simulation recently_played_sports recently_played_strategy recently_played_action_normalized recently_played_adventure_normalized recently_played_casual_normalized recently_played_fps_normalized recently_played_mmorpg_normalized recently_played_moba_normalized recently_played_multiplayer_normalized recently_played_platformer_normalized recently_played_puzzle_normalized recently_played_rpg_normalized recently_played_simulation_normalized recently_played_sports_normalized recently_played_strategy_normalized friends_count friends primary_group group_count groups achievements_count achievements_action achievements_adventure achievements_casual achievements_fps achievements_mmorpg achievements_moba achievements_multiplayer achievements_platformer achievements_puzzle achievements_rpg achievements_simulation achievements_sports achievements_strategy achievements_action_normalized achievements_adventure_normalized achievements_casual_normalized achievements_fps_normalized achievements_mmorpg_normalized achievements_moba_normalized achievements_multiplayer_normalized achievements_platformer_normalized achievements_puzzle_normalized achievements_rpg_normalized achievements_simulation_normalized achievements_sports_normalized achievements_strategy_normalized artwork_count guides_count wishlists_count reviews_count reviews recommededs_count comments_count comments screenshots_count screenshots captions_count blurb profile'.split()



# initialize tag database
tag_records = [line for line in csv.reader(open('./metadata/tag_database.csv'))]
tag_records.pop(0)
tag_database = defaultdict(list)
for record in tag_records:
  tag_database[record[0]] = ast.literal_eval(record[1])


# initialize achievements database -- format: achievements[steam_id][app_id] = <achievement_count>
achievements = defaultdict(lambda : defaultdict(int))

## first load from initial scrape achievement dump
for _, user_row in pd.read_csv('users-6.csv').iterrows():
	profile_url = user_row['Profile URL'].rstrip('/')
	mturk_id = user_row['ID']
	initial_achievements = csv.DictReader(open('./baseline_achievements/' + str(mturk_id) + '.csv', 'rt', errors='replace'))
	for achievement_row in initial_achievements:
		app_id = achievement_row['App ID']
		achievement_count = achievement_row['Achieved']
		if achievement_count:
			achievements[profile_url][app_id] += int(achievement_count)
		else:
			achievements[profile_url][app_id] += 0

## then load incremental achievements from user files
for filename in user_files:
  user_data = pd.read_csv(filename)
  for index, row in user_data.iterrows():
    profile_url = row['Profile URL'].rstrip('/')
    user_achievements = {}
    try:
      user_achievements = eval(row['Achievements'])
    except SyntaxError:
      print("[Error] Couldn't parse achievements for " + profile_url)
    for app_id, game_achievements in user_achievements.items():
      for achievement in game_achievements:
      	if (achievement['achieved']):
        	achievements[profile_url][app_id] += 1


## initialize playtimes database -- format: playtimes_database[steam_id][app_id] = <playtime_forever>
playtimes_database = defaultdict(lambda: defaultdict(int))
for index, row in pd.read_csv('users-6.csv').iterrows():
  steam_id = row['Profile URL'].strip('/')
  for app_id, playtime_forever in re.findall("'appid': (\d+).*?'playtime_forever': (\d+)", row['Owned Games']):
    playtimes_database[steam_id][app_id] = int(playtime_forever)


# maintain a dgms category scores so that I can later determine median and simplify to boolean variables
dgms_scores = defaultdict(list)

df = pd.read_csv('dataset-5.csv')

clean_participants = []
for index, dirty_participant in df.iterrows():
  clean_participant = {}
  clean_participant['profile_url'] = dirty_participant['Profile URL']

  clean_participant['dgms_habit'] = dirty_participant['dgms_habit']
  dgms_scores['dgms_habit'].append(dirty_participant['dgms_habit'])
  clean_participant['dgms_moral'] = dirty_participant['dgms_moral']
  dgms_scores['dgms_moral'].append(dirty_participant['dgms_moral'])
  clean_participant['dgms_agency'] = dirty_participant['dgms_agency']
  dgms_scores['dgms_agency'].append(dirty_participant['dgms_agency'])
  clean_participant['dgms_narrative'] = dirty_participant['dgms_narrative']
  dgms_scores['dgms_narrative'].append(dirty_participant['dgms_narrative'])
  clean_participant['dgms_escapism'] = dirty_participant['dgms_escapism']
  dgms_scores['dgms_escapism'].append(dirty_participant['dgms_escapism'])
  clean_participant['dgms_pastime'] = dirty_participant['dgms_pastime']
  dgms_scores['dgms_pastime'].append(dirty_participant['dgms_pastime'])
  clean_participant['dgms_performance'] = dirty_participant['dgms_performance']
  dgms_scores['dgms_performance'].append(dirty_participant['dgms_performance'])
  clean_participant['dgms_social'] = dirty_participant['dgms_social']
  dgms_scores['dgms_social'].append(dirty_participant['dgms_social'])

  clean_participant['age'] = dirty_participant['Demographics_age']
  clean_participant['gender'] = dirty_participant['Demographics_gender']
  clean_participant['gender_other'] = dirty_participant['Demographics_gender_other']
  clean_participant['ethnicity'] = dirty_participant['Demographics_ethnicity']
  clean_participant['education'] = dirty_participant['Demographics_education']
  clean_participant['subject'] = dirty_participant['Demographics_subject']
  clean_participant['employment'] = dirty_participant['Demographics_employment']
  clean_participant['income'] = dirty_participant['Demographics_income']
  clean_participant['marital'] = dirty_participant['Demographics_marital']
  clean_participant['gamer_identity'] = dirty_participant['Demographics_gamer_identity']

  clean_participant['enjoy_action'] = 1 if bool(dirty_participant['Games_action']) else 0
  clean_participant['enjoy_adventure'] = 1 if bool(dirty_participant['Games_adventure']) else 0
  clean_participant['enjoy_casual'] = 1 if bool(dirty_participant['Games_casual']) else 0
  clean_participant['enjoy_fps'] = 1 if bool(dirty_participant['Games_fps']) else 0
  clean_participant['enjoy_mmorpg'] = 1 if bool(dirty_participant['Games_mmorpg']) else 0
  clean_participant['enjoy_moba'] = 1 if bool(dirty_participant['Games_moba']) else 0
  clean_participant['enjoy_platformer'] = 1 if bool(dirty_participant['Games_platform']) else 0
  clean_participant['enjoy_puzzle'] = 1 if bool(dirty_participant['Games_puzzle']) else 0
  clean_participant['enjoy_rpg'] = 1 if bool(dirty_participant['Games_rpg']) else 0
  clean_participant['enjoy_simulation'] = 1 if bool(dirty_participant['Games_sim']) else 0
  clean_participant['enjoy_sports'] = 1 if bool(dirty_participant['Games_sport']) else 0
  clean_participant['enjoy_strategy'] = 1 if bool(dirty_participant['Games_strategy']) else 0

  clean_participant['game_ban_count'] = dirty_participant['Number of Game Bans']

  ## Owned games
  game_ids = re.findall("'appid': (\d+)", dirty_participant['Owned Games'])
  clean_participant['owned_count'] = len(game_ids)
  clean_participant['owned_games'] = game_ids

  ### break-apart by tag
  tag_counts = defaultdict(int)
  for game_id in game_ids:
    tags = tag_database[game_id]
    for tag in tags:
      tag_counts[tag] += 1


  clean_participant['owned_action'] = tag_counts['Action']
  clean_participant['owned_adventure'] = tag_counts['Adventure']
  clean_participant['owned_casual'] = tag_counts['Casual']
  clean_participant['owned_fps'] = tag_counts['FPS']
  clean_participant['owned_mmorpg'] = tag_counts['MMORPG']
  clean_participant['owned_moba'] = tag_counts['MOBA']
  clean_participant['owned_multiplayer'] = tag_counts['Multiplayer']
  clean_participant['owned_platformer'] = tag_counts['Platformer']
  clean_participant['owned_puzzle'] = tag_counts['Puzzle']
  clean_participant['owned_rpg'] = tag_counts['RPG']
  clean_participant['owned_simulation'] = tag_counts['Simulation']
  clean_participant['owned_sports'] = tag_counts['Sports']
  clean_participant['owned_strategy'] = tag_counts['Strategy']

  if len(game_ids):
    clean_participant['owned_action_normalized'] = float(tag_counts['Action']) / float(len(game_ids))
    clean_participant['owned_adventure_normalized'] = float(tag_counts['Adventure']) / float(len(game_ids))
    clean_participant['owned_casual_normalized'] = float(tag_counts['Casual']) / float(len(game_ids))
    clean_participant['owned_fps_normalized'] = float(tag_counts['FPS']) / float(len(game_ids))
    clean_participant['owned_mmorpg_normalized'] = float(tag_counts['MMORPG']) / float(len(game_ids))
    clean_participant['owned_moba_normalized'] = float(tag_counts['MOBA']) / float(len(game_ids))
    clean_participant['owned_multiplayer_normalized'] = float(tag_counts['Multiplayer']) / float(len(game_ids))
    clean_participant['owned_platformer_normalized'] = float(tag_counts['Platformer']) / float(len(game_ids))
    clean_participant['owned_puzzle_normalized'] = float(tag_counts['Puzzle']) / float(len(game_ids))
    clean_participant['owned_rpg_normalized'] = float(tag_counts['RPG']) / float(len(game_ids))
    clean_participant['owned_simulation_normalized'] = float(tag_counts['Simulation']) / float(len(game_ids))
    clean_participant['owned_sports_normalized'] = float(tag_counts['Sports']) / float(len(game_ids))
    clean_participant['owned_strategy_normalized'] = float(tag_counts['Strategy']) / float(len(game_ids))
  else:
    clean_participant['owned_action_normalized'] = 0
    clean_participant['owned_adventure_normalized'] = 0
    clean_participant['owned_casual_normalized'] = 0
    clean_participant['owned_fps_normalized'] = 0
    clean_participant['owned_mmorpg_normalized'] = 0
    clean_participant['owned_moba_normalized'] = 0
    clean_participant['owned_multiplayer_normalized'] = 0
    clean_participant['owned_platformer_normalized'] = 0
    clean_participant['owned_puzzle_normalized'] = 0
    clean_participant['owned_rpg_normalized'] = 0
    clean_participant['owned_simulation_normalized'] = 0
    clean_participant['owned_sports_normalized'] = 0
    clean_participant['owned_strategy_normalized'] = 0


  ## Game Playtimes
  participant_playtimes = playtimes_database[clean_participant['profile_url']]

  playtime_total = 0
  playtime_by_genre = defaultdict(int)
  for game_id, playtime_forever in participant_playtimes.items():
    game_genres = tag_database[str(game_id)]
    playtime_total += playtime_forever
    for genre in game_genres:
      playtime_by_genre[genre] += playtime_forever

  clean_participant['playtime_count'] = playtime_total

  clean_participant['playtime_action'] = playtime_by_genre['Action']
  clean_participant['playtime_adventure'] = playtime_by_genre['Adventure']
  clean_participant['playtime_casual'] = playtime_by_genre['Casual']
  clean_participant['playtime_fps'] = playtime_by_genre['FPS']
  clean_participant['playtime_mmorpg'] = playtime_by_genre['MMORPG']
  clean_participant['playtime_moba'] = playtime_by_genre['MOBA']
  clean_participant['playtime_multiplayer'] = playtime_by_genre['Multiplayer']
  clean_participant['playtime_platformer'] = playtime_by_genre['Platformer']
  clean_participant['playtime_puzzle'] = playtime_by_genre['Puzzle']
  clean_participant['playtime_rpg'] = playtime_by_genre['RPG']
  clean_participant['playtime_simulation'] = playtime_by_genre['Simulation']
  clean_participant['playtime_sports'] = playtime_by_genre['Sports']
  clean_participant['playtime_strategy'] = playtime_by_genre['Strategy']

  if playtime_total:
    clean_participant['playtime_action_normalized'] = float(playtime_by_genre['Action']) / float(playtime_total)
    clean_participant['playtime_adventure_normalized'] = float(playtime_by_genre['Adventure']) / float(playtime_total)
    clean_participant['playtime_casual_normalized'] = float(playtime_by_genre['Casual']) / float(playtime_total)
    clean_participant['playtime_fps_normalized'] = float(playtime_by_genre['FPS']) / float(playtime_total)
    clean_participant['playtime_mmorpg_normalized'] = float(playtime_by_genre['MMORPG']) / float(playtime_total)
    clean_participant['playtime_moba_normalized'] = float(playtime_by_genre['MOBA']) / float(playtime_total)
    clean_participant['playtime_multiplayer_normalized'] = float(playtime_by_genre['Multiplayer']) / float(playtime_total)
    clean_participant['playtime_platformer_normalized'] = float(playtime_by_genre['Platformer']) / float(playtime_total)
    clean_participant['playtime_puzzle_normalized'] = float(playtime_by_genre['Puzzle']) / float(playtime_total)
    clean_participant['playtime_rpg_normalized'] = float(playtime_by_genre['RPG']) / float(playtime_total)
    clean_participant['playtime_simulation_normalized'] = float(playtime_by_genre['Simulation']) / float(playtime_total)
    clean_participant['playtime_sports_normalized'] = float(playtime_by_genre['Sports']) / float(playtime_total)
    clean_participant['playtime_strategy_normalized'] = float(playtime_by_genre['Strategy']) / float(playtime_total)
  else:
    clean_participant['playtime_action_normalized'] = 0
    clean_participant['playtime_adventure_normalized'] = 0
    clean_participant['playtime_casual_normalized'] = 0
    clean_participant['playtime_fps_normalized'] = 0
    clean_participant['playtime_mmorpg_normalized'] = 0
    clean_participant['playtime_moba_normalized'] = 0
    clean_participant['playtime_multiplayer_normalized'] = 0
    clean_participant['playtime_platformer_normalized'] = 0
    clean_participant['playtime_puzzle_normalized'] = 0
    clean_participant['playtime_rpg_normalized'] = 0
    clean_participant['playtime_simulation_normalized'] = 0
    clean_participant['playtime_sports_normalized'] = 0
    clean_participant['playtime_strategy_normalized'] = 0


  ## Recently Played Games
  recent_games_string = dirty_participant['Recents 1'] + dirty_participant['Recents 2'] + dirty_participant['Recents 3'] + dirty_participant['Recents 4'] + dirty_participant['Recents 5'] + dirty_participant['Recents 6']
  recent_ids = list(set(re.findall("'appid': (\d+)", recent_games_string)))
  clean_participant['recently_played_count'] = len(recent_ids)
  clean_participant['recently_played_games'] = recent_ids

  ### break-apart by tag
  tag_counts = defaultdict(int)
  for game_id in recent_ids:
    tags = tag_database[game_id]
    for tag in tags:
      tag_counts[tag] += 1

  clean_participant['recently_played_action'] = tag_counts['Action']
  clean_participant['recently_played_adventure'] = tag_counts['Adventure']
  clean_participant['recently_played_casual'] = tag_counts['Casual']
  clean_participant['recently_played_fps'] = tag_counts['FPS']
  clean_participant['recently_played_mmorpg'] = tag_counts['MMORPG']
  clean_participant['recently_played_moba'] = tag_counts['MOBA']
  clean_participant['recently_played_multiplayer'] = tag_counts['Multiplayer']
  clean_participant['recently_played_platformer'] = tag_counts['Platformer']
  clean_participant['recently_played_puzzle'] = tag_counts['Puzzle']
  clean_participant['recently_played_rpg'] = tag_counts['RPG']
  clean_participant['recently_played_simulation'] = tag_counts['Simulation']
  clean_participant['recently_played_sports'] = tag_counts['Sports']
  clean_participant['recently_played_strategy'] = tag_counts['Strategy']

  if len(recent_ids):
    clean_participant['recently_played_action_normalized'] = float(tag_counts['Action']) / float(len(recent_ids))
    clean_participant['recently_played_adventure_normalized'] = float(tag_counts['Adventure']) / float(len(recent_ids))
    clean_participant['recently_played_casual_normalized'] = float(tag_counts['Casual']) / float(len(recent_ids))
    clean_participant['recently_played_fps_normalized'] = float(tag_counts['FPS']) / float(len(recent_ids))
    clean_participant['recently_played_mmorpg_normalized'] = float(tag_counts['MMORPG']) / float(len(recent_ids))
    clean_participant['recently_played_moba_normalized'] = float(tag_counts['MOBA']) / float(len(recent_ids))
    clean_participant['recently_played_multiplayer_normalized'] = float(tag_counts['Multiplayer']) / float(len(recent_ids))
    clean_participant['recently_played_platformer_normalized'] = float(tag_counts['Platformer']) / float(len(recent_ids))
    clean_participant['recently_played_puzzle_normalized'] = float(tag_counts['Puzzle']) / float(len(recent_ids))
    clean_participant['recently_played_rpg_normalized'] = float(tag_counts['RPG']) / float(len(recent_ids))
    clean_participant['recently_played_simulation_normalized'] = float(tag_counts['Simulation']) / float(len(recent_ids))
    clean_participant['recently_played_sports_normalized'] = float(tag_counts['Sports']) / float(len(recent_ids))
    clean_participant['recently_played_strategy_normalized'] = float(tag_counts['Strategy']) / float(len(recent_ids))
  else:
    clean_participant['recently_played_action_normalized'] = 0
    clean_participant['recently_played_adventure_normalized'] = 0
    clean_participant['recently_played_casual_normalized'] = 0
    clean_participant['recently_played_fps_normalized'] = 0
    clean_participant['recently_played_mmorpg_normalized'] = 0
    clean_participant['recently_played_moba_normalized'] = 0
    clean_participant['recently_played_multiplayer_normalized'] = 0
    clean_participant['recently_played_platformer_normalized'] = 0
    clean_participant['recently_played_puzzle_normalized'] = 0
    clean_participant['recently_played_rpg_normalized'] = 0
    clean_participant['recently_played_simulation_normalized'] = 0
    clean_participant['recently_played_sports_normalized'] = 0
    clean_participant['recently_played_strategy_normalized'] = 0

  ## Friends
  friend_data = ast.literal_eval(dirty_participant['Friends'])
  friends = [friend_id for (friend_id, start_timestamp) in friend_data]
  clean_participant['friends_count'] = len(friends)
  clean_participant['friends'] = friends

  ## Groups
  clean_participant['primary_group'] = dirty_participant['Primary Group']
  groups = ast.literal_eval(dirty_participant['Groups'])
  clean_participant['group_count'] = len(groups)
  clean_participant['groups'] = groups


  ## Achievements
  participant_achievements = achievements[clean_participant['profile_url']]

  total_achievement_count = 0
  genre_achievement_counts = defaultdict(int)
  for game_id, achievement_count in participant_achievements.items():
    game_genres = tag_database[str(game_id)]
    total_achievement_count += achievement_count
    for genre in game_genres:
        genre_achievement_counts[genre] += achievement_count

  clean_participant['achievements_count'] = total_achievement_count

  clean_participant['achievements_action'] = genre_achievement_counts['Action']
  clean_participant['achievements_adventure'] = genre_achievement_counts['Adventure']
  clean_participant['achievements_casual'] = genre_achievement_counts['Casual']
  clean_participant['achievements_fps'] = genre_achievement_counts['FPS']
  clean_participant['achievements_mmorpg'] = genre_achievement_counts['MMORPG']
  clean_participant['achievements_moba'] = genre_achievement_counts['MOBA']
  clean_participant['achievements_multiplayer'] = genre_achievement_counts['Multiplayer']
  clean_participant['achievements_platformer'] = genre_achievement_counts['Platformer']
  clean_participant['achievements_puzzle'] = genre_achievement_counts['Puzzle']
  clean_participant['achievements_rpg'] = genre_achievement_counts['RPG']
  clean_participant['achievements_simulation'] = genre_achievement_counts['Simulation']
  clean_participant['achievements_sports'] = genre_achievement_counts['Sports']
  clean_participant['achievements_strategy'] = genre_achievement_counts['Strategy']

  if total_achievement_count:
    clean_participant['achievements_action_normalized'] = float(genre_achievement_counts['Action']) / float(total_achievement_count)
    clean_participant['achievements_adventure_normalized'] = float(genre_achievement_counts['Adventure']) / float(total_achievement_count)
    clean_participant['achievements_casual_normalized'] = float(genre_achievement_counts['Casual']) / float(total_achievement_count)
    clean_participant['achievements_fps_normalized'] = float(genre_achievement_counts['FPS']) / float(total_achievement_count)
    clean_participant['achievements_mmorpg_normalized'] = float(genre_achievement_counts['MMORPG']) / float(total_achievement_count)
    clean_participant['achievements_moba_normalized'] = float(genre_achievement_counts['MOBA']) / float(total_achievement_count)
    clean_participant['achievements_multiplayer_normalized'] = float(genre_achievement_counts['Multiplayer']) / float(total_achievement_count)
    clean_participant['achievements_platformer_normalized'] = float(genre_achievement_counts['Platformer']) / float(total_achievement_count)
    clean_participant['achievements_puzzle_normalized'] = float(genre_achievement_counts['Puzzle']) / float(total_achievement_count)
    clean_participant['achievements_rpg_normalized'] = float(genre_achievement_counts['RPG']) / float(total_achievement_count)
    clean_participant['achievements_simulation_normalized'] = float(genre_achievement_counts['Simulation']) / float(total_achievement_count)
    clean_participant['achievements_sports_normalized'] = float(genre_achievement_counts['Sports']) / float(total_achievement_count)
    clean_participant['achievements_strategy_normalized'] = float(genre_achievement_counts['Strategy']) / float(total_achievement_count)
  else:
    clean_participant['achievements_action_normalized'] = 0
    clean_participant['achievements_adventure_normalized'] = 0
    clean_participant['achievements_casual_normalized'] = 0
    clean_participant['achievements_fps_normalized'] = 0
    clean_participant['achievements_mmorpg_normalized'] = 0
    clean_participant['achievements_moba_normalized'] = 0
    clean_participant['achievements_multiplayer_normalized'] = 0
    clean_participant['achievements_platformer_normalized'] = 0
    clean_participant['achievements_puzzle_normalized'] = 0
    clean_participant['achievements_rpg_normalized'] = 0
    clean_participant['achievements_simulation_normalized'] = 0
    clean_participant['achievements_sports_normalized'] = 0
    clean_participant['achievements_strategy_normalized'] = 0


  ## Stats (TODO: I don't really know what to do with these)
  #clean_participant['stats_count'] = 
  #clean_participant['stats'] = 


  clean_participant['artwork_count'] = dirty_participant['Artwork Count']
  clean_participant['guides_count'] = dirty_participant['Guides Count']
  clean_participant['wishlists_count'] = dirty_participant['Wishlist Count']

  ## Reviews (TODO: What sort of features should I extract from here?)
  clean_participant['reviews_count'] = len(dirty_participant['Reviews'])
  #clean_participant['reviews'] = dirty_participant['Reviews']

  clean_participant['recommededs_count'] = dirty_participant['Recommended Count']

  ## Comments
  comment_recipients = re.findall("'recipient': (\d+)", dirty_participant['Comments'])
  clean_participant['comments_count'] = len(comment_recipients)
  #clean_participant['comments'] = dirty_participant['Comments'] # TODO: parse errors -- not really sure what to do about this

  ## Screenshots
  screenshot_app_ids = re.findall("'appid': (\d)", dirty_participant['Screenshots'])
  clean_participant['screenshots_count'] = len(screenshot_app_ids)
  #clean_participant['screenshots'] = dirty_participant['Screenshots']

  clean_participant['captions_count'] = dirty_participant['Captions Count']

  ## Videos (TODO: no-one posted videos)
  # clean_participant['videos_count'] = 
  # clean_participant['videos'] = 
  # clean_participant['video_captions_count'] =

  ## TODO: this results is a huge amount of data...
  # clean_participant['blurb'] = dirty_participant['Blurb']
  # clean_participant['profile'] = dirty_participant['Profile']

  ## Append to list
  clean_participants.append(clean_participant)


# DGMS categories now require further post processing
dgms_medians = {}
for category, scores in dgms_scores.items():
  dgms_medians[category] = numpy.median([float(s) for s in scores])

for clean_participant in clean_participants:
  for category, median in dgms_medians.items():
      clean_participant[category + '_bin'] = 1 if float(clean_participant[category]) >= median else -1


## Write everything to a csv file
writer = csv.DictWriter(open('processed-dataset-6.csv', 'w+', newline=''), desired_field_order)
writer.writeheader()
writer.writerows(clean_participants)
