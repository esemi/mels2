import abc
import logging
import string
import sys
from typing import Optional


class BaseInvariant(abc.ABC):
    @abc.abstractmethod
    def compare(self, matrix: list) -> set:
        """
        :param matrix: list of lists
        :return: {'A', 'B', 'C'}
        """
        pass


class DummyInvariant(BaseInvariant):
    def compare(self, matrix: list) -> set:
        return set(string.ascii_uppercase)


class SeriesInvariant(BaseInvariant):
    def compare(self, matrix: list) -> set:
        # series_matrix

        return {'B', 'C'}


class CompareStrategyBase:
    @staticmethod
    def determine(determined_letters: list) -> Optional[str]:
        """
        Выбираем букву, которая чаще всего встречается.
        Если одинаковый ранг - первую
        """
        from collections import Counter

        summary_letters = sorted([l for row in determined_letters for l in row])
        try:
            return Counter(summary_letters).most_common(1)[0][0]
        except IndexError:
            return None


def prepare_matrix(source: list) -> list:
    matrix = [list(row[:-1].strip().replace(' ', '0').replace('*', '1')) for row in source]
    return matrix


def main(filepath: str) -> Optional[str]:
    with open(filepath, 'r') as f:
        logging.info('read file %s', filepath)
        matrix = prepare_matrix(f.readlines())

    logging.debug('prepare matrix %s', matrix)
    comparators_enabled = [DummyInvariant(), SeriesInvariant()]

    determined_letters = [compare_cls.compare(matrix) for compare_cls in comparators_enabled]
    logging.info('comparators result %s', determined_letters)

    strategy = CompareStrategyBase
    selected_letter = strategy.determine(determined_letters)
    logging.info('result %s', selected_letter)

    return selected_letter


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main(sys.argv[1])
