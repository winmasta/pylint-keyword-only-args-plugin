from astroid import extract_node
from pylint.interfaces import UNDEFINED
from pylint.testutils import CheckerTestCase, MessageTest

from pylint_keyword_only_args_plugin import checker


class TestUniqueReturnChecker(CheckerTestCase):
    CHECKER_CLASS = checker.KeywordOnlyArgsChecker

    def test_keyword_only_args_success(self):
        node = extract_node(
            """                 
            func_call(a=1, b=3)
            """
        )
        with self.assertNoMessages():
            self.checker.visit_call(node)

    def test_all_no_keyword_only_args_fail(self):
        node = extract_node(
            """                 
            func_call(a, b)
            """
        )
        with self.assertAddsMessages(
                MessageTest(
                    msg_id="keyword-only-args",
                    line=2,
                    confidence=UNDEFINED,
                    node=node,
                    col_offset=0,
                    end_line=2,
                    end_col_offset=9,
                )
        ):
            self.checker.visit_call(node)

    def test_one_no_keyword_only_args_fail(self):
        node = extract_node(
            """                 
            func_call(a, b=3)
            """
        )
        with self.assertAddsMessages(
                MessageTest(
                    msg_id="keyword-only-args",
                    line=2,
                    confidence=UNDEFINED,
                    node=node,
                    col_offset=0,
                    end_line=2,
                    end_col_offset=9,
                )
        ):
            self.checker.visit_call(node)
