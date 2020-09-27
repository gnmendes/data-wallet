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
    def anything_after_str_matches(search_for, name):
        pattern = Util.get_pattern(search_for=search_for)
        return re.match(pattern, name)

    @staticmethod
    def get_pattern(search_for):
        return re.compile('{}.*'.format(search_for))


class CPFValidator:

    @staticmethod
    def is_cpf_valid(cpf):
        CPFValidator.is_valid_cpf_length(cpf=cpf)
        first_nine_sum = CPFValidator.__sum_first_n_digits(cpf=cpf, number_of_digits=10)
        CPFValidator.validate_verifier_digit(sum_of_digits=first_nine_sum, verifier_digit=cpf[10:11])
        first_ten_sum = CPFValidator.__sum_first_n_digits(cpf=cpf, number_of_digits=11)
        CPFValidator.validate_verifier_digit(sum_of_digits=first_ten_sum, verifier_digit=cpf[-1])

    @staticmethod
    def validate_verifier_digit(sum_of_digits, verifier_digit):
        remain = CPFValidator.get_rest(sum=sum_of_digits)
        assert remain == verifier_digit

    @staticmethod
    def get_rest(sum):
        return (sum * 10) % 11

    @staticmethod
    def __sum_first_n_digits(cpf, number_of_digits):
        sum_first_digits = 0
        sequence_desc = number_of_digits
        for digits in cpf[:number_of_digits]:
            sum_first_digits += int(digits) * sequence_desc
            sequence_desc -= 1
        return sum_first_digits

    @staticmethod
    def is_valid_cpf_length(cpf):
        assert len(cpf) == 11
