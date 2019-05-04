import sqlite3

'''''
string = ''Касательная, прикосновение, соприкосновение, касательный; прилагательное, предположение, обложение, полагать, изложение, налагать, разлагать, полог. Нагар, нагореть, нагорать, загорелый, изгарь, угорать, угореть, горючий, выгарки, угар; поклон, уклон, склонность, наклониться, закланяться, наклоняться. Зорька, лучезарный, зарница, зарево, озарение, заревой, зоревать, зарничный, озарять, зорянка. Вырастить, выросла, водоросль, отрастить, нарастание, выросший, росток, нарост, ростовщик, заросль, Ростов, поросль, Ростислав, отрасль, наращение, растительность, недоросль, рост. Скачок, проскакать, поскакать, подскакать, проскочить, подскочить, скачу, заскочить. Плавучий, плавучесть, плавательный, пловец, пловчиха, плывун, жук-плавунец. Обмакнуть, непромокаемый, вымокнуть, обмакивать, промокание, промокашка, промокательный. Равный, равномерный, ровный, равнозначный, уравнение, уровень, равнина, подровнять, подравнять''
string = string.lower()
string = string.replace(';', ',').replace('.', ',')
array = string.split(', ')
print(array)
'''''
with open('text_scratch', 'r') as f:
    array = f.read().split('\n')
    with sqlite3.connect(r'src/rus_slovo.db') as con:
        cur = con.cursor()
        for answer in array:
            test = list(cur.execute(f"SELECT * FROM orthography WHERE answer='{answer}'"))
            cur.fetchall()
            if not test:
                print(answer)
                word = input()
                wrong = word.replace('..', input())
                print(word, answer, wrong, sep='/')
                sql = f"INSERT INTO orthography (word, answer, wrong) VALUES ('{word}', '{answer}', '{wrong}')"
                try:
                    cur.execute(sql)
                except Exception as e:
                    print(e)
        con.commit()
        cur.close()
