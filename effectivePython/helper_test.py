from unittest import TestCase, main


def sum_sqaures(values):
    cumulative = 0
    for value in values:
        cumulative += value ** 2
        yield cumulative


class HelperTestCase(TestCase):
    def verify_complex_case(self, values, expected):
        expect_it = iter(expected)
        found_it = iter(sum_sqaures(values))
        test_it = zip(expect_it, found_it)

        for i, (expect, found) in enumerate(test_it):
            self.assertEqual(
                expect,
                found,
                f'잘못된 인덱스: {i}')

        #- 두 제너레이터를 모두 소진했는지 확인
        try:
            next(expect_it)
        except StopIteration:
            pass
        else:
            self.fail('실제보다 예상한 제너레이터가 더 김')

        try:
            next(found_it)
        except StopIteration:
            pass
        else:
            self.fail('예상한 제너레이터보다 실제가 더 김')



    def test_wrong_lengths(self):
        values = [1.1, 2.2, 3.3]
        expected = [
            1.1 ** 2,
        ]
        self.verify_complex_case(values, expected)


    def test_wrong_results(self):
        values = [1.1, 2.2, 3.3]
        expected = [
            1.1 ** 2,
            1.1 ** 2 + 2.2 ** 2,
            1.1 ** 2 + 2.2 ** 2 + 3.3 ** 2 + 4.4 ** 2,
                    ]
        self.verify_complex_case(values, expected)


if __name__ == '__main__':
    main()

