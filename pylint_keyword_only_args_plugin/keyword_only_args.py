from pylint.lint import PyLinter

from pylint_keyword_only_args_plugin.checker import KeywordOnlyArgsChecker


def register(linter: PyLinter) -> None:
    linter.register_checker(KeywordOnlyArgsChecker(linter))
