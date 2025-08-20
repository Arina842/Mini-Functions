 def round_5(number):
      """Округляет число до ближайшего кратного 5.

      Args:
        number: Целое число для округления.

      Returns:
        Округленное число.
      """
      ost = number % 5
      if ost < 2.5:
          return number - ost
      else:
          return number + (5 - ost)
