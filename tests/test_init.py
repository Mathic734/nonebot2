import pytest

import nonebot
from nonebot.drivers import ReverseDriver
from nonebot import get_app, get_bot, get_asgi, get_bots, get_driver


@pytest.mark.asyncio
async def test_init():
    env = nonebot.get_driver().env
    assert env == "test"

    config = nonebot.get_driver().config
    assert config.config_from_env == {"test": "test"}
    assert config.config_override == "new"
    assert config.config_from_init == "init"
    assert config.common_config == "common"
    assert config.common_override == "new"
    assert config.nested_dict == {"a": 1, "b": 2, "c": {"d": 3}}
    assert config.nested_missing_dict == {"a": 1, "b": {"c": 2}}
    assert config.not_nested == "some string"


@pytest.mark.asyncio
async def test_get(monkeypatch: pytest.MonkeyPatch):
    with monkeypatch.context() as m:
        m.setattr(nonebot, "_driver", None)
        with pytest.raises(ValueError):
            get_driver()

    driver = get_driver()
    assert isinstance(driver, ReverseDriver)
    assert get_asgi() == driver.asgi
    assert get_app() == driver.server_app

    runned = False

    def mock_run(*args, **kwargs):
        nonlocal runned
        runned = True
        assert args == ("arg",) and kwargs == {"kwarg": "kwarg"}

    monkeypatch.setattr(driver, "run", mock_run)
    nonebot.run("arg", kwarg="kwarg")
    assert runned

    with pytest.raises(ValueError):
        get_bot()

    monkeypatch.setattr(driver, "_bots", {"test": "test"})
    assert get_bot() == "test"
    assert get_bot("test") == "test"
    assert get_bots() == {"test": "test"}
