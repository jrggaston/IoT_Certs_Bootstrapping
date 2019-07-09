import random
import hashlib
import time

#funcion to generate a random number of four bytes
def generate_random_number():
   random_int = random.randint(0,255) + random.randint(0,255) * 2**8 + random.randint(0,255) * 2**16 + random.randint(0,255)* 2**24
   
   return random_int

#function to calculate the hash that solves the challenge.
def resolve_challenge(snr, factory_date, challenge):

   aux = str(snr) + str(factory_date) + str(challenge)
   hash = hashlib.sha256(aux).hexdigest()

   return hash


#function to check if the challenge received is valid.
def check_challenge(response, solution, timeout):

   result = False
   current_time = time.time()

   if ((response == solution) and (current_time <= timeout)):
      result = True
   else:
      result = False

   return result



