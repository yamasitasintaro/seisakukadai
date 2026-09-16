import random

print ("テキストRPG風・冒険コマンドゲーム")
name1 = input("プレイヤー名を入力:")
print (f"{name1}の冒険が始まった")

sutatus = {
    "name" : name1 ,
    # "LV" : 1,
    # "exp" : 100,
    "HP" : 100,
   "ATK" : 15,
   "G" : 10,
   "froa" : 1
}

enemy_status1 = [
    # モンスターのステータスをリスト（enemy_status）の中の辞書に入力
    {"id" : 0,"name" : "スライム","HP" : 30,"ATK" : 3,"dorop":5},
    {"id" : 1,"name" : "ゴブリン","HP" : 25,"ATK" : 5,"dorop":10},
    {"id" : 2,"name" : "ウルフ","HP" : 30,"ATK" : 10,"dorop":10}
    # {"id" :0,"name" : "","HP" : 30,"ATK" : 5,"dorop":5}
]

enemy_status2 = [
    {"id" : 0,"name" : "レッドスライム","HP" : 50,"ATK" : 5,"dorop":10},
    {"id" : 1,"name" : "ホブゴブリン","HP" : 40,"ATK" : 15,"dorop":15},
    {"id" : 2,"name" : "オルトロス","HP" : 50,"ATK" : 20,"dorop":15}
]

boss_status= [
    {"id":0, "name" : "ケルベロス","HP":150,"ATK" : 30,"dorop":60,"skill":"ATKが高いが、HPが1/3減ると弱体化していく"},
    {"id":1,"name":"ドラゴン","HP":300,"ATK":25,"dorop":999,"skill":"3ターンごとに高火力の炎を吐く(50ダメージ)"}#推奨ステータス　 5t atk60 hp151以上　６t atk50 hp201以上
    # {"id":0,"name":,"HP":,"ATK":,"dorop":}
]

elite_status = [
    {"id":0,"name":"ゾンビ","HP":30,"ATK":10,"dorop":30,"skill":"倒されると1度だけ復活する"},
    {"id":1,"name":"ガーゴイル","HP":5,"ATK":10,"dorop":50,"skill":"防御力が高く1ダメージしか受けない"},
    {"id":2,"name":"オーク","HP":80,"ATK":20,"dorop":50,"skill":"ステータスが高いが2ターンに1度しか行動しない"},
    
    # {"id":0,"name":"","HP":50,"ATK":10,"dorop":30,"skill":""}
]

# 要調整
mimic =[
    {
    "id":0,"name":"ミミック","HP":50,"ATK":10,"dorop":100,"skill":"倒すと100Gを落とす"
    }
]

syouhi = 0 #ショップ用の定義

#HPを計算させるための空リスト
php=[] 

#リストの指定した場所（０＝先頭）に数値を追加する
php.insert(0,sutatus["HP"])

def show_status():
    print("ステータス")
    print("_"*20)
    print(f"HP:{php[0]}/{sutatus['HP']}")
    print(f"ATK:{sutatus['ATK']}")
    print(f"所持金:{sutatus['G']}G")
    print(f"現在の階層{sutatus['froa']}")
    return ("_"*20)


def battle(enemy_status):#モンスターのリスト名とIDを指定して特定モンスターの呼び出し
    e = random.randint(1,100)#モンスター出現パターンをランダム化するための数値
    # e = 81#エリートの挙動チェック用
    
    if enemy_status == mimic:
        e = 0
    if enemy_status == elite_status:
        e = 81


    if e <= 80:
        # ランダムにモンスターとそのステータスを代入
        random_enemy1 = random.choice(enemy_status)
        random_enemy_name =random_enemy1["name"]
        random_enemy_HP =random_enemy1["HP"]
        random_enemy_ATK =random_enemy1["ATK"]
        random_enemy_drop =random_enemy1["dorop"]

        # 戦闘開始時のメッセージ
        print("_"*20)
        if random_enemy_name == "ミミック":
            pdamege =(php[0] - random_enemy_ATK *2)
            php.append(pdamege)
            php.pop(0)
            print(f"不意打ちで{20}のダメージを受けた\n{random_enemy_name}")
            if php[0] <= 0:
                php[0] = 0
                

                if php[0] <= 0:
                        print(f"{sutatus['name']}はHPが0になった")
                        return "ゲームオーバー"
           
        else:
            print(f"{random_enemy_name}に遭遇した!")
        print(f"HP：{random_enemy_HP} ATK{random_enemy_ATK}")
        print("_"*20)
        print(f"{sutatus['name']}\nHP:{php[0]}  ATK{sutatus['ATK']}")
        print("_"*20)
        comand = input("コマンドを入力して下さい\nfight / ran\n")

        
        while True :    
            if comand == "fight" or comand == "f":
                turn = 1
                
                #リストの指定した場所（先頭）に数値を追加する
                ehp=[]
                ehp.insert(0,random_enemy_HP)

                while php[0] >=0:

                    pdamege =(php[0] - random_enemy_ATK)
                    edamege = (ehp[0] - sutatus["ATK"])

                    ehp.append(edamege)#リストの末尾に追加
                    ehp.pop(0)             
                    kuuhaku = input("Enterで続行")  

                    print(f"ターン{turn}\n{sutatus['name']}の攻撃！\n{random_enemy_name}は{sutatus['ATK']}のダメージを受けた")
                    
                    if ehp[0] <= 0:
                        sutatus["G"]+= random_enemy_drop
                        print(f"{random_enemy_name}を倒した！\n{random_enemy_drop}Gを獲得!")
                        return (f"残りHP：{php[0]}\n____________________")
                                        
                    php.append(pdamege)
                    php.pop(0)
                    if php[0] <= 0:
                        php[0] = 0
                    print(f"{random_enemy_name}の攻撃！\n{sutatus['name']}は{random_enemy_ATK}のダメージを受けた\n{sutatus['name']}のHP:{php[0]}  {random_enemy_name}のHP:{ehp[0]}")
                    turn += 1


                    if php[0] <= 0:
                        print(f"{sutatus['name']}は{random_enemy_name}に敗北した")
                        return "ゲームオーバー"

                    print("_"*20)  

            elif comand == "ran" or comand == "r":
                print(f"{sutatus['name']}は{random_enemy_name}から逃げ出した！")
                break
            else:
                print("無効なコマンドです")
                comand = input("コマンドを再入力して下さい\nfight / ran\n")


# エリートモンスターとの戦闘# ランダムにモンスターとそのステータスを代入
    elif e <= 100:
        elite = random.randint(2,3,)#エリートのランダム化 ゾンビは除外中
        
        if elite ==1:
            random_enemy1 = elite_status[0]#ゾンビ
        elif elite ==2:
            random_enemy1 = elite_status[1]#ガーゴイル
        elif elite ==3:
            random_enemy1 = elite_status[2]#オーク
        
        random_enemy_name =random_enemy1["name"]
        random_enemy_HP =random_enemy1["HP"]
        random_enemy_ATK =random_enemy1["ATK"]
        random_enemy_drop =random_enemy1["dorop"]
        enemy_skill = random_enemy1["skill"]

        # 戦闘開始時のメッセージ
        print("_"*20)
        print(f"エリートモンスターの{random_enemy_name}に遭遇した!")
        print(f"HP：{random_enemy_HP} ATK{random_enemy_ATK}\n{enemy_skill}")
        print("_"*20)
        print(f"{sutatus['name']}\nHP:{php[0]}  ATK{sutatus['ATK']}")
        print("_"*20)

        while True: 
            comand = input("コマンドを入力して下さい\nfight / ran\n")
            if comand == "fight" or comand == "f":
                turn = 1
                #リストの指定した場所（先頭）に数値を追加する
                ehp=[]
                ehp.insert(0,random_enemy_HP)

                while php[0] >=0:                    
                    pdamege =(php[0] - random_enemy_ATK)                    
                    
                    if elite ==2:#ガーゴイルの挙動
                        ehp.append(ehp[0]-1)
                        ehp.pop(0)
                        kuuhaku = input("Enterで続行")  
                        print(f"ターン{turn}\n{sutatus['name']}の攻撃！\n{random_enemy_name}は{1}のダメージを受けた") 
                        turn += 1  
                    else :
                        edamege = (ehp[0] - sutatus["ATK"])
                        ehp.append(edamege)#リストの末尾に追加
                        ehp.pop(0)   
                        kuuhaku = input("Enterで続行")  
                        print(f"ターン{turn}\n{sutatus['name']}の攻撃！\n{random_enemy_name}は{sutatus['ATK']}のダメージを受けた")
                        turn += 1  

                    if ehp[0] <= 0:
                        sutatus["G"]+= random_enemy_drop
                        print(f"{random_enemy_name}を倒した！\n{random_enemy_drop}Gを獲得!")
                        return print (f"残りHP：{php[0]}")
                    
                    #オークの挙動
                    if elite == 3:
                        if turn %2 ==1:
                            print(f"オークは動けない!") 
                        elif turn %2 ==0:
                            php.append(pdamege)
                            php.pop(0)
                            if php[0] <= 0:
                                php[0] = 0
                            print(f"{random_enemy_name}の攻撃！\n{sutatus['name']}は{random_enemy_ATK}のダメージを受けた\n{sutatus['name']}のHP:{php[0]}  {random_enemy_name}のHP:{ehp[0]}")
                    else:
                        php.append(pdamege)
                        php.pop(0)
                        if php[0] <= 0:
                            php[0] = 0
                        print(f"{random_enemy_name}の攻撃！\n{sutatus['name']}は{random_enemy_ATK}のダメージを受けた\n{sutatus['name']}のHP:{php[0]}  {random_enemy_name}のHP:{ehp[0]}")

                    if php[0] <= 0:
                        print(f"{sutatus['name']}は{random_enemy_name}に敗北した")
                        return "ゲームオーバー"

                    print("_"*20)  

            elif comand == "ran" or comand == "r":
                print(f"{sutatus['name']}は{random_enemy_name}から逃げ出した！")
                break
            else:
                print("無効なコマンドです")       
    else:
        print("エラー")


def rest_player():
    hp = sutatus["HP"]
    r = random.randrange(10,20,5)#10から15の範囲で5刻みの数字を出力する
    heal = int(hp / 100 * r)
    php[0] = (php[0] + heal)
    if php[0] > sutatus["HP"]:
        php[0] = sutatus["HP"]
    sutatus["froa"] += 1
    return (f"{name1}は休憩してHPを{heal}回復した\n{name1}のHP:{php[0]}/{sutatus['HP']}")


def treasue():#
    print("宝箱を見つけた！が、罠かもしれない...")
    r = random.randint(1,3)
    while True:
        comand = input(f"宝箱を開けますか？\nyes/no\n")

        if comand == "yes" or comand == "y":
            # print(r)
            if r ==3:
                print("宝箱はミミックだった")
                return battle(mimic)               
            else:
                g = random.randint(20,30)#Gの量をランダム化
                sutatus["G"] += g
                return (f"お宝を見つけた！{g}Gを獲得!\n____________________")
            

        if comand == "no" or comand == "n":
            return "先に進んだ"
        
        else:
            print("無効なコマンドです")
        

def move_player():
    move = random.uniform(1,100)#行動をランダムにするための数値
    # move = 90 #乱数を試す用
    if move <=80:
        if sutatus["froa"] < 10:
            return battle(enemy_status1)#モンスターのリスト名とIDを指定して特定モンスターの呼び出し
        elif sutatus["froa"] >= 11:
            return battle(enemy_status2)
    elif move <=100:
        return treasue()#宝箱の関数
    else:
        return "何も起こらなかった"


def boss(a):
    boss1 = boss_status[a]
    boss_status_name = boss1["name"]
    boss_status_hp = boss1["HP"]
    boss_status_atk = boss1["ATK"]
    boss_status_drop = boss1["dorop"]
    boss_status_skill = boss1["skill"]

    print("_"*20)
    print(f"ボスモンスターの{boss_status_name}に遭遇した!")
    print(f"HP：{boss_status_hp} ATK{boss_status_atk}\n{boss_status_skill}")
    print("_"*20)
    comand = input("コマンドを入力して下さい\nfight / ran\n")

        
    while True :    
        if comand == "fight" or comand == "f":
            turn = 1
            
            #リストの指定した場所（先頭）に数値を追加する
            ehp=[]
            ehp.insert(0,boss_status_hp)

            while php[0] >=0:
                
                fire = (php[0] - 50)
                pdamege =(php[0] - boss_status_atk)
                edamege = (ehp[0] - sutatus["ATK"])

                ehp.append(edamege)#リストの末尾に追加
                ehp.pop(0)             
                kuuhaku = input("Enterで続行")  

                print(f"ターン{turn}\n{sutatus['name']}の攻撃！\n{boss_status_name}は{sutatus['ATK']}のダメージを受けた")
                
                

                if ehp[0] <= 0:
                    sutatus["G"]+= boss_status_drop
                    print(f"{boss_status_name}を倒した！\n{boss_status_drop}Gを獲得!")
                    sutatus["froa"] += 1
                    return (f"残りHP：{php[0]}\n____________________")
                
                if boss1["id"] == 0: #ケルベロスの挙動
                    if ehp[0] <=50:
                        if boss_status_atk ==10:
                            True
                        elif boss_status_atk != 10:
                            boss_status_atk = 10
                            print("HPが1/3以下になったためATKが10下がった")
                            pdamege =(php[0] - boss_status_atk)
                    elif ehp[0] <= 100:
                        if boss_status_atk == 20:
                            True
                        elif boss_status_atk != 20:
                            boss_status_atk = 20
                            print("HPが2/3以下になったためATKが10下がった")
                            pdamege =(php[0] - boss_status_atk)

                if boss1["id"] == 1 and turn % 3 ==0: #ドラゴンの挙動
                    php.append(fire)
                    php.pop(0)
                    print(f"{boss_status_name}は炎を吐いた！\n{sutatus['name']}は50のダメージを受けた\n{sutatus['name']}のHP:{php[0]}  {boss_status_name}のHP:{ehp[0]}")
                    turn += 1
                
                else:
                    php.append(pdamege)
                    php.pop(0)
                    print(f"{boss_status_name}の攻撃！\n{sutatus['name']}は{boss_status_atk}のダメージを受けた\n{sutatus['name']}のHP:{php[0]}  {boss_status_name}のHP:{ehp[0]}")
                    turn += 1


                if php[0] <= 0:
                    print(f"{sutatus['name']}は{boss_status_name}に敗北した")
                    return "ゲームオーバー"

                print("_"*20)  

        elif comand == "ran" or comand == "r":
            print("この戦闘から逃げることはできない!")
            comand = input("コマンドを再入力して下さい\nfight / ran\n")

        else:
            print("無効なコマンドです")
            comand = input("コマンドを再入力して下さい\nfight / ran\n")

    
def shop():
    while True:
        print(f"現在の所持金:{sutatus['G']}\n現在のHP:{php[0]}/{sutatus['HP']}\n現在のATK:{sutatus['ATK']}")
        comand = input("強化する項目を入力してください\nHP / ATk\n1HP = 2g / 1ATK = 3G\n")
       
        if comand == "ATK" or comand =="atk" or comand == "a":       
            syouhi = int(input("使用する金額を入力して下さい\n1ATK = 3G\n"))
            if syouhi %3 ==0 and syouhi <= sutatus["G"]:
                sutatus["G"] -= syouhi
                sutatus["ATK"] += int(syouhi / 3)
                k = int(syouhi / 3)
                return (f"{sutatus['name']}のATKが{k}増加した！")
            elif syouhi %3 ==0 and syouhi >= sutatus["G"]:
                print(f"所持金が不足しています\n不足金額:{sutatus['G'] - syouhi}")
            elif syouhi %3 !=0 :
                print("金額は3刻みで入力して下さい")
            else:
                return print("エラー")
        elif comand == "HP"or comand == "hp" or comand == "h":
            syouhi = int(input("使用する金額を入力して下さい\n1HP = 2G\n"))
            if syouhi %2 ==0 and syouhi <= sutatus["G"]:
                sutatus["G"] -= syouhi
                sutatus["HP"] += int(syouhi / 2)
                php[0] = (php[0] + int(syouhi / 2))
                if php[0] > sutatus["HP"]:
                    php[0] = sutatus["HP"]
                k = int(syouhi / 2)
                return print(f"{sutatus['name']}の最大HPが{k}増加した！")

            elif syouhi %2 ==0 and syouhi >= sutatus["G"]:
                print(f"所持金が不足しています\n不足金額:{sutatus['G'] - syouhi}")       
            
            elif syouhi %2 !=0 :
                print("金額は2刻みで入力して下さい") 
        else:
            print("無効なコマンドです")


# メインループ
comand = ""
    # ただしいコマンドを入力するまで繰り返す 
while True:
    if php[0] <=0:
        print("ゲームを終了します")
        break

    
    if sutatus["froa"] == 21:
        print(f"ゲームクリア!!")
        print("ゲームを終了します")
        break

    print(f"第{sutatus["froa"]}層")    

    if sutatus["froa"] == 5 or sutatus["froa"] == 9 or sutatus["froa"] == 15 or sutatus["froa"] == 19:
        print("ショップを見つけた！\nショップでステータス強化ができます")
        froa = sutatus["froa"] 
        while froa == sutatus["froa"]:
            comand = input("コマンドを入力して下さい\nshop / move / rest / status/puit\n")
            if comand == "move" or comand == "m":
                print(move_player())
                sutatus["froa"] += 1
                break
            elif comand == "status" or comand == "s":
                print(show_status())
                
            elif comand == "quit" or comand =="q":
                print("ゲームを終了します")
                break
            elif comand == "shop" or comand =="sh":
                print(shop())    
            elif comand == "rest" or comand =="r":
                if php[0] == sutatus["HP"]:
                    print(f"{name1}のHPはMAXだ!")
                else:
                    print (rest_player())
            else:
                print ("無効なコマンドです")
    
    elif sutatus["froa"] ==10:
        print(boss(0))
        if php[0] <=0:
            print("ゲームを終了します")
            break
        #ケルベロスを指定
        php[0] += int(sutatus["HP"] * 0.6)
        if php[0] > sutatus["HP"]:
            php[0] = sutatus["HP"]
        print(f"{name1}は泉を見つけHPを{int(sutatus["HP"] * 0.6)}回復した\n{name1}のHP:{php[0]}/{sutatus['HP']}")

        
    elif sutatus["froa"] == 20:
        print(boss(1))#ドラゴンを指定
    # if sutatas["froa"] == 11:#ボスクリア後の回復挙動
        
        
    else: 
        comand = input("コマンドを入力して下さい\nmove / rest / status / quit\n")
        if comand == "move" or comand == "m":
            print(move_player())
            sutatus["froa"] += 1
        elif comand == "status" or comand == "s":
            print(show_status())
        elif comand == "quit" or comand == "q":
            print("ゲームを終了します")
            break
            
        elif comand == "rest" or comand == "r":
            if php[0] == sutatus["HP"]:
                print(f"{name1}のHPはMAXだ!")
                sutatus["froa"] += 1
            else:
                print (rest_player())
        else:
            print ("無効なコマンドです")
