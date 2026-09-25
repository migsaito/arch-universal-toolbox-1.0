# Maintainer: Jules
pkgname=arch-tool
pkgver=1.0.0
pkgrel=1
pkgdesc="A modern GUI to manage pacman/AUR packages, repositories, and AUR helpers"
arch=('any')
url="https://github.com/yourusername/arch-tool"
license=('GPL3')
depends=('python' 'python-pyqt6' 'pacman' 'xterm')
makedepends=('git')
source=("git+file://${PWD}")
sha256sums=('SKIP')

package() {
  cd "$srcdir/${pkgname}"

  # Install binary
  install -Dm755 src/main.py "$pkgdir/usr/bin/$pkgname"

  # Install other source files if needed
  install -d "$pkgdir/usr/share/$pkgname"
  cp -r src/* "$pkgdir/usr/share/$pkgname/"

  # Create a wrapper script to run the python app correctly
  cat << _EOF_ > "$pkgdir/usr/bin/$pkgname"
#!/bin/bash
python /usr/share/$pkgname/main.py "\$@"
_EOF_
  chmod +x "$pkgdir/usr/bin/$pkgname"

  # Install desktop file
  install -Dm644 arch-tool.desktop "$pkgdir/usr/share/applications/$pkgname.desktop"
}
