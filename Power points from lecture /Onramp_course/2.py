# Problem Set 7
# SI 106

# These import statements are necessary for the tests to run in your code. Do not change them!
import unittest

##########

## [PROBLEM 1]

fall_list = ["leaves","apples","autumn","bicycles","pumpkin","squash","excellent"]
print(fall_list)

## [PROBLEM 2]

food_amounts = [{"sugar_grams":245,"carbohydrate":83,"fiber":67},{"carbohydrate":74,"sugar_grams":52,"fiber":26},{"fiber":47,"carbohydrate":93,"sugar_grams":6}]

## [PROBLEM 3]

# Write code here.



## [PROBLEM 4]

letter_values = {'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f':4, 'g': 2, 'h':4, 'i':1, 'j':8, 'k':5, 'l':1, 'm':3, 'n':1, 'o':1, 'p':3, 'q':10, 'r':1, 's':1, 't':1, 'u':1, 'v':8, 'w':4, 'x':8, 'y':4, 'z':10}



## [PROBLEM 5]

nl = [["nested","data","is"],["really","fun"],[11,["hooray","hooray"],"yay"]]


## [PROBLEM 6]

# Define your function here.
# Remember, it should be called convert_nums, and it should accept
# 1 input, representing a number of hours.






## [PROBLEM 7]

## Define your function sort_nested_lists here as the instructions describe.




############# BELOW THIS LINE IS CODE FOR PROBLEM SET TESTS #####################
################### DO NOT CHANGE CODE BELOW THIS LINE ##########################
class Problem1(unittest.TestCase):

    def test1(self):
        self.assertEqual(sorted_fall_list, ['squash', 'pumpkin', 'leaves', 'excellent', 'bicycles', 'autumn', 'apples'], "sorted_fall_list is not accurately sorted")

class Problem2(unittest.TestCase):

    def test2(self):
        self.assertEqual(sorted_sugar,[{'carbohydrate': 93, 'fiber': 47, 'sugar_grams': 6}, {'carbohydrate': 74, 'fiber': 26, 'sugar_grams': 52}, {'carbohydrate': 83, 'fiber': 67, 'sugar_grams': 245}])
    def test3(self):
        self.assertEqual(raw_carb_sort,[{'carbohydrate': 83, 'fiber': 67, 'sugar_grams': 245}, {'carbohydrate': 93, 'fiber': 47, 'sugar_grams': 6}, {'carbohydrate': 74, 'fiber': 26, 'sugar_grams': 52}])

class Problem3(unittest.TestCase):

    def test4(self):
        self.assertEqual(short_z_words,['zoo', 'zoa', 'zit', 'zip', 'zig', 'zek', 'zee', 'zed', 'zax', 'zap', 'zag', 'wiz', 'lez', 'fiz', 'fez', 'coz', 'biz', 'azo', 'adz'], "short_z_words does not have the correct value")


class Problem4(unittest.TestCase):

    def test5(self):
        self.assertEqual(best_z_words[:3],['zyzzyvas', 'zyzzyva', 'pizazzy'],"best_z_words does not have the correct value -- check out how you're sorting them")
        self.assertEqual("jazzlike" in best_z_words[3:],True,"missing something from your best_z_words")
        self.assertEqual("pizazzes" in best_z_words[3:],True,"missing something from your best_z_words")
        self.assertEqual("pazazzes" in best_z_words[3:],True,"missing something from your best_z_words")
        self.assertEqual("jazzlike" in best_z_words[3:],True,"missing something from your best_z_words")
        self.assertEqual("quizzing" in best_z_words[6:], True, "missing something from your best_z_words")


class Problem5(unittest.TestCase):

    def test6(self):
        self.assertEqual(second_elems, ['data', 'fun', ['hooray', 'hooray']], "second_elems does not have the correct value")

class Problem6(unittest.TestCase):

    def test7(self):
       self.assertEqual(convert_nums(1),(60,3600),"incorrect output of function with input 1")
       self.assertEqual(convert_nums(50),(60*50,3600*50), "incorrect output of function with input 50")
       self.assertEqual(convert_nums(0), (0,0), "incorrect output of function with input 0")

class Problem7(unittest.TestCase):

    def test8(self):
        self.assertEqual(sort_nested_lists([[2,3],[45,100,2],[536],[103,2,8]]),[[2,3],[103,2,8],[45,100,2],[536]],"testing a case of a sorted nested list -- check out your function output")
        self.assertEqual(sort_nested_lists([[1],[50],[6]]),[[1],[6],[50]],"testing a case of a sorted nested list -- check out your function output")
        self.assertEqual(sort_nested_lists([[],[1]]),[[],[1]],"testing a case of a sorted nested list -- check out your function output")
        self.assertEqual(sort_nested_lists([[0],[-4,-5,-7],[-56,4]]),[[-56,4],[-4,-5,-7],[0]],"testing a case of a sorted nested list -- check out your function output")

if __name__ == '__main__':
    unittest.main(verbosity=2)
