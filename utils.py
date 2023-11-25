import psycopg2
import requests
from pprint import pprint


def get_vacancies(employer_id):
    """Получение данных вакансий по API"""

    params = {
        'area': 1,
        'page': 0,
        'per_page': 10
    }
    url = f"https://api.hh.ru/vacancies?employer_id={employer_id}"
    data_vacancies = requests.get(url, params=params).json()

    vacancies_data = []
    for item in data_vacancies["items"]:
        hh_vacancies = {
            'vacancy_id': int(item['id']),
            'vacancies_name': item['name'],
            'payment': item["salary"]["from"] if item["salary"] else None,
            'requirement': item['snippet']['requirement'],
            'vacancies_url': item['alternate_url'],
            'employer_id': employer_id
        }
        vacancies_data.append(hh_vacancies)

        return vacancies_data


def get_employer(employer_id):
    """Получение данных о работодателей по API"""

    url = f"https://api.hh.ru/employers/{employer_id}"
    data_vacancies = requests.get(url).json()
    hh_company = {
        "employer_id": int(employer_id),
        "company_name": data_vacancies['name'],
        "open_vacancies": data_vacancies['open_vacancies']
    }

    return hh_company


def create_tables():
    """Создание таблиц"""

    conn = psycopg2.connect(host="localhost", database="coursework_db",
                            user="postgres", password="5r36d6ft")

    with conn.cursor() as cur:
        cur.execute('DROP TABLE IF EXISTS vacancies, employers CASCADE;')

    conn.commit()

    with conn.cursor() as cur:
        cur.execute("""
                    CREATE TABLE employers (
                    employer_id INTEGER PRIMARY KEY,
                    company_name varchar(255),
                    open_vacancies INTEGER
                    )""")

        cur.execute("""
                    CREATE TABLE vacancies (
                    vacancy_id SERIAL PRIMARY KEY,
                    vacancies_name varchar(255),
                    payment INTEGER,
                    requirement TEXT,
                    vacancies_url TEXT,
                    employer_id INTEGER REFERENCES employers(employer_id)
                    )""")
    conn.commit()
    conn.close()


def add_to_table(employers_list):
    """Добавление данных в таблицу"""

    conn = psycopg2.connect(database="coursework_db",
                            user="postgres",
                            password="5r36d6ft",
                            host="127.0.0.1",
                            port="5432")

    conn.autocommit = True

    with conn.cursor() as cur:
        cur.execute('TRUNCATE TABLE employers, vacancies RESTART IDENTITY;')

        for employer in employers_list:
            employer_list = get_employer(employer)
            cur.execute('INSERT INTO employers (employer_id, company_name, open_vacancies) '
                        'VALUES (%s, %s, %s) RETURNING employer_id',
                        (employer_list['employer_id'], employer_list['company_name'],
                         employer_list['open_vacancies']))

        for employer in employers_list:
            vacancy_list = get_vacancies(employer)
            for v in vacancy_list:
                cur.execute('INSERT INTO vacancies (vacancy_id, vacancies_name, '
                            'payment, requirement, vacancies_url, employer_id) '
                            'VALUES (%s, %s, %s, %s, %s, %s)',
                            (v['vacancy_id'], v['vacancies_name'], v['payment'],
                             v['requirement'], v['vacancies_url'], v['employer_id']))

    conn.commit()
    conn.close()

add_to_table([1740, 15478, 8620, 3529, 78638, 4006, 4504679, 561525, 64174, 8642172])