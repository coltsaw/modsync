# modsync

A simple command-line utility for downloading all compatible mods from one or more Modrinth collections.

`modsync` allows you to build a client or server modpack directly from Modrinth collections without manually downloading every mod. Simply provide a collection URL (or use a configuration file), choose your Minecraft version and loader, and let `modsync` do the rest.

> **Disclaimer**
>
> `modsync` is an independent, open-source project and is **not affiliated with or endorsed by Modrinth**.
>
> This project is licensed under the MIT License.

---

## Features

* Download every compatible mod from a Modrinth collection
* Support for Fabric, with additional loaders planned
* Automatically select the correct mod version for a given Minecraft version
* Support multiple collections in a single configuration (coming soon)
* Dry-run mode to preview downloads
* Colorized terminal output
* Cross-platform (Windows, Linux, and macOS)

---

## Installation

### Download a Release (Recommended)

Download the latest executable from the project's GitHub Releases page.

Run the executable directly—no Python installation required.

### Run from Source

Clone the repository:

```bash
git clone https://github.com/coltsaw/modsync.git
cd modsync
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python main.py
```

---

## Usage

### Using command-line arguments

Download a collection by minecraft version and loader:

```bash
modsync \
    --collection https://modrinth.com/collection/XXXXXXXX \
    --loader=fabric
    --mc-version=26.2
```

Preview downloads without downloading anything:

```bash
modsync \
    --collection https://modrinth.com/collection/XXXXXXXX \
    --loader=fabric
    --mc-version=26.2
    --dry-run
```

---

## Roadmap

Planned features include:

* Dependency resolution
* Automatic update checking
* `.mrpack` export

---

## Contributing

Contributions are welcome!

Whether you'd like to:

* Fix a bug
* Improve documentation
* Add support for additional loaders
* Suggest new features
* Improve code quality

please feel free to open an issue or submit a pull request.

If you're planning a large change, opening an issue first to discuss the idea is appreciated.

---

## Creating a Release

Run:

```bash
python release.py
```

---

## Reporting Issues

Found a bug or have a feature request?

Please open an issue on GitHub:

https://github.com/coltsaw/modsync/issues

When reporting a bug, please include:

* Operating system
* `modsync` version
* Minecraft version
* Loader
* Collection URL (if public)
* Full console output, if applicable

---

## License

This project is licensed under the MIT License.

See the `LICENSE` file for details.
