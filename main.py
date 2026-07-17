from lib.arguments import Arguments
from lib.configs import Configs
from lib.mod import Mod
from lib.downloader import Downloader
from colorama import init, Fore
from version import __version__

def main():
  # colors
  init(autoreset=True)
  
  print("=" * 50)
  print("Thanks for using my Modrinth collection downloader! If you have any issues,")
  print(f"please report them at {Fore.CYAN}https://github.com/coltsaw/modsync/issues")
  print("This program is not affiliated with Modrinth in any way.")
  print("This program is licensed under the MIT License. See LICENSE for more information.")
  print(f"Version: {Fore.BLUE}{__version__}")
  print("=" * 50)
  print()
  print()
  print("Starting collection download...")

  args = Arguments.parse()

  configs = Configs.from_args(args)
  print(f"{Fore.YELLOW}** DRY RUN **") if configs.dry_run else None
  print(f"Collection: {configs.collection}")
  print(f"Minecraft version: {configs.mc_version}")
  print()
  
  mods = Mod.from_collections(configs)

  Downloader.download_mods(mods, configs)

if __name__ == "__main__":
  main()