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
        return set()


class DummyInvariant(BaseInvariant):
    def compare(self, matrix: list) -> set:
        return set(string.ascii_uppercase)


class SeriesInvariant(BaseInvariant):
    letters = [
        ('1313', 'A'),
        ('13131', 'B'),
    ]

    @staticmethod
    def compute_series_num(row: list) -> int:
        # @todo make beautiful
        series_count = 0
        last_mask = None
        for i in row:
            if last_mask is None or last_mask != i:
                series_count += 1
                last_mask = i
                continue
        return series_count

    def compare(self, matrix: list) -> set:
        series_matrix = [self.compute_series_num(i) for i in matrix]
        unique_series = ''
        # @todo make beautiful
        for elem in map(str, filter(lambda x: x > 0, series_matrix)):
            if not unique_series or elem != unique_series[-1]:
                unique_series += elem

        return set([i[1] for i in self.letters if i[0] == unique_series])


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
    # @todo clean noise
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
