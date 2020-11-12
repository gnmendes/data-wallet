
class InputValidator:
    @staticmethod
    def validate_input(required_parameters, incoming_data):
        for param in required_parameters:
            if param not in incoming_data:
                return False
        return True


class Util:

    @staticmethod
    def produces_error_object(err):
        assert err
        return {'error': 500, 'errorMessage': str(err)}

    @staticmethod
    def is_valid(required, data):
        return InputValidator.validate_input(required_parameters=required, incoming_data=data)

    @staticmethod
    def get_status(body, status_when_ok=200):
        return body['error'] if 'error' in body else status_when_ok


class CPFValidator:

    @staticmethod
    def is_cpf_valid(cpf):
        cpf_as_text = str(cpf)
        if not CPFValidator.is_valid_cpf_length(cpf=cpf_as_text):
            return False
        first_nine_sum = CPFValidator.__sum_first_n_digits(cpf=cpf_as_text, number_of_digits=9)
        if not CPFValidator.validate_verifier_digit(sum_of_digits=first_nine_sum, verifier_digit=cpf_as_text[9:10]):
            return False
        first_ten_sum = CPFValidator.__sum_first_n_digits(cpf=cpf_as_text, number_of_digits=10)
        if not CPFValidator.validate_verifier_digit(sum_of_digits=first_ten_sum, verifier_digit=cpf_as_text[-1]):
            return False
        return True

    @staticmethod
    def validate_verifier_digit(sum_of_digits, verifier_digit):
        remain = CPFValidator.get_rest(total=sum_of_digits)
        return remain == int(verifier_digit)

    @staticmethod
    def get_rest(total):
        rem = total % 11
        if rem < 2:
            return 0

        return 11 - rem

    @staticmethod
    def __sum_first_n_digits(cpf, number_of_digits):
        sum_first_digits = 0
        sequence_desc = number_of_digits + 1
        for digits in cpf[:number_of_digits]:
            sum_first_digits += int(digits) * sequence_desc
            sequence_desc -= 1
        return sum_first_digits

    @staticmethod
    def is_valid_cpf_length(cpf):
        return len(cpf) == 11
