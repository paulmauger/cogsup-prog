from expyriment import design
import expyriment.design.randomize as rd

# TEST 2 : 
# Same as test1 but for our original code (using shuffle_list instead of shuffle_trials)
# (plus I realized I don't need the is_valid function just to add the bools)

# From my few runs, old version around 300, new version 500

j = 0


for i in range(500): 
    l = ["A"] * 100 + ["B"] * 100


    shuffled_bool = rd.shuffle_list(l, max_repetitions=3)


    print(l)
    print(shuffled_bool)
    if shuffled_bool is True: 
        j+=1

print(j)



