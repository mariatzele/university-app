
# list of dictionaries of available tableviews and their fields
table_metadata_dict_list = [{
    "table_name": "Students" , "column_names" : ["Name", "Advisor" ,
                                                 "Program"]},
    {"table_name":"Courses", "column_names" : ["Course", "Department",
                                               "Lecturer"]}]

# course and student data
course_records = [    {"Course": "Maths", "Lecturer": "John Doe",
                       "Department": ""},
    {"Lecturer": "Jane Smith", "Course": "Biology",  "Department": "Science"}]

student_records = [    {"Name": "Marvin Wash", "Advisor": "John Doe",
                       "Program": "Maths"}, {"Name": "Holly Mill",
                                             "Advisor": "John Doe",
                       "Program": "Science"}]