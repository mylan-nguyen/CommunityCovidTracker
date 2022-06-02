import json

# ===================================================
# Function to have a defined type of student
# ===================================================
class Member:

    def __init__(self, sin_number, name, is_sick=False):
        try:
            if Member.is_valid_id(sin_number) is False:
                raise ValueError("The sin number {} is not a sin number".format(sin_number))
            self.sin_number = sin_number
            self.name = name
            self.is_sick = is_sick
        except ValueError as e:
            print(e)

    def __str__(self):
        return '{} ({})'.format(self.name, self.sin_number)

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def is_valid_id(sin_number):
        if sin_number[0:1] != '4':
            return False

        for i in sin_number:
            if i not in '0123456789':
                return False

        return True

    @classmethod
    def from_JSON(cls, json_string):
        return Member(json_string["sin"], json_string["name"])
'''
def main():
    larry = Member("464591165", "Larry")
    print(str(larry))

    print(repr(larry))
    print(larry)

    print(Member.is_valid_id('464591165'))
    print(Member.is_valid_id('2601543s'))

    larry = Member.from_JSON('{"sin": "464591165", "name": "Larry"}')
    print(str(larry))


main()
'''
