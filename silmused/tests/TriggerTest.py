from silmused.tests.TestDefinition import TestDefinition
from silmused.utils import list_to_string


class TriggerTest(TestDefinition):
    def __init__(self, name, title=None, description=None, points=0, arguments=None,
                 custom_feedback=None, manipulation=None, action_timing=None, should_exist=True,
                 llm_check=False, debug=None):

        query = f"SELECT {list_to_string(arguments)[1:-1] if arguments is not None else '*'} FROM information_schema.triggers WHERE trigger_name = '{name}'"
        if manipulation is not None:
            if isinstance(manipulation, str):
                query += f" AND event_manipulation = '{manipulation}'"
            elif isinstance(manipulation, list):
                for (index, arg) in enumerate(manipulation):
                    operator = 'AND (' if index == 0 else 'OR'
                    query += f" {operator} event_manipulation = '{arg}'"
                query += ")"
            else:
                raise AttributeError('Parameter arguments must be a list')

        if action_timing is not None:
            if isinstance(action_timing, str):
                query += f" AND action_timing = '{action_timing}'"
            else:
                raise AttributeError('Parameter action_timing must be a string')

        super().__init__(
            name=name,
            title=title,
            points=points,
            description=description,
            arguments=arguments,
            should_exist=should_exist,
            custom_feedback=custom_feedback,
            llm_check=llm_check,
            query=query,
            debug=debug,
        )

        self.action_timing = action_timing
        self.manipulation = manipulation
        self.test_type = "trigger_test"

    def execute(self, cursor):

        if isinstance(self.arguments, list):
            self.query = self._check_separately_for_all_event_manipulations(cursor)

        cursor.execute(self.query)
        result = cursor.fetchall()


        if self.debug is not None: self.debug_output(result)

        if self.should_exist:
            if self.manipulation is not None:
                return super().response(
                    len(result) > 0,
                    {"test_type": self.test_type,
                     "test_key": "trigger_should_exist_manipulation_positive_feedback",
                     "params": {"trigger_name": self.name, "manipulation": self.manipulation}},
                    {"test_type": self.test_type,
                     "test_key": "trigger_should_exist_manipulation_negative_feedback",
                     "params": {"trigger_name": self.name, "manipulation": self.manipulation}},
                )

            elif self.action_timing is not None:
                return super().response(
                    len(result) > 0,
                    {"test_type": self.test_type,
                     "test_key": "trigger_should_exist_action_timing_positive_feedback",
                     "params": {"trigger_name": self.name, "action_timing": self.action_timing}},
                    {"test_type": self.test_type,
                     "test_key": "trigger_should_exist_action_timing_negative_feedback",
                     "params": {"trigger_name": self.name, "action_timing": self.action_timing}},
                )
            else:
                return super().response(
                    len(result) > 0,
                    {"test_type": self.test_type,
                     "test_key": "trigger_should_exist_positive_feedback",
                     "params": {"trigger_name": self.name}},
                    {"test_type": self.test_type,
                     "test_key": "trigger_should_exist_negative_feedback",
                     "params": {"trigger_name": self.name}},
                )
        else:
            if self.manipulation is not None:
                return super().response(
                    len(result) == 0,
                    {"test_type": self.test_type,
                     "test_key": "trigger_should_not_exist_manipulation_positive_feedback",
                     "params": {"trigger_name": self.name, "manipulation": self.manipulation}},
                    {"test_type": self.test_type,
                     "test_key": "trigger_should_not_exist_manipulation_negative_feedback",
                     "params": {"trigger_name": self.name, "manipulation": self.manipulation}},
                )

            elif self.action_timing is not None:
                return super().response(
                    len(result) == 0,
                    {"test_type": self.test_type,
                     "test_key": "trigger_should_not_exist_action_timing_positive_feedback",
                     "params": {"trigger_name": self.name, "action_timing": self.action_timing}},
                    {"test_type": self.test_type,
                     "test_key": "trigger_should_not_exist_action_timing_negative_feedback",
                     "params": {"trigger_name": self.name, "action_timing": self.action_timing}},
                )
            else:
                return super().response(
                    len(result) == 0,
                    {"test_type": self.test_type,
                     "test_key": "trigger_should_not_exist_positive_feedback",
                     "params": {"trigger_name": self.name}},
                    {"test_type": self.test_type,
                     "test_key": "trigger_should_not_exist_negative_feedback",
                     "params": {"trigger_name": self.name}},
                )

    def _check_separately_for_all_event_manipulations(self, cursor):
        found = []
        for arg in self.manipulation:
            query = (f"SELECT trigger_name FROM information_schema.triggers WHERE trigger_name = '{self.name}' "
                     f"AND event_manipulation = '{arg}'")
            cursor.execute(query)
            result = cursor.fetchall()
            if len(result) > 0:
                found.append(arg)
        if len(found) == 0: return self.query
        query = f"SELECT trigger_name FROM information_schema.triggers WHERE trigger_name = '{self.name}'"
        self.manipulation = found
        for (index, c_name) in enumerate(self.manipulation):
            operator = 'AND (' if index == 0 else 'OR'
            query += f" {operator} event_manipulation = '{c_name}'"
        query += ")"
        return query

    def debug_output(self, result):
        print('TRIGGER TEST DEBUG: ')
        if self.debug == 'DEBUG':
            if self.title is not None: print(f"Test title: {self.title}")
            print(f"query: {self.query}")
            print(f"result: {result}")
        if self.debug == 'ALL':
            if self.title is not None: print(f"Test title: {self.title}")
            if self.name is not None: print(f"name: {self.name}")
            if self.description is not None: print(f"description: {self.description}")
            if self.arguments is not None: print(f"arguments: {self.arguments}")
            if self.manipulation is not None: print(f"manipulations: {self.manipulation}")
            if self.action_timing is not None: print(f"action_timing: {self.action_timing}")
            if self.custom_feedback is not None: print(f"custom_feedback: {self.custom_feedback}")
            if self.llm_check is not None: print(f"llm_check: {self.llm_check}")
            if self.should_exist is not None: print(f"should_exist: {self.should_exist}")
        if self.debug not in ['DEBUG', 'ALL']:
            print(f"Warning! {self.debug} is not valid debug level, choose 'DEBUG' or 'ALL'")
