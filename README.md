О проекте
Проект направлен на сбор данных о компаниях и вакансиях с hh.ru с последующим хранением в базе данных PostgreSQL. Для удобства работы с данными предоставлен класс DBManager, который обеспечивает простое взаимодействие с базой данных. Процесс включает в себя получение данных через API hh.ru, проектирование структуры базы данных, и загрузку данных в таблицы.

Как запустить проект

-Склонируйте проект с GitHub
-Установите все зависимости
-Используйте main.py

Использование
DBManager 
# Импорт класса
from db_manager import DBManager

# Создание экземпляра DBManager
db_manager = DBManager()

# Получение компаний и количества вакансий
companies_vacancies_count = db_manager.get_companies_and_vacancies_count()

# Получение всех вакансий
all_vacancies = db_manager.get_all_vacancies()

# Получение средней зарплаты
avg_salary = db_manager.get_avg_salary()

# Получение вакансий с зарплатой выше средней
higher_salary_vacancies = db_manager.get_vacancies_with_higher_salary()

# Получение вакансий с ключевым словом
python_vacancies = db_manager.get_vacancies_with_keyword("python")

# Замечания
Проект предоставляет удобный способ собирать и анализировать данные о вакансиях с hh.ru.
Рекомендуется использовать виртуальное окружение для управления зависимостями.
