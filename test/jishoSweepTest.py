"""
:file: jishoSweepTest.py
:author: Christopher Mason
:email: christophermason125@gmail.com
"""


import unittest
import src.jishoSweep as jishoSweep


class JishoSweepTest(unittest.TestCase):
    """
    Tests jishoSweep.py
    """
    def test_sweep_jisho(self):
        """
        Tests jishoSweep.sweep_jisho
        """
        result = jishoSweep.sweep_jisho(max_page=3)
        self.assertListEqual(result, ['上げる', '仕事', '先生', '公園', '動物', '名前', '周り', '問題', '声', '夏', '夜',
                                      '大学', '子供', '学校', '家族', '宿題', '山', '川', '年', '意味', '戸', '手', '手紙',
                                      '散歩', '料理', '新聞', '旅行', '映画', '時計', '時間', '朝', '木', '机', '歌', '毎日',
                                      '水', '煙草', '猫', '病気', '目', '眼鏡', '窓', '箱', '結婚', '自転車', '花', '英語',
                                      '言葉', '赤', '走る', '足', '道', '部屋', '雨', '雪', '電話', '電車', '靴', '音楽',
                                      '飛行機'])

        result = jishoSweep.sweep_jisho(query="年", max_page=1)
        self.assertTrue(result.count("年") == 1)

        result = jishoSweep.sweep_jisho(query="frog", min_page=3, max_page=4)
        self.assertTrue(result, ['かえるの目借時', 'ぴょこぴょこ', 'アオガエル科', 'アカガエル科', 'アマガエルモドキ科', 'カエル目',
                                 'カメガエル科', 'ガマグチヨタカ科', 'クサガエル科', 'コガネガエル科', 'コロコロ', 'サエズリガエル科',
                                 'スキアシガエル科', 'スズガエル科', 'セーシェルガエル科', 'ダーウィンガエル科', 'パセリガエル科',
                                 'ヒメアマガエル科', 'ピパ科', 'フロンノルウェー', 'マダガスカルカエル科', 'ムカシガエル科',
                                 'メキシコジムグリガエル科', 'ヤドクガエル科', 'ユウレイガエル科', 'ユビナガガエル科', '井の中の蛙',
                                 '井蛙は以って海を語る可からず', '泡吹虫', '無尾目', '蛙の子は蛙', '蛙の面に小便', '蛙の面に水',
                                 '蛙喜劇', '蛙声', '蛙泳ぎ', '蛙鮟鱇', '躄魚', '閣閣'])

        with self.assertRaises(ValueError):
            jishoSweep.sweep_jisho(min_page=5, max_page=1)

        with self.assertRaises(ValueError):
            jishoSweep.sweep_jisho(query="")


if __name__ == '__main__':
    unittest.main()
