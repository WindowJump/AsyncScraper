"""
Asynchronous scraper utilizing asyncio, aiohttp, and BeautifulSoup for scraping
information about NVIDIA graphics cards on eBay.
"""
import aiohttp
import asyncio
from bs4 import BeautifulSoup


async def fetch_and_save(session, page_index):
    try:
        async with session.get('https://www.ebay.com/sch/i.html?_from=R40&_nkw=nvidia+graphic+cards&_sacat=27386'
                               f'&_pgn={page_index}') as resp:
            resp.raise_for_status()
            html_doc = await resp.text()

        soup = BeautifulSoup(html_doc, 'html.parser')
        div_elements = soup.find_all('div', class_='s-item__info clearfix')

        if div_elements:
            with open(f'output_page.txt', 'a', encoding='utf-8') as file:
                for div_elem in div_elements:
                    span_elem = div_elem.find('span', {'aria-level': '3', 'role': 'heading'})
                    card_price = div_elem.find('span', class_='s-item__price')                    
                    file.write(span_elem.get_text(strip=True) + '  ' + card_price.get_text(strip=True) + '\n')
            print(f'{page_index} finished')
    except Exception as e:
        print(f'Error processing page {page_index}: {e}')


async def main():
    async with aiohttp.ClientSession() as session:
        async with asyncio.TaskGroup() as tg:
            for page_index in range(1, 51):
                tg.create_task(fetch_and_save(session, page_index))


if __name__ == "__main__":
    asyncio.run(main())
