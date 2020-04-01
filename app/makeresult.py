

def make_result(user_answers, userdata, dep_type, otdel='ОПиР'):
    """
    Подсчет результатов тестирования.
    Подсчет произодится по количеству правильных ответов в зависимости от тем тестирования.
    Темы тестирования зависят от отдела - переменна otdel.
    """
    dep_type = {
        'ОПиР': {'python': 6, 'ds': 6, 'c_': 0, 'sql': 3},
        'ОАКБ': {'python': 5, 'ds': 5, 'c_': 0, 'sql': 5},
        'ОАРБ': {'python': 5, 'ds': 0, 'c_': 0, 'sql': 10},
        'ОАРБ_c#': {'python': 0, 'ds': 0, 'c_': 6, 'sql': 9},
        'ОАОП': {'python': 10, 'ds': 2, 'c_': 0, 'sql': 3},
        'ОАОП_c#': {'python': 0, 'ds': 0, 'c_': 6, 'sql': 9},
        'ОАКБ_python': {'python': 15, 'ds': 0, 'c_': 0, 'sql': 0},
        'ОАОП_sql': {'python': 0, 'ds': 0, 'c_': 0, 'sql': 15},
        'ОАРБ_sql': {'python': 0, 'ds': 0, 'c_': 0, 'sql': 15},
    }

    user_answers_data = [i for i in user_answers.values()][:-1]
    result = {otdel: {'python': 0, 'ds': 0, 'c_': 0, 'sql': 0}}
    result_part = {otdel: {'python': 0, 'ds': 0, 'c_': 0, 'sql': 0}}
    for num, data in enumerate(userdata):
        result[otdel][data['q_type']] += data['id'] == int(user_answers_data[num])

    for score in result_part[otdel]:
        if dep_type[otdel][score] != 0:
            result_part[otdel][score] = round(result[otdel][score] / dep_type[otdel][score] * 100, 1)
        else:
            result_part[otdel][score] = 0.0

    pos_result = sum(score for score in result[otdel].values()) # число правильных ответов
    all_result = sum(score for score in dep_type[otdel].values()) # общее число вопросов в тесте
    part_pos_result = round(pos_result / all_result * 100, 1) # доля правильных ответов

    return dep_type[otdel], result[otdel], result_part[otdel], pos_result, all_result, part_pos_result
