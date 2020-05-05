
import pulp
import pandas as pd
import math

def get_nutrion(eat1,eat2,eat3,eat4):
        # 数理最適化問題（最大化）を宣言
        prob = pulp.LpProblem("Problem-1", pulp.LpMinimize)

        #　栄養素一覧
        origin_data = pd.read_csv('nutriton/data/nutriton_choice.csv')
        origin_data = origin_data.sample(frac=1)
        
        #　嫌いな料理
        nutriton_table = origin_data[origin_data['料理名'] != 'ちゃんちゃん焼き']
        nutriton_table = nutriton_table[nutriton_table['料理名'] != 'オムレツ']
        nutriton_table = nutriton_table[nutriton_table['料理名'] != '鮭のホイル焼き']

        nutriton_table = nutriton_table.reset_index()

        #　全料理数
        lenge = len(nutriton_table) 

        #　栄養素の種類
        nutriton_header = nutriton_table.columns.values.tolist()
        nutriton_header.remove('index')
        nutriton_header.remove('料理名')
        nutriton_header.remove('エネルギーkcal')
        nutriton_header.remove('食塩相当量')

        #　食べた料理
        if len(eat1) != 0:
                finished_food1 = origin_data[origin_data['料理名'] == eat1]
        else:
                finished_food1 = pd.DataFrame()
        if len(eat2) != 0:
                finished_food2 = origin_data[origin_data['料理名'] == eat2]
        else:
                finished_food2 = pd.DataFrame()
        if len(eat3) != 0:
                finished_food3 = origin_data[origin_data['料理名'] == eat3]
        else:
                finished_food3 = pd.DataFrame()
        if len(eat4) != 0:
                finished_food4 = origin_data[origin_data['料理名'] == eat4]
        else:
                finished_food4 = pd.DataFrame()
        your_food = [finished_food1,finished_food2,finished_food3,finished_food4]

        #　１日の必要量
        required_amount = pd.read_csv('nutriton/data/required_amount.csv')

        # 変数の定義
        x = {}
        for i in range(lenge):
                x[i] = pulp.LpVariable("x({:})".format(i), 0, 1, pulp.LpInteger)

        # 目的関数
        prob += pulp.lpSum([x[i] for i in range(lenge)])

        # 制約条件
        required_list = ['','']
        for name in nutriton_header:
                nutriton = nutriton_table[name]                
                required_nutriton = required_amount[name].values[0]
                if not finished_food1.empty:
                        finished_food_val = finished_food1[name]
                        required_nutriton = required_nutriton - finished_food_val.values[0]
                if not finished_food2.empty:
                        finished_food_val = finished_food2[name]
                        required_nutriton = required_nutriton - finished_food_val.values[0]
                if not finished_food3.empty:
                        finished_food_val = finished_food3[name]
                        required_nutriton = required_nutriton - finished_food_val.values[0]
                if not finished_food4.empty:
                        finished_food_val = finished_food4[name]
                        required_nutriton = required_nutriton - finished_food_val.values[0]
                if required_nutriton <= 0:
                        required_nutriton = 0

                required_list.append(math.floor(required_nutriton))
                prob += pulp.lpSum([x[i]*v for i,v in nutriton.iteritems()]) >= required_nutriton

        prob += pulp.lpSum([x[i] for i in range(lenge)]) >= 3

        # 実行
        status = prob.solve()

        # 結果の表示
        result = pd.DataFrame()
        for i in range(lenge):
                if x[i].value() == 1:
                        result = pd.concat([result, round(nutriton_table[i:i+1],1)], axis=0)

        # 既存の栄養
        finish_food = pd.DataFrame()
        for i in your_food:
                finish_food = pd.concat([finish_food, i], axis=0)

        return result,finish_food,required_list