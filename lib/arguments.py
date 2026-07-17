from dataclasses import dataclass
from pathlib import Path
  
@dataclass
class Arguments:
  mc_version: str
  loader: str
  collection: str
  output: Path
  dry_run: bool

  @staticmethod
  def parse():
    import argparse

    parser = argparse.ArgumentParser(
      description="Download mods from a Modrinth collection"
    )

    parser.add_argument(
      "--mc-version",
      required=True,
      help="Minecraft version to filter mods by"
    )

    parser.add_argument(
      "--loader",
      required=True,
      help="Mod loader to filter mods by (e.g., fabric, forge)"
    )

    parser.add_argument(
      "--collection",
      required=True,
      help="Modrinth collection URL (or ID) for server mods"
    )

    parser.add_argument(
      "--output",
      required=False,
      type=Path,
      default=Path("downloads"),
      help="Output directory for downloaded mods"
    )

    parser.add_argument(
      "--dry-run",
      action="store_true",
      default=False,
      help="Resolve mods but do not download files"
    )

    args = parser.parse_args()

    return Arguments(
      mc_version=args.mc_version,
      loader=args.loader,
      collection=args.collection,
      output=args.output,
      dry_run=args.dry_run
    )