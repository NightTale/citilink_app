from flask import Flask, render_template
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.options import Options

app = Flask(__name__)

app.config['SECRET_KEY'] = 'SECRET_KEY'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/category/<string:id>')
def category(id: str):
    titles = {
        'noutbuki': 'Ноутбуки',
        'smartfony': 'Смартфоны',
        'televizory': 'Телевизоры',
        'monitory': 'Мониторы',
        'processory': 'Процессоры'
    }

    # прячем открывающийся браузер
    driver_exe = 'edgedriver'
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Edge(driver_exe, options=options)

    # основной парсер
    website = f'https://www.citilink.ru/catalog/{id}/?pf=discount.any%2Crating.any&f=rating.any%2Cdiscount.price1_20&pprice_min=0&pprice_max=1000000&price_min=0&price_max=1000000'
    driver.get(website)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    cells = soup.find_all('div', class_='e12wdlvo0 app-catalog-1bogmvw e1loosed0')
    info = []
    for i in range(len(cells)):
        try:
            image = cells[i].find('div', class_='app-catalog-lxji0k e153n9o30').find('img').get('src')
            description = cells[i].find('div', class_='app-catalog-1tp0ino e1an64qs0').find('a').text
            old_price = int(cells[i].find('span', class_='e1ap1az10 e119ip7e0 e106ikdt0 app-catalog-1q0401k e1gjr6xo0').text.replace(" ", ""))
            new_price = int(cells[i].find('span', class_='e10p9yfm0 e2bu0ii0 e106ikdt0 app-catalog-1bqq3d9 e1gjr6xo0').text.replace(" ", "")[:-1])
            ref = f"https://www.citilink.ru{cells[i].find('div', class_='app-catalog-1tp0ino e1an64qs0').find('a').get('href')}"
            reduction = f'{round(((old_price - new_price) / old_price) * 100)} %'
            info.append([reduction, image, description, new_price, old_price, ref])
        except Exception:
            pass
    info.sort(reverse=True)
    inscr = ''
    if len(info) == 0:
        inscr = 'Нет товаров со скидкой больше 20%. Проверьте позже'
    print(len(info))
    return render_template('category.html', id=id, title=titles[id], info=info, inscr=inscr)


if __name__ == '__main__':
    app.run(debug=True)
