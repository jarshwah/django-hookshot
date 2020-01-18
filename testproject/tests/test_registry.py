import pytest
from hookshot.registry import _registry, HookArgs, webhook
from application import hello_webhook


def _f(*args, **kwargs):
    pass


def test_hook_registered():
    assert "hello_webhook" in _registry
    hook_args: HookArgs = _registry["hello_webhook"]
    assert hook_args.name == "hello_webhook"
    assert hook_args.func == hello_webhook
    assert hook_args.insecure is False
    assert hook_args.description == "Returns Hello"


def test_good_hook_names():
    webhook("justletters")(_f)
    assert "justletters" in _registry
    webhook("JUSTLETTERS")(_f)
    assert "JUSTLETTERS" in _registry
    webhook("some_other-symbols-123")(_f)
    assert "some_other-symbols-123" in _registry


def test_illegal_hook_names():
    with pytest.raises(ValueError, match=r".* does not match the pattern"):
        webhook("illegal!")(_f)
    with pytest.raises(ValueError, match=r".* does not match the pattern"):
        webhook("123_starts_with_number")(_f)
    with pytest.raises(ValueError, match=r".* does not match the pattern"):
        webhook("_starts_with_underscore")(_f)
    with pytest.raises(ValueError, match=r".* does not match the pattern"):
        webhook("-starts_with_hyphen")(_f)
