import asyncio
from playwright.async_api import async_playwright
from json import dumps

async def all_laptops_info():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto('https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops')

        all_laptops_title_locator = page.locator('.title', has_text='Lenovo')

        all_info_laptops = list()
        for laptop_count in range(all_laptops_title_locator.count()):

            single_laptop_title_locator = all_laptops_title_locator.nth(laptop_count)
            single_laptop_title_locator.click()

            #tenho ciencia que o segundo lenovo parece um cadastro errado, em uma situacao real eu iria levar isso ao PO
            # para entender como ele iria querer lidar, fazer tratamento de erro, ignorar e arrumar na resposta, etc. 
            # nesse caso eu so ignorei e fingi que todos sao iguais
            laptop_description =    page.locator('.description').inner_text().replace('"','')
            laptop_splitted_description = laptop_description.split(sep=',')

            title = laptop_splitted_description[0]
            screen = laptop_splitted_description[1]
            cpu = laptop_splitted_description[2]
            ram_memory = laptop_splitted_description[3]

            #infelizmente as informacoes ficam muito fora de padrao a partir daqui
            other_description_info = laptop_description.split(ram_memory)[1].replace(',','')


            laptop_price = float(page.locator('.pull-right', has_text='$').inner_text().replace('$',''))

            reviews = int(page.locator('text=reviews').inner_text().replace(' reviews',''))

            stars = page.locator('.glyphicon-star').count()

            hdd_128_opt_available = page.locator('button', has_text='128').get_attribute('class').find('disabled') == -1

            hdd_256_opt_available = page.locator('button', has_text='256').get_attribute('class').find('disabled') == -1

            hdd_512_opt_available = page.locator('button', has_text='512').get_attribute('class').find('disabled') == -1        

            hdd_1024_opt_available =    page.locator('button', has_text='1024').get_attribute('class').find('disabled') == -1

            all_info_laptops.append({
                'title':title,
                'laptop_price':laptop_price,
                'screen':screen,
                'cpu':cpu,
                'ram_memory':ram_memory,
                'stars':stars,
                'reviews':reviews,
                'hdd_128_opt_available':hdd_128_opt_available,
                'hdd_256_opt_available':hdd_256_opt_available,
                'hdd_512_opt_available':hdd_512_opt_available,
                'hdd_1024_opt_available':hdd_1024_opt_available,
                'other_description_info':other_description_info})
            
            page.goto('https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops')

        await browser.close()

        all_info_laptops = sorted(all_info_laptops,key=lambda d: d['laptop_price'])

        return dumps(all_info_laptops)

