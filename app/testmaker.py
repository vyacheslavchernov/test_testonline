import pandas as pd
import random


def make_test(user, otdel, seed=0):
    """
    Make tests
    """
    random.seed(seed)
    df_1 = pd.read_csv('./data/data.csv')
    df_2 = pd.read_csv('./data/ans.csv')

    dep_type = {
        'ОПиР': {'python': 6, 'ds': 6, 'c#': 0, 'sql': 3},
        'ОАКБ': {'python': 5, 'ds': 5, 'c#': 0, 'sql': 5},
        'ОАРБ': {'python': 5, 'ds': 0, 'c#': 0, 'sql': 10},
        'ОАРБ_c#': {'python': 4, 'ds': 0, 'c#': 3, 'sql': 8},
        'ОАОП': {'python': 10, 'ds': 2, 'c#': 0, 'sql': 3},
        'ОАОП_c#': {'python': 5, 'ds': 0, 'c#': 5, 'sql': 5},
        'ОАКБ_python': {'python': 15, 'ds': 0, 'c#': 0, 'sql': 0},
        'ОАОП_sql': {'python': 0, 'ds': 0, 'c#': 0, 'sql': 15},
        'ОАРБ_sql': {'python': 0, 'ds': 0, 'c#': 0, 'sql': 15},
    }
    python_q = df_1.iloc[random.sample(range(0, 15), dep_type[otdel]['python']), 0:2]
    ds_q = df_1.iloc[random.sample(range(16, 25), dep_type[otdel]['ds']), 0:2]
    c_q = df_1.iloc[random.sample(range(26, 32), dep_type[otdel]['c#']), 0:2]
    sql_q = df_1.iloc[random.sample(range(33, 48), dep_type[otdel]['sql']), 0:2]
    all_data = [python_q, ds_q, c_q, sql_q]
    tests = []
    userdata = []
    num = 1
    for data in all_data:
        for i in range(data.shape[0]):
            ques = []
            tests.append({'questions': '', 'answers': ''})
            ques.append('Вопрос ' + str(num) + ':')
            ques.append(str(data.iloc[i]['question']))
            tests[num-1]['questions'] = ques

            userdata.append(
                    {'user': '', 'q_type': '', 'questions': '', 'answers': ''})
            userdata[num-1]['questions'] = str(data.iloc[i]['question'])
            # userdata[num-1]['q_type'] = str(data.iloc[i]['q_type'])
            userdata[num-1]['user'] = user
            ans = df_2[df_2['question_id'] == data.iloc[i]['id']]
            answ = []
            useransw = ''
            for j in range(ans.shape[0]):
                answ.append(str(ans.iloc[j]['answer']))
                if ans.iloc[j]['yes_no'] == 1:
                    useransw = ans.iloc[j]['answer']
            tests[num-1]['answers'] = answ
            userdata[num-1]['answers'] = useransw
            num += 1
    return userdata, tests