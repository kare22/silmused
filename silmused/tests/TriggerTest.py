from silmused.tests.TestDefinition import TestDefinition


class TriggerTest(TestDefinition):
    def __init__(self, name, title=None, description=None, points=0, arguments=None, action_timing=None):
        super().__init__(
            name=name,
            title=title,
            points=points,
            description=description,
            arguments=arguments,
            query=f"SELECT * FROM information_schema.views WHERE table_name = '{name}'",
        )

        self.action_timing = action_timing

    def execute(self, cursor):

        # Check that trigger name exists
        test_trigger_exists_result = self.test_trigger_exists(cursor)
        if test_trigger_exists_result is not None:
            return test_trigger_exists_result

        # Check trigger event manipulation on arguments and trigger action timing
        errors = self.test_trigger_manipulation(cursor) if len(self.arguments) > 0 else []

        return super().response(
            len(errors) == 0,
            {"test_type": "trigger_test",
             "test_key": "trigger_definition_positive_feedback",
             "params": [self.name]},
            {"test_type": "trigger_test",
             "test_key": "trigger_definition_negative_feedback",
             "params": [self.name, {', '.join(errors)}]},  # TODO errorid on hetkel inglise keeles
        )

    def test_trigger_exists(self, cursor):
        cursor.execute(f"SELECT trigger_name FROM information_schema.triggers WHERE trigger_name = '{self.name}'")

        if len(cursor.fetchall()) <= 0:
            return super().response(
                False,
                {"test_type": "trigger_test",
                 "test_key": "trigger_exists_positive_feedback",
                 "params": [self.name]},
                {"test_type": "trigger_test",
                 "test_key": "trigger_exists_negative_feedback",
                 "params": [self.name]},
            )
        return None

    def test_trigger_manipulation(self, cursor):
        errors = []
        for manipulation in self.arguments:
            cursor.execute(
                f"SELECT trigger_name FROM information_schema.triggers WHERE trigger_name = '{self.name}' "
                f"AND event_manipulation = '{manipulation}'")

            if len(cursor.fetchall()) <= 0:
                errors.append(f"manipulation {manipulation} was not found")

        cursor.execute(
            f"SELECT trigger_name FROM information_schema.triggers WHERE trigger_name = '{self.name}' "
            f"AND action_timing = '{self.action_timing}'")

        if len(cursor.fetchall()) <= 0:
            errors.append(f"action timing {self.action_timing} was not found")

        return errors
