
# based on class HttpStatus

from enum import IntEnum

__all__ = ['ExitCode']

class ExitCode(IntEnum):

    def __new__(cls, value, phrase, description=''):
        obj = int.__new__(cls, value)
        obj._value_ = value

        obj.phrase = phrase
        obj.description = description
        return obj

    SUCCESS        =  0, 'SUCCESS', ''
    COMPARE_FAILED = 42, 'output does not match', ''

    # http: // git.savannah.gnu.org / cgit / coreutils.git / tree / src / timeout.c
    TIMEOUT        = 124, 'timeoue expired', ''
    TIMEOUT_KILL   = 128+9, 'timeoue expired with SIGKILL', ''
    PROCESS_ERROR  = 50, 'process terminated with error', 'your code crashed'
    SERVER_ERROR   = 500, 'internal server error'

    @staticmethod
    def values():
        # get the attributes without the magic '_*'
        names = tuple(filter(lambda x: x[0] != '_', dir(ExitCode)))
        return tuple(map( lambda x: getattr(ExitCode,x), names))

    # TODO: get all values
    # @staticmethod
    # def values(cls):
    #     return {}


if __name__ == "__main__":
    print(42 in map(int,ExitCode.values()))

