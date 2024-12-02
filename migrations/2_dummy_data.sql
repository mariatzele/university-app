START TRANSACTION;

INSERT INTO `departments` (`name`, `research_areas`) VALUES
('Computer Science', 'Artificial Intelligence, Machine Learning'),
('Electrical Engineering', 'Robotics, Signal Processing'),
('Mechanical Engineering', 'Thermodynamics, Fluid Mechanics'),
('Physics', 'Quantum Physics, Nanotechnology'),
('Biology', 'Genetics, Molecular Biology'),
('Mathematics', 'Pure Mathematics, Statistics'),
('Chemistry', 'Organic Chemistry, Analytical Chemistry'),
('Psychology', 'Cognitive Science, Neuroscience'),
('Economics', 'Macroeconomics, Behavioral Economics'),
('Law', 'International Law, Criminal Law');

INSERT INTO `programs` (`name`, `degree_awarded`, `duration_years`, `course_requirements`, `enrollment_details`) VALUES
('Computer Science', 'BSc', 3, 'Mathematics, Programming, Data Structures', 'Open enrollment'),
('Electrical Engineering', 'BSc', 4, 'Physics, Calculus, Circuit Design', 'Open enrollment'),
('Mechanical Engineering', 'BSc', 4, 'Physics, Thermodynamics, Mechanics', 'Open enrollment'),
('Physics', 'BSc', 3, 'Mathematics, Physics', 'Open enrollment'),
('Biology', 'BSc', 3, 'Chemistry, Biology', 'Open enrollment'),
('Mathematics', 'BSc', 3, 'Calculus, Algebra', 'Open enrollment'),
('Chemistry', 'BSc', 3, 'Chemistry, Physics', 'Open enrollment'),
('Psychology', 'BSc', 3, 'Psychology, Biology', 'Open enrollment'),
('Economics', 'BSc', 3, 'Mathematics, Economics', 'Open enrollment'),
('Law', 'LLB', 3, 'Political Science, Philosophy', 'Open enrollment');

INSERT INTO `lecturers` (`name`, `academic_qualifications`, `department_id`, `expertise`, `research_interests`) VALUES
('Dr. John Smith', 'PhD in AI', 1, 'Artificial Intelligence', 'Machine Learning, Robotics'),
('Dr. Jane Doe', 'PhD in Electrical Engineering', 2, 'Signal Processing', 'Communication Systems'),
('Dr. Alan Turing', 'PhD in Mathematics', 6, 'Algorithm Theory', 'Computational Complexity'),
('Dr. Albert Einstein', 'PhD in Physics', 4, 'Theoretical Physics', 'Quantum Mechanics'),
('Dr. Ada Lovelace', 'PhD in Computing', 1, 'Computer Programming', 'Software Engineering'),
('Dr. Nikola Tesla', 'PhD in Electrical Engineering', 2, 'Electromagnetic Systems', 'Wireless Communication'),
('Dr. Charles Babbage', 'PhD in Mathematics', 6, 'Computational Theory', 'Artificial Intelligence'),
('Dr. Marie Curie', 'PhD in Physics', 4, 'Radioactivity', 'Nuclear Physics'),
('Dr. Sigmund Freud', 'MD in Psychology', 8, 'Cognitive Psychology', 'Neuropsychology'),
('Dr. Eleanor Roosevelt', 'PhD in Economics', 9, 'Macroeconomics', 'International Economics');

INSERT INTO `courses` (`name`, `description`, `department_id`, `lecturer_id`, `level`, `credits`, `prerequisites`, `schedule`) VALUES
('Introduction to AI', 'Basics of Artificial Intelligence', 1, 1, 100, 3, 'Mathematics, Programming', 'Mon, Wed, Fri'),
('Circuit Analysis', 'Fundamentals of Electrical Circuits', 2, 2, 100, 4, 'Physics, Calculus', 'Tue, Thu'),
('Fluid Mechanics', 'Study of Fluid Behavior and Mechanics', 3, 3, 200, 3, 'Physics', 'Mon, Wed'),
('Quantum Physics', 'Introduction to Quantum Mechanics', 4, 4, 300, 3, 'Mathematics, Physics', 'Mon, Fri'),
('Molecular Biology', 'Basic principles of Biology', 5, 5, 100, 3, 'Chemistry', 'Tue, Thu'),
('Discrete Mathematics', 'Introduction to Discrete Mathematics', 6, 7, 200, 3, 'Mathematics', 'Mon, Wed'),
('Organic Chemistry', 'Study of Organic Compounds and Reactions', 7, 6, 200, 3, 'Chemistry', 'Tue, Thu'),
('Cognitive Psychology', 'Understanding the human mind and behavior', 8, 9, 100, 3, 'Psychology', 'Mon, Wed'),
('Macroeconomics', 'Study of economy-wide phenomena', 9, 10, 100, 3, 'Mathematics', 'Tue, Fri'),
('Introduction to Law', 'Fundamentals of Law and Legal Systems', 10, 10, 100, 3, 'Political Science', 'Mon, Thu');

INSERT INTO `students` (`name`, `advised_by_lecturer_id`, `date_of_birth`, `contact_info`, `program_id`, `year_of_study`, `graduation_status`, `disciplinary_records`) VALUES
('Alice Johnson', 1, '2000-01-15', 'alice@email.com', 1, 2, FALSE, 'None'),
('Bob Williams', 2, '1999-05-23', 'bob@email.com', 2, 1, TRUE, 'None'),
('Charlie Brown', 3, '2001-08-30', 'charlie@email.com', 3, 3, FALSE, 'None'),
('David Clark', 4, '2000-02-12', 'david@email.com', 4, 1, TRUE, 'None'),
('Eva Green', 5, '1998-11-18', 'eva@email.com', 5, 2, FALSE, 'None'),
('Frank Harris', 6, '2000-07-09', 'frank@email.com', 6, 3, FALSE, 'None'),
('Grace Lee', 7, '2001-03-05', 'grace@email.com', 7, 1, TRUE, 'None'),
('Hannah King', 8, '2000-04-24', 'hannah@email.com', 8, 2, FALSE, 'None'),
('Isla White', 9, '1999-06-30', 'isla@email.com', 9, 3, TRUE, 'None'),
('Jack Wright', 10, '2001-07-21', 'jack@email.com', 10, 1, FALSE, 'None'),
('Karen Adams', 1, '2000-05-10', 'karen@email.com', 1, 2, FALSE, 'None'),
('Leo Harris', 2, '2001-10-11', 'leo@email.com', 2, 3, TRUE, 'None'),
('Mona Richards', 3, '1999-12-04', 'mona@email.com', 3, 1, FALSE, 'None'),
('Nina Scott', 4, '2000-08-29', 'nina@email.com', 4, 2, TRUE, 'None'),
('Oscar Allen', 5, '2000-01-06', 'oscar@email.com', 5, 3, FALSE, 'None'),
('Paula Evans', 6, '1999-11-12', 'paula@email.com', 6, 1, TRUE, 'None'),
('Quincy Stevens', 7, '2000-04-04', 'quincy@email.com', 7, 2, FALSE, 'None'),
('Rita Murphy', 8, '2001-02-20', 'rita@email.com', 8, 3, TRUE, 'None'),
('Steve Roberts', 9, '2000-09-18', 'steve@email.com', 9, 1, FALSE, 'None'),
('Tom Carter', 10, '1999-12-22', 'tom@email.com', 10, 2, TRUE, 'None');

INSERT INTO `student_enrollments` (`student_id`, `course_id`, `grade`) VALUES
(1, 1, 85),
(1, 3, 90),
(2, 2, 75),
(2, 4, 80),
(3, 1, 92),
(3, 5, 88),
(4, 6, 84),
(4, 8, 78),
(5, 7, 80),
(5, 9, 89),
(6, 2, 82),
(6, 4, 91),
(7, 5, 86),
(7, 10, 93),
(8, 6, 77),
(8, 1, 83),
(9, 3, 88),
(9, 7, 85),
(10, 9, 79),
(10, 8, 87);

INSERT INTO `research_projects` (`title`, `principal_investigator`, `outcomes`) VALUES
('AI for Healthcare', 1, 'Improved diagnostic systems using AI'),
('Quantum Computing', 4, 'Development of quantum algorithms'),
('Machine Learning for Robotics', 2, 'Enhanced robotic autonomy using ML techniques'),
('Neural Networks for Data Mining', 5, 'Better data classification models using neural networks');

INSERT INTO `funding_sources` (`name`, `research_projects_id`) VALUES
('National Science Foundation', 1),
('European Research Council', 2),
('Google AI Research', 3),
('Tech University', 4);

INSERT INTO `research_projects_members` (`student_id`, `research_projects_id`) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 1),
(6, 2),
(7, 3),
(8, 4),
(9, 1),
(10, 2);

INSERT INTO `student_organisations` (`name`, `description`) VALUES
('AI Club', 'A club for AI enthusiasts'),
('Robotics Team', 'A team focused on robotics projects'),
('Chemistry Society', 'A society for chemistry lovers'),
('Psychology Group', 'A group for psychology discussions'),
('Law Society', 'A society for law students'),
('Mathematics Club', 'A club for math enthusiasts');

INSERT INTO `student_memberships` (`student_id`, `organisation_id`) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 1),
(8, 2),
(9, 3),
(10, 4);

INSERT INTO `research_groups` (`name`, `head_lecturer_id`) VALUES
('AI Research Group', 1),
('Robotics Research Group', 2),
('Chemistry Research Group', 6),
('Psychology Research Group', 9),
('Economics Research Group', 10);

INSERT INTO `committees` (`committee_name`) VALUES
('Research Ethics Committee'),
('Curriculum Committee'),
('Admissions Committee'),
('Examination Committee'),
('Student Affairs Committee');

INSERT INTO `committee_memberships` (`committee_id`, `lecturer_id`) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5);

INSERT INTO `disciplinary_records` (`id`, `student_id`, `description`) VALUES
(1, 1, 'Late submission of assignments multiple times'),
(2, 3, 'Disruptive behavior in class during lectures'),
(3, 4, 'Plagiarism detected in final project'),
(4, 6, 'Repeated violations of lab safety protocols'),
(5, 7, 'Inappropriate behavior during group project presentations'),
(6, 8, 'Disrespectful comments towards faculty members'),
(7, 9, 'Unapproved absence from mandatory academic meetings'),
(8, 10, 'Late payment of tuition fees for multiple semesters');

COMMIT;