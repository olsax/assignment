import pandas
import numpy as np

pandas.set_option('display.max_columns', 15)
pandas.set_option('display.width', 800)

#task1 - load received files
classf = pandas.read_csv('class.csv', sep=';')
testf = pandas.read_csv('test.csv', sep=';')
test_lvlf = pandas.read_csv('test_level.csv', sep=';')


#task2 - check if files are correct according to the data in the columns
# removed NaN numbers from the three tables
testf = testf.dropna().reset_index(drop=True)
test_lvlf = test_lvlf.dropna().reset_index(drop=True)
classf = classf.dropna().reset_index(drop=True)

#task3 - dataset containing info about frequency of tests utilization
class_com = pandas.DataFrame(classf.loc[:, :])
class_com = class_com.rename(index=str, columns={"id": "class_id", "name": "class_name"})
class_com = class_com.drop(['institution_id', 'owner_id', 'created_at', 'updated_at', 'latest_test_time', 'has_student_with_scored_test'], axis=1)

test_ut = testf.loc[:, ['id', 'class_id', 'created_at', 'authorized_at', 'test_level_id']]
test_ut = pandas.merge(test_ut, class_com, on=['class_id'], how='inner')
test_ut= test_ut.rename(index=str, columns={"id": "test_id",
	"created_at": "test_created_at", "authorized_at": "test_authorized_at",
	 "test_level_id": "test_level"})
test_ut = test_ut[['class_id', 'class_name', 'teaching_hours', 'test_id', 'test_level', 'test_created_at', 'test_authorized_at']]

current_val = test_ut['class_id'][0]
counter = 1
index_counter = 0
test_number_list = pandas.DataFrame(columns=['class_test_number'])

for y in (test_ut['class_id'].values):
	if(y == current_val):
		test_number_list.loc[index_counter] = [counter]
		counter += 1
	else:
		counter = 1
		test_number_list.loc[index_counter] = [counter]
		current_val = y
	index_counter += 1

test_ut = test_ut.reset_index(drop=True)
test_number_list = test_number_list.reset_index(drop=True)
test_ut = test_ut.join(test_number_list)

test_ut.to_csv('test_utilization.csv', sep=',', encoding='utf-8')


#task4 - dataset containing info about average overall scores for tests in classes.
class_data = pandas.DataFrame(classf.loc[:, :])
class_data = class_data.rename(index=str, columns={"id": "class_id", "name": "class_name"})
class_data = class_data.drop(['institution_id', 'owner_id', 'created_at', 'updated_at', 'latest_test_time', 'has_student_with_scored_test'], axis=1)


test_avg = testf.loc[:, ['id', 'class_id', 'created_at', 'authorized_at', 'test_status', 'overall_score']]
test_avg = pandas.merge(test_avg, class_data, on=['class_id'], how='inner')
test_avg= test_avg.rename(index=str, columns={"id": "test_id",
	"created_at": "test_created_at", "authorized_at": "test_authorized_at"})
test_avg = test_avg[test_avg.test_status == 'SCORING_SCORED']

current_val = test_avg['class_id'][0]
counter = 1
index_counter = 0
index_counter_test = 1
suma = 0
test_avg_list = pandas.DataFrame(columns=['avg_class_test_overall_score', 'class_id'])
test_avg_list.loc[0, 'class_id'] = test_avg['class_id'][0]
for y in (test_avg['class_id'].values):
	if(y == current_val):
		if(y == test_avg['class_id'][0]):
			test_avg_list.loc[0, 'avg_class_test_overall_score'] = round(suma/counter, 0)
		suma += test_avg['overall_score'][index_counter]
		counter += 1
	else:
		test_avg_list.loc[index_counter_test, 'avg_class_test_overall_score'] = round(suma/counter, 0)
		test_avg_list.loc[index_counter_test, 'class_id'] = test_avg['class_id'][index_counter]
		index_counter_test += 1
		counter = 1
		suma = 0
		suma += test_avg['overall_score'][index_counter]
		current_val = y
	index_counter += 1

test_avg = test_avg.drop_duplicates(['class_id'], keep='first')
test_avg_list = test_avg_list.drop(['class_id'], axis=1)

test_avg = test_avg.reset_index(drop=True)
test_avg_list = test_avg_list.reset_index(drop=True)

test_avg = test_avg.join(test_avg_list)
test_avg = test_avg.drop(['test_id', 'test_status', 'overall_score'], axis=1)
test_avg = test_avg[['class_id', 'class_name', 'teaching_hours', 'test_created_at', 'test_authorized_at', 'avg_class_test_overall_score']]
test_avg.to_csv('test_average_scores.csv', sep=',', encoding='utf-8')
