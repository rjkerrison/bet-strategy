from bets import SuperHeinz, Line, FixedFolds

def test_qualifier_superheinz():
  denmark = Line(8/11, True)
  croatia = Line(1/2, True)
  spain = Line(1/2, True)
  switzerland = Line(1, True)
  mexico = Line(10/11, True)
  colombia = Line(4/11, True)
  russia = Line(4/11, True)

  accumulator = SuperHeinz([
    denmark,
    croatia,
    spain,
    switzerland,
    mexico,
    colombia,
    russia,
  ], 0.25, include_stake = False)

  print('all', accumulator.returns())

  colombia._success = False

  print('not colombia', accumulator.returns())

  switzerland._success = False

  print('not colombia, not switzerland', accumulator.returns())

  switzerland._success = True
  spain._success = False

  print('not colombia, not spain', accumulator.returns())

def test_winner_folds():
  france = Line(3/10, True)
  uruguay = Line(4/6, True)
  argentina = Line(8/13, False)
  brazil = Line(2/7, True)
  germany = Line(1/3, True)

  lines = [
    france,
    uruguay,
    argentina,
    brazil,
    germany
  ]

  four_folds = FixedFolds(lines, 1.00, 4, include_stake = False)
  three_folds = FixedFolds(lines, 0.50, 3, include_stake = False)

  print('four folds now that argentina ruined everything', four_folds.returns(), four_folds.total_stake())
  print('three folds now that argentina ruined everything', three_folds.returns(), three_folds.total_stake())

  germany._success = False

  print('four folds if germany also bails', four_folds.returns())
  print('three folds if germany also bails', three_folds.returns())

test_qualifier_superheinz()
