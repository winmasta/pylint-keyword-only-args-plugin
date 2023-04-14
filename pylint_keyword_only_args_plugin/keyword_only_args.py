from pylint_keyword_only_args_plugin.checker import KeywordOnlyArgsChecker


def register(linter):
    linter.register_checker(KeywordOnlyArgsChecker(linter))
