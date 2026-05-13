from database import SessionLocal
import models

SPECIALTIES = [
    "Computer Science",
    "Artificial Intelligence",
    "Engineering",
    "Medicine",
    "Business",
    "Economics",
    "Law",
    "Mathematics",
    "Physics",
    "Humanities",
    "Arts",
    "Architecture",
]

UNIVERSITIES = [
    {
        "name": "Massachusetts Institute of Technology",
        "country": "USA",
        "city": "Cambridge, MA",
        "description": (
            "MIT — один из ведущих мировых университетов в области науки, техники и технологий. "
            "Основан в 1861 году, является родиной многочисленных лауреатов Нобелевской премии "
            "и лидеров технологической индустрии. Расположен в Кембридже, штат Массачусетс."
        ),
        "website": "https://mit.edu",
        "ranking": 1,
        "founded_year": 1861,
        "tuition_min": 55000,
        "tuition_max": 60000,
        "students_count": 11574,
        "image_url": "https://images.unsplash.com/photo-1562774053-701939374585?w=800&q=80",
        "logo_url": None,
        "specialties": ["Computer Science", "Engineering", "Artificial Intelligence", "Physics", "Mathematics"],
    },
    {
        "name": "Stanford University",
        "country": "USA",
        "city": "Stanford, CA",
        "description": (
            "Стэнфордский университет — один из ведущих мировых исследовательских и учебных заведений. "
            "Расположен в Силиконовой долине, известен культурой предпринимательства "
            "и передовыми исследованиями в области ИИ, медицины и бизнеса."
        ),
        "website": "https://stanford.edu",
        "ranking": 2,
        "founded_year": 1885,
        "tuition_min": 57000,
        "tuition_max": 62000,
        "students_count": 17249,
        "image_url": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800&q=80",
        "logo_url": None,
        "specialties": ["Computer Science", "Business", "Artificial Intelligence", "Engineering", "Medicine"],
    },
    {
        "name": "University of Oxford",
        "country": "UK",
        "city": "Oxford",
        "description": (
            "Оксфордский университет — старейший англоязычный университет в мире, основан в 1096 году. "
            "Предлагает исключительное обучение и исследования в широком спектре дисциплин: "
            "от права и медицины до гуманитарных наук и физики."
        ),
        "website": "https://ox.ac.uk",
        "ranking": 3,
        "founded_year": 1096,
        "tuition_min": 30000,
        "tuition_max": 40000,
        "students_count": 24000,
        "image_url": "https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=800&q=80",
        "logo_url": None,
        "specialties": ["Law", "Medicine", "Humanities", "Economics", "Physics"],
    },
    {
        "name": "University of Cambridge",
        "country": "UK",
        "city": "Cambridge",
        "description": (
            "Кембриджский университет — один из старейших в мире, основан в 1209 году. "
            "800-летняя традиция академического превосходства. Включает 31 колледж "
            "и более 150 факультетов. Среди выпускников — 121 лауреат Нобелевской премии."
        ),
        "website": "https://cam.ac.uk",
        "ranking": 4,
        "founded_year": 1209,
        "tuition_min": 28000,
        "tuition_max": 38000,
        "students_count": 23000,
        "image_url": "https://images.unsplash.com/photo-1526129318478-62ed807ebdf9?w=800&q=80",
        "logo_url": None,
        "specialties": ["Mathematics", "Physics", "Computer Science", "Engineering", "Medicine", "Humanities"],
    },
    {
        "name": "ETH Zurich",
        "country": "Switzerland",
        "city": "Zurich",
        "description": (
            "ETH Zurich — один из ведущих мировых университетов в области науки и технологий. "
            "Основан в 1855 году, специализируется на точных науках и инженерии. "
            "21 выпускник — лауреат Нобелевской премии. Обучение доступное по стоимости."
        ),
        "website": "https://ethz.ch",
        "ranking": 7,
        "founded_year": 1855,
        "tuition_min": 1500,
        "tuition_max": 3000,
        "students_count": 22200,
        "image_url": "https://images.unsplash.com/photo-1573455494060-c5595004fb6c?w=800&q=80",
        "logo_url": None,
        "specialties": ["Engineering", "Computer Science", "Mathematics", "Physics", "Architecture"],
    },
    {
        "name": "National University of Singapore",
        "country": "Singapore",
        "city": "Singapore",
        "description": (
            "NUS — ведущий университет Азии, стабильно входящий в топ-15 мирового рейтинга. "
            "Предлагает широкий спектр программ в области бизнеса, инженерии, медицины "
            "и компьютерных наук. Сильные связи с азиатским рынком труда."
        ),
        "website": "https://nus.edu.sg",
        "ranking": 8,
        "founded_year": 1905,
        "tuition_min": 15000,
        "tuition_max": 25000,
        "students_count": 38000,
        "image_url": "https://images.unsplash.com/photo-1525625293386-3f8f99389edd?w=800&q=80",
        "logo_url": None,
        "specialties": ["Business", "Engineering", "Computer Science", "Medicine", "Law"],
    },
    {
        "name": "University of Toronto",
        "country": "Canada",
        "city": "Toronto",
        "description": (
            "Университет Торонто — ведущий университет Канады и один из лучших в мире (топ-20). "
            "Известен прорывными исследованиями в медицине, инженерии и ИИ — "
            "именно здесь зародился глубокое обучение. Крупнейший университет Северной Америки."
        ),
        "website": "https://utoronto.ca",
        "ranking": 18,
        "founded_year": 1827,
        "tuition_min": 25000,
        "tuition_max": 45000,
        "students_count": 93000,
        "image_url": "https://images.unsplash.com/photo-1576495199011-eb94736d05d6?w=800&q=80",
        "logo_url": None,
        "specialties": ["Medicine", "Engineering", "Computer Science", "Business", "Artificial Intelligence", "Arts"],
    },
    {
        "name": "Peking University",
        "country": "China",
        "city": "Beijing",
        "description": (
            "Пекинский университет — самый престижный университет Китая, основан в 1898 году. "
            "Комплексный исследовательский университет, охватывающий естественные науки, "
            "инженерию, гуманитарные и общественные науки. Символ китайской академической традиции."
        ),
        "website": "https://pku.edu.cn",
        "ranking": 14,
        "founded_year": 1898,
        "tuition_min": 4000,
        "tuition_max": 10000,
        "students_count": 40000,
        "image_url": "https://images.unsplash.com/photo-1547981609-4b6bfe67ca0b?w=800&q=80",
        "logo_url": None,
        "specialties": ["Computer Science", "Engineering", "Mathematics", "Economics", "Humanities"],
    },
    {
        "name": "University of Melbourne",
        "country": "Australia",
        "city": "Melbourne",
        "description": (
            "Мельбурнский университет — ведущий исследовательский университет Австралии, "
            "входит в топ-35 мировых рейтингов. Известен высоким качеством обучения, "
            "сильными программами по медицине, бизнесу и праву."
        ),
        "website": "https://unimelb.edu.au",
        "ranking": 33,
        "founded_year": 1853,
        "tuition_min": 30000,
        "tuition_max": 42000,
        "students_count": 54000,
        "image_url": "https://images.unsplash.com/photo-1523482580672-f109ba8cb9be?w=800&q=80",
        "logo_url": None,
        "specialties": ["Business", "Medicine", "Arts", "Engineering", "Law"],
    },
    {
        "name": "Technical University of Munich",
        "country": "Germany",
        "city": "Munich",
        "description": (
            "ТУ Мюнхен — ведущий технический университет Германии и один из лучших в Европе. "
            "Основан в 1868 году, отличается тесными связями с промышленностью, "
            "сильными программами по инженерии и компьютерным наукам. Обучение практически бесплатное."
        ),
        "website": "https://tum.de",
        "ranking": 37,
        "founded_year": 1868,
        "tuition_min": 0,
        "tuition_max": 2000,
        "students_count": 45000,
        "image_url": "https://images.unsplash.com/photo-1485081669829-bacb8c7bb1f3?w=800&q=80",
        "logo_url": None,
        "specialties": ["Engineering", "Computer Science", "Mathematics", "Business", "Physics"],
    },
    {
        "name": "Sorbonne University",
        "country": "France",
        "city": "Paris",
        "description": (
            "Сорбонна — один из старейших и наиболее престижных университетов мира, "
            "основан в 1257 году. Исторически сильна в гуманитарных науках, искусстве, медицине. "
            "Расположена в сердце Парижа, обучение доступное по цене."
        ),
        "website": "https://sorbonne-universite.fr",
        "ranking": 59,
        "founded_year": 1257,
        "tuition_min": 3000,
        "tuition_max": 10000,
        "students_count": 55000,
        "image_url": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=800&q=80",
        "logo_url": None,
        "specialties": ["Humanities", "Arts", "Medicine", "Law", "Mathematics", "Physics"],
    },
    {
        "name": "University of Tokyo",
        "country": "Japan",
        "city": "Tokyo",
        "description": (
            "Токийский университет — самый престижный университет Японии. "
            "Комплексный исследовательский университет с высоким уровнем преподавания "
            "во всех академических дисциплинах. Является центром японской науки и культуры."
        ),
        "website": "https://u-tokyo.ac.jp",
        "ranking": 28,
        "founded_year": 1877,
        "tuition_min": 5000,
        "tuition_max": 8000,
        "students_count": 28000,
        "image_url": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=800&q=80",
        "logo_url": None,
        "specialties": ["Engineering", "Medicine", "Computer Science", "Economics", "Humanities"],
    },
    {
        "name": "Lomonosov Moscow State University",
        "country": "Russia",
        "city": "Moscow",
        "description": (
            "МГУ — крупнейший и наиболее престижный университет России, основан в 1755 году. "
            "Силён в фундаментальных науках, математике и гуманитарных исследованиях. "
            "Главный корпус — архитектурный символ Москвы."
        ),
        "website": "https://msu.ru",
        "ranking": 87,
        "founded_year": 1755,
        "tuition_min": 3000,
        "tuition_max": 8000,
        "students_count": 47000,
        "image_url": "https://images.unsplash.com/photo-1513326738677-b964603b136d?w=800&q=80",
        "logo_url": None,
        "specialties": ["Mathematics", "Physics", "Humanities", "Law", "Economics", "Computer Science"],
    },
    {
        "name": "HSE University",
        "country": "Russia",
        "city": "Moscow",
        "description": (
            "ВШЭ — один из ведущих исследовательских университетов России, "
            "специализирующийся в экономике, социальных науках и компьютерных науках. "
            "Известен инновационными методами обучения и сильной интеграцией с бизнес-средой."
        ),
        "website": "https://hse.ru",
        "ranking": 301,
        "founded_year": 1992,
        "tuition_min": 4000,
        "tuition_max": 10000,
        "students_count": 43000,
        "image_url": "https://images.unsplash.com/photo-1497366216548-37526070297c?w=800&q=80",
        "logo_url": None,
        "specialties": ["Economics", "Computer Science", "Business", "Law", "Mathematics"],
    },
    {
        "name": "ITMO University",
        "country": "Russia",
        "city": "Saint Petersburg",
        "description": (
            "ИТМО — ведущий российский университет в области информационных технологий и оптики. "
            "Многократный победитель чемпионата мира по программированию ACM ICPC. "
            "Входит в топ-5 лучших IT-университетов мира по версии различных рейтингов."
        ),
        "website": "https://itmo.ru",
        "ranking": 401,
        "founded_year": 1900,
        "tuition_min": 3000,
        "tuition_max": 7000,
        "students_count": 16000,
        "image_url": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&q=80",
        "logo_url": None,
        "specialties": ["Computer Science", "Artificial Intelligence", "Engineering", "Mathematics", "Physics"],
    },
]


ADMISSIONS = {
    "Massachusetts Institute of Technology": {
        "description": (
            "Поступление крайне конкурентно (процент зачисления ~4%). Необходимы выдающиеся "
            "академические результаты, исследовательский опыт и сильные рекомендательные письма. "
            "Оценивается интеллектуальная любознательность и вклад в сообщество."
        ),
        "min_gpa": 3.9,
        "language_requirement": "TOEFL iBT 90+ или IELTS 7.0+ для не носителей английского языка",
        "exams": [
            {"exam_name": "SAT", "min_score": "1500", "max_score": "1600", "notes": "или ACT 34+"},
            {"exam_name": "TOEFL iBT", "min_score": "90", "max_score": "120", "notes": "обязателен для не носителей английского"},
            {"exam_name": "IELTS", "min_score": "7.0", "max_score": "9.0", "notes": "альтернатива TOEFL"},
            {"exam_name": "GRE", "min_score": "160", "max_score": "170", "notes": "для магистратуры (Quantitative)"},
        ],
    },
    "Stanford University": {
        "description": (
            "Стэнфорд отбирает студентов с выдающимися интеллектуальными качествами и доказанным "
            "влиянием в своей области. Процент зачисления ~3.7%. Высоко ценятся личные качества, "
            "лидерство и оригинальность мышления."
        ),
        "min_gpa": 3.9,
        "language_requirement": "TOEFL iBT 100+ или IELTS 7.0+",
        "exams": [
            {"exam_name": "SAT", "min_score": "1500", "max_score": "1600", "notes": "или ACT 34+"},
            {"exam_name": "TOEFL iBT", "min_score": "100", "max_score": "120"},
            {"exam_name": "IELTS", "min_score": "7.0", "max_score": "9.0"},
            {"exam_name": "GRE / GMAT", "min_score": "163", "max_score": "170", "notes": "для магистерских программ"},
        ],
    },
    "University of Oxford": {
        "description": (
            "Оксфорд требует блестящих академических результатов и проводит вступительные тесты "
            "по специальности. Почти все финалисты проходят собеседование с тьюторами. "
            "Ожидаются оценки A*AA на A-Levels или эквивалент."
        ),
        "min_gpa": 3.7,
        "language_requirement": "IELTS 7.0 (мин. 6.5 по каждому компоненту) или TOEFL iBT 110+",
        "exams": [
            {"exam_name": "A-Levels", "min_score": "A*AA", "max_score": None, "notes": "или IB 38–40 баллов"},
            {"exam_name": "IELTS", "min_score": "7.0", "max_score": "9.0", "notes": "мин. 6.5 по каждому компоненту"},
            {"exam_name": "TOEFL iBT", "min_score": "110", "max_score": "120"},
            {"exam_name": "Предметный тест (LNAT/PAT/MAT)", "min_score": None, "max_score": None, "notes": "обязателен — зависит от специальности"},
        ],
    },
    "University of Cambridge": {
        "description": (
            "Кембридж ожидает исключительных академических успехов (A*A*A на A-Levels). "
            "Почти все серьёзные кандидаты проходят собеседование. "
            "Предметные вступительные тесты обязательны для большинства специальностей."
        ),
        "min_gpa": 3.8,
        "language_requirement": "IELTS 7.5 (мин. 7.0 по каждому компоненту) или TOEFL iBT 110+",
        "exams": [
            {"exam_name": "A-Levels", "min_score": "A*A*A", "max_score": None, "notes": "или IB 40–42 балла"},
            {"exam_name": "IELTS", "min_score": "7.5", "max_score": "9.0", "notes": "мин. 7.0 по каждому компоненту"},
            {"exam_name": "TOEFL iBT", "min_score": "110", "max_score": "120"},
            {"exam_name": "STEP (математика)", "min_score": "Grade 1", "max_score": None, "notes": "обязателен для технических специальностей"},
        ],
    },
    "ETH Zurich": {
        "description": (
            "ETH Zurich строго отбирает студентов по академическим результатам. "
            "Бакалавриат ведётся на немецком языке, магистратура — преимущественно на английском. "
            "Первый год обучения является отборочным и очень интенсивным."
        ),
        "min_gpa": 3.5,
        "language_requirement": "Немецкий C1 (бакалавриат) или IELTS 7.0 / TOEFL 100 (магистратура)",
        "exams": [
            {"exam_name": "Аттестат зрелости / Matura", "min_score": "5.0/6.0", "max_score": "6.0", "notes": "или A-Levels AA, IB 37+"},
            {"exam_name": "TestDaF / Goethe C1", "min_score": "C1", "max_score": None, "notes": "для программ на немецком языке"},
            {"exam_name": "IELTS", "min_score": "7.0", "max_score": "9.0", "notes": "для английских магистерских программ"},
            {"exam_name": "TOEFL iBT", "min_score": "100", "max_score": "120", "notes": "альтернатива IELTS"},
        ],
    },
    "National University of Singapore": {
        "description": (
            "NUS принимает студентов с сильными академическими результатами и ценит "
            "лидерский опыт и внеучебные достижения. Конкурс высокий — около 5% зачисления."
        ),
        "min_gpa": 3.5,
        "language_requirement": "IELTS 6.0+ или TOEFL iBT 85+",
        "exams": [
            {"exam_name": "SAT", "min_score": "1400", "max_score": "1600", "notes": "или A-Levels AAB"},
            {"exam_name": "IELTS", "min_score": "6.0", "max_score": "9.0"},
            {"exam_name": "TOEFL iBT", "min_score": "85", "max_score": "120"},
            {"exam_name": "GRE / GMAT", "min_score": None, "max_score": None, "notes": "для некоторых магистерских программ"},
        ],
    },
    "University of Toronto": {
        "description": (
            "UofT оценивает академические достижения, мотивационное письмо и внеучебную "
            "деятельность. Требования различаются по факультетам. Многие программы включают "
            "интервью или портфолио."
        ),
        "min_gpa": 3.6,
        "language_requirement": "IELTS 6.5+ или TOEFL iBT 100+",
        "exams": [
            {"exam_name": "IELTS", "min_score": "6.5", "max_score": "9.0"},
            {"exam_name": "TOEFL iBT", "min_score": "100", "max_score": "120"},
            {"exam_name": "GRE", "min_score": "155", "max_score": "170", "notes": "для ряда магистерских программ"},
        ],
    },
    "Peking University": {
        "description": (
            "Для иностранных студентов предлагаются программы на английском и китайском языках. "
            "Необходимо предоставить мотивационное письмо, два рекомендательных письма и "
            "академические транскрипты. Требуется прохождение собеседования."
        ),
        "min_gpa": 3.5,
        "language_requirement": "HSK 5 (для китайских программ) или IELTS 6.5 / TOEFL 90 (английские)",
        "exams": [
            {"exam_name": "HSK", "min_score": "5", "max_score": "6", "notes": "уровень 5 для обучения на китайском"},
            {"exam_name": "IELTS", "min_score": "6.5", "max_score": "9.0", "notes": "для англоязычных программ"},
            {"exam_name": "TOEFL iBT", "min_score": "90", "max_score": "120", "notes": "альтернатива IELTS"},
        ],
    },
    "University of Melbourne": {
        "description": (
            "Мельбурнский университет отбирает студентов на основе ATAR для австралийцев "
            "и академических результатов для иностранцев. Некоторые программы требуют "
            "портфолио или дополнительного тестирования."
        ),
        "min_gpa": 3.5,
        "language_requirement": "IELTS 6.5 (мин. 6.0 по каждому компоненту) или TOEFL iBT 79+",
        "exams": [
            {"exam_name": "IELTS", "min_score": "6.5", "max_score": "9.0", "notes": "мин. 6.0 по каждому компоненту"},
            {"exam_name": "TOEFL iBT", "min_score": "79", "max_score": "120"},
            {"exam_name": "ATAR", "min_score": "90", "max_score": "99.95", "notes": "для абитуриентов из Австралии"},
        ],
    },
    "Technical University of Munich": {
        "description": (
            "TU Munich предъявляет высокие требования к академической успеваемости. "
            "Большинство магистерских программ — на английском языке и бесплатны. "
            "Конкурсные программы включают aptitude assessment."
        ),
        "min_gpa": 3.0,
        "language_requirement": "IELTS 6.5 / TOEFL 88 (английские) или TestDaF 4×4 / DSH-2 (немецкие)",
        "exams": [
            {"exam_name": "IELTS", "min_score": "6.5", "max_score": "9.0", "notes": "для англоязычных программ"},
            {"exam_name": "TOEFL iBT", "min_score": "88", "max_score": "120", "notes": "альтернатива IELTS"},
            {"exam_name": "TestDaF", "min_score": "4×4", "max_score": None, "notes": "или DSH-2 для немецких программ"},
            {"exam_name": "GRE / GMAT", "min_score": None, "max_score": None, "notes": "рекомендуется для ряда программ"},
        ],
    },
    "Sorbonne University": {
        "description": (
            "Сорбонна принимает на основе досье кандидата и мотивационного письма. "
            "Для большинства программ обязательно знание французского. "
            "Число англоязычных программ постоянно растёт."
        ),
        "min_gpa": 3.0,
        "language_requirement": "DALF C1 или DELF B2 (французские программы); IELTS 6.5 (английские)",
        "exams": [
            {"exam_name": "DELF / DALF", "min_score": "B2", "max_score": None, "notes": "обязателен для программ на французском"},
            {"exam_name": "TCF / TEF", "min_score": "B2", "max_score": None, "notes": "альтернатива DELF/DALF"},
            {"exam_name": "IELTS", "min_score": "6.5", "max_score": "9.0", "notes": "для программ на английском"},
        ],
    },
    "University of Tokyo": {
        "description": (
            "Университет Токио проводит собственные вступительные экзамены. "
            "Для иностранных студентов действуют отдельные англоязычные программы (PEAK, G30), "
            "не требующие знания японского языка."
        ),
        "min_gpa": 3.7,
        "language_requirement": "JLPT N1 (японские программы) или IELTS 6.5 (PEAK/G30)",
        "exams": [
            {"exam_name": "EJU", "min_score": None, "max_score": None, "notes": "Examination for Japanese University Admission (японские программы)"},
            {"exam_name": "JLPT", "min_score": "N1", "max_score": None, "notes": "уровень N1 для обучения на японском"},
            {"exam_name": "IELTS", "min_score": "6.5", "max_score": "9.0", "notes": "для программ PEAK / G30 на английском"},
            {"exam_name": "TOEFL iBT", "min_score": "79", "max_score": "120", "notes": "альтернатива IELTS"},
        ],
    },
    "Lomonosov Moscow State University": {
        "description": (
            "МГУ принимает по результатам ЕГЭ для российских граждан. Иностранные "
            "абитуриенты сдают внутренние вступительные испытания. Необходимо знание "
            "русского языка на уровне не ниже B2."
        ),
        "min_gpa": 3.5,
        "language_requirement": "Русский язык обязателен — ТРКИ B2 для иностранных студентов",
        "exams": [
            {"exam_name": "ЕГЭ (Математика)", "min_score": "80", "max_score": "100", "notes": "профильный уровень, для российских граждан"},
            {"exam_name": "ЕГЭ (Русский язык)", "min_score": "70", "max_score": "100", "notes": "для российских граждан"},
            {"exam_name": "ТРКИ / TORFL", "min_score": "B2", "max_score": None, "notes": "для иностранных студентов"},
            {"exam_name": "Внутренний экзамен МГУ", "min_score": None, "max_score": None, "notes": "для отдельных факультетов"},
        ],
    },
    "HSE University": {
        "description": (
            "ВШЭ принимает по ЕГЭ и результатам олимпиад для граждан России. "
            "Для иностранцев — внутренние экзамены. Многие программы ведутся на английском, "
            "для них достаточно IELTS 6.0."
        ),
        "min_gpa": 3.3,
        "language_requirement": "ТРКИ B1 (мин.) для иностранцев или IELTS 6.0 для англоязычных программ",
        "exams": [
            {"exam_name": "ЕГЭ (профильный предмет)", "min_score": "75", "max_score": "100", "notes": "зависит от программы"},
            {"exam_name": "ЕГЭ (Математика)", "min_score": "70", "max_score": "100"},
            {"exam_name": "IELTS", "min_score": "6.0", "max_score": "9.0", "notes": "для англоязычных программ"},
            {"exam_name": "ТРКИ / TORFL", "min_score": "B1", "max_score": None, "notes": "для иностранных студентов"},
        ],
    },
    "ITMO University": {
        "description": (
            "ИТМО высоко ценит победителей олимпиад по программированию и математике — "
            "они могут поступить без экзаменов. Принимает по ЕГЭ, результатам ICPC и другим "
            "олимпиадам. Активно развивает международные англоязычные программы."
        ),
        "min_gpa": 3.5,
        "language_requirement": "ТРКИ B1 для иностранцев; IELTS 6.0 для англоязычных программ",
        "exams": [
            {"exam_name": "ЕГЭ (Математика)", "min_score": "85", "max_score": "100", "notes": "профильный уровень"},
            {"exam_name": "ЕГЭ (Информатика)", "min_score": "80", "max_score": "100", "notes": "для IT-направлений"},
            {"exam_name": "Олимпиада ICPC / Всерос", "min_score": None, "max_score": None, "notes": "победители и призёры — льготное зачисление"},
            {"exam_name": "IELTS", "min_score": "6.0", "max_score": "9.0", "notes": "для англоязычных программ"},
        ],
    },
}


def seed(db=None):
    close = False
    if db is None:
        db = SessionLocal()
        close = True
    try:
        # --- Universities + Specialties ---
        if db.query(models.University).count() == 0:
            specialty_map: dict[str, models.Specialty] = {}
            for name in SPECIALTIES:
                spec = models.Specialty(name=name)
                db.add(spec)
                db.flush()
                specialty_map[name] = spec

            for data in UNIVERSITIES:
                spec_names = data.pop("specialties")
                uni = models.University(**data)
                for sn in spec_names:
                    if sn in specialty_map:
                        uni.specialties.append(specialty_map[sn])
                db.add(uni)

            db.commit()
            print(f"Seeded {len(UNIVERSITIES)} universities.")

        # --- Admission requirements (idempotent) ---
        if db.query(models.AdmissionRequirement).count() == 0:
            all_unis = db.query(models.University).all()
            for uni in all_unis:
                adm_data = ADMISSIONS.get(uni.name)
                if not adm_data:
                    continue
                exam_list = adm_data.get("exams", [])
                req = models.AdmissionRequirement(
                    university_id=uni.id,
                    description=adm_data.get("description"),
                    min_gpa=adm_data.get("min_gpa"),
                    language_requirement=adm_data.get("language_requirement"),
                )
                db.add(req)
                db.flush()
                for ex in exam_list:
                    db.add(models.AdmissionExam(requirement_id=req.id, **ex))

            db.commit()
            print(f"Seeded admission requirements for {db.query(models.AdmissionRequirement).count()} universities.")
    except Exception as exc:
        db.rollback()
        print(f"Seed error: {exc}")
        raise
    finally:
        if close:
            db.close()


if __name__ == "__main__":
    seed()
