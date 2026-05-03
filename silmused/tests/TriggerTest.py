from silmused.tests.TestDefinition import TestDefinition


class TriggerTest(TestDefinition):
    def __init__(self, name, title=None, description=None, points=0, arguments=None,
                 custom_feedback=None, action_timing=None, llm_check=False, debug=None):
        super().__init__(
            name=name,
            title=title,
            points=points,
            description=description,
            arguments=arguments,
            custom_feedback=custom_feedback,
            llm_check=llm_check,
            query=f"SELECT * FROM information_schema.views WHERE table_name = '{name}'",
            debug=debug
        )

        self.action_timing = action_timing
        self.test_type = "trigger_test"

    def execute(self, cursor):

        if self.debug is not None: self.debug_output()

        # Check that trigger name exists
        test_trigger_exists_result = self.test_trigger_exists(cursor)
        if test_trigger_exists_result is not None:
            return test_trigger_exists_result

        # Check trigger event manipulation on arguments and trigger action timing
        errors = self.test_trigger_manipulation(cursor) if len(self.arguments) > 0 else []

        return super().response(
            len(errors) == 0,
            {"test_type": self.test_type,
             "test_key": "trigger_definition_positive_feedback",
             "params": [self.name]},
            {"test_type": self.test_type,
             "test_key": "trigger_definition_negative_feedback",
             "params": [self.name, {', '.join(errors)}]},  # TODO errorid on hetkel inglise keeles
        )

    def test_trigger_exists(self, cursor):
        query = f"SELECT trigger_name FROM information_schema.triggers WHERE trigger_name = '{self.name}'"
        cursor.execute(query)
        result = cursor.fetchall()

        if self.debug is not None:
            print(f"query: {query}")
            print(f"result: {result}")

        # Result assessment
        if len(result) <= 0:
            return super().response(
                False,
                {"test_type": self.test_type,
                 "test_key": "trigger_exists_positive_feedback",
                 "params": [self.name]},
                {"test_type": self.test_type,
                 "test_key": "trigger_exists_negative_feedback",
                 "params": [self.name]},
            )
        return None

    def test_trigger_manipulation(self, cursor):
        errors = []
        for manipulation in self.arguments:
            query = (f"SELECT trigger_name FROM information_schema.triggers WHERE trigger_name = '{self.name}' "
                     f"AND event_manipulation = '{manipulation}'")
            cursor.execute(query)
            result = cursor.fetchall()

            if self.debug is not None:
                print(f"query: {query}")
                print(f"result: {result}")

            if len(result) <= 0:
                errors.append(f"manipulation {manipulation} was not found")

        query = (f"SELECT trigger_name FROM information_schema.triggers WHERE trigger_name = '{self.name}' "
                 f"AND action_timing = '{self.action_timing}'")
        cursor.execute(query)
        result = cursor.fetchall()

        if len(result) <= 0:
            errors.append(f"action timing {self.action_timing} was not found")

        if self.debug is not None:
            print(f"query: {query}")
            print(f"result: {result}")
            print(f"errors: {errors}")

        return errors

    def debug_output(self):
        print('TRIGGER TEST DEBUG: ')
        if self.title is not None: print(f"Test title: {self.title}")
        if self.name is not None: print(f"name: {self.name}")
        if self.description is not None: print(f"description: {self.description}")
        if self.arguments is not None: print(f"arguments: {self.arguments}")
        if self.custom_feedback is not None: print(f"custom_feedback: {self.custom_feedback}")
        if self.llm_check is not None: print(f"llm_check: {self.llm_check}")
