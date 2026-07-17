from dataclasses import dataclass
import re

@dataclass
class Configs:
  mc_version: str
  loader: str
  collection: str
  output: str
  dry_run: bool

  def parse_collection_id(value):
    match = re.search(r"collection/([A-Za-z0-9]+)", value)

    if match:
      return match.group(1)

    return value
  
  def from_args(args):
    return Configs(
      mc_version=args.mc_version,
      loader=args.loader,
      collection=Configs.parse_collection_id(args.collection),
      output=args.output if args.output else "downloads",
      dry_run=args.dry_run
    )