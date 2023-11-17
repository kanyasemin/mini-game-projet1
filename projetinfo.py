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
            if j==p['x'] and i==p['y']: print(p['char'], end='')
            else :print(d[m[i][j]], end='')
        print()
    return ''
perso=create_perso((3,4))
print(display_map_and_char(map,dico,perso))

d=input("Quel déplacement ?")
# on dit que 'z' déplace le perso vers le haut, 'q' vers la gauche, 's' vers le bas et 'd' vers la droite
def update_p(letter,p,m):
    if letter=='z' and p['y']>0:p["y"]-=1
    elif letter=='q'and p['x']>0: p["x"]-=1
    elif letter=='s'and p['y']<len(m)-1: p["y"]+=1 
    elif letter=='d'and p['x']<len(m[0])-1: p['x']+=1
    #on fait une autre elif afin d'afficher le maps encore une fois 
    else: update_p(input("Quel déplacement (z,q,s ou d stp)?"),p,m)
    return p

#rajouter test dans update pour s'arrêter devant le mur (même principe que les limites))

# on fait ça pour le 'z ': m[p['y']-1][p['x']]
print(display_map_and_char(map,dico,(update_p(d,perso))))

while True:
    lettre= input("Quel lettre?")
    print(display_map_and_char(map,dico,(update_p(lettre,perso,map))))
    
    
