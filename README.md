## Plugin for pylint which checks that call statements has only keyword args

Install:
```bash
pip install pylint-keyword-only-args-plugin
```

Usage:
```bash
pylint --load-plugins pylint_keyword_only_args_plugin FILES_TO_CHECK
```

Add to `pylintrc` file to skip desired callable names:
```bash
[VARIABLES]
skip-names-list=callable_name_1,callable_name_1  # Comma separated list of callable names to skip
```
