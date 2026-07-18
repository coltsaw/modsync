from dataclasses import dataclass
import re
from pathlib import Path
import yaml

@dataclass
class Configs:
  mc_version: str
  loader: str
  collection: str
  output: str
  dry_run: bool

  def validatable_attrs(self):
    return [self.mc_version, self.loader, self.collection]

  def parse_collection_id(value):
    if value is None:
      return value

    match = re.search(r"collection/([A-Za-z0-9]+)", value)

    if match:
      return match.group(1)

    return value
  
  def from_args(args):
    return Configs(
      mc_version=args.mc_version,
      loader=args.loader,
      collection=Configs.parse_collection_id(args.collection),
      output=args.output,
      dry_run=args.dry_run
    )
  
  def from_yaml():
    if not Path("modpack.yml").exists():
      # return a default config that can be overridden
      return Configs(
        mc_version=None,
        loader=None,
        collection=None,
        output=Path("downloads"),
        dry_run=False
      )

    with open("modpack.yml", "r") as f:
      data = yaml.safe_load(f)

    try:
      mc_version = data.get("minecraft", {}).get("version")
      loader = data.get("minecraft", {}).get("loader")
      collection = Configs.parse_collection_id(data.get("collections")[0])
      output = Path(data.get("output", {}).get("directory")) if data.get("output") else Path("downloads")
      dry_run = data.get("options", {}).get("dry_run", False)
    except AttributeError as e:
      raise ValueError("Malformed modpack.yml. Please refer to modpack.yml.ex for example")

    return Configs(
      mc_version=mc_version,
      loader=loader,
      collection=collection,
      output=output,
      dry_run=dry_run
    )

  def merge(self, other):
    return Configs(
      mc_version=other.mc_version or self.mc_version,
      loader=other.loader or self.loader,
      collection=other.collection or self.collection,
      output=other.output or self.output,
      dry_run=other.dry_run or self.dry_run
    )

  def validate(self):
    if any(attr == None for attr in self.validatable_attrs()):
      raise AttributeError("Missing required config attribute. Verify mc_version, loader, and collection are present")
    
    return self
