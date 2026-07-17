from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore

class Downloader:
  def download_mods(mods, configs):
    total = len(mods)
    print(f"Found {total} mods to download")
    print()

    downloaded = []
    missing = []

    with ThreadPoolExecutor(max_workers=8) as executor:
      futures = {
        executor.submit(
          mod.download,
          configs.output,
          configs.dry_run
        ): mod

        for mod in mods
      }

      for index, future in enumerate(
        as_completed(futures),
        start=1
      ):
        result = future.result()

        if result["status"] == "available":
          print(
            f"[{index}/{total}] "
            f"{Fore.GREEN}✓ {result['name']}{Fore.RESET}"
          )

          downloaded.append(result)

        else:
          print(
              f"[{index}/{total}] "
              f"{Fore.RED}✗ {result['name']}{Fore.RESET}"
          )

          missing.append(
              result["name"]
          )
  
    print()
    print("=" * 50)
    print("Complete")
    print("=" * 50)

    print(
      f"{configs.dry_run and 'Would have d' or 'D'}ownloaded: {len(downloaded)}"
    )
    print(
      f"Missing: {len(missing)}"
    )
    if missing:
      print()
      print("No compatible version:")
      for mod in missing:
        print(f" - {mod}")