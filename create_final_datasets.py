import pandas
import numpy as np

####task1 - load received files
def load_files():

	classf = pandas.read_csv('class.csv', sep=';')
	testf = pandas.read_csv('test.csv', sep=';')
	test_lvlf = pandas.read_csv('test_level.csv', sep=';')

	return (classf, testf, test_lvlf)

####task2 - check if files are correct according to the data in the columns
# removed NaN numbers from the three tables
def check_correctness(file0, file1, file2):

	classf = file0.dropna().reset_index(drop=True)
	testf = file1.dropna().reset_index(drop=True)
	test_lvlf = file2.dropna().reset_index(drop=True)

	return (classf, testf, test_lvlf)

####task3 - dataset containing info about frequency of tests utilization
def get_test_utilization(class_file, test_file):

	class_com = pandas.DataFrame(class_file.loc[:, :])
	class_com = class_com.rename(index=str, columns={"id": "class_id", "name": "class_name"})
	class_com = class_com.drop(['institution_id', 'owner_id', 'created_at', 'updated_at', 'latest_test_time', 'has_student_with_scored_test'], axis=1)

	##test utilization
	test_ut = test_file.loc[:, ['id', 'class_id', 'created_at', 'authorized_at', 'test_level_id']]
	test_ut = pandas.merge(test_ut, class_com, on=['class_id'], how='inner')
	test_ut= test_ut.rename(index=str, columns={"id": "test_id",
		"created_at": "test_created_at", "authorized_at": "test_authorized_at",
		 "test_level_id": "test_level"})
	test_ut = test_ut[['class_id', 'class_name', 'teaching_hours', 'test_id', 'test_level', 'test_created_at', 'test_authorized_at']]

	return(class_com, test_ut)


##current_val = test_ut['class_id'][0]

def get_numoftests(test_ut, current_val):

	counter = 1
	index_counter = 0
	test_number_list = pandas.DataFrame(columns=['class_test_number'])

	#getting the number of tests in each of the classes
	for y in (test_ut['class_id'].values):
		if(y == current_val):
			test_number_list.loc[index_counter] = [counter]
			counter += 1
		else: #go to the next class
			counter = 1
			test_number_list.loc[index_counter] = [counter]
			current_val = y
		index_counter += 1

	test_ut = test_ut.reset_index(drop=True)
	test_number_list = test_number_list.reset_index(drop=True)

	return (test_ut, test_number_list)



####task4 - dataset containing info about average overall scores for tests in classes.
def get_test_avg(class_file, test_file):

	class_data = pandas.DataFrame(class_file.loc[:, :])
	class_data = class_data.rename(index=str, columns={"id": "class_id", "name": "class_name"})
	class_data = class_data.drop(['institution_id', 'owner_id', 'created_at', 'updated_at', 'latest_test_time', 'has_student_with_scored_test'], axis=1)

	test_avg = test_file.loc[:, ['id', 'class_id', 'created_at', 'authorized_at', 'test_status', 'overall_score']]
	test_avg = pandas.merge(test_avg, class_data, on=['class_id'], how='inner')
	test_avg= test_avg.rename(index=str, columns={"id": "test_id",
		"created_at": "test_created_at", "authorized_at": "test_authorized_at"})
	test_avg = test_avg[test_avg.test_status == 'SCORING_SCORED']

	return test_avg

#getting the average score in each of the classes
def get_avg_scores(test_avg):

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
		else: #count the average score and go to the next class
			test_avg_list.loc[index_counter_test, 'avg_class_test_overall_score'] = round(suma/counter, 0)
			test_avg_list.loc[index_counter_test, 'class_id'] = test_avg['class_id'][index_counter]
			index_counter_test += 1
			counter = 1
			suma = 0
			suma += test_avg['overall_score'][index_counter]
			current_val = y
		index_counter += 1

	return test_avg_list

def save_test_avg(test_avg, test_avg_list):	

	test_avg = test_avg.drop_duplicates(['class_id'], keep='first')
	test_avg_list = test_avg_list.drop(['class_id'], axis=1)

	test_avg = test_avg.reset_index(drop=True)
	test_avg_list = test_avg_list.reset_index(drop=True)

	#joining the data from csv files with created test_avg_list
	#containing column of average scored for each of the classes
	test_avg = test_avg.join(test_avg_list)
	test_avg = test_avg.drop(['test_id', 'test_status', 'overall_score'], axis=1)

	#rearrange columns in a particular order
	test_avg = test_avg[['class_id', 'class_name', 'teaching_hours', 'test_created_at', 'test_authorized_at', 'avg_class_test_overall_score']]
	test_avg.to_csv('test_average_scores.csv', sep=',', encoding='utf-8')


def main():

	files = load_files()
	classf = files[0]
	testf = files[1]
	test_lvlf = files[2]
	
	correct_files = check_correctness(classf, testf, test_lvlf)
	classf = correct_files[0]
	testf = correct_files[1]
	test_lvlf = correct_files[2]
	
	test_utilization = get_test_utilization(classf, testf)
	test_ut = test_utilization[1]
	current_val = test_ut['class_id'][0]

	test_ut, test_number_list = get_numoftests(test_ut, current_val)

	#joining the data from csv files with created test_number_list
	#containing column of number of tests for each of the classes
	test_ut = test_ut.join(test_number_list)
	test_ut.to_csv('test_utilization.csv', sep=',', encoding='utf-8')

	test_avg = get_test_avg(classf, testf)
	#print(test_avg)

	#current_val = test_avg['class_id'][0]
	#current_val = test_avg['class_id']
	#current_val = test_avg
	test_avg_list = get_avg_scores(test_avg)
	save_test_avg(test_avg, test_avg_list)


if __name__== "__main__":
    
	main()