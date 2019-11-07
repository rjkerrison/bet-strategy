class Bet():
  def __init__(self, probability, returns):
    self.probability = probability
    self.returns = returns

class StandardBet(Bet):
  def __init__(self, probability):
    super(**find_returns_from_probability(probability))

def co_prime(a, b):
  a, b = min(a, b), max(a, b)

  if a == 1:
    return True
  if b % a == 0:
    return False

  return co_prime(a, b % a)

def acceptable_numerator_range(denominator):
  if denominator == 1:
    return list(range(1, 21)) + [25, 33, 50, 75, 100, 150, 200, 250, 300, 400, 500, 1000]
  if denominator == 2:
    return range(1, 20)
  if denominator == 3:
    return range(1, 12)
  if denominator == 4:
    return range(1, 16)
  if denominator == 5:
    return range(1, 20)
  if denominator == 10:
    return range(1, 15)

  return range(1, denominator * 2)

def find_returns_from_probability(probability):
  min_diff = 1
  closest_return = (None, None)

  for denominator in range(1, 11):
    for i in acceptable_numerator_range(denominator):
      if co_prime(i, denominator):
        fraction = denominator / (denominator + i)
        if fraction > probability*1.02:
          # print(i, denominator, fraction, probability)

          current_diff = fraction - probability
          if current_diff < min_diff:
            if fraction < probability*1.05:
              return probability, (i, denominator)

            min_diff = current_diff
            closest_return = (i, denominator)

  return probability, closest_return

def find_returns_from_probability2(probability):
  adjusted_probability = probability * 1.1
  target_reciprocal = 1 / adjusted_probability

  min_diff = 1
  closest_return = (None, None)

  for denominator in range(1, 5):
    for numerator in acceptable_numerator_range(denominator):
      if co_prime(numerator, denominator):
        current_diff = denominator * target_reciprocal / (numerator + denominator) - 1
        if current_diff < 0:
          print(f'breaking on {denominator}, {numerator}')
          break
        if current_diff < min_diff:
          min_diff = current_diff
          closest_return = (numerator, denominator)

  return probability, closest_return

def co_prime_test():
  for i in range(3, 10):
    for j in range(2, i):
      print(i, j, co_prime(i, j))

for prob in [0.18, 0.2, 0.23, 0.3, 0.33, 0.4, 0.47, 0.52, 0.63, 0.7, 0.9, 0.94]:
  a, b = find_returns_from_probability2(prob)
  print(a, b, a * (1 + b[0]/b[1]))
