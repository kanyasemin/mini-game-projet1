#afficher une carte à partir d'une matrice et d'un dictionnaire

def display_map(m,d):
    for i in m:
        for j in i:
            print(d[j], end='')
        print()
    return ''

map=[[0,0,0,1,1],[0,0,0,0,1],[1,1,0,0,0],[0,0,0,0,0]]
dico={0:' ',1:'#'}
print(display_map(map,dico))

#pour faire un dictionnaire à partir des coordonnées du personnages et de comment on représente le personnage dans l'espace
def create_perso(dep):
    return {"char":"o","x":dep[0],"y":dep[1]}

#print(create_perso((0,0)))

#pour afficher la carte avec le personnage représenté
def display_map_and_char(m,d,p):
    for i in range(len(m)):
        for j in range(len(m[0])):
            if i==p['x'] and j==p['y']: print(p['char'], end='')
            else :print(d[m[i][j]], end='')
        print()
    return ''
perso=create_perso((3,4))
print(display_map_and_char(map,dico,perso))

d=input("Quel déplacement ?")
# on dit que 'z' déplace le perso vers le haut, 'q' vers la gauche, 's' vers le bas et 'd' vers la droite
def update_p(letter,p):
    if letter=='z' and p['x']!=0:p["x"]-=1
    elif letter=='q'and p['y']!=0: p["y"]-=1
    elif letter=='s'and p['x']!=-1: p["x"]+=1
    elif letter=='d'and p['x']!=-1: p['y']+=1
    else: update_p(input("Quel déplacement (z,q,s ou d stp)?"),p)
    return p



print(display_map_and_char(map,dico,(update_p(d,perso))))

while True:
    lettre= input("Quel lettre?")
    print(display_map_and_char(map,dico,(update_p(lettre,perso))))
    
    
