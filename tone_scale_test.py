import streamlit as st
import json

# Загрузка данных из файла questions_data.json
with open('questions_data.json', 'r', encoding='utf-8') as f:
    questions_data = json.load(f)

# Функция для получения ответов от пользователя
def get_user_answers(questions_data):
    answers = {}
    for question in questions_data['questions']:
        group = question['group']
        if group not in answers:
            answers[group] = []
        
        # Ввод ответа от пользователя через Streamlit
        answer = st.radio(f"{question['question_id']}. {question['text']}", options=["1 (ДА)", "2 (НЕТ)"])
        
        # Преобразуем ответ в "ДА" или "НЕТ"
        if answer == "1 (ДА)":
            answers[group].append("ДА")
        else:
            answers[group].append("НЕТ")
    
    return answers

# Функция для подсчета ответов в тесте
def count_answers(test):
    yes_count = test.count("ДА")
    no_count = test.count("НЕТ")
    return yes_count, no_count

# Функция для оценки по шкале тонов
def evaluate_tone_scale(answers):
    test1_yes, test1_no = count_answers(answers['test1'])
    
    if test1_yes > test1_no:
        test2_yes, test2_no = count_answers(answers['test2'])
        if test2_yes > test2_no:
            test4_yes, test4_no = count_answers(answers['test4'])
            if test4_yes > test4_no:
                return "Индекс: 3.6-4.0"
            else:
                return "Индекс: 3.1-3.5"
        else:
            test6_yes, test6_no = count_answers(answers['test6'])
            if test6_yes > test6_no:
                return "Индекс: 2.6-3.0"
            else:
                return "Индекс: 2.1-2.5"
    else:
        test3_yes, test3_no = count_answers(answers['test3'])
        if test3_yes > test3_no:
            test5_yes, test5_no = count_answers(answers['test5'])
            if test5_yes > test5_no:
                return "Индекс: 1.5-2.0"
            else:
                return "Индекс: 1.1-1.4"
        else:
            test7_yes, test7_no = count_answers(answers['test7'])
            if test7_yes > test7_no:
                return "Индекс: 0.6-1.0"
            else:
                return "Индекс: 0.1-0.5"

# Заголовок приложения
st.title("Тест по шкале тонов")

# Получение ответов от пользователя
user_answers = get_user_answers(questions_data)

# Кнопка для завершения теста и получения результата
if st.button("Показать результат"):
    result = evaluate_tone_scale(user_answers)
    st.write(f"Ваш эмоциональный тон: {result}")
