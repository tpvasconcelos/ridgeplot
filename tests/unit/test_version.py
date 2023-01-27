def test_version() -> None:
    from ridgeplot import __version__ as v_public
    from ridgeplot._version import __version__ as v_private

    assert v_public is v_private
    assert v_public == "0.1.21"
