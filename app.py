from scripts.instagram_info import Instagram
from scripts.instagram_analyze import InstaAnalyze
from pathlib import Path


def inter_metrics(metrics):
    if metrics['colorfulness'] in (3, 4) and metrics['diversity'] in (3, 4) and metrics['harmony'] in (3, 4):
        print('У человека высокая доброжелательность (Agreeableness)')
    else:
        print('Скорее всего у человека не высокая доброжелательность (Agreeableness)')

    if metrics['harmony'] == 2:
        print('Возможно у человека есть невротизм (neuroticism)')
    elif metrics['harmony'] == 1:
        print('Скорее всего у человека точно есть невротизм (neuroticism)')
    else:
        print('Вряд ли человек подвержен сильному невротизму (neuroticism)')

    if metrics['diversity'] in (1, 2):
        print('Скорее всего человек более одинок, в частности вряд ли он состоит в отношениях')

    if metrics['harmony'] in (3, 4):
        print('У человека положительное отношение к инстаграму')

    if metrics['diversity'] == 3:
        print('У человека повышенная экстраверсия (Extraversion)')
    elif metrics['diversity'] == 4:
        print('У человека высокая экстраверсия (Extraversion)')

    if metrics['diversity'] in (1, 2) and metrics['harmony'] in (1, 2):
        print('У человека высокая открытость (Openness)')

    if metrics['saturation']:
        print('У человека есть признаки депрессии')
    else:
        print('Отсутствуют признаки депрессии')


if __name__ == '__main__':
    path = Path.cwd() / 'data'
    insta = Instagram('krupskaya_', path)
    data = insta.get_user_insta_info()
    insta.save_data(data)

    analyze = InstaAnalyze('krupskaya_')
    metrics = analyze.get_metrics()
    print(metrics)
    inter_metrics(metrics)

