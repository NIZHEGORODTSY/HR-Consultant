# data_processing.py
import pandas as pd
import numpy as np
from datetime import datetime
from hr_database import get_data_from_db, create_test_data


class DataProcessor:
    def __init__(self):
        self.users, self.skills, self.roles, self.educations, self.career_preferences = get_data_from_db()
        self.merged_data = pd.DataFrame()
        self.process_data()

    def process_data(self):
        """Обработка и подготовка данных"""
        # Проверяем, что данные загружены успешно
        if self.users.empty:
            print("Предупреждение: Не удалось загрузить данные из базы. Используются тестовые данные.")
            self.users, self.skills, self.roles, self.educations, self.career_preferences = create_test_data()

        try:
            # Переименовываем колонки для совместимости
            self.users = self.users.rename(columns={'id': 'user_id'})

            self.merged_data = self.users.merge(self.roles, on='user_id', how='left') \
                .merge(self.educations, on='user_id', how='left') \
                .merge(self.career_preferences, on='user_id', how='left')

            # Добавляем вычисление опыта работы
            self._calculate_experience()

        except Exception as e:
            print(f"Ошибка при обработке данных: {e}")

    def _calculate_experience(self):
        """Вычисление опыта работы"""
        if 'start_date' in self.roles.columns and pd.api.types.is_datetime64_any_dtype(self.roles['start_date']):
            self.roles['experience'] = (pd.Timestamp.now() - self.roles['start_date']).dt.days / 365.25
            self.roles['experience'] = self.roles['experience'].fillna(0).round(1)
        else:
            self.roles['experience'] = np.random.randint(1, 15, len(self.roles))

    def get_skill_counts(self):
        """Статистика по навыкам"""
        if not self.skills.empty and 'description' in self.skills.columns:
            return self.skills['description'].value_counts().reset_index().rename(
                columns={'description': 'skill', 'count': 'count'})
        return pd.DataFrame({'skill': [], 'count': []})

    def get_role_stats(self):
        """Статистика по профессиям"""
        if not self.roles.empty and 'role' in self.roles.columns:
            return self.roles['role'].value_counts().reset_index().rename(columns={'role': 'role', 'count': 'count'})
        return pd.DataFrame({'role': [], 'count': []})

    def get_education_stats(self):
        """Статистика по образованию"""
        if not self.educations.empty and 'level' in self.educations.columns:
            return self.educations['level'].value_counts().reset_index().rename(
                columns={'level': 'level', 'count': 'count'})
        return pd.DataFrame({'level': [], 'count': []})

    def get_university_stats(self):
        """Статистика по университетам"""
        if not self.educations.empty and 'university' in self.educations.columns:
            return self.educations['university'].value_counts().reset_index().rename(
                columns={'university': 'university', 'count': 'count'})
        return pd.DataFrame({'university': [], 'count': []})

    def get_role_university_crosstab(self):
        """Кросс-таблица профессии vs университеты"""
        if not self.merged_data.empty and 'role' in self.merged_data.columns and 'university' in self.merged_data.columns:
            return pd.crosstab(self.merged_data['role'], self.merged_data['university'])
        return pd.DataFrame()

    def get_career_pref_stats(self):
        """Статистика по карьерным предпочтениям"""
        if not self.career_preferences.empty and 'desired_position' in self.career_preferences.columns:
            return self.career_preferences['desired_position'].value_counts().reset_index().rename(
                columns={'desired_position': 'preference', 'count': 'count'})
        return pd.DataFrame({'preference': [], 'count': []})

    def get_speciality_stats(self):
        """Статистика по специальностям"""
        if not self.educations.empty and 'speciality' in self.educations.columns:
            return self.educations['speciality'].value_counts().reset_index().rename(
                columns={'speciality': 'speciality', 'count': 'count'})
        return pd.DataFrame({'speciality': [], 'count': []})

    def get_sunburst_data(self):
        """Данные для sunburst chart"""
        if not self.merged_data.empty and 'university' in self.merged_data.columns and 'role' in self.merged_data.columns:
            return self.merged_data.groupby(['university', 'role']).size().reset_index(name='count')
        return pd.DataFrame({'university': [], 'role': [], 'count': []})

    def get_filtered_data(self, selected_roles=None, selected_universities=None, selected_experience=None):
        """Фильтрация данных по выбранным параметрам"""
        if self.merged_data.empty:
            return pd.DataFrame()

        filtered_data = self.merged_data.copy()

        if selected_roles:
            filtered_data = filtered_data[filtered_data['role'].isin(selected_roles)]
        if selected_universities:
            filtered_data = filtered_data[filtered_data['university'].isin(selected_universities)]
        if selected_experience and 'experience' in filtered_data.columns:
            experience_filters = []
            for exp_range in selected_experience:
                if exp_range == '0-3':
                    experience_filters.append(filtered_data['experience'] <= 3)
                elif exp_range == '3-5':
                    experience_filters.append((filtered_data['experience'] > 3) & (filtered_data['experience'] <= 5))
                elif exp_range == '5-10':
                    experience_filters.append((filtered_data['experience'] > 5) & (filtered_data['experience'] <= 10))
                elif exp_range == '10+':
                    experience_filters.append(filtered_data['experience'] > 10)

            if experience_filters:
                combined_filter = experience_filters[0]
                for f in experience_filters[1:]:
                    combined_filter = combined_filter | f
                filtered_data = filtered_data[combined_filter]

        return filtered_data
