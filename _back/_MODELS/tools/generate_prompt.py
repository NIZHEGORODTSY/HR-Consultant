def build_user_context_from_json(user_data: dict, analysis_results: dict, username: str, is_first_message: bool = False,
                                 message_history: list = []) -> dict:
    """
    Формирует контекст для промпта из полученного JSON
    """
    educations = user_data.get('educations', {})
    additional_educations = user_data.get('additional_educations', {})
    roles = user_data.get('roles', {})
    skills = user_data.get('skills', {})
    additional_info = user_data.get('additional_info', {})
    career_prefs = user_data.get('career_preferences', {})

    education_list = []
    for edu_id, edu in educations.items():
        edu_str = f"{edu.get('university', '')}, {edu.get('level', '')}, {edu.get('spec', '')}, {edu.get('grad_year', '')}"
        education_list.append(edu_str)

    add_edu_list = []
    for add_edu_id, add_edu in additional_educations.items():
        add_edu_str = f"{add_edu.get('name', '')} ({add_edu.get('company', '')}, {add_edu.get('issued', '')})"
        add_edu_list.append(add_edu_str)

    current_role = None
    all_roles = []
    for role_id, role in roles.items():
        role_str = f"{role.get('role', '')} ({role.get('start_date', '')} - {role.get('end_date', 'по настоящее время')})"
        all_roles.append(role_str)
        if role.get('end_date') is None:
            current_role = role

    skills_list = []
    for skill_id, skill_desc in skills.items():
        skills_list.append(skill_desc)

    languages = additional_info.get('languages', [])
    projects = additional_info.get('projects', [])

    languages_str = ", ".join([f"{lang.get('language', '')} ({lang.get('level', '')})" for lang in languages])
    projects_str = "; ".join([f"{proj.get('name', '')}: {proj.get('description', '')}" for proj in projects])

    desired_position = career_prefs.get('desired_position', 'Не указана')
    preferred_tech = ", ".join(career_prefs.get('preferred_technologies', []))
    work_format = career_prefs.get('work_format', 'Не указан')
    expected_salary = career_prefs.get('expected_salary', 'Не указана')

    context = {
        "user_full_name": username,

        "user_skills": "; ".join(skills_list)[:500] + "..." if len(skills_list) > 0 else "Не указаны",
        "current_role": current_role.get('role', 'Не указана') if current_role else "Не указана",
        "current_experience": calculate_experience(current_role.get('start_date')) if current_role else "0",
        "func_role": ", ".join(all_roles) if len(all_roles) > 0 else "Не указано",  # Можно вывести из анализа роли
        "team_role": "Individual Contributor",  # Можно вывести из анализа роли
        "functionality": "Backend Development, System Architecture",  # Можно вывести из анализа навыков

        "university": education_list[0].split(',')[0] if education_list else "Не указано",
        "level": ", ".join([edu.split(',')[1].strip() for edu in education_list]) if education_list else "",
        "speciality": ", ".join([edu.split(',')[2].strip() for edu in education_list]) if education_list else "",
        "graduation_year": ", ".join([edu.split(',')[3].strip() for edu in education_list]) if education_list else "",
        "additional_educations": "; ".join(add_edu_list) if add_edu_list else "Нет дополнительного образования",
        "blob_diploma_info": "Есть дипломы и сертификаты" if education_list or add_edu_list else "Нет документов об образовании",

        "career_preferences": f"Целевая должность: {desired_position}. Предпочитаемые технологии: {preferred_tech}. Формат работы: {work_format}. Ожидаемая зарплата: {expected_salary} руб.",
        "additional_info": f"Языки: {languages_str}. Проекты: {projects_str}" if languages_str or projects_str else "Дополнительная информация не указана",

        "recommended_roles": analysis_results.get('recommended_roles', ""),
        "skills_gap": analysis_results.get('skills_gap', ""),
        "recommended_courses": analysis_results.get('recommended_courses', ""),
        "mobility_score": analysis_results.get('mobility_score', ""),
        "last_activities": analysis_results.get('last_activities', ""),

        "is_first_message": str(is_first_message),
        "message_history": message_history or "История диалога отсутствует"
    }

    return context


def calculate_experience(start_date: str) -> str:
    """
    Вычисляет опыт работы в годах на основе даты начала
    """
    if not start_date:
        return "0"

    try:
        from datetime import datetime
        start = datetime.strptime(start_date, '%Y-%m-%d')
        now = datetime.now()
        experience_years = (now - start).days / 365.25
        return f"{experience_years:.1f}"
    except:
        return "Не указан"


def get_final_prompt(username: str, is_first_message: bool, message_history: list = []):
    user_json = {
        "educations": {
            "1": {
                "user_id": 1,
                "university": "Санкт-Петербургский политехнический университет Петра Великого",
                "level": "Бакалавр",
                "spec": "Программная инженерия",
                "grad_year": 2018,
                "diploma": "диплом_ИТ_2018.pdf"
            },
            "2": {
                "user_id": 1,
                "university": "НИУ ВШЭ",
                "level": "Магистр",
                "spec": "Анализ данных и искусственный интеллект",
                "grad_year": 2020,
                "diploma": "диплом_магистра_2020.pdf"
            }
        },
        "additional_educations": {
            "1": {
                "user_id": 1,
                "name": "AWS Certified Solutions Architect",
                "company": "Amazon Web Services",
                "issued": "2021-06-15",
                "hours_amount": 40,
                "diploma": "aws_certificate_2021.pdf"
            },
            "2": {
                "user_id": 1,
                "name": "Курс по машинному обучению",
                "company": "Coursera",
                "issued": "2022-03-10",
                "hours_amount": 60,
                "diploma": "ml_course_certificate.pdf"
            }
        },
        "roles": {
            "1": {
                "user_id": 1,
                "role": "Senior Backend Developer",
                "start_date": "2021-04-01",
                "end_date": 'null'
            },
            "2": {
                "user_id": 1,
                "role": "Middle Python Developer",
                "start_date": "2020-01-15",
                "end_date": "2021-03-31"
            }
        },
        "skills": {
            "1": "Глубокое знание языка Python, включая асинхронное программирование, декораторы, контекстные менеджеры. Опыт разработки высоконагруженных приложений с использованием asyncio и aiohttp. Знание современных практик кодирования и паттернов проектирования.",
            "2": "Опыт разработки полного цикла на Django и Django REST Framework. Создание REST API, работа с ORM, миграциями, аутентификацией и авторизацией. Оптимизация производительности запросов к базе данных и кэширование с помощью Redis.",
            "3": "Проектирование и оптимизация сложных схем баз данных. Написание эффективных SQL-запросов, использование индексов, представлений, хранимых процедур и триггеров. Опыт работы с репликацией и обеспечением целостности данных.",
            "4": "Создание и настройка Docker-контейнеров для приложений. Написание Dockerfile, работа с Docker Compose для оркестрации многоконтейнерных приложений. Понимание лучших практик создания образов и управления контейнерами.",
            "5": "Базовые знания развертывания и управления приложениями в Kubernetes. Опыт работы с Pod'ами, Deployments, Services и ConfigMaps. Понимание принципов работы кластера и основ мониторинга приложений в K8s."
        },
        "additional_info": {
            "languages": [
                {
                    "language": "Английский",
                    "level": "B2"
                },
                {
                    "language": "Русский",
                    "level": "Родной"
                }
            ],
            "projects": [
                {
                    "name": "Разработка микросервисной архитектуры",
                    "description": "Lead developer проекта по миграции монолита на микросервисы"
                }
            ]
        },
        "career_preferences": {
            "desired_position": "Tech Lead",
            "preferred_technologies": ["Python", "Go", "Kubernetes"],
            "work_format": "Гибридный",
            "relocation": "Рассматриваю",
            "expected_salary": 350000
        }
    }

    analysis_data = {
        'recommended_roles': 'Tech Lead, Software Architect',
        'skills_gap': 'Управление командой, публичные выступления',
        'recommended_courses': 'Курс по лидерству, курс по публичным выступлениям',
        'mobility_score': 'Высокая',
        'last_activities': 'Обновлен профиль 2024-01-15'
    }

    user_context = build_user_context_from_json(
        user_data=user_json,
        analysis_results=analysis_data,
        is_first_message=is_first_message,
        username=username,
        message_history=message_history
    )

    with open('_Models/tools/prompt_employee.txt', 'r', encoding='utf-8') as file:
        prompt_template = file.read()

    final_prompt = prompt_template.format(**user_context)
    return final_prompt
