from colorama import Fore, Style

class Formatter:
  COLLECTION_COLORS = [
    Fore.BLUE, Fore.MAGENTA, 
    Fore.CYAN, Fore.YELLOW,
    Fore.BLACK
  ]

  def success(text):
    return f"{Fore.GREEN}{text}{Style.RESET_ALL}"

  def error(text):
    return f"{Fore.RED}{text}{Style.RESET_ALL}"

  def downloaded(name):
    return f"{Formatter.CHECK} {Formatter.success(name)}"
  
  def failed(name):
    return f"{Formatter.CROSS} {Formatter.error(name)}"

  # simple attempt as hashing color by collection ID so
  # they display the same in the output
  @staticmethod
  def pretty_collection(cid):
    idx = (sum([ord(c) for c in cid]) + 1) % len(Formatter.COLLECTION_COLORS)
    return f"{Formatter.COLLECTION_COLORS[idx]}[{cid}]{Style.RESET_ALL}"

  CHECK = success("✓")
  CROSS = error("✗")