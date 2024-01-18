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
        # TODO small tests in separate functions
        cursor.execute(f"SELECT trigger_name FROM information_schema.triggers WHERE trigger_name = '{self.name}'")

        if len(cursor.fetchall()) <= 0:
            return super().response(
                False,
                ''
                f"Trigger {self.name} was not found",
            )

        errors = []

        if len(self.arguments) > 0:
            for manipulation in self.arguments:
                cursor.execute(
                    f"SELECT trigger_name FROM information_schema.triggers WHERE trigger_name = '{self.name}' AND event_manipulation = '{manipulation}'")
                if len(cursor.fetchall()) <= 0:
                    errors.append(f"manipulation {manipulation} was not found")

        # TODO this is a bit of a copy-paste
        cursor.execute(f"SELECT trigger_name FROM information_schema.triggers WHERE trigger_name = '{self.name}' AND action_timing = '{self.action_timing}'")
        if len(cursor.fetchall()) <= 0:
            errors.append(f"action timing {self.action_timing} was not found")

        return super().response(
            len(errors) == 0,
            f"Correct, trigger {self.name} definition is correct",
            f"Trigger {self.name} had the following errors: {', '.join(errors)}",
        )
