
class InputValidator:
    @staticmethod
    def validate_input(required_parameters, incoming_data):
        for param in required_parameters:
            if param not in incoming_data:
                return False
        return True
