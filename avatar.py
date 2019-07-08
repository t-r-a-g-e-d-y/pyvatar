import random as r
a=[f'\x1b[48;5;{r.randint(0,255)}m  ','\x1b[48;5;254m  ']
b=lambda:r.choice(a)
c=a[1]*7
d='\x1b[0m\n'
e=d.join(['{d}{a}{b}{c}{b}{a}{d}'.format(a=b(),b=b(),c=b(),d=a[1]) for _ in range(5)])
print(c,e,c,sep=d,end=d)