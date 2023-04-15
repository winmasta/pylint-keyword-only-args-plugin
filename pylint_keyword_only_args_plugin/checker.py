import builtins
from typing import Iterable

from astroid.nodes import Call, Assign, Tuple
from pylint.checkers import BaseChecker


class KeywordOnlyArgsChecker(BaseChecker):
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
    options = (
        (
            "skip-names-list",
            {"default": "", "type": "string", "help": "Comma separated list of callable names to skip"}
        ),
    )

    def visit_call(self, node: Call) -> None:
        nodes: Iterable = [node]
        if isinstance(node, Assign):
            if isinstance(node.value, Call):
                nodes = [node.value]

            if isinstance(node.value, Tuple):
                nodes = node.value.elts

        skip_names_list = [*dir(builtins), *self.linter.config.skip_names_list.split(","), "Path"]
        for _node in nodes:
            if _node.func.name in skip_names_list:
                return

            if node.args:
                self.add_message("keyword-only-args", node=_node)
