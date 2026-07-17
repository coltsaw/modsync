from dataclasses import dataclass
import requests
from lib.modrinth_client import ModrinthClient
from os import path

@dataclass
class Mod:
  name: str
  version: str
  file_name: str
  download_url: str

  def from_collections(configs):
    mods = []
    client = ModrinthClient()

    collections = client.get_collections([configs.collection])

    for c in collections:
      for project_id in c.project_ids:
        project = client.get_project(project_id)
        versions = client.get_versions(
          project_id,
          loaders=[configs.loader],
          game_versions=[configs.mc_version]
        )

        latest_version = max(versions, key=lambda v: v.date_published) if versions else None

        mods.append(Mod(
          name=project.name,
          version=latest_version.version_number if latest_version else None,
          file_name=latest_version.primary_file().filename if latest_version else None,
          download_url=latest_version.primary_file().url if latest_version else None
        ))

    return mods
  
  def download(self, destination, dry_run):
    if self.download_url is not None:
      response = requests.get(
        self.download_url,
        stream=True,
        timeout=60
      )

      try:
        response.raise_for_status()
      except requests.exceptions.HTTPError as e:
        print(f"Failed to download {self.name}: {e}")
        return {
          "status": "missing",
          "name": self.name
        }
      
      output = path.join(destination, self.file_name)

      resp = {
        "status": "available",
        "name": self.name,
      }

      if not dry_run:
        with open(output, "wb") as file:
          for chunk in response.iter_content(8192):
            file.write(chunk)
        
        
        resp["destination"] = str(output)

      return resp        
    else:
      return {
        "status": "missing",
        "name": self.name
      }
