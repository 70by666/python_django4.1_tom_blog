# Tom's Blog

## Короткое описание
Данный проект - простенький блог на Django, который позволяет пользователям просматривать статьи на разные темы. Доступна регистрация и авторизации(и связанный с этим функционал). Работа со статьями(добавлять, редактировать, удалять).

## Подробно
* Отображение последних и закрепленных статей на главной странице(есть возможность закреплять статьи)
* Отображение всех статей, отсортированные по дате создания на странице Blog
* Древовидные категории и сортировка по ним
* Возможность просмотра отдельной статьи
* Администрация может добавлять, редактировать и удалять любую статью
* Редакторы могут добавлять статьи и собственные статьи редактировать
* Простая система лайков на постах, поставить его может только авторизованный пользователь, без накрутки
* Простая система просмотров на постах, посмотреть могут, также как и с лайками, только авторизованные пользователи, без накрутки(через модель Ip)
* Регистрация и авторизация
* Отображение профиля, автарки и информация о пользователе
* При регистрации отправляется письмо на почту, для подтверждения, без этого нельзя авторизоваться
* При смене почты тоже самое
* Форма обратной связи, сообщение оттуда приходит мне в личные сообщения в телеграме
* Если в форме обратной связи были запрещенные фразы, IP банится
* Древовидные комментарии под постами
* Комментарии под профилем
* reCAPTCHA
* Поиск по постам
* sitemap.xml
* Статут пользователя: онлайн/не в сети
* Рассылка уведомлений о новых постах пользователям, которые подписались

## Зависимости

* Python 3.11.2
* Django 4.1.7
* PostgreSQL 14.7
* Redis server 6.0.16
* Celery 5.2.7
* Django-redis 5.2.0
* Django-environ 0.10.0
* Django-extensions 3.2.1
* Django-mptt 0.14.0
* Django_debug_toolbar 3.8.1
* Django-recaptcha 3.0.0
* Pillow 9.4.0
* Pytils 0.4.1
* Requests 2.28.2
* Psycopg2-binary 2.9.5

## Автор

70by666
