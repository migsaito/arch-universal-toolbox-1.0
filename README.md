# Arch Tool

Arch Tool is a modern Graphical User Interface (GUI) tool to manage pacman and AUR packages on Arch Linux based systems. It allows users to manage repositories, install/uninstall `yay` and `paru`, and features a package store to search and install packages. It also comes with multi-language support (PT-BR, EN-US, DE).

## Features
- **Store**: Search and install pacman and AUR packages easily.
- **Repository Manager**: Add or remove custom repositories directly to/from `/etc/pacman.conf`.
- **AUR Helpers**: One-click install/uninstall for `yay` and `paru`.
- **Multi-language**: Supported languages: English (EN-US), Portuguese (PT-BR), and German (DE).
- **Modern GUI**: Clean and user-friendly interface powered by PyQt6.

## Installation

You can install Arch Tool using the provided `PKGBUILD`.

```bash
git clone https://github.com/yourusername/arch-tool.git
cd arch-tool
makepkg -si
```

## License
This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.
