from datetime import datetime
from main import *


def early_leaving():
  d1 = datetime.now().hour * 60 + datetime.now().minute
  d2 = 17*60 + 30 #разрешенное время для ухода

  if d1 < d2:
    return True
  return False


def late_coming():
  current = datetime.now().hour * 60 + datetime.now().minute
  on_time = 9*60 + 30

  if current > on_time:
    return True
  return False

    
