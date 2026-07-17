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
  print(f"modsync v{Fore.BLUE}{__version__}")
  print("Download compatible mods from Modrinth collections.")
  print()
  print("This project is not affiliated with or endorsed by Modrinth.")
  print(f"Report issues: {Fore.CYAN}https://github.com/coltsaw/modsync/issues")
  print("Licensed under the MIT License.")
  print()
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