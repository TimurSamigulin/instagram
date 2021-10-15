from scripts.instagram_info import Instagram
from scripts.instagram_analyze import InstaAnalyze

if __name__ == '__main__':
    insta = Instagram()
    data = insta.get_user_insta_info('falcon151')
    insta.save_data(data)
    analyze = InstaAnalyze('falcon151')
    metrics = analyze.get_metrics()