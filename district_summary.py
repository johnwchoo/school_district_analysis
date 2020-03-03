import pandas as pd
import numpy as np

school_data_to_load = "Resources/schools_complete.csv"
student_data_to_load = "Resources/students_complete.csv"

school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)

school_data_complete = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])

# print(school_data_complete)

# Total School ------------------------------------------------------------------------------------
total_schools = school_data_complete["school_name"].nunique()
# print("Total Schools: " + str(total_schools))

total_students = school_data_complete["student_name"].nunique()
# print("Total Students: " + str(total_students))
	

# Total Budget ------------------------------------------------------------------------------------

school_budget = school_data_complete["budget"]
unique_budgets = []
for values in school_budget:
    if values not in unique_budgets:
        unique_budgets.append(values)


unique_budgets_int = [int(i) for i in unique_budgets]
total_budget = sum(unique_budgets_int)
total_budget = "{:,}".format(total_budget)
# print("Total Budget: $" + str(total_budget))



# Average Math Score ------------------------------------------------------------------------------------

math_score = school_data_complete["math_score"]
unique_math_scores = []
for values in math_score:
	if values not in unique_math_scores:
		unique_math_scores.append(values)

unique_math_scores_int = [int(i) for i in unique_math_scores]
unique_math_scores_avg = sum(unique_math_scores_int)/(len(unique_math_scores_int) - 1)
# print(unique_math_scores_avg)


# Average Reading Score ------------------------------------------------------------------------------------
reading_scores = school_data_complete["reading_score"]
unique_reading_scores = []
for values in reading_scores:
	if values not in unique_reading_scores:
		unique_reading_scores.append(values)

unique_reading_scores_int = [int(i) for i in unique_reading_scores]
unique_reading_scores_avg = sum(unique_reading_scores_int)/(len(unique_reading_scores_int) - 1)



# Passing Math Score % ------------------------------------------------------------------------------------
passing_math_scores = []
for values in math_score:
	if values >= 70:
		passing_math_scores.append(values)



passing_math_scores_percentage = (len(passing_math_scores) * 100)/len(math_score)
# print(passing_math_score_percentage)


# Passing Reading Score % ------------------------------------------------------------------------------------
passing_reading_scores = []
for values in reading_scores:
	if values >= 70:
		passing_reading_scores.append(values)

passing_reading_scores_percentage = (len(passing_reading_scores) * 100)/len(reading_scores)



# Overall Passing Rate % ------------------------------------------------------------------------------------
overall_passing_rate = (passing_math_scores_percentage + passing_reading_scores_percentage)/2
# print(overall_passing_rate)


# Output ------------------------------------------------------------------------------------
#print(" ")
#print("District Summary")
#print("--------------------")
#print("Total Schools: " + str(total_schools))
#print("Total Students: " + str(total_students))
#print("Total Budget: $" + str(total_budget))
#print("Average Math Score: " + str(unique_math_scores_avg))
#print("Average Reading Score: " + str(unique_reading_scores_avg))
#print("% Passing Math: " + str(passing_math_scores_percentage))
#print("% Passing Reading: " + str(passing_reading_scores_percentage))
#print("% Passing Rate: " + str(overall_passing_rate))


district_summary = pd.DataFrame({"Total Schools": [total_schools], 
                                 "Total Students": [total_students], 
                                 "Total Budget": [total_budget],
                                 "Average Math Score": [unique_math_scores_avg], 
                                 "Average Reading Score": [unique_reading_scores_avg],
                                 "% Passing Math": [passing_math_scores_percentage],
                                 "% Passing Reading": [passing_reading_scores_percentage],
                                 "% Overall Passing Rate": [overall_passing_rate]})

print(district_summary)
