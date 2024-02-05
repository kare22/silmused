from silmused.tests.TestDefinition import TestDefinition


class ConstraintTest(TestDefinition):
    def __init__(self, name, title=None, column_name=None, constraint_name=None, constraint_type=None, description=None, should_exist=True, points=0):
        query = f"SELECT * FROM information_schema.table_constraints WHERE table_name = '{name}'"

        if constraint_name is not None:
            query += f" AND constraint_name = '{constraint_name}'"
        if constraint_type is not None:
            query += f" AND constraint_type = '{constraint_type}'"

        super().__init__(
            name=name,
            column_name=column_name,
            title=title,
            points=points,
            description=description,
            query=query,
            should_exist=should_exist,
        )

        self.constraint_name = constraint_name
        self.constraint_type = constraint_type

        self.feedback = f"table {self.name}"

        if self.column_name is not None:
            self.feedback += f" with column = '{self.column_name}'"
        if self.constraint_name is not None:
            self.feedback += f" with constraint name = '{self.constraint_name}'"
        if self.constraint_type is not None:
            if self.constraint_name is None:
                self.feedback += f" with constraint type = '{self.constraint_type}'"
            else:
                self.feedback += f" and type = '{self.constraint_type}'"

    def execute(self, cursor):
        check_columns_result = self.check_columns(cursor)
        if check_columns_result is not None:
            return check_columns_result
        cursor.execute(self.query)
        result = cursor.fetchall()
        if self.should_exist:
            if self.column_name is None and self.constraint_name is None and self.constraint_type is None:
                return super().response(
                    len(result) > 0,
                    {"test_type": "constraint_test",
                     "test_key": "table_constraint_should_exist_positive_feedback",
                     "params": [self.name]},
                    {"test_type": "constraint_test",
                     "test_key": "table_constraint_should_exist_negative_feedback",
                     "params": [self.name]},
                )

            elif self.column_name is not None and self.constraint_name is None and self.constraint_type is None:
                return super().response(
                    len(result) > 0,
                    {"test_type": "constraint_test",
                     "test_key": "table_column_constraint_should_exist_positive_feedback",
                     "params": [self.name, self.column_name]},
                    {"test_type": "constraint_test",
                     "test_key": "table_column_constraint_should_exist_negative_feedback",
                     "params": [self.name, self.column_name]},
                )
            elif self.column_name is not None and self.constraint_name is not None and self.constraint_type is None:
                return super().response(
                    len(result) > 0,
                    {"test_type": "constraint_test",
                     "test_key": "table_column_constraint_name_should_exist_positive_feedback",
                     "params": [self.name, self.column_name, self.constraint_name]},
                    {"test_type": "constraint_test",
                     "test_key": "table_column_constraint_name_should_exist_negative_feedback",
                     "params": [self.name, self.column_name, self.constraint_name]},
                )
            elif self.column_name is not None and self.constraint_type is not None:
                if self.constraint_name is None:
                    return super().response(
                        len(result) > 0,
                        {"test_type": "constraint_test",
                         "test_key": "table_column_constraint_type_should_exist_positive_feedback",
                         "params": [self.name, self.column_name, self.constraint_type]},
                        {"test_type": "constraint_test",
                         "test_key": "table_column_constraint_type_should_exist_negative_feedback",
                         "params": [self.name, self.column_name, self.constraint_type]},
                    )
                else:
                    return super().response(
                        len(result) > 0,
                        {"test_type": "constraint_test",
                         "test_key": "table_column_constraint_name_and_type_should_exist_positive_feedback",
                         "params": [self.name, self.column_name, self.constraint_name, self.constraint_type]},
                        {"test_type": "constraint_test",
                         "test_key": "table_column_constraint_name_and_type_should_exist_negative_feedback",
                         "params": [self.name, self.column_name, self.constraint_name, self.constraint_type]},
                    )
            else:
                if self.constraint_name is not None and self.constraint_type is None:
                    return super().response(
                        len(result) > 0,
                        {"test_type": "constraint_test",
                         "test_key": "table_constraint_name_should_exist_positive_feedback",
                         "params": [self.constraint_name, self.name]},
                        {"test_type": "constraint_test",
                         "test_key": "table_constraint_name_should_exist_negative_feedback",
                         "params": [self.constraint_name, self.name]},
                    )
                elif self.constraint_name is None and self.constraint_type is not None:
                    return super().response(
                        len(result) > 0,
                        {"test_type": "constraint_test",
                         "test_key": "table_constraint_type_should_exist_positive_feedback",
                         "params": [self.constraint_type, self.name]},
                        {"test_type": "constraint_test",
                         "test_key": "table_constraint_type_should_exist_negative_feedback",
                         "params": [self.constraint_type, self.name]},
                    )
                else:
                    return super().response(
                        len(result) > 0,
                        {"test_type": "constraint_test",
                         "test_key": "table_constraint_name_and_type_should_exist_positive_feedback",
                         "params": [self.constraint_name, self.constraint_type, self.name]},
                        {"test_type": "constraint_test",
                         "test_key": "table_constraint_name_and_type_should_exist_negative_feedback",
                         "params": [self.constraint_name, self.constraint_type, self.name]},
                    )

        # Should exist = False
        else:
            if self.column_name is None and self.constraint_name is None and self.constraint_type is None:
                return super().response(
                    len(result) == 0,
                    {"test_type": "constraint_test",
                     "test_key": "table_constraint_should_not_exist_positive_feedback",
                     "params": [self.name]},
                    {"test_type": "constraint_test",
                     "test_key": "table_constraint_should_not_exist_negative_feedback",
                     "params": [self.name]},
                )

            elif self.column_name is not None and self.constraint_name is None and self.constraint_type is None:
                return super().response(
                    len(result) == 0,
                    {"test_type": "constraint_test",
                     "test_key": "table_column_constraint_should_not_exist_positive_feedback",
                     "params": [self.name, self.column_name]},
                    {"test_type": "constraint_test",
                     "test_key": "table_column_constraint_should_not_exist_negative_feedback",
                     "params": [self.name, self.column_name]},
                )
            elif self.column_name is not None and self.constraint_name is not None and self.constraint_type is None:
                return super().response(
                    len(result) == 0,
                    {"test_type": "constraint_test",
                     "test_key": "table_column_constraint_name_should_not_exist_positive_feedback",
                     "params": [self.name, self.column_name, self.constraint_name]},
                    {"test_type": "constraint_test",
                     "test_key": "table_column_constraint_name_should_not_exist_negative_feedback",
                     "params": [self.name, self.column_name, self.constraint_name]},
                )
            elif self.column_name is not None and self.constraint_type is not None:
                if self.constraint_name is None:
                    return super().response(
                        len(result) == 0,
                        {"test_type": "constraint_test",
                         "test_key": "table_column_constraint_type_should_not_exist_positive_feedback",
                         "params": [self.name, self.column_name, self.constraint_type]},
                        {"test_type": "constraint_test",
                         "test_key": "table_column_constraint_type_should_not_exist_negative_feedback",
                         "params": [self.name, self.column_name, self.constraint_type]},
                    )
                else:
                    return super().response(
                        len(result) == 0,
                        {"test_type": "constraint_test",
                         "test_key": "table_column_constraint_name_and_type_should_not_exist_positive_feedback",
                         "params": [self.name, self.column_name, self.constraint_name, self.constraint_type]},
                        {"test_type": "constraint_test",
                         "test_key": "table_column_constraint_name_and_type_should_not_exist_negative_feedback",
                         "params": [self.name, self.column_name, self.constraint_name, self.constraint_type]},
                    )
            else:
                if self.constraint_name is not None and self.constraint_type is None:
                    return super().response(
                        len(result) == 0,
                        {"test_type": "constraint_test",
                         "test_key": "table_constraint_name_should_not_exist_positive_feedback",
                         "params": [self.constraint_name, self.name]},
                        {"test_type": "constraint_test",
                         "test_key": "table_constraint_name_should_not_exist_negative_feedback",
                         "params": [self.constraint_name, self.name]},
                    )
                elif self.constraint_name is None and self.constraint_type is not None:
                    return super().response(
                        len(result) == 0,
                        {"test_type": "constraint_test",
                         "test_key": "table_constraint_type_should_not_exist_positive_feedback",
                         "params": [self.constraint_type, self.name]},
                        {"test_type": "constraint_test",
                         "test_key": "table_constraint_type_should_not_exist_negative_feedback",
                         "params": [self.constraint_type, self.name]},
                    )
                else:
                    return super().response(
                        len(result) == 0,
                        {"test_type": "constraint_test",
                         "test_key": "table_constraint_name_and_type_should_not_exist_positive_feedback",
                         "params": [self.constraint_name, self.constraint_type, self.name]},
                        {"test_type": "constraint_test",
                         "test_key": "table_constraint_name_and_type_should_not_exist_negative_feedback",
                         "params": [self.constraint_name, self.constraint_type, self.name]},
                    )

    def check_columns(self, cursor):
        if self.column_name is None:
            return None

        query = f"SELECT * FROM information_schema.key_column_usage WHERE table_name = '{self.name}'"

        if self.constraint_name is not None:
            query += f" AND constraint_name = '{self.constraint_name}'"

        cursor.execute(query)
        result = cursor.fetchall()

        columns = [res[6] for res in result]

        #print(columns)

        if type(self.column_name) == str and self.column_name in columns:
            return None
        elif type(self.column_name) == list:
            is_correct = True
            for column_name in self.column_name:
                if not column_name in columns:
                    is_correct = False
                    break
            if is_correct:
                return None
        if self.constraint_name is None:
            return super().response(
                False,
                None,
                {"test_type": "constraint_test",
                 "test_key": "multi_column_name_negative_feedback",
                 "params": [self.column_name, columns]},
            )
        else:
            if len(columns) > 0:
                return super().response(
                    False,
                    None,
                    {"test_type": "constraint_test",
                     "test_key": "multi_column_constraint_name_negative_feedback",
                     "params": [self.constraint_name, self.column_name, columns]},
                )
            else:
                return super().response(
                    False,
                    None,
                    {"test_type": "constraint_test",
                     "test_key": "multi_column_constraint_name_column_not_found_negative_feedback",
                     "params": [self.constraint_name, self.column_name]},
                )
