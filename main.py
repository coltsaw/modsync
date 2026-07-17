from lib.arguments import Arguments
from lib.configs import Configs
from lib.mod import Mod
from lib.downloader import Downloader
from colorama import init

def main():
  # colors
  init(autoreset=True)

  args = Arguments.parse()

  configs = Configs.from_args(args)

  mods = Mod.from_collections(configs)

  Downloader.download_mods(mods, configs)

if __name__ == "__main__":
  main()