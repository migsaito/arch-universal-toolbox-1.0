import subprocess
import os

class Backend:
    def __init__(self):
        pass

    def run_command(self, cmd, sudo=False):
        if sudo:
            cmd = ["pkexec"] + cmd
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            return False, e.stderr

    def search_pacman(self, query):
        success, output = self.run_command(["pacman", "-Ss", query])
        if success:
            return self._parse_pacman_search(output)
        return []

    def _parse_pacman_search(self, output):
        packages = []
        lines = output.split('\n')
        for i in range(0, len(lines) - 1, 2):
            if not lines[i].strip():
                continue
            name_part = lines[i].strip().split(' ')[0]
            version = lines[i].strip().split(' ')[1] if len(lines[i].strip().split(' ')) > 1 else ""
            desc = lines[i+1].strip() if i+1 < len(lines) else ""
            packages.append({"name": name_part, "version": version, "desc": desc, "source": "pacman"})
        return packages

    def search_aur(self, query, helper="yay"):
        success, output = self.run_command([helper, "-Ss", query])
        if success:
            return self._parse_aur_search(output)
        return []

    def _parse_aur_search(self, output):
        packages = []
        lines = output.split('\n')
        for i in range(0, len(lines) - 1, 2):
            if not lines[i].strip():
                continue
            # example line: aur/google-chrome 129.0.6668.70-1 (+2898 33.64) (Installed)
            parts = lines[i].strip().split(' ')
            name_part = parts[0]
            version = parts[1] if len(parts) > 1 else ""
            desc = lines[i+1].strip() if i+1 < len(lines) else ""
            packages.append({"name": name_part, "version": version, "desc": desc, "source": "aur"})
        return packages

    def install_package(self, pkg_name, helper=None):
        if helper:
            # Install via AUR helper
            # We use subprocess.Popen to open an external terminal to show progress since AUR/pacman installation needs interaction or at least shows progress
            cmd = ["xterm", "-e", helper, "-S", "--noconfirm", pkg_name]
            subprocess.Popen(cmd)
        else:
            # Install via pacman
            cmd = ["xterm", "-e", "pkexec", "pacman", "-S", "--noconfirm", pkg_name]
            subprocess.Popen(cmd)

    def remove_package(self, pkg_name, helper=None):
        if helper:
            cmd = ["xterm", "-e", helper, "-Rns", "--noconfirm", pkg_name]
            subprocess.Popen(cmd)
        else:
            cmd = ["xterm", "-e", "pkexec", "pacman", "-Rns", "--noconfirm", pkg_name]
            subprocess.Popen(cmd)

    def check_installed(self, pkg_name):
        success, _ = self.run_command(["pacman", "-Q", pkg_name])
        return success

    def add_repo(self, repo_name, server_url):
        import shlex
        # We need to append to /etc/pacman.conf
        repo_str = f"\n[{repo_name}]\nServer = {server_url}\n"
        quoted_repo_str = shlex.quote(repo_str)
        cmd = ["bash", "-c", f"echo {quoted_repo_str} | pkexec tee -a /etc/pacman.conf"]
        return self.run_command(cmd)

    def install_aur_helper(self, helper):
        # Install yay or paru using makepkg
        script = f"""
        cd /tmp
        rm -rf {helper}
        git clone https://aur.archlinux.org/{helper}.git
        cd {helper}
        makepkg -si --noconfirm
        """
        # Run in a terminal so user can see what's happening and input password if needed
        cmd = ["xterm", "-e", "bash", "-c", script]
        subprocess.Popen(cmd)

    def uninstall_aur_helper(self, helper):
        self.remove_package(helper)
