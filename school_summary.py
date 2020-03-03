#School Summary

#Create an overview table that summarizes key metrics about each school, including:

#School Name +
#School Type + 
#Total Students +
#Total School Budget +
#Per Student Budget +
#Average Math Score +
#Average Reading Score +
#% Passing Math +
#% Passing Reading +
#Overall Passing Rate (Average of the above two)

# Set Up ------------------------------------------------------------------------------------
import pandas as pd
import numpy as np

school_data_to_load = "Resources/schools_complete.csv"
student_data_to_load = "Resources/students_complete.csv"

school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)

school_data_complete = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])

# School Name ------------------------------------------------------------------------------------
#skip

# School Type ------------------------------------------------------------------------------------
school_type = school_data.set_index(['school_name'])['type']
#print(school_type)

# Total Students per school ------------------------------------------------------------------------------------
total_students_per_school = school_data_complete["school_name"].value_counts()
#print(students_per_school)

# Total School & Student Budget ------------------------------------------------------------------------------------
per_school_budget = school_data_complete.groupby(['school_name']).mean()['budget']
per_student_budget = per_school_budget/ total_students_per_school
#print(per_student_budget)

# Average Math Score per School ------------------------------------------------------------------------------------
avg_math_score_per_school = school_data_complete.groupby(['school_name']).mean()['math_score']
#print(avg_math_score_per_school)

# Average Reading Score per School ------------------------------------------------------------------------------------
avg_reading_score_per_school = school_data_complete.groupby(['school_name']).mean()['reading_score']
#print(avg_reading_score_per_school)

#% Passing Math ------------------------------------------------------------------------------------
school_passing_math = school_data_complete[(school_data_complete["math_score"] > 70)] 
per_school_passing_math = school_passing_math.groupby(["school_name"]).count()["student_name"] / total_students_per_school * 100 

# 1 - total students passing math
# 2 - total students passing math grouped by school name and turned into percentage

#% Passing Reading ------------------------------------------------------------------------------------
school_passing_reading = school_data_complete[(school_data_complete["reading_score"] > 70)] 
per_school_passing_reading = school_passing_reading.groupby(["school_name"]).count()["student_name"] / total_students_per_school * 100 


#% Overall Passing Rate ------------------------------------------------------------------------------------
overall_passing_rate = (per_school_passing_reading + per_school_passing_math)/ 2
#print(overall_passing_rate)


# School Summary ------------------------------------------------------------------------------------
per_school_summary = pd.DataFrame({"School Type": school_type,
                                   "Total Students": total_students_per_school,
                                   "Total School Budget": per_school_budget,
                                   "Per Student Budget": per_student_budget,
                                   "Average Math Score": avg_math_score_per_school,
                                   "Average Reading Score": avg_reading_score_per_school,
                                   "% Passing Math": per_school_passing_math,
                                   "% Passing Reading": per_school_passing_reading,
                                   "% Overall Passing Rate": overall_passing_rate})

#print(per_school_summary)




#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------




#Top Performing Schools (By Passing Rate) ------------------------------------------------------------------------------------
top_schools = per_school_summary.sort_values(["% Overall Passing Rate"], ascending=False)

#Bottom Performing Schools (By Passing Rate) ------------------------------------------------------------------------------------
bottom_schools = per_school_summary.sort_values(["% Overall Passing Rate"], ascending=True)

#Math Scores by Grade ------------------------------------------------------------------------------------
ninth_graders = school_data_complete[(school_data_complete["grade"] == "9th")]
tenth_graders = school_data_complete[(school_data_complete["grade"] == "10th")]
eleventh_graders = school_data_complete[(school_data_complete["grade"] == "11th")]
twelfth_graders = school_data_complete[(school_data_complete["grade"] == "12th")]

ninth_graders_scores = ninth_graders.groupby(["school_name"]).mean()["math_score"]
tenth_graders_scores = tenth_graders.groupby(["school_name"]).mean()["math_score"]
eleventh_graders_scores = eleventh_graders.groupby(["school_name"]).mean()["math_score"]
twelfth_graders_scores = twelfth_graders.groupby(["school_name"]).mean()["math_score"]

#categorize by grade
#Group each grade by school
scores_by_grade = pd.DataFrame({"9th": ninth_graders_scores, "10th": tenth_graders_scores,
                                "11th": eleventh_graders_scores, "12th": twelfth_graders_scores})


#Reading Scores by Grade ------------------------------------------------------------------------------------
ninth_graders = school_data_complete[(school_data_complete["grade"] == "9th")]
tenth_graders = school_data_complete[(school_data_complete["grade"] == "10th")]
eleventh_graders = school_data_complete[(school_data_complete["grade"] == "11th")]
twelfth_graders = school_data_complete[(school_data_complete["grade"] == "12th")]

# Group each by school name
ninth_graders_scores = ninth_graders.groupby(["school_name"]).mean()["reading_score"]
tenth_graders_scores = tenth_graders.groupby(["school_name"]).mean()["reading_score"]
eleventh_graders_scores = eleventh_graders.groupby(["school_name"]).mean()["reading_score"]
twelfth_graders_scores = twelfth_graders.groupby(["school_name"]).mean()["reading_score"]


scores_by_grade = pd.DataFrame({"9th": ninth_graders_scores, "10th": tenth_graders_scores,
                                "11th": eleventh_graders_scores, "12th": twelfth_graders_scores})


#****Scores by School Spending ------------------------------------------------------------------------------------
spending_bins = [0, 250, 500, 750]
group_names = ['<250','250-500','500-750']

per_school_summary["Spending Ranges (Per Student)"] = pd.cut(per_student_budget, spending_bins, labels=group_names)
print(per_school_summary)

spending_math_scores = per_school_summary.groupby(["Spending Ranges (Per Student)"]).mean()["Average Math Score"]
spending_reading_scores = per_school_summary.groupby(["Spending Ranges (Per Student)"]).mean()["Average Reading Score"]
spending_passing_math = per_school_summary.groupby(["Spending Ranges (Per Student)"]).mean()["% Passing Math"]
spending_passing_reading = per_school_summary.groupby(["Spending Ranges (Per Student)"]).mean()["% Passing Reading"]
overall_passing_rate = (spending_math_scores + spending_reading_scores) / 2

spending_summary = pd.DataFrame({"Average Math Score" : spending_math_scores,
                                 "Average Reading Score": spending_reading_scores,
                                 "% Passing Math": spending_passing_math,
                                 "% Passing Reading": spending_passing_reading,
                                 "% Overall Passing Rate": overall_passing_rate})

#print(spending_summary)


#****Scores by School Size ------------------------------------------------------------------------------------
size_bins = [0, 1000, 2000, 5000]
label_names = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]

# Categorize the spending based on the bins
per_school_summary["School Size"] = pd.cut(per_school_summary["Total Students"], size_bins, labels=label_names)

# Calculate the scores based on bins
size_math_scores = per_school_summary.groupby(["School Size"]).mean()["Average Math Score"]
size_reading_scores = per_school_summary.groupby(["School Size"]).mean()["Average Reading Score"]
size_passing_math = per_school_summary.groupby(["School Size"]).mean()["% Passing Math"]
size_passing_reading = per_school_summary.groupby(["School Size"]).mean()["% Passing Reading"]
overall_passing_rate = (size_passing_math + size_passing_reading) / 2

# Assemble into data frame
size_summary = pd.DataFrame({"Average Math Score" : size_math_scores,
                             "Average Reading Score": size_reading_scores,
                             "% Passing Math": size_passing_math,
                             "% Passing Reading": size_passing_reading,
                             "% Overall Passing Rate": overall_passing_rate})

#print(size_summary)
#print(per_school_summary)


#****Scores by School Type ------------------------------------------------------------------------------------

type_math_score = per_school_summary.groupby(['School Type']).mean()["Average Math Score"]
type_reading_score = per_school_summary.groupby(['School Type']).mean()["Average Reading Score"]
type_passing_math = per_school_summary.groupby(['School Type']).mean()['% Passing Math']
type_passing_reading = per_school_summary.groupby(['School Type']).mean()['% Passing Reading']
overall_passing_rate = (type_passing_math + type_passing_reading) / 2

type_summary = pd.DataFrame({"Average Math Score": type_math_score,
                             "Average Reading Score": type_reading_score,
                             "% Passing Math": type_passing_math,
                             "% Passing Reading": type_passing_reading,
                             "% Overall Passing Rate": overall_passing_rate})

print(type_summary)
