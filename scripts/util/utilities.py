import re


class InputValidator:
    @staticmethod
    def validate_input(required_parameters, incoming_data):
        for param in required_parameters:
            if param not in incoming_data:
                return False
        return True


class Util:

    @staticmethod
    def anything_after_matches(search_for, name):
        pattern = Util.get_pattern(search_for=search_for)
        return re.match(pattern, name)

    @staticmethod
    def get_pattern(search_for):
        return re.compile('{}.*'.format(search_for))
