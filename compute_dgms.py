import pandas as pd

scoring_template = {
    'dgms_habit': 'DGMS_1 DGMS_2 DGMS_3'.split(),
    'dgms_moral': 'DGMS_4 DGMS_5 DGMS_6 DGMS_7'.split(),
    'dgms_agency': 'DGMS_8 DGMS_9 DGMS_10 DGMS_11 DGMS_12'.split(),
    'dgms_narrative': 'DGMS_13 DGMS_14 DGMS_15 DGMS_16 DGMS_17 DGMS_18 DGMS_19 DGMS_20 DGMS_21'.split(),
    'dgms_escapism': 'DGMS_22 DGMS_23 DGMS_24 DGMS_25 DGMS_26'.split(),
    'dgms_pastime': 'DGMS_27 DGMS_28 DGMS_29 DGMS_30'.split(),
    'dgms_performance': 'DGMS_31 DGMS_32 DGMS_33 DGMS_34'.split(),
    'dgms_social': 'DGMS_35 DGMS_36 DGMS_37 DGMS_38 DGMS_39 DGMS_40 DGMS_41 DGMS_42 DGMS_43'.split(),
  }

demographic_columns = 'Demographics_age Demographics_gender Demographics_gender_other Demographics_ethnicity Demographics_education Demographics_subject Demographics_employment Demographics_income Demographics_marital'.split()

genre_preference_columns = 'Games_action Games_adventure Games_casual Games_fps Games_mmorpg Games_moba Games_mobile Games_music Games_platform Games_puzzle Games_rpg Games_sim Games_sport Games_strategy'.split()


# read csv file
raw_data = pd.read_csv(open('demographics.csv'))

# filter valid DGMS columns
dgms_questionnaire_responses = raw_data[raw_data['DGMS_1'] != 0]

# reverse scoring for question 'DGMS_6'
dgms_questionnaire_responses['DGMS_6'] = 6 - dgms_questionnaire_responses['DGMS_6']

# compute category scores and store in a new data frame
dgms_category_scores = pd.DataFrame()
dgms_category_scores['profile URL'] = dgms_questionnaire_responses['profile URL']
for category_name, column_names in scoring_template.items():
  dgms_category_scores[category_name] = dgms_questionnaire_responses[column_names].mean(axis=1)

# also take the Demographics columns since these will be useful later
for column_name in demographic_columns:
  dgms_category_scores[column_name] = dgms_questionnaire_responses[column_name]

# Game genre preferences will also be useful later
for column_name in genre_preference_columns:
  dgms_category_scores[column_name] = dgms_questionnaire_responses[column_name]


# dump to a csv file
print(dgms_category_scores.head())
dgms_category_scores.to_csv('dgms-results.csv')

