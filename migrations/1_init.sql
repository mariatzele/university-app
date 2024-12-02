START TRANSACTION;

CREATE TABLE `students` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(255) NOT NULL,
  `advised_by_lecturer_id` INT,
  `date_of_birth` DATE NOT NULL,
  `contact_info` VARCHAR(255),
  `program_id` INT NOT NULL,
  `year_of_study` INT,
  `graduation_status` BOOLEAN,
  `disciplinary_records` VARCHAR(255)
);

CREATE TABLE disciplinary_records (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `student_id` INT,
  `description` TEXT NOT NULL
);

CREATE TABLE `lecturers` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(255) NOT NULL,
  `academic_qualifications` VARCHAR(255),
  `department_id` INT NOT NULL,
  `expertise` VARCHAR(255),
  `research_interests` VARCHAR(255)
);

CREATE TABLE `publications` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `lecturer_id` INT,
  `research_projects_id` INT,
  `published_at` DATE,
  `title` VARCHAR(255)
);

CREATE TABLE `non_academic_staff` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(255) NOT NULL,
  `job_title` VARCHAR(255),
  `department_id` INT,
  `employment_type` VARCHAR(255),
  `contract_details` VARCHAR(255),
  `salary` DECIMAL(10, 2),
  `emergency_contact_info` VARCHAR(255)
);

CREATE TABLE `courses` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(255) NOT NULL,
  `description` VARCHAR(255),
  `department_id` INT,
  `lecturer_id` INT,
  `level` INT,
  `credits` INT,
  `prerequisites` VARCHAR(255),
  `schedule` VARCHAR(255)
);

CREATE TABLE `departments` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(255) NOT NULL,
  `research_areas` VARCHAR(255)
);

CREATE TABLE `programs` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(255) NOT NULL,
  `degree_awarded` VARCHAR(255),
  `duration_years` INT,
  `course_requirements` VARCHAR(255),
  `enrollment_details` VARCHAR(255)
);

CREATE TABLE `research_projects` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `title` VARCHAR(255),
  `principal_investigator` INT,
  `outcomes` VARCHAR(255)
);

CREATE TABLE `funding_sources` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(255) NOT NULL,
  `research_projects_id` INT
);

CREATE TABLE `research_projects_members` (
  `student_id` INT,
  `research_projects_id` INT,
  PRIMARY KEY (`student_id`, `research_projects_id`)
);

CREATE TABLE `student_organisations` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(255) NOT NULL,
  `description` VARCHAR(255)
);

CREATE TABLE `student_enrollments` (
  `student_id` INT,
  `course_id` INT,
  `grade` INT,
  PRIMARY KEY (`student_id`, `course_id`)
);

CREATE TABLE `research_groups` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(255) NOT NULL,
  `head_lecturer_id` INT
);

CREATE TABLE `committees` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `committee_name` VARCHAR(255)
);

CREATE TABLE `committee_memberships` (
  `committee_id` INT,
  `lecturer_id` INT,
  PRIMARY KEY (`committee_id`, `lecturer_id`)
);

CREATE TABLE `student_memberships` (
  `student_id` INT,
  `organisation_id` INT,
  PRIMARY KEY (`student_id`, `organisation_id`)
);

-- Foreign key constraints
-- Create constraints only after all the tables have been created to avoid conflicts
-- during creation that can be caused by ordering

ALTER TABLE `students` ADD FOREIGN KEY (`advised_by_lecturer_id`) REFERENCES `lecturers` (`id`);

ALTER TABLE `students` ADD FOREIGN KEY (`program_id`) REFERENCES `programs` (`id`);

ALTER TABLE `disciplinary_records` ADD FOREIGN KEY (`student_id`) REFERENCES `students` (`id`);

ALTER TABLE `lecturers` ADD FOREIGN KEY (`department_id`) REFERENCES `departments` (`id`);

ALTER TABLE `publications` ADD FOREIGN KEY (`lecturer_id`) REFERENCES `lecturers` (`id`);

ALTER TABLE `publications` ADD FOREIGN KEY (`research_projects_id`) REFERENCES `research_projects` (`id`);

ALTER TABLE `non_academic_staff` ADD FOREIGN KEY (`department_id`) REFERENCES `departments` (`id`);

ALTER TABLE `courses` ADD FOREIGN KEY (`department_id`) REFERENCES `departments` (`id`);

ALTER TABLE `courses` ADD FOREIGN KEY (`lecturer_id`) REFERENCES `lecturers` (`id`);

ALTER TABLE `research_projects` ADD FOREIGN KEY (`principal_investigator`) REFERENCES `lecturers` (`id`);

ALTER TABLE `funding_sources` ADD FOREIGN KEY (`research_projects_id`) REFERENCES `research_projects` (`id`);

ALTER TABLE `research_projects_members` ADD FOREIGN KEY (`student_id`) REFERENCES `students` (`id`);

ALTER TABLE `research_projects_members` ADD FOREIGN KEY (`research_projects_id`) REFERENCES `research_projects` (`id`);

ALTER TABLE `student_enrollments` ADD FOREIGN KEY (`student_id`) REFERENCES `students` (`id`);

ALTER TABLE `student_enrollments` ADD FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`);

ALTER TABLE `research_groups` ADD FOREIGN KEY (`head_lecturer_id`) REFERENCES `lecturers` (`id`);

ALTER TABLE `committee_memberships` ADD FOREIGN KEY (`committee_id`) REFERENCES `committees` (`id`);

ALTER TABLE `committee_memberships` ADD FOREIGN KEY (`lecturer_id`) REFERENCES `lecturers` (`id`);

ALTER TABLE `student_memberships` ADD FOREIGN KEY (`student_id`) REFERENCES `students` (`id`);

ALTER TABLE `student_memberships` ADD FOREIGN KEY (`organisation_id`) REFERENCES `student_organisations` (`id`);

-- Indexes

CREATE INDEX idx_students_advised_by ON students(advised_by_lecturer_id);
CREATE INDEX idx_students_program ON students(program_id);

CREATE INDEX idx_lecturers_department ON lecturers(department_id);
CREATE INDEX idx_lecturers_expertise ON lecturers(expertise);

CREATE INDEX idx_courses_department ON courses(department_id);
CREATE INDEX idx_courses_lecturer ON courses(lecturer_id);

CREATE INDEX idx_publications_lecturer ON publications(lecturer_id);
CREATE INDEX idx_publications_research_projects ON publications(research_projects_id);
CREATE INDEX idx_publications_date ON publications(published_at);

CREATE INDEX idx_staff_department ON non_academic_staff(department_id);

CREATE INDEX idx_research_principal ON research_projects(principal_investigator);

CREATE INDEX idx_student_enrollments_student ON student_enrollments(student_id);
CREATE INDEX idx_student_enrollments_course ON student_enrollments(course_id);
CREATE INDEX idx_student_memberships_student ON student_memberships(student_id);
CREATE INDEX idx_student_memberships_org ON student_memberships(organisation_id);

CREATE INDEX idx_committee_memberships_committee ON committee_memberships(committee_id);
CREATE INDEX idx_committee_memberships_lecturer ON committee_memberships(lecturer_id);

COMMIT;