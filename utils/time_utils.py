def get_seconds(h, m, s):
    """
    時間（時・分・秒）を秒へ変換
    """

    try:
        h = int(h)
        m = int(m)
        s = int(s)

        if not (0 <= m <= 59 and 0 <= s <= 59 and h >= 0):
            raise ValueError

        return h * 3600 + m * 60 + s

    except:
        raise ValueError("時間入力が不正です（分・秒は0〜59）")