# Пакет продавца · Зарплатный проект Сбера

Внутренний материал для продающих ролей. Актуально на 21.10.2026.

- `index.html` — лендинг: главная с двумя колонками (компания / сотрудник) и 20 разворотов с диплинками.
- `paket-prodavca-zp.pdf` — саммари на 3 страницы A4: компания, сотрудник, единый раздел на сайте банка (ссылка и QR-код).
- `qr-privilegii.png`, `qr-privilegii.svg` — QR-код на раздел https://www.sberbank.ru/ru/person/privilegii-dlya-zarplatnikov#perevod_zp

## Публикация на GitHub Pages
1. Создайте репозиторий и загрузите оба файла в корень.
2. Settings → Pages → Source: *Deploy from a branch*, ветка `main`, папка `/ (root)`.
3. Через минуту сайт откроется по адресу `https://<аккаунт>.github.io/<репозиторий>/`.

## Диплинки
Каждый раздел открывается по ссылке вида `…/index.html#emp-cashback`.
Компании: `biz-money`, `biz-sberbusiness`, `biz-cards`, `biz-anybank`, `biz-gig`, `biz-hr`, `biz-launch`.
Сотрудникам: `emp-card`, `emp-security`, `emp-cashback`, `emp-credit`, `emp-savings`, `emp-mobile`, `emp-partners`, `emp-promo`, `emp-supreme`, `emp-premium`, `emp-switch`.
Прочее: `bank-site` (блок со ссылкой и QR на главной), `objections`, `sources`.

Важно: в материале есть внутренние пилоты (МБ, СРБ, СЗБ). Если репозиторий публичный, страницу увидит любой — для внутренних данных лучше приватный репозиторий или корпоративный хостинг.
