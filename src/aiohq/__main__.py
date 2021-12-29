from aiohttp.web import run_app
from .server import create_app

def main() -> None:
    run_app(create_app())


if __name__ == '__main__':
    main()
