# instagram

Два модуля:
1) Класс Instagram в файле instagram_info. Класс для получения и 
сохранения информации и последних постов из профиля пользователя

     Два параметра для иницилизации класса тэг пользователя
     и путь до папки data.
     
        insta = Instagram(user_tag, path)
        data = insta.get_user_insta_info()
        insta.save_data(data)
        
     Он возвращает и сохраняет в папку с название "user_tag"
     всю основную инфу из профиля в файл user_tag.pcl, изображения профиля
     = profile_pic.jpg, а так же 10-20 последних постов, которые 
     называются по их id.
     Если в пост состоит из нескольких медиа, то все медиа из этого поста
     сохраняются в отдельную папку под название id поста.
    
2) Класс InstaAnalyze в файле instagram_analyze 
Анализирует профиль пользователя и его фотографиям и выдает некоторые
характеристики основанные на тесте big5. 

        analyze = InstaAnalyze(user_tag)
        metrics = analyze.get_metrics()

Возвращаются словарь из 4 метрик. Их интерпритацию можно посмотреть в 
файле app функция inter_metrics

    metrics = {'colorfulness': int, 
                'diversity': int, 
                'harmony': int, 
                'saturation': int}



    
