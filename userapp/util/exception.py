"""
    Written by ©Anirban Bhattacherji
    2021
"""

from userapp.util import constants


class CustomErr(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
            self.code = args[1]
        else:
            self.message = constants.INTERNAL_ERR
            self.code = 500

    def __str__(self):
        return 'Exception occurred: {}'.format(self.message)
