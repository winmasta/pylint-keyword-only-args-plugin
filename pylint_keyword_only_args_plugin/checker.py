import builtins
from typing import TYPE_CHECKING

from astroid.nodes import Assign, Attribute, Call, Tuple
from pylint.checkers import BaseChecker

if TYPE_CHECKING:
    from collections.abc import Iterable


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
            {
                "default": "",
                "type": "string",
                "help": "Comma separated list of callable names to skip",
            },
        ),
    )

    def visit_call(self: "KeywordOnlyArgsChecker", node: Call) -> None:
        nodes: Iterable = [node]
        if isinstance(node, Assign):
            if isinstance(node.value, Call):
                nodes = [node.value]

            if isinstance(node.value, Tuple):
                nodes = node.value.elts

        skip_names_list = [
            *dir(builtins),
            *self.linter.config.skip_names_list.split(","),
            "Path",
        ]
        for _node in nodes:
            node_name = (
                _node.func.attrname
                if isinstance(_node.func, Attribute)
                else _node.func.name
            )

            if node_name in skip_names_list:
                return

            if _node.args:
                self.add_message("keyword-only-args", node=_node)
