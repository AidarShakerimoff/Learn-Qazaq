class State:
  def __init__(self, letters_left, time, time_for_word, num_errors, theme, gender):
    self.letters_left = letters_left    # array of 26 elements, each element is either 0 or 1 indicating whether a corresponding letter is already exlpored 
    self.time = time    # indicates how much time passed from the beginning of an episode (10 words)
    self.time_for_word = time_for_word    # how much time was spent by student on the recent word 
    self.num_errors = num_errors    # indicates how much problematic errors (those which are still written wrongly by a student) left
    self.theme = theme
    self.gender = gender

  def print_info(self):
    print("current state: ")
    print("list of unexplored letters: " + str(self.letters_left))
    print("time total: " + str(self.time))
    print("time for recent word: " + str(self.time_for_word))
    print("current number of errors: " + str(self.num_errors))
    print("current theme" + str(self.theme))
    print("gender" + str(self.gender))
    print("")

