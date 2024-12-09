class MetadataProvier:
    def __init__(self):
        self.table_metadata = [
            {
                "table_name": "students",
                "column_names": [
                    "id",
                    "name",
                    "advised_by_lecturer_id",
                    "date_of_birth",
                    "contact_info",
                    "program_id",
                    "year_of_study",
                    "graduation_status",
                    "disciplinary_records",
                    "avg_grade",
                ],
            },
            {
                "table_name": "courses",
                "column_names": [
                    "id",
                    "name",
                    "description",
                    "department_id",
                    "lecturer_id",
                    "level",
                    "credits",
                    "prerequisites",
                    "schedule",
                ],
            },
            {
                "table_name": "departments",
                "column_names": [
                    "id",
                    "name",
                    "research_areas",
                ],
            },
        ]

    def get_table_metadata(self, table_name):
        for i in range(0, len(self.table_metadata)):
            if self.table_metadata[i].get("table_name") == table_name:
                return self.table_metadata[i]
        return None

    def get_all_table_metadata(self):
        return self.table_metadata
