from dataclasses import dataclass
from datetime import datetime
import requests

class ModrinthClient:
  API = "https://api.modrinth.com/v3"

  def get_collections(self, collections):
    url = f"{self.API}/collections?ids=[{','.join(f'\"{c}\"' for c in collections)}]"
    data = self.get(url)

    # iterate over data array and create collection
    return [Collection.from_hash(collection) for collection in data]
  
  def get_project(self, project_id):
    url = f"{self.API}/project/{project_id}"
    data = self.get(url)

    return Project.from_hash(data)
  
  def get_versions(self, project_id, loaders=None, game_versions=None):
    params = []
    if loaders:
      params.append(f"loaders=[{','.join(f'\"{l}\"' for l in loaders)}]")
    if game_versions:
      version_str = ','.join(f'\"{v}\"' for v in game_versions)
      params.append("loader_fields={\"game_versions\":[%s]}" % version_str)

    url = f"{self.API}/project/{project_id}/version"
    if params:
      url += f"?{'&'.join(params)}"
    data = self.get(url)

    return [Version.from_hash(version) for version in data]

  def get(self, url):
    response = requests.get(
      url,
      timeout=30,
      headers={
          "User-Agent": "collection_download/0.1"
      }
    )

    response.raise_for_status()
    return response.json()

@dataclass
class Collection:
  id: str
  name: str
  description: str
  project_ids: list[str]

  def from_hash(data):
    return Collection(
      id=data["id"],
      name=data["name"],
      description=data["description"],
      project_ids=data["projects"]
    )

@dataclass
class Project:
  id: str
  name: str
  description: str

  def from_hash(data):
    return Project(
      id=data["id"],
      name=data["name"],
      description=data["description"]
    )

@dataclass
class File:
  filename: str
  url: str
  hashes: dict[str, str]
  primary: bool

  def from_hash(data):
    return File(
      filename=data["filename"],
      url=data["url"],
      hashes=data["hashes"],
      primary=data["primary"]
    )

  def is_primary(self):
    return self.primary
  
@dataclass
class Version:
  id: str
  name: str
  version_number: str
  game_versions: list[str]
  loaders: list[str]
  files: list[File]
  date_published: datetime

  def from_hash(data):
    return Version(
      id=data["id"],
      name=data["name"],
      version_number=data["version_number"],
      game_versions=data["game_versions"],
      loaders=data["loaders"],
      files=[File.from_hash(file) for file in data["files"]],
      date_published=datetime.fromisoformat(data["date_published"].replace("Z", "+00:00"))
    )

  def primary_file(self):
    for file in self.files:
      if file.is_primary():
        return file

    return None

