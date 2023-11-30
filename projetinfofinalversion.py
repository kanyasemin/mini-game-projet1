import random

import curses
stdscr = curses.initscr()
curses.noecho()

#tester si c (coordonnée) correspond à une case de m vide
def vide(m,coord):
    x,y=coord
    #test si coordonnées existent
    if x<0 or y<0 or x>len(m)-1 or y>len(m[0])-1:
        return False
    if m[x][y]==1:
        return False
    return True

def voisinage(coord):
    x,y=coord
    return {(x+1,y),(x-1,y),(x,y+1),(x,y-1)}

def test_map(m):
    for i in range(len(m)):
        for j in range (len(m[0])):
            if m[i][j]==3: s=(i,j)
            if m[i][j]==2: p_1=(i,j)
            if m[i][j]==4: p_2=(i,j)
    cc_1={p_1}
    voisins={v for v in voisinage(p_1) if vide(m,v)}
    while len(voisins)>0:
        cc_1=cc_1 | voisins
        voisins=set()
        for c in cc_1:
            for v in voisinage(c):
                if vide(m,v):
                    voisins.add(v)
        h=voisins & cc_1
        voisins=voisins - h
    cc_2={p_2}
    voisins={v for v in voisinage(p_2) if vide(m,v)}
    while len(voisins)>0:
        cc_2=cc_2 | voisins
        voisins=set()
        for c in cc_2:
            for v in voisinage(c):
                if vide(m,v):
                    voisins.add(v)
        h=voisins & cc_2
        voisins=voisins - h
    return s in cc_1 and s in cc_2

def zero(n,m):
    return [[0]*m for i in range (n)]

def generate_random_map(size_map,proportion_wall):
    m=zero(size_map[0],size_map[1])
    e=set()
    m[random.randint(0,size_map[0]-1)][random.randint(0,size_map[1]-1)]=2
    #permet de créer l'entrée de la map avec des coordonnées aléatoires
    h=random.randint(0,size_map[0]-1)
    k=random.randint(0,size_map[1]-1)
    while m[h][k]!=0:
        h=random.randint(0,size_map[0]-1)
        k=random.randint(0,size_map[1]-1)
    m[h][k]=4
    x=random.randint(0,size_map[0]-1)
    y=random.randint(0,size_map[1]-1)
    while m[x][y]!=0:
        #vérifier que les coordonnées de la sortie sont différentes de celles de l'entrée
        x=random.randint(0,size_map[0]-1)
        y=random.randint(0,size_map[1]-1)
    m[x][y]=3
    for i in range(int(size_map[0]*size_map[1]*proportion_wall)):
        g=random.randint(0,size_map[0]-1)
        h=random.randint(0,size_map[1]-1)
        while m[g][h]!=0:
            #vérifier que les coordonnées du mur sont bien des cases vides (ni l'entrée ni la sortie)
            g=random.randint(0,size_map[0]-1)
            h=random.randint(0,size_map[1]-1)
        m[g][h]=1
    while test_map(m)==False:
        m=generate_random_map(size_map,proportion_wall)
    return m

def create_new_level(p_1,p_2,m,obj,bomb,size_map,proportion_wall):
    m=generate_random_map(size_map,proportion_wall)
    obj=create_objects(random.randint(10,20),m)
    bomb=create_bombs(random.randint(4,8),m)
    for i in range(len(m)):
        for j in range(len(m[0])):
            if m[i][j]==2: p_1['x'],p_1['y']=i,j
            if m[i][j]==4: p_2['x'],p_2['y']=i,j
    return m,obj,bomb        
    

def create_objects(nb_objects,m):
    e=set()
    for i in range(nb_objects):
        g=random.randint(0,len(m)-1)
        h=random.randint(0,len(m[0])-1)
        if m[g][h]==0: e.add((g,h))
    return e

def update_objects(p_1,p_2,objects):
    if (p_1['x'],p_1['y']) in objects:
        objects.discard((p_1['x'],p_1['y']))
        p_1['score']+=1
    if (p_2['x'],p_2['y']) in objects:
        objects.discard((p_2['x'],p_2['y']))
        p_2['score']+=1
    return objects

def create_bombs(nb_bombs,m):
    e=set()
    for i in range(nb_bombs):
        g=random.randint(0,len(m)-1)
        h=random.randint(0,len(m[0])-1)
        if m[g][h]==0: e.add((g,h))
    return e

def update_bombs(p_1,p_2,bombs):
    if (p_1['x'],p_1['y']) in bombs:
        bombs.discard((p_1['x'],p_1['y']))
        p_1['bombe']+=1
    if (p_2['x'],p_2['y']) in bombs:
        bombs.discard((p_2['x'],p_2['y']))
        p_2['bombe']+=1
    return bombs

def delete_all_walls(m,pos):
    x,y=pos
    for i in range(x-1,x+2):
        for j in range(y-1,y+2):
            if abs(j)<len(m[0]) and abs(i)<len(m) and m[abs(i)][abs(j)]==1 : m[abs(i)][abs(j)]=0
    return m
   
def display_map_and_char_and_objects_and_bombs(m,d,p_1,p_2,objects,bombs):
    curses.start_color()
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(1, curses.COLOR_RED,curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE,curses.COLOR_BLACK)
    for i in range(len(m)):
        for j in range(len(m[0])):
            if i==p_1['x'] and j==p_1['y']:
                #print(p['char'], end='')
                stdscr.addstr(i, j, p_1['char'],curses.color_pair(1))
            elif i==p_2['x'] and j==p_2['y']:
                #print(p['char'], end='')
                stdscr.addstr(i, j, p_2['char'],curses.color_pair(3))
            elif (i,j) in objects:
                #print('.', end='')
                stdscr.addstr(i, j, '.')
            elif (i,j) in bombs:
                #print('*',end='')
                stdscr.addstr(i, j, '*')
            else :
                #print(d[m[i][j]], end='')
                if m[i][j]==1:
                    stdscr.addstr(i, j, d[m[i][j]], curses.color_pair(2))
                else: stdscr.addstr(i,j,d[m[i][j]])
        #print()
    stdscr.addstr(len(map) +1,0,'J1',curses.color_pair(1))
    stdscr.addstr(len(map) + 2,0,'SCORE = %d' %(p_1['score']))
    stdscr.addstr(len(map) + 3,0,'BOMBE = %d' %(p_1['bombe']))
    stdscr.addstr(len(map) +1,15,'J2',curses.color_pair(3))
    stdscr.addstr(len(map) + 2,15,'SCORE = %d' %(p_2['score']))
    stdscr.addstr(len(map) + 3,15,'BOMBE = %d' %(p_2['bombe']))

def create_perso(m,k):
    for i in range(len(m)):
        for j in range (len(m[0])):
            if k==1 and m[i][j]==2:
                return {"char":"♫","x":i,"y":j,'score':0, 'bombe':0}
            if k==2 and m[i][j]==4:
                return {"char":"♥","x":i,"y":j,'score':0, 'bombe':0}

map=generate_random_map((6,30),0.4)
dico={0:' ',1:'#', 2:' ',3:'X', 4:' '}
perso_1=create_perso(map,1)
perso_2=create_perso(map,2)
objects=create_objects(random.randint(10,20),map)
bombs=create_bombs(random.randint(4,8),map)

    
def update_p(letter,p_1,p_2,m):
    if letter=='z' and p_1['x']>0 and m[p_1['x']-1][p_1['y']]!=1:p_1["x"]-=1
    elif letter=='q'and p_1['y']>0 and m[p_1['x']][p_1['y']-1]!=1: p_1["y"]-=1
    elif letter=='s'and p_1['x']<len(m)-1 and m[p_1['x']+1][p_1['y']]!=1: p_1["x"]+=1 
    elif letter=='d'and p_1['y']<len(m[0])-1 and m[p_1['x']][p_1['y']+1]!=1: p_1['y']+=1
    elif p_1['bombe']>0 and letter=='e' :
        m=delete_all_walls(m,(p_1['x'],p_1['y']))
        p_1['bombe']-=1
        x,y=p_1['x'],p_1['y']
        if p_2['x']==x and p_2['y']==y: p_2['score']-=1
        for i in range(x-1,x+2):
            for j in range(y-1,y+2):
                if abs(j)<len(m[0]) and abs(i)<len(m) and abs(i)==p_2['x'] and abs(j)==p_2['y'] :
                    p_2['score']-=1
    elif letter=='i' and p_2['x']>0 and m[p_2['x']-1][p_2['y']]!=1:p_2["x"]-=1
    elif letter=='j'and p_2['y']>0 and m[p_2['x']][p_2['y']-1]!=1: p_2["y"]-=1
    elif letter=='k'and p_2['x']<len(m)-1 and m[p_2['x']+1][p_2['y']]!=1: p_2["x"]+=1 
    elif letter=='l'and p_2['y']<len(m[0])-1 and m[p_2['x']][p_2['y']+1]!=1: p_2['y']+=1
    elif p_2['bombe']>0 and letter=='o' :
        m=delete_all_walls(m,(p_2['x'],p_2['y']))
        p_2['bombe']-=1
        x,y=p_2['x'],p_2['y']
        if p_1['x']==x and p_1['y']==y: p_1['score']-=1
        for i in range(x-1,x+2):
            for j in range(y-1,y+2):
                if abs(j)<len(m[0]) and abs(i)<len(m) and abs(i)==p_1['x'] and abs(j)==p_1['y'] : p_1['score']-=1
    return p_1,p_2

#d=input("Quel déplacement ?")
#print(display_map_and_char_and_objects_and_bombs(map,dico,(update_p(d,perso_1,perso_2,map)),objects,bombs))

#while perso_1['score']<10 and perso_2['score']<10:
    #lettre= input("Quel déplacement ?")
    #p_1,p_2=update_p(lettre,perso_1,perso_2,map)
    #if map[p_1['x']][p_1['y']]==3 or map[p_2['x']][p_2['y']]==3:
        #map,objects,bombs=create_new_level(p_1,p_2,map,objects,bombs,(6,30),0.4)
    #h=update_objects(p_1,p_2,objects)
    #k=update_bombs(p_1,p_2,bombs)
    #print(display_map_and_char_and_objects_and_bombs(map,dico,p_1,p_2,h,k))


display_map_and_char_and_objects_and_bombs(map,dico,perso_1,perso_2,objects,bombs)
while perso_1['score']<10 and perso_2['score']<10:
    lettre= stdscr.getkey()
    stdscr.erase()
    update_p(lettre,perso_1,perso_2,map)
    #stdscr.addstr(len(map) + 2, 0,"erreur, vous n'avez pas indiqu´e un caract`ere dans {z,q,s,d}")
    if map[perso_1['x']][perso_1['y']]==3 or map[perso_2['x']][perso_2['y']]==3:
        map,objects,bombs=create_new_level(perso_1,perso_2,map,objects,bombs,(6,30),0.4)
    update_objects(perso_1,perso_2,objects)
    update_bombs(perso_1,perso_2,bombs)
    display_map_and_char_and_objects_and_bombs(map,dico,perso_1,perso_2,objects,bombs)
    stdscr.refresh()
