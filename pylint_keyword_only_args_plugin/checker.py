from astroid.nodes import Call
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


class KeywordOnlyArgsChecker(BaseChecker):
    __implements__ = IAstroidChecker

    name = "keyword-only-args"
    priority = -100
    msgs = {
        "C0004": (
            "Only keyword arguments allowed to callable.",
            "keyword-only-args",
            "Positional arguments to callable not allowed. "
            "Example: func_call(a=1, b=2) - good, func_call(a, b) - bad, func_call(a, b=2) - bad.",
        ),
    }

    def visit_call(self, node: Call) -> None:
        if node.args:
            self.add_message("keyword-only-args", node=node)
