import abc
import logging
import sys


class BaseInvariant(abc.ABC):
    @abc.abstractmethod
    def determine(self, matrix: list) -> set:
        pass


class DummyInvariant(BaseInvariant):
    def determine(self, matrix: list) -> set:

        return set()


def prepare_matrix(source: list) -> list:
    matrix = [list(row[:-1].strip().replace(' ', '0').replace('*', '1')) for row in source]
    return matrix


def main(filepath: str):
    with open(filepath, 'r') as f:
        matrix = prepare_matrix(f.readlines())

    comparators_enabled = [DummyInvariant()]
    determined_letters = [compare_cls.determine(matrix) for compare_cls in comparators_enabled]
    logging.info('result %s', determined_letters)


if __name__ == '__main__':
    main(sys.argv[1])
