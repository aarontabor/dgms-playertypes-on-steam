#
# CMPT820: Course Project -- Predicting DGMS Player Type
#
# Aaron Tabor, awt282
# University of Saskatchewan, Saskatoon, SK
#

# TODO: preprocessing.StandardScaler (get a common variance)


from numpy import mean, var
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


label_columns = 'dgms_habit_bin dgms_moral_bin dgms_agency_bin dgms_narrative_bin dgms_escapism_bin dgms_pastime_bin dgms_performance_bin dgms_social_bin'.split()

genres = 'action adventure casual fps mmorpg moba platformer puzzle rpg simulation sports strategy'.split()
enjoy_columns = ['enjoy_' + genre for genre in genres]
owned_columns = ['owned_' + genre + '_normalized' for genre in genres]
playtime_columns = ['playtime_' + genre + '_normalized' for genre in genres]
recently_played_columns = ['recently_played_' + genre + '_normalized' for genre in genres]
achievements_columns = ['achievements_' + genre + '_normalized' for genre in genres]

training_columns = 'gamer_identity owned_count playtime_count recently_played_count friends_count group_count achievements_count wishlists_count'.split() + enjoy_columns + owned_columns +  playtime_columns + recently_played_columns + achievements_columns
columns_to_scale = 'gamer_identity owned_count playtime_count recently_played_count friends_count group_count achievements_count wishlists_count'.split()


# import dataset
dataset = pd.read_csv('../data/dataset.csv')


# pre-processing: scale columns to a common range
scaled_columns = pd.DataFrame(StandardScaler().fit_transform(dataset[columns_to_scale]), columns=columns_to_scale)
for column in columns_to_scale:
	dataset[column] = scaled_columns[column]



# pre-processing: reduce dimensionality by conducting PCA on all per-genre columns
n_components = 2
for prefix, columns in [('owned', owned_columns), ('playtime', playtime_columns), ('recently_played', recently_played_columns), ('achievements', achievements_columns)]:

	new_columns = ['%s_pca_%d' % (prefix, i) for i in range(n_components)]
	principle_components = pd.DataFrame(PCA(n_components=n_components).fit_transform(dataset[columns]), columns=new_columns)
	for column in columns:
		training_columns.remove(column)
	for column in new_columns:
		dataset[column] = principle_components[column]
		training_columns.append(column)


# reserve 10% of data for final test
peeking_xs, reserved_xs, peeking_labels, reserved_labels = train_test_split(dataset[training_columns], dataset[label_columns], test_size=0.1)


# perform N-fold cross validation for each DGMS category (repeat R times)
peeking_accuracies = {}
for category in label_columns:
  classifier = SVC()
  accuracies = cross_val_score(classifier, peeking_xs, peeking_labels[category], cv=10)
  #error_rates = [1.0-accuracy_rate for accuracy_rate in accuracy_rates]
  peeking_accuracies[category] = accuracies


# report results
print('5-Fold Cross Validation Results')
for category, accuracies in peeking_accuracies.items():
  print('%s,%f,%f' % (category, mean(accuracies), var(accuracies)))
print('Overall,%f' % mean([mean(a) for a in [accuracies for accuracies in peeking_accuracies.values()]]))

# perform the 'true' test, with the hold-out data 
testing_accuracies = {}
for category in label_columns:
	classifier = SVC()
	classifier.fit(peeking_xs, peeking_labels[category])
	accuracy = classifier.score(reserved_xs, reserved_labels[category])
	testing_accuracies[category] = accuracy

# report results
print()
print('Reserved Dataset Results')
for category, accuracy in testing_accuracies.items():
  print('%s,%f' % (category, accuracy))
print('Overall: %f' % mean([mean(a) for a in [accuracies for accuracies in testing_accuracies.values()]]))