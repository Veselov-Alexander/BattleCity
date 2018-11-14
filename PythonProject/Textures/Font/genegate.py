letter = list()

alph = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

i = 0
with open("Textures/alphabet", encoding='utf-8') as file:
    for line in file:
        if line != "\n":
            letter.append(line)
        else:
            letter[-1] = letter[-1][:-1]
            with open("Font/" + alph[i], "w+", encoding='utf-8') as save:
                save.write('\n')
                for l in letter:
                    save.write(l)
                save.close()
            letter.clear()
            i += 1