import PIL.Image
import numpy
import android_auto_play_opencv as am
import cv2
import pyocr
import pyocr.builders
from PIL import Image
from PIL import ImageOps


class exp:
    aapo = None
    step = 1
    oldLevel = 0
    battleTimes = 0

    # コンストラクタ（引数なし）
    def __init__(self, aapo):
        self.aapo = aapo
        pass

    def exp_method(self, battleTimes):
        self.battleTimes = battleTimes
        self.step = 1
        battleCount = 0
        while True:
            # 画面キャプチャ
            self.aapo.screencap()
            if self.step == 1:
                # self.oldLevel = self.checkLevel()
                # 冒険ボタンがあったら、
                if self.aapo.chkImg('./template/bouken.png'):
                    self.gotoExpStander()
            elif self.step == 2:
                self.battlePrepare()
            elif self.step == 3:
                battleCount = self.expStanderBattle(battleCount, self.battleTimes)
            else:
                return

    def battleRepeat(self, times=10000):
        countTimes=0
        while countTimes < times:
            self.aapo.screencap()
            # 再戦画面
            if self.aapo.chkImg('./template/rebattle.png'):
                # 再戦ボタン押下
                self.aapo.touchPos(400, 1720)
                self.aapo.sleep(3)
                countTimes = countTimes + 1
                print("countTimes = " + str(countTimes))

            # クリア後画面
            # elif self.aapo.chkImg('./template/bouken_advice.png'):
            elif self.aapo.chkImg('./template/adviceOK.png'):
                result, x, y = self.aapo.chkImg2('./template/adviceOK.png')
                # 任意キー
                if result:
                    self.aapo.touchPos(x + 20, y + 20)
                    self.aapo.sleep(2)
            # 戦闘画面
            elif self.aapo.chkImg('./template/auto_battle.png'):
                # 自動戦闘button押下
                for i in range(3):
                    self.aapo.touchPos(110, 480)
                    self.aapo.sleep(1)
            else:
                self.aapo.touchPos(550, 2000)
            # 体力回復画面
            if self.aapo.chkImg('./template/stamina_flg.png'):
                self.aapo.touchPos(400, 1710)
                self.aapo.sleep(3)
                self.aapo.touchPos(540, 1210)

    # 体力回復
    def sitaminaRecovery(self):
        self.aapo.touchPos(400, 1690)
        self.aapo.sleep(2)
        self.aapo.touchPos(540, 1200)

    def gotoExpStander(self):
        # 　冒険ボタン押す
        self.aapo.touchPos(100, 1900)
        self.aapo.sleep(1)
        # 　イベント押す
        self.aapo.touchPos(520, 1050)
        while True:
            self.aapo.screencap()
            # 　麦わら一味取得タスク（1 stamina=400 exp)である場合
            if self.aapo.chkImg('./template/expstander1.png'):
                # 　タスクに入る
                self.aapo.touchPos(535, 1672)
                self.aapo.sleep(1)
                # 　麦わら一味メンバー取得タスクを選択する
                self.aapo.swipeTouchPos(550, 1666, 720, 1672, 1000)
                self.aapo.touchPos(535, 1672)
                # 　次のステップへ
                self.step = self.step + 1
                break
            if self.aapo.chkImg('./template/ikusei.png'):
                self.aapo.touchPos(400, 1200)
                self.aapo.sleep(1)
                self.aapo.swipeTouchPos(550, 1666, 880, 1672, 1000)
                self.aapo.sleep(0.5)

    def battlePrepare(self):
        # 　助っ人選択
        self.aapo.touchPos(500, 800)
        self.aapo.sleep(2)
        # 　選択ボタン押下
        self.aapo.touchPos(530, 1300)
        while True:
            self.aapo.screencap()
            # スタミナ３倍ボタンがある場合
            if self.aapo.chkImg('./template/3bai.png'):
                # ボタン押下
                self.aapo.touchPos(870, 1700)
                self.aapo.sleep(1)
                # はいボタン押下
                self.aapo.touchPos(380, 1500)
                self.aapo.sleep(1)
                # はいボタン押下
                self.aapo.touchPos(390, 1500)
                # 　次のステップへ
                self.step = self.step + 1
                break

    def expStanderBattle(self, battleCount, battleTimes):
        goNext = False
        bc = battleCount
        while True:
            self.aapo.screencap()
            # 冒険説明画面
            if self.aapo.chkImg('./template/exp_stander_start.png'):
                self.aapo.swipeTouchPos(600, 1300, 550, 1300, 500)
                self.aapo.sleep(1)
                self.aapo.touchPos(530, 1650)
                goNext = True
                bc = bc + 1
            if goNext:
                # 再戦画面
                if self.aapo.chkImg('./template/rebattle.png'):
                    # レベルチェック
                    # newLevel = self.checkLevel()
                    # 　次のステップへ
                    # if newLevel > oldLevel:
                    #     self.step = self.step + 1
                    #     break
                    print("battle times = " + str(bc))
                    if bc > battleTimes:
                        self.aapo.touchPos(680, 1720)
                        self.step = self.step + 1
                        break
                    else:
                        # 再戦ボタン押下
                        self.aapo.touchPos(400, 1720)
                        self.aapo.sleep(3)
                        break
                # クリア後画面
                elif self.aapo.chkImg('./template/bouken_advice.png'):
                    result, x, y = self.aapo.chkImg2('./template/adviceOK.png')
                    # 任意キー
                    if result:
                        self.aapo.touchPos(x + 20, y + 20)
                        self.aapo.sleep(2)
                # 戦闘画面
                elif self.aapo.chkImg('./template/auto_battle.png'):
                    # 自動戦闘button押下
                    for i in range(3):
                        self.aapo.touchPos(110, 480)
                        self.aapo.sleep(1)
                else:
                    self.aapo.touchPos(550, 2000)
            # 体力回復画面
            if self.aapo.chkImg('./template/stamina_flg.png'):
                self.aapo.touchPos(400, 1710)
                self.aapo.sleep(3)
                self.aapo.touchPos(540, 1210)
        return bc

    def checkLevel(self):
        level = 0
        img = cv2.imdecode(numpy.frombuffer(self.aapo.adbl.screenImg, numpy.uint8), 0)
        img = img[410:448, 490:590]
        img = Image.fromarray(img)
        tools = pyocr.get_available_tools()
        if len(tools) == 0:
            print('pyocrが見付かりません。pyocrをインストールして下さい。')
        tool = tools[0]
        number = tool.image_to_string(img, lang='eng', builder=pyocr.builders.TextBuilder())
        print(number)
        return int(number)
