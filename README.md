# django-hookshot
A django package for writing simple webhooks with admin configurable access per user

[![CircleCI](https://circleci.com/gh/jarshwah/django-hookshot.svg?style=svg)](https://circleci.com/gh/jarshwah/django-hookshot)

## Contributing

We use `pre-commit <https://pre-commit.com/>` to enforce our code style rules
locally before you commit them into git. Once you install the pre-commit library
(locally via pip is fine), just install the hooks::

    pre-commit install -f --install-hooks

The same checks are executed on the build server, so skipping the local linting
(with `git commit --no-verify`) will only result in a failed test build.

Current style checking tools:

- flake8: python linting
- isort: python import sorting
- black: python code formatting

Note:

    You must have python3.6 available on your path, as it is required for some
    of the hooks.
