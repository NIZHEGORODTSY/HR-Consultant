def build_user_context(user_id: int, analysis_results: dict) -> dict:
    # Получаем данные из БД
    # user_data = get_user_data(user_id)  # Ваша функция к БД
    # skills = get_user_skills(user_id)
    # roles = get_user_roles(user_id)
    # education = get_education(user_id)
    # career_prefs = get_career_preferences(user_id)
    # add_info = get_additional_info(user_id)
    # add_education = get_additional_education(user_id)

    # Прочитать весь файл как одну строку
    data = get_all_info(user_id)

    user_fullname = 'Иван Михайлович'  # Ваша функция к БД
    skills = ['мужчина']
    roles = ['python']
    education = 'высшее'
    career_prefs = 'всех победить'
    add_info = 'пр-та-та'
    add_education = 'специализация Яндекс'

    # Формируем контекст
    context = {
        # Основная информация
        "user_full_name": user_fullname,

        # Навыки и опыт
        "user_skills": ", ".join([skill['description'] for skill in skills]),
        "current_role": roles[0]['role'] if roles else "Не указана",
        "current_experience": roles[0]['experiance'] if roles else "0",
        "func_role": roles[0]['func_role'] if roles else "Не указана",
        "team_role": roles[0]['team_role'] if roles else "Не указана",
        "functionality": roles[0]['functionality'] if roles else "Не указана",

        # Образование
        "university": education['university'] if education else "Не указано",
        "level": education['level'] if education else "",
        "speciality": education['speciality'] if education else "",
        "graduation_year": education['graduation_year'] if education else "",
        "additional_educations": ", ".join([edu['description'] for edu in add_education]),
        "blob_diploma_info": "Есть сертификаты" if education and education['blob_diploma'] else "Нет сертификатов",

        # Предпочтения
        "career_preferences": career_prefs['description'] if career_prefs else "Не указаны",
        "additional_info": add_info['description'] if add_info else "",

        # Результаты анализа (из других моделей)
        "recommended_roles": analysis_results.get('recommended_roles', ""),
        "skills_gap": analysis_results.get('skills_gap', ""),
        "recommended_courses": analysis_results.get('recommended_courses', ""),
        "mobility_score": analysis_results.get('mobility_score', ""),
        "last_activities": analysis_results.get('last_activities', "")
    }

    return context


def get_final_prompt():
    with open('../_MODELS/prompt.txt', 'r', encoding='utf-8') as file:
        prompt_template = file.read()
    analysis_data = '000'

    # Использование

    user_context = build_user_context(user_id=1, analysis_results=analysis_data)
    final_prompt = prompt_template.format(**user_context)
