# This Python file uses the following encoding: utf-8
# pip install android-auto-play-opencv
import PIL.Image
import numpy
import android_auto_play_opencv as am
import cv2
import pyocr
import pyocr.builders
from PIL import Image
from PIL import ImageOps
import gainExp

adbpath = './android sdk/platform-tools/'
aapo = am.AapoManager(adbpath)
ge = gainExp.exp(aapo)

def gotoTreasure():
    # 　冒険ボタン押す
    aapo.touchPos(100, 1900)
    aapo.sleep(1)
    # トレジャーマップ押す
    aapo.touchPos(300, 1300)
    aapo.sleep(2)
    while True:
        # 画面キャプチャ
        aapo.screencap()
        if aapo.chkImg('./template/treasuremap.png'):
            aapo.touchPos(540, 1640)
            aapo.sleep(2)
            aapo.touchPos(400, 1650)
            aapo.sleep(2)
            aapo.touchPos(400, 1270)
            break
        elif aapo.chkImg('./template/haveTreasureData.png'):
            aapo.touchPos(400, 1370)
            aapo.sleep(1)
            break
    return True

def inTreasure():
    actSwitch = True
    sogusenTimes = 0
    while True:
        # 画面キャプチャ
        aapo.screencap()
        # 航海力足りない
        if aapo.chkImg('./template/noHp.png'):
            gotoExp()
            break
        # 強敵出現
        elif aapo.chkImg('./template/strongEnemy.png'):
            aapo.touchPos(540, 1580)
            aapo.sleep(1)
        # 大連戦
        elif aapo.chkImg('./template/rollbattle.png'):
            rollBattle()
            break
        # ポイント画面
        elif aapo.chkImg('./template/treasurePoint.png'):
            aapo.touchPos(550, 1580)
        # 強敵戦闘
        elif aapo.chkImg('./template/strongEnemyBattle.png'):
            aapo.touchPos(370, 1500)
            aapo.sleep(3)
            aapo.touchPos(400, 1480)
        # 強敵終了
        elif aapo.chkImg('./template/strongEnemyWin.png'):
            aapo.touchPos(550, 1540)
        # チーム選択
        elif aapo.chkImg('./template/teamSelect.png'):
            inBattle()
        # 遭遇戦
        elif aapo.chkImg('./template/sogusen.png'):
            sogusenTimes = sogusenTimes + 1
            aapo.touchPos(540, 1590)
            aapo.sleep(1)
        # 宝箱
        elif aapo.chkImg('./template/takarabako.png'):
            aapo.touchPos(540, 1580)
        else:
            if actSwitch:
                aapo.touchPos(940, 1800)
                actSwitch = False
            else:
                if sogusenTimes < 2:
                    aapo.screencap()
                    if not (aapo.chkImg('./template/rollbattle.png') or aapo.chkImg('./template/teamSelect.png') or
                            aapo.chkImg('./template/strongEnemyBattle.png')):
                        # 最速
                        # aapo.touchPos(660, 1200)
                        # 寄り道
                        aapo.touchPos(750, 1550)
                actSwitch = True

        # # OKボタンがある場合
        # result, x, y = aapo.chkImg2('./template/adviceOK.png')
        # # 任意キー
        # if result:
        #     aapo.touchPos(x + 20, y + 20)
        #     aapo.sleep(2)
    return False

def rollBattle():
    while True:
        # 画面キャプチャ
        aapo.screencap()
        # 大連戦
        if aapo.chkImg('./template/rollbattle.png'):
            aapo.touchPos(370, 1820)
            aapo.sleep(3)
            inBattle()
        # ポイント画面
        elif aapo.chkImg('./template/treasurePoint.png'):
                aapo.touchPos(550, 1580)
        # 周回終了
        elif aapo.chkImg('./template/treasuremap.png'):
           return

def inBattle():
    aapo.touchPos(550, 1900)
    aapo.sleep(3)
    # 　助っ人選択
    aapo.touchPos(500, 800)
    aapo.sleep(3)
    # 　選択ボタン押下
    aapo.touchPos(530, 1300)
    aapo.sleep(2)
    aapo.touchPos(550, 1900)
    while True:
        # 画面キャプチャ
        aapo.screencap()
        # 戦闘終了
        if aapo.chkImg('./template/rebattle.png'):
            aapo.touchPos(690, 1560)
            aapo.touchPos(690, 1630)
            return
        elif aapo.chkImg('./template/bouken_advice.png'):
            result, x, y = aapo.chkImg2('./template/adviceOK.png')
            # 任意キー
            if result:
                aapo.touchPos(x + 20, y + 20)
                aapo.sleep(2)
        else:
            aapo.touchPos(420, 1430)
            aapo.sleep(0.5)
            aapo.touchPos(950, 1430)
            aapo.sleep(0.5)
            aapo.touchPos(420, 1620)
            aapo.sleep(0.5)
            aapo.touchPos(950, 1620)
            aapo.sleep(0.5)
            aapo.touchPos(420, 1820)
            aapo.sleep(0.5)
            aapo.touchPos(950, 1820)

def gotoExp():
    # 航海力足りない画面で戻るを選択
    aapo.touchPos(680, 1590)
    aapo.sleep(3)
    # MENU
    aapo.touchPos(120, 560)
    while True:
        # 画面キャプチャ
        aapo.screencap()
        if aapo.chkImg('./template/leaveTreaOk.png'):
            aapo.touchPos(400, 1600)
            aapo.sleep(5)
            break
        elif aapo.chkImg('./template/leaveTreasure.png'):
            aapo.touchPos(540, 1710)
    ge.exp_method(10)

def torekuru():
    step = 1
    inTreasureOk = True
    while True:
        # 画面キャプチャ
        aapo.screencap()
        if aapo.chkImg('./template/noHp.png'):
            gotoExp()
        # ポイント画面
        elif aapo.chkImg('./template/treasurePoint.png'):
                aapo.touchPos(550, 1580)
        elif aapo.chkImg('./template/bouken.png'):
            inTreasureOk = gotoTreasure()
        elif (aapo.chkImg('./template/roll.png') or aapo.chkImg('./template/rollbattle.png')) and inTreasureOk:
            inTreasureOk = inTreasure()

def crrwBattle():
    while True:
        aapo.screencap()
        if aapo.chkImg('./template/crrwBattleOver.png'):
            result, x, y = aapo.chkImg2('./template/crrwBattleOver.png')
            aapo.touchPos(x + 20, y + 20)
            aapo.sleep(1)
            return
        aapo.swipeTouchPos(340, 2070, 520, 1710, 300)

#クラロワ自動戦闘
def crrw():
    while True:
        aapo.screencap()
        if aapo.chkImg('./template/crrwBattleStart.png'):
            aapo.touchPos(330, 1500)
            aapo.sleep(1)
            aapo.touchPos(500, 1470)
            aapo.sleep(2)
            crrwBattle()

#トレクル自動戦闘（戦闘に入る必要ある）
def simpleRepeatBattle(times):
    ge.battleRepeat(times)

if __name__ == '__main__':
    # トレクル大連戦
    # torekuru()
    # クラロワ自動戦闘
    crrw()
    # ト レクル自動戦闘(simple)
    # simpleRepeatBattle(199)
    # 麦わら一味イベントロープ
    # ge.exp_method(5000)
