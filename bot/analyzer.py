import pandas as pd
import matplotlib.pyplot as plt
import math
import io

def get_stat(filepath, agr_col = "Tags"):
    df = pd.read_csv(filepath)
    df['Duration'] = pd.to_timedelta(df['Duration'])
    df = df.groupby(agr_col)['Duration'].sum()
    df = df.apply(lambda x: math.ceil(x.total_seconds() / 3600 * 10) / 10)

    tasks = dict()
    for category, time in df.items():
        tasks[category] = time
    return tasks

def get_text(dict_tasks, rate, start_date:str, end_date:str):
    txt = ""
    all_time = 0

    txt += f"Отчет за период с {start_date} по {end_date}\n\n"

    for category in dict_tasks:
        all_time += dict_tasks[category]

    for category, time in dict_tasks.items():
        txt += f"{category}: {time} часа ({round(time/all_time*100,2)}% от общего времени)\n"

    txt += "\n"
    txt += f"Итого: {all_time} часов или {all_time*rate} рублей"
    return txt

def get_pie(data):
    labels = list(data.keys())
    values = list(data.values())
    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, startangle=90)
    ax.axis('equal')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    return buf

#Проставить исключения!!!

