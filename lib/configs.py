from dataclasses import dataclass
import re
from pathlib import Path
import yaml

@dataclass
class Configs:
  mc_version: str
  loader: str
  collections: list[str]
  output: str
  dry_run: bool

  def validatable_attrs(self):
    return [self.mc_version, self.loader, self.collections]

  def parse_collection_ids(values):
    ids = []
    if values is None:
      return ids

    for v in values:

      match = re.search(r"collection/([A-Za-z0-9]+)", v)

      if match:
        ids.append(match.group(1))

    return ids
  
  def from_args(args):
    return Configs(
      mc_version=args.mc_version,
      loader=args.loader,
      collections=Configs.parse_collection_ids(args.collection),
      output=args.output,
      dry_run=args.dry_run
    )
  
  def from_yaml():
    if not Path("modpack.yml").exists():
      # return a default config that can be overridden
      return Configs(
        mc_version=None,
        loader=None,
        collections=None,
        output=Path("downloads"),
        dry_run=False
      )

    with open("modpack.yml", "r") as f:
      data = yaml.safe_load(f)

    try:
      mc_version = data.get("minecraft", {}).get("version")
      loader = data.get("minecraft", {}).get("loader")
      collections = Configs.parse_collection_ids(data.get("collections"))
      output = Path(data.get("output", {}).get("directory")) if data.get("output") else Path("downloads")
      dry_run = data.get("options", {}).get("dry_run", False)
    except AttributeError as e:
      raise ValueError("Malformed modpack.yml. Please refer to modpack.yml.ex for example")

    return Configs(
      mc_version=mc_version,
      loader=loader,
      collections=collections,
      output=output,
      dry_run=dry_run
    )

  def merge(self, other):
    return Configs(
      mc_version=other.mc_version or self.mc_version,
      loader=other.loader or self.loader,
      collections=other.collections or self.collections,
      output=other.output or self.output,
      dry_run=other.dry_run or self.dry_run
    )

  def validate(self):
    if any(attr == None for attr in self.validatable_attrs()):
      raise AttributeError("Missing required config attribute. Verify mc_version, loader, and collections are present")
    
    return self
