import itertools
from functools import reduce
import operator

def product(iterable):
  return reduce(operator.mul, iterable, 1)

class Line():
  def __init__(self, odds, success):
    self.odds = odds
    self._success = success

  def success(self):
    return self._success

class Bet():
  def __init__(self, line, stake, include_stake = True):
    self.line = line
    self.stake = stake
    self.include_stake = include_stake

  def win(self):
    return self.line.success()

  def returns(self):
    if not self.win():
      return 0
    return self.stake * (self.line.odds + (1 if self.include_stake else 0))

class AccumulatedLine(Line):
  def __init__(self, lines):
    self.odds = product((1 + x.odds) for x in lines) - 1
    self.lines = lines

  def success(self):
    return all(x.success() for x in self.lines)

class Accumulator(Bet):
  def __init__(self, lines, stake, include_stake = True):
    self.line = AccumulatedLine(lines)
    self.stake = stake
    self.include_stake = include_stake

class AccumulatorSelection():
  def __init__(self, lines, stake, include_stake = True):
    self.lines = lines
    self.stake = stake
    self.include_stake = include_stake
    self.accumulators = None

  def get_accumulators(self):
    if self.accumulators is None:
      self.__build_accumulators()

    return self.accumulators

  def total_stake(self):
    return self.stake * len(self.get_accumulators())

  def returns(self):
    return sum(a.returns() for a in self.get_accumulators())

class SuperHeinz(AccumulatorSelection):
  def _AccumulatorSelection__build_accumulators(self):
    self.accumulators = []
    # don't include singles
    for i in range (2,8):
      for combination in itertools.combinations(self.lines, i):
        accumulator = Accumulator(combination, self.stake, self.include_stake)
        self.accumulators.append(accumulator)

class FixedFolds(AccumulatorSelection):
  def __init__(self, lines, stake, folds, include_stake = True):
    super().__init__(lines, stake, include_stake)
    self.folds = folds

  def _AccumulatorSelection__build_accumulators(self):
    self.accumulators = []
    for combination in itertools.combinations(self.lines, self.folds):
      accumulator = Accumulator(combination, self.stake, self.include_stake)
      self.accumulators.append(accumulator)
