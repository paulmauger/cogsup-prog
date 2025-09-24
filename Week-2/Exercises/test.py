

dct = {1:4, 10:11}

print(dct.keys())

print(dct.values())

print(dct.items())

 
#clé:valeur, valeur:clé
dct2 = {4:1, 10:11}

dct2_nous = {
    v:k for (k,v) in dct.items()
}

print(dct2 == dct2_nous)

dct3 = {
    k:v**2 for (k,v) in dct.items() if "pomme" in k
}

print(dct3)