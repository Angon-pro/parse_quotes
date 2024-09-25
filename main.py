import asyncio

from selenium_parser import SeleniumParser


async def main() -> None:
    url: str = 'https://www.finam.ru/quote/forex/usdrub/'
    await SeleniumParser.parse_content(url)


if __name__ == '__main__':
    asyncio.run(main())
