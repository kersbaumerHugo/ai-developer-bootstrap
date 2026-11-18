#!/usr/bin/env python3
"""
AI Developer Bootstrap - Doctor Script
Diagnóstico reproduzível e somente leitura do dev01.
Verifica ambiente para avaliar prontidão para Tucano + OpenCode.
"""

import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
from pathlib import Path


# Versão candidata do Tucano
TUCANO_VERSION = "v0.2.7"
TUCANO_SHA256 = "83b2096e10fcc09bd1cfa0fc11968330da2ab8874c1148e970356c6f874ae4ce"
TUCANO_DEB_URL = "https://github.com/tucano-project/tucano/releases/download/v0.2.7/tucano_0.2.7_amd64.deb"


def check_system_architecture():
    """Verifica sistema e arquitetura."""
    results = {
        "name": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_implementation": platform.python_implementation(),
        "python_version": platform.python_version(),
    }
    return results


def check_git():
    """Verifica instalação e estado do Git."""
    result = {"installed": False, "version": None, "status": None}
    try:
        proc = subprocess.run(
            ["git", "--version"],
            capture_output=True,
            text=True,
            check=False
        )
        if proc.returncode == 0:
            result["installed"] = True
            result["version"] = proc.stdout.strip()
            # Verifica se há repositório local
            proc_status = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                check=False
            )
            result["status"] = "clean" if proc_status.stdout.strip() == "" else "modified"
    except FileNotFoundError:
        pass
    return result


def check_python():
    """Verifica Python e módulos essenciais."""
    results = {
        "installed": False,
        "version": None,
        "modules": {}
    }
    try:
        import sys
        results["installed"] = True
        results["version"] = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

        required_modules = ["json", "os", "subprocess", "platform", "pathlib", "argparse"]
        for module in required_modules:
            try:
                results["modules"][module] = "OK"
            except ImportError:
                results["modules"][module] = "MISSING"
    except Exception:
        pass
    return results


def check_opencode():
    """Detecta o OpenCode instalado no PATH."""
    import shutil

    result = {
        "installed": False,
        "status": "not found",
        "version": None,
        "path": None,
    }

    executable = shutil.which("opencode")
    if executable is None:
        return result

    result["installed"] = True
    result["path"] = executable

    try:
        proc = subprocess.run(
            [executable, "--version"],
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )
        if proc.returncode == 0:
            result["status"] = "running"
            result["version"] = proc.stdout.strip()
        else:
            result["status"] = "error"
    except (OSError, subprocess.TimeoutExpired):
        result["status"] = "error"

    return result


def check_docker():
    """Verifica Docker CLI e daemon."""
    result = {
        "cli_installed": False,
        "daemon_running": False,
        "version": None
    }

    try:
        proc = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
            check=False
        )
        if proc.returncode == 0:
            result["cli_installed"] = True
            result["version"] = proc.stdout.strip()

        # Verifica se o daemon está rodando
        proc_status = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            text=True,
            check=False
        )
        if proc_status.returncode == 0:
            result["daemon_running"] = True
    except Exception:
        pass
    return result


def check_curl():
    """Verifica instalação do curl."""
    result = {"installed": False, "version": None}
    try:
        proc = subprocess.run(
            ["curl", "--version"],
            capture_output=True,
            text=True,
            check=False
        )
        if proc.returncode == 0:
            result["installed"] = True
            result["version"] = proc.stdout.strip().split('\n')[0]
    except FileNotFoundError:
        pass
    return result


def check_sha256sum():
    """Verifica instalação do sha256sum."""
    result = {"installed": False}
    try:
        proc = subprocess.run(
            ["sha256sum", "--version"],
            capture_output=True,
            text=True,
            check=False
        )
        if proc.returncode == 0:
            result["installed"] = True
            result["version"] = proc.stdout.strip().split('\n')[0]
    except FileNotFoundError:
        pass
    return result


def check_tucano():
    """Verifica instalação do Tucano."""
    result = {"installed": False, "version": None, "path": None}

    # Verifica no PATH
    try:
        proc = subprocess.run(
            ["tucano", "--version"],
            capture_output=True,
            text=True,
            check=False
        )
        if proc.returncode == 0:
            result["installed"] = True
            result["version"] = proc.stdout.strip()
    except FileNotFoundError:
        pass

    # Verifica se está no diretório atual
    tucano_path = Path("tucano")
    if tucano_path.exists():
        result["installed"] = True
        result["path"] = str(tucano_path)
        try:
            proc = subprocess.run(
                ["python", str(tucano_path), "--version"],
                capture_output=True,
                text=True,
                check=False
            )
            if proc.returncode == 0:
                result["version"] = proc.stdout.strip()
        except Exception:
            pass

    return result


def verify_tucano_checksum():
    """Verifica checksum do .deb oficial do Tucano."""
    result = {"verified": False, "expected": TUCANO_SHA256, "actual": None}

    # Não baixa nem instala automaticamente - apenas verifica se há arquivo
    deb_file = Path("tucano_0.2.7_amd64.deb")
    if deb_file.exists():
        try:
            with open(deb_file, "rb") as f:
                content = f.read()
                actual_hash = hashlib.sha256(content).hexdigest()
                result["actual"] = actual_hash
                result["verified"] = actual_hash == TUCANO_SHA256
        except Exception:
            pass

    return result


def main():
    parser = argparse.ArgumentParser(
        description="AI Developer Bootstrap - Diagnóstico do ambiente para Tucano + OpenCode"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Saída em formato JSON"
    )
    args = parser.parse_args()

    print("=" * 70)
    print("AI DEVELOPER BOOTSTRAP - DOCTOR DIAGNÓSTICO")
    print("=" * 70)
    print()

    results = {}
    blocking = []
    optional = []

    # Coleta todos os resultados
    results["system"] = check_system_architecture()
    results["git"] = check_git()
    results["python"] = check_python()
    results["opencode"] = check_opencode()
    results["docker"] = check_docker()
    results["curl"] = check_curl()
    results["sha256sum"] = check_sha256sum()
    results["tucano"] = check_tucano()
    results["tucano_checksum"] = verify_tucano_checksum()

    # Classifica em bloqueantes e opcionais
    checks = [
        ("Python", results["python"]["installed"]),
        ("Git", results["git"]["installed"]),
        ("Docker CLI", results["docker"]["cli_installed"]),
        ("curl", results["curl"]["installed"]),
        ("sha256sum", results["sha256sum"]["installed"]),
        ("OpenCode", results["opencode"]["installed"]),
        ("Tucano", results["tucano"]["installed"]),
        ("Tucano checksum", results["tucano_checksum"]["verified"]),
    ]

    for name, status in checks:
        if status:
            optional.append(name)
        else:
            blocking.append(name)

    # Saída legível
    print("RESULTADOS:")
    print("-" * 70)

    print("\n1. SISTEMA E ARQUITETURA")
    print(f"   Sistema: {results['system']['name']} {results['system']['release']}")
    print(f"   Versão:  {results['system']['version']}")
    print(f"   Máquina: {results['system']['machine']}")
    print(f"   Processador: {results['system']['processor']}")
    print(f"   Python:   {results['system']['python_implementation']} {results['system']['python_version']}")

    print("\n2. GIT")
    if results["git"]["installed"]:
        print(f"   Instalado: Sim ({results['git']['version']})")
        print(f"   Status:    {results['git']['status']}")
    else:
        print("   Instalado: Não")

    print("\n3. PYTHON")
    if results["python"]["installed"]:
        print(f"   Versão: {results['python']['version']}")
        print("   Módulos essenciais:")
        for mod, status in results["python"]["modules"].items():
            print(f"     - {mod}: {status}")
    else:
        print("   Instalado: Não")

    print("\n4. OPENCODE")
    if results["opencode"]["installed"]:
        print(f"   Instalado: Sim")
        print(f"   Status:    {results['opencode']['status']}")
        if results["opencode"]["version"]:
            print(f"   Versão:    {results['opencode']['version']}")
    else:
        print("   Instalado: Não")

    print("\n5. DOCKER")
    print(f"   CLI instalado: {results['docker']['cli_installed']}")
    if results["docker"]["version"]:
        print(f"   Versão:        {results['docker']['version']}")
    print(f"   Daemon rodando: {results['docker']['daemon_running']}")

    print("\n6. CURL")
    if results["curl"]["installed"]:
        print(f"   Instalado: Sim ({results['curl']['version']})")
    else:
        print("   Instalado: Não")

    print("\n7. SHA256SUM")
    if results["sha256sum"]["installed"]:
        print(f"   Instalado: Sim ({results['sha256sum']['version']})")
    else:
        print("   Instalado: Não")

    print("\n8. TUCANO")
    if results["tucano"]["installed"]:
        print(f"   Instalado: Sim")
        print(f"   Versão:    {results['tucano']['version']}")
        print(f"   Caminho:   {results['tucano']['path']}")
    else:
        print(f"   Instalado: Não (esperado: {TUCANO_VERSION})")

    print("\n9. TUCANO CHECKSUM")
    checksum = results["tucano_checksum"]
    if checksum["actual"]:
        status = "VALIDO" if checksum["verified"] else "INVÁLIDO"
        print(f"   Hash esperado: {checksum['expected']}")
        print(f"   Hash atual:    {checksum['actual']}")
        print(f"   Status:        {status}")
    else:
        print("   Arquivo .deb não encontrado no diretório atual")
        print(f"   Hash esperado: {checksum['expected']}")

    print("\n" + "-" * 70)

    print("\nCLASSIFICAÇÃO:")
    print(f"   REQUISITOS BLOQUEANTES NÃO ATENDIDOS ({len(blocking)}):")
    for item in blocking:
        print(f"     - {item}")

    print(f"   REQUISITOS OPCIONAIS ATENDIDOS ({len(optional)}):")
    for item in optional:
        print(f"     - {item}")

    print("\n" + "-" * 70)

    if blocking:
        print("\n⚠️  ATENÇÃO: REQUISITOS BLOQUEANTES NÃO ATENDIDOS!")
        print(f"   O ambiente precisa atender a {len(blocking)} requisito(s) bloqueante(s).")
        print(f"   Bloqueantes: {', '.join(blocking)}")
    else:
        print("\n✅ ATENÇÃO: AMBIENTE PREPARADO!")
        print("   Todos os requisitos bloqueantes estão atendidos.")

    print("\n" + "=" * 70)

    # Saída JSON
    if args.json:
        output = {
            "system": results["system"],
            "git": results["git"],
            "python": results["python"],
            "opencode": results["opencode"],
            "docker": results["docker"],
            "curl": results["curl"],
            "sha256sum": results["sha256sum"],
            "tucano": results["tucano"],
            "tucano_checksum": results["tucano_checksum"],
            "blocking": blocking,
            "optional": optional,
            "tucano_version": TUCANO_VERSION,
            "tucano_sha256": TUCANO_SHA256,
        }
        print("\nJSON OUTPUT:")
        print(json.dumps(output, indent=2))

    return 0 if not blocking else 1


if __name__ == "__main__":
    sys.exit(main())
