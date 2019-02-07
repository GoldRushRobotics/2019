'''

This is the main function. EVERYTHING should be called from here. This should be the only python thingy running on game day.


'''

import time

import movement as mov
import FindMyHome as home
import FindMeContours as cont



# This is crap, but can be used to test FindMeContours
if __name__ == "__main__":

<<<<<<< HEAD
=======
<<<<<<< Updated upstream
>>>>>>> 5260c724b530e764e63d99257073e48c24688c8e
  vs,args = cont.setup()

  time.sleep(2.0)

  cont.loop(vs,args)

  cont.death(vs,args)
<<<<<<< HEAD
=======
=======
    vs, args = cont.setup()

#    cont.sleep(2.0)

    cont.loop(vs, args)

    cont.death(vs, args)
>>>>>>> Stashed changes
>>>>>>> 5260c724b530e764e63d99257073e48c24688c8e

