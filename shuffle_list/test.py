from expyriment import design

# TEST : With the old version : Warnings Warning: Could not find an appropriate trial randomisation!
# The new version corrects this (and runs quicker even if that wasn't my goal)

# Print every of the 500 shuffle attempts and print a final int that represents the number of successfull attempts
# From my few tries, old version = 0, new version = 500

def is_valid(l, max_rep=2):
   last = l[0]
   streak = 1
   for elem in l[1:]:
       if elem == last:
           streak += 1
       else:
           streak = 1
       if streak > max_rep:
           return False
       last = elem
   return True


j=0


for i in range(500):
   d = {"condition": ["A", "B"]}


   bl = design.Block()
   bl.add_trials_full_factorial(d, copies=100)
   bl.shuffle_trials(method=0, max_repetitions=3)


   lines = bl.design_as_text.split("\n")
   elems = [l.split(",")[2] for l in lines][1:] #parse only A/B (index 0 is str 'condition')

   print(elems)
   if is_valid(elems, 3):
       j+=1


print(j)