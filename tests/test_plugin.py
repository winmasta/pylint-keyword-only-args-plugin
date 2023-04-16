from astroid import extract_node
from pylint.interfaces import UNDEFINED
from pylint.testutils import CheckerTestCase, MessageTest

from pylint_keyword_only_args_plugin import checker


class TestUniqueReturnChecker(CheckerTestCase):
    CHECKER_CLASS = checker.KeywordOnlyArgsChecker

    def test_keyword_only_args_success(self: "TestUniqueReturnChecker") -> None:
        node = extract_node(
            """
            func_call(a=1, b=3)
            """,
        )
        with self.assertNoMessages():
            self.checker.visit_call(node)

    def test_all_no_keyword_only_args_fail(self: "TestUniqueReturnChecker") -> None:
        node = extract_node(
            """
            func_call(a, b)
            """,
        )
        with self.assertAddsMessages(
            MessageTest(
                msg_id="keyword-only-args",
                line=2,
                confidence=UNDEFINED,
                node=node,
                col_offset=0,
                end_line=2,
                end_col_offset=15,
            ),
        ):
            self.checker.visit_call(node)

    def test_one_no_keyword_only_args_fail(self: "TestUniqueReturnChecker") -> None:
        node = extract_node(
            """
            func_call(a, b=3)
            """,
        )
        with self.assertAddsMessages(
            MessageTest(
                msg_id="keyword-only-args",
                line=2,
                confidence=UNDEFINED,
                node=node,
                col_offset=0,
                end_line=2,
                end_col_offset=17,
            ),
        ):
            self.checker.visit_call(node)

    def test_builtin_success(self: "TestUniqueReturnChecker") -> None:
        node = extract_node(
            """
            str(1)
            int("1")
            float(1)
            bool(1)
            list({1, 2})
            set([1, 2])
            tuple([1, 2])
            dict([[1, 2]])
            """,
        )
        with self.assertNoMessages():
            self.checker.visit_call(node)

    def test_path_success(self: "TestUniqueReturnChecker") -> None:
        node = extract_node(
            """
            Path("/")
            """,
        )
        with self.assertNoMessages():
            self.checker.visit_call(node)

    def test_skip_names_success(self: "TestUniqueReturnChecker") -> None:
        self.checker.linter.config.skip_names_list = "custom_func_1,custom_func_2"
        node = extract_node(
            """
            custom_func_1(1)
            custom_func_2(2)
            """,
        )
        with self.assertNoMessages():
            self.checker.visit_call(node)

    def test_assign_success(self: "TestUniqueReturnChecker") -> None:
        self.checker.linter.config.skip_names_list = "custom_func_1"
        node = extract_node(
            """
            value = custom_func_1(1)
            """,
        )
        with self.assertNoMessages():
            self.checker.visit_call(node)

    def test_assign_tuple_success(self: "TestUniqueReturnChecker") -> None:
        self.checker.linter.config.skip_names_list = "custom_func_1,custom_func_2"
        node = extract_node(
            """
            value = custom_func_1(1), custom_func_2(2)
            """,
        )
        with self.assertNoMessages():
            self.checker.visit_call(node)

    def test_func_is_attr_success(self: "TestUniqueReturnChecker") -> None:
        self.checker.linter.config.skip_names_list = "safe_load,read"
        node = extract_node(
            """
            prom_conf = safe_load(f.read())
            """,
        )
        with self.assertNoMessages():
            self.checker.visit_call(node)
