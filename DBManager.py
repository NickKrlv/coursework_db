import psycopg2


class DBManager:
    """
    Класс для работы с базой данных
    """

    def __init__(self):
        self.db_name = 'coursework_db'
        self.db_user = 'postgres'
        self.db_password = '5r36d6ft'
        self.db_host = '127.0.0.1'
        self.db_port = '5432'
        self.conn = None
        self.cur = None

    def connect(self):
        self.conn = psycopg2.connect(
            dbname=self.db_name,
            user=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port
        )
        self.cur = self.conn.cursor()

    def disconnect(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

    def get_companies_and_vacancies_count(self):
        """Получение данных о компаниях и количестве вакансий"""
        if not self.cur:
            self.connect()
        self.cur.execute('SELECT company_name, open_vacancies FROM employers')
        rows = self.cur.fetchall()
        self.conn.commit()
        return rows

    def get_all_vacancies(self):
        """Получение всех вакансий"""
        if not self.cur:
            self.connect()
        self.cur.execute('SELECT * FROM vacancies')
        rows = self.cur.fetchall()
        self.conn.commit()
        return rows

    def get_avg_salary(self):
        """Получение средней заработной платы"""

        if not self.cur:
            self.connect()
        self.cur.execute('SELECT ROUND(AVG(payment), 2) FROM vacancies WHERE payment IS NOT NULL')
        rows = self.cur.fetchall()

        self.conn.commit()
        return f"Средняя заработная плата среди вакансий, в которых указана зарплата: {rows[0][0]} руб."

    def get_vacancies_with_higher_salary(self):
        """Получение вакансий с окладом выше среднего"""

        if not self.cur:
            self.connect()
        self.cur.execute('SELECT * FROM vacancies WHERE payment > (SELECT AVG(payment) FROM vacancies)')
        rows = self.cur.fetchall()

        self.conn.commit()
        return f"Вакансии с окладом выше среднего: {rows}"

    def get_vacancies_with_keyword(self, keyword):
        """Получение вакансий по ключевому слову"""

        if not self.cur:
            self.connect()
        self.cur.execute(f"SELECT * FROM vacancies WHERE vacancies_name LIKE '%{keyword}%'")
        rows = self.cur.fetchall()

        if not rows:
            return f"Вакансии по ключевому слову '{keyword}': нет"

        self.conn.commit()
        return f"Вакансии по ключевому слову '{keyword}': {rows}"
