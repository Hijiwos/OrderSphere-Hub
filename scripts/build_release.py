# scripts/build_release.py
"""
一键构建 release 脚本（跨平台支持基本操作）。
功能：
- 在 frontend 目录运行 npm install (或 npm ci) 并执行 npm run build
- 将 frontend/dist 拷贝到 backend/dist
- 在临时 venv 中安装 pyinstaller 并使用 PyInstaller 将 backend/run_server.py 打包为单文件 exe
- 将可执行文件与必要静态文件（dist、data、db）打包到 release 文件夹
- 可选：使用 GITHUB_TOKEN 与 GITHUB_REPOSITORY 上传到 GitHub Release（需要 --tag 参数）
"""
import argparse
import os
import shutil
import subprocess
import sys
import time
import venv
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FRONTEND_DIR = ROOT / "frontend"
BACKEND_DIR = ROOT / "backend"
BACKEND_APP_DIR = BACKEND_DIR / "app"
BACKEND_DIST = BACKEND_DIR / "dist"
BACKEND_DATA = BACKEND_DIR / "data"
DB_DIR = ROOT / "db"
DB_FILE = DB_DIR / "ordersphere.db"

RELEASES_DIR = ROOT / "release_builds"


def run(cmd, cwd=None, env=None, check=True):
    # cmd: list or str
    if isinstance(cmd, (list, tuple)):
        print("> " + " ".join(cmd))
    else:
        print("> " + str(cmd))
    try:
        subprocess.check_call(cmd, cwd=cwd, env=env, shell=False)
    except FileNotFoundError as e:
        # Fallback on Windows: try running via cmd /c to let shell resolve npm/npm.cmd etc.
        if os.name == 'nt' and isinstance(cmd, (list, tuple)):
            try:
                shell_cmd = ["cmd", "/c"] + list(cmd)
                print("尝试通过 cmd /c 调用：", " ".join(shell_cmd))
                subprocess.check_call(shell_cmd, cwd=cwd, env=env, shell=False)
                return
            except Exception:
                pass
        raise FileNotFoundError(f"命令未找到: {cmd[0] if isinstance(cmd, (list,tuple)) else cmd}. 请确认该工具已安装并在 PATH 中.") from e
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"命令执行失败: {cmd} (cwd={cwd})") from e


def find_pkg_manager():
    """Return an executable to invoke for package manager commands (npm or yarn)."""
    import shutil

    # First try shutil.which
    for candidate in ["npm", "npm.cmd", "yarn", "yarn.cmd"]:
        p = shutil.which(candidate)
        if p:
            return p

    # On Windows try `where`
    if os.name == "nt":
        try:
            out = subprocess.check_output(["where", "npm"], stderr=subprocess.STDOUT, shell=False, text=True)
            first = out.splitlines()[0].strip()
            if first:
                return first
        except Exception:
            pass
        try:
            out = subprocess.check_output(["where", "yarn"], stderr=subprocess.STDOUT, shell=False, text=True)
            first = out.splitlines()[0].strip()
            if first:
                return first
        except Exception:
            pass

        # Check common install locations
        common = [
            os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "nodejs", "npm.cmd"),
            os.path.join(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"), "nodejs", "npm.cmd"),
            os.path.join(os.environ.get("USERPROFILE", ""), "AppData", "Roaming", "npm", "npm.cmd"),
        ]
        for p in common:
            if p and os.path.exists(p):
                return p
    else:
        for p in ["/usr/local/bin/npm", "/usr/bin/npm", "/opt/homebrew/bin/npm"]:
            if os.path.exists(p):
                return p

    return None


def build_frontend():
    if not FRONTEND_DIR.exists():
        print("frontend 目录不存在，跳过前端构建。")
        return
    pkg = find_pkg_manager()
    if not pkg:
        print(
            "未在 PATH 中找到 npm 或 yarn。若想构建前端，请先安装 Node.js (含 npm)，"
            "或在本机使用已安装的 Node 构建前端后再运行脚本，"
            "或者使用 --skip-frontend 跳过前端构建。"
        )
        raise FileNotFoundError("找不到 npm 或 yarn，可用 --skip-frontend 跳过前端构建。")

    try:
        pkgbase = os.path.basename(pkg).lower()
        if 'npm' in pkgbase:
            # 首选 npm ci；若失败则回退到 npm install（并尝试 legacy-peer-deps）
            try:
                lockfile = FRONTEND_DIR / "package-lock.json"
                if lockfile.exists():
                    run([pkg, "ci"], cwd=str(FRONTEND_DIR))
                else:
                    # 无 lockfile 时直接 install
                    run([pkg, "install"], cwd=str(FRONTEND_DIR))
            except Exception as ci_err:
                print("npm ci 失败，尝试使用 npm install 作为回退：", ci_err)
                try:
                    run([pkg, "install"], cwd=str(FRONTEND_DIR))
                except Exception as install_err:
                    # 有时因 peer deps 导致 install 失败，尝试带 legacy-peer-deps
                    print("npm install 也失败，尝试使用 --legacy-peer-deps：", install_err)
                    run([pkg, "install", "--legacy-peer-deps"], cwd=str(FRONTEND_DIR))
            # 最后进行构建
            run([pkg, "run", "build"], cwd=str(FRONTEND_DIR))
        else:
            # yarn workflow
            run([pkg, "install"], cwd=str(FRONTEND_DIR))
            run([pkg, "build"], cwd=str(FRONTEND_DIR))
    except Exception as e:
        print("前端构建失败：", e)
        raise

    src = FRONTEND_DIR / "dist"
    if not src.exists():
        raise RuntimeError("前端构建失败：frontend/dist 未生成")
    if BACKEND_DIST.exists():
        shutil.rmtree(BACKEND_DIST)
    shutil.copytree(src, BACKEND_DIST)
    print("已将 frontend/dist 拷贝到 backend/dist")


def prepare_venv(venv_dir: Path):
    if venv_dir.exists():
        shutil.rmtree(venv_dir)
    print("创建临时虚拟环境：", venv_dir)
    venv.create(venv_dir, with_pip=True)
    py = venv_dir / ("Scripts" if os.name == "nt" else "bin") / ("python.exe" if os.name == "nt" else "python")
    return str(py)


def install_in_venv(python_exe, requirements=None, extra_pkgs=None):
    cmd = [python_exe, "-m", "pip", "install", "--upgrade", "pip", "setuptools"]
    run(cmd)
    if requirements:
        run([python_exe, "-m", "pip", "install", "-r", str(requirements)])
    if extra_pkgs:
        run([python_exe, "-m", "pip", "install"] + extra_pkgs)


def build_pyinstaller(python_exe, entry_script: Path, name: str):
    add_data = []

    def ad(src, dst):
        sep = ";" if os.name == "nt" else ":"
        add_data.append(f"{str(src)}{sep}{dst}")

    if BACKEND_DIST.exists():
        ad(BACKEND_DIST, "dist")
    if BACKEND_DATA.exists():
        ad(BACKEND_DATA, "data")
    if DB_FILE.exists():
        ad(DB_FILE, "db")
    cmd = [
        python_exe,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onefile",
        "--name",
        name,
    ]
    for a in add_data:
        cmd += ["--add-data", a]
    cmd.append(str(entry_script))
    run(cmd, cwd=str(BACKEND_DIR))


def collect_release(name: str):
    timestamp = time.strftime("%Y%m%d%H%M%S")
    out = RELEASES_DIR / f"{name}-{timestamp}"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    built_dir = BACKEND_DIR / "dist"
    exe_name = name + (".exe" if os.name == "nt" else "")
    exe_path = built_dir / exe_name
    if not exe_path.exists():
        alt = ROOT / "dist" / exe_name
        if alt.exists():
            exe_path = alt
    if not exe_path.exists():
        raise RuntimeError("未找到打包好的可执行文件")
    shutil.copy2(exe_path, out / exe_name)
    if BACKEND_DIST.exists():
        shutil.copytree(BACKEND_DIST, out / "dist")
    if BACKEND_DATA.exists():
        shutil.copytree(BACKEND_DATA, out / "data")
    if DB_FILE.exists():
        db_outdir = out / "db"
        db_outdir.mkdir(exist_ok=True)
        shutil.copy2(DB_FILE, db_outdir / DB_FILE.name)
    readme = out / "README.txt"
    readme.write_text("双击可执行文件以启动服务。默认监听 0.0.0.0:8000\n")
    zip_path = RELEASES_DIR / f"{name}-{timestamp}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(out):
            for f in files:
                full = Path(root) / f
                zf.write(full, arcname=str(full.relative_to(out)))
    print("生成 release 包：", zip_path)
    return zip_path, out


def try_github_release(zip_path: Path, tag: str, repo: str, token: str):
    try:
        import requests
    except Exception:
        print("缺少 requests 库，跳过自动上传到 GitHub Release。")
        return
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    owner_repo = repo
    url = f"https://api.github.com/repos/{owner_repo}/releases"
    data = {"tag_name": tag, "name": tag, "body": f"Release {tag}", "draft": False, "prerelease": False}
    r = requests.post(url, json=data, headers=headers)
    if not r.ok:
        print("创建 release 失败：", r.status_code, r.text)
        return
    resp = r.json()
    upload_url = resp.get("upload_url")
    if not upload_url:
        print("release 创建返回无 upload_url，跳过资产上传。")
        return
    upload_url = upload_url.split("{")[0]
    headers2 = {"Authorization": f"token {token}", "Content-Type": "application/zip"}
    with open(zip_path, "rb") as fh:
        upload_resp = requests.post(f"{upload_url}?name={zip_path.name}", headers=headers2, data=fh.read())
    if not upload_resp.ok():
        print("上传资产失败：", upload_resp.status_code, upload_resp.text)
    else:
        print("已上传 release 资产到 GitHub")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", default="OrderSphereHub", help="可执行文件名/release 名称")
    parser.add_argument("--tag", default=None, help="可选：创建 GitHub Release 的 tag 名称")
    parser.add_argument("--skip-frontend", action="store_true", help="跳过前端构建（如果你已经手动构建）")
    args = parser.parse_args()

    if not args.skip_frontend:
        try:
            build_frontend()
        except FileNotFoundError as e:
            print("前端构建被中断：", e)
            print("你可以： 1) 安装 Node.js/npm 并确保 npm 在 PATH 中；2) 运行脚本时加 --skip-frontend")
            sys.exit(1)

    entry = BACKEND_DIR / "run_server.py"
    if not entry.exists():
        print("错误：期待 backend/run_server.py 存在以作为打包入口。请参考仓库提供的 run_server.py 并放置于 backend/")
        sys.exit(1)

    env_dir = ROOT / ".release_venv"
    python_exe = prepare_venv(env_dir)
    backend_req = BACKEND_DIR / "requirements.txt"
    install_in_venv(python_exe, requirements=backend_req if backend_req.exists() else None, extra_pkgs=["pyinstaller", "requests"])
    build_pyinstaller(python_exe, entry, args.name)
    zip_path, out_dir = collect_release(args.name)

    if args.tag:
        gh_token = os.environ.get("GITHUB_TOKEN")
        gh_repo = os.environ.get("GITHUB_REPOSITORY")
        if gh_token and gh_repo:
            try_github_release(zip_path, args.tag, gh_repo, gh_token)
        else:
            print("未提供 GITHUB_TOKEN 或 GITHUB_REPOSITORY，跳过 GitHub Release 上传。")
    print("构建完成。release 目录：", RELEASES_DIR)


if __name__ == "__main__":
    main()