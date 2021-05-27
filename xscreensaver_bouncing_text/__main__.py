
def main() -> None:
    """Entrypoint to the ``celery`` umbrella command."""
    from xscreensaver_bouncing_text.bin.xscreensaver_bouncing_text import main as _main
    _main()


if __name__ == '__main__':  # pragma: no cover
    main()
