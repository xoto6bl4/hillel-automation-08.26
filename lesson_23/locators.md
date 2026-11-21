# Локатори для https://qauto2.forstudy.space/

Дані для входу: `guest` / `welcome2qauto` (HTTP Basic Auth на весь сайт,
далі кнопка **Guest log in** всередині застосунку).

Усі локатори перевірені на реальному DOM сайту (Garage, модалка
"Add a car", Fuel expenses, Instructions, футер головної сторінки).

## XPath (25)

1. `//button[text()='Add car']` — кнопка додавання авто (Garage)
2. `//button[text()='Search']` — кнопка пошуку інструкцій
3. `//h1[text()='Fuel expenses']` — заголовок сторінки витрат
4. `//h4[@class='modal-title' and text()='Add a car']` — заголовок модалки
5. `//button[@aria-label='Close']` — кнопка закриття модалки
6. `//input[@name='mileage' and @formcontrolname='mileage']` — поле пробігу (2 атрибути)
7. `//select[@id='addCarBrand']/option[text()='Porsche']` — опція бренду в селекті (2 елементи)
8. `//select[@formcontrolname='model']/option[@value='1: 2']` — опція моделі за value (R8)
9. `//div[@class='input-group-text' and text()='km']` — одиниця виміру пробігу
10. `//button[@class='btn btn-secondary' and text()='Cancel']` — кнопка Cancel
11. `//button[contains(@class,'btn-primary') and @disabled and text()='Add']` — неактивна кнопка Add
12. `//a[@routerlink='/panel/garage' and text()='Garage']` — пункт меню Garage (хедер)
13. `//a[@routerlink='expenses']/span[@class='icon icon-fuel']` — іконка пункту сайдбару (parent→child)
14. `//nav[@class='sidebar d-flex flex-column']/a[contains(text(),'Log out')]` — Log out в сайдбарі
15. `//nav[contains(@class,'user-nav_menu')]/button[text()='Logout']` — Logout у меню користувача
16. `//button[@id='userNavDropdown' and contains(.,'My profile')]` — тогл меню користувача
17. `//a[contains(@href,'.pdf') and contains(@href,'wipers')]` — посилання на PDF-інструкцію
18. `//p[@class='instruction-link_description' and text()='Front windshield wipers on Audi TT']` — назва інструкції
19. `//a[@class='instruction-link_download' and text()='Download']/parent::a` — батьківська картка (axis parent)
20. `//li[@class='instruction-list_item'][1]//p[@class='instruction-link_description']` — опис першої картки (3 елементи)
21. `//button[@id='brandSelectDropdown' and text()='Audi']` — тогл фільтра бренду
22. `//ul[@aria-labelledby='brandSelectDropdown']/li[text()='BMW']` — пункт BMW у списку брендів
23. `//ul[@aria-labelledby='modelSelectDropdown']/li[contains(@class,'-active') and text()='TT']` — активна модель фільтра
24. `//a[@href='https://ithillel.ua' and text()='ithillel.ua']` — посилання на сайт школи (футер, головна)
25. `//div[@class='panel-page_empty panel-empty']/p[contains(text(),'have any cars in your garage')]` — порожній стан гаража (2 елементи)

## CSS (25)

1. `.header_nav > a[routerlink="/panel/garage"]` — Garage в хедері (дочірній комбінатор)
2. `#userNavDropdown > img.icon-btn` — іконка профілю
3. `a.sidebar_btn[routerlink="expenses"] > span.icon-fuel` — іконка Fuel expenses в сайдбарі
4. `.panel-page_heading > button.btn.btn-primary` — кнопка Add car / Add an expense
5. `input#addCarMileage[type="number"][formcontrolname="mileage"]` — поле пробігу (3 умови)
6. `select[formcontrolname="brand"] > option:nth-child(2)` — другий option бренду (BMW)
7. `select[formcontrolname="model"] > option:last-child` — останній option моделі (A8)
8. `.modal-footer > button.btn-primary[disabled]` — неактивна кнопка Add
9. `.modal-footer > button.btn-secondary` — кнопка Cancel
10. `.modal-header > button[aria-label="Close"]` — кнопка закриття модалки
11. `a.instruction-link[href$=".pdf"]` — посилання на PDF (суфікс)
12. `a.instruction-link[href*="Audi TT"]` — конкретна інструкція (підрядок)
13. `.instruction-list_item:first-child > a.instruction-link` — перша картка інструкції
14. `.instruction-list_item + .instruction-list_item` — будь-яка картка, що йде одразу за іншою (усі, крім першої; сусідній елемент)
15. `a.instruction-link > p.instruction-link_description` — опис інструкції (дочірній)
16. `a.instruction-link > a.instruction-link_download[download]` — посилання завантаження всередині картки
17. `.brand-select-dropdown_menu > li:nth-child(3)` — третій бренд у фільтрі (Ford)
18. `.model-select-dropdown_menu > li.dropdown-item:not(.-active)` — неактивні моделі фільтра
19. `.instructions-search-controls > button.btn-primary` — кнопка Search
20. `footer .footer_item.-right > a.footer_logo` — лого в футері
21. `footer a.contacts_link[href^="mailto:"]` — email-посилання футера
22. `footer a.socials_link[href*="facebook"]` — посилання на Facebook
23. `.user-nav_menu > a.dropdown-item[routerlink="/panel/instructions"]` — Instructions у меню користувача
24. `.sidebar > a.sidebar_btn.text-danger` — Log out в сайдбарі
25. `.modal-body .form-group + .form-group` — form-group модалки, що йде одразу за іншим (блоки Model і Mileage; сусідній елемент)
