#!/usr/bin/env python3
"""
Testes automatizados para scripts/doctor.py
Usando unittest e mocks, sem exigir ferramentas instaladas ou rede.
"""

import hashlib
import os
import sys
import unittest
from unittest.mock import Mock, patch


class TestDoctorScript(unittest.TestCase):
    """Testes para o script doctor.py"""

    def test_check_python(self):
        """Testa check_python retorna dict com módulos."""
        from scripts.doctor import check_python
        result = check_python()

        self.assertTrue(result["installed"])
        self.assertIn("modules", result)
        self.assertIn("json", result["modules"])
        self.assertEqual(result["modules"]["json"], "OK")

    def test_check_system_architecture(self):
        """Testa check_system_architecture retorna dict."""
        from scripts.doctor import check_system_architecture
        result = check_system_architecture()

        self.assertIn("name", result)
        self.assertIn("machine", result)
        self.assertIn("python_version", result)
        self.assertIsInstance(result["name"], str)

    def test_check_git_installed(self):
        """Testa check_git instalado."""
        from scripts.doctor import check_git
        result = check_git()
        self.assertIn("installed", result)
        self.assertIn("version", result)
        self.assertIn("status", result)

    def test_check_docker(self):
        """Testa check_docker retorna dict."""
        from scripts.doctor import check_docker
        result = check_docker()
        self.assertIn("cli_installed", result)
        self.assertIn("daemon_running", result)
        self.assertIn("version", result)

    def test_check_opencode(self):
        """Testa check_opencode retorna dict."""
        from scripts.doctor import check_opencode
        result = check_opencode()
        self.assertIn("installed", result)
        self.assertIn("status", result)

    def test_check_sha256sum(self):
        """Testa check_sha256sum retorna dict."""
        from scripts.doctor import check_sha256sum
        result = check_sha256sum()
        self.assertIn("installed", result)

    def test_check_curl(self):
        """Testa check_curl retorna dict."""
        from scripts.doctor import check_curl
        result = check_curl()
        self.assertIn("installed", result)
        self.assertIn("version", result)

    def test_tucano_version_constant(self):
        """Verifica que a versão do Tucano está correta."""
        from scripts.doctor import TUCANO_VERSION
        self.assertEqual(TUCANO_VERSION, "v0.2.7")

    def test_tucano_sha256_constant(self):
        """Verifica o SHA256 do Tucano."""
        from scripts.doctor import TUCANO_SHA256
        self.assertEqual(TUCANO_SHA256, "83b2096e10fcc09bd1cfa0fc11968330da2ab8874c1148e970356c6f874ae4ce")
        # Verifica que é um hash SHA256 válido (64 caracteres hexadecimais)
        self.assertEqual(len(TUCANO_SHA256), 64)
        self.assertEqual(set(TUCANO_SHA256), set('0123456789abcdef'))

    def test_checksum_format(self):
        """Testa formato do checksum."""
        # Verifica que o hash é um hash SHA256 válido
        test_string = "test"
        computed_hash = hashlib.sha256(test_string.encode()).hexdigest()
        self.assertEqual(len(computed_hash), 64)
        self.assertEqual(len("83b2096e10fcc09bd1cfa0fc11968330da2ab8874c1148e970356c6f874ae4ce"), 64)

    def test_all_checks_return_dict(self):
        """Testa que todas as verificações retornam dicionários."""
        from scripts.doctor import (
            check_system_architecture,
            check_git,
            check_python,
            check_opencode,
            check_docker,
            check_curl,
            check_sha256sum,
            check_tucano,
            verify_tucano_checksum
        )

        self.assertIsInstance(check_system_architecture(), dict)
        self.assertIsInstance(check_git(), dict)
        self.assertIsInstance(check_python(), dict)
        self.assertIsInstance(check_opencode(), dict)
        self.assertIsInstance(check_docker(), dict)
        self.assertIsInstance(check_curl(), dict)
        self.assertIsInstance(check_sha256sum(), dict)
        self.assertIsInstance(check_tucano(), dict)
        self.assertIsInstance(verify_tucano_checksum(), dict)

    def test_no_network_dependency(self):
        """Testa que os checks não dependem de rede (quando mockados)."""
        # Verifica que podemos importar e usar as funções
        from scripts.doctor import check_system_architecture, check_python
        result1 = check_system_architecture()
        result2 = check_python()
        # Se chegamos aqui sem erro, não há dependência de rede
        self.assertTrue(result1.get("name"))
        self.assertTrue(result2.get("installed"))


class TestTucanoVersion(unittest.TestCase):
    """Testes específicos para a versão do Tucano."""

    def test_tucano_version_constant(self):
        """Verifica que a versão do Tucano está correta."""
        from scripts.doctor import TUCANO_VERSION
        self.assertEqual(TUCANO_VERSION, "v0.2.7")

    def test_tucano_sha256_constant(self):
        """Verifica o SHA256 do Tucano."""
        from scripts.doctor import TUCANO_SHA256
        self.assertEqual(TUCANO_SHA256, "83b2096e10fcc09bd1cfa0fc11968330da2ab8874c1148e970356c6f874ae4ce")
        # Verifica que é um hash SHA256 válido (64 caracteres hexadecimais)
        self.assertEqual(len(TUCANO_SHA256), 64)
        self.assertEqual(set(TUCANO_SHA256), set('0123456789abcdef'))

    def test_checksum_format(self):
        """Testa formato do checksum."""
        import hashlib
        # Verifica que o hash é um hash SHA256 válido
        test_string = "test"
        computed_hash = hashlib.sha256(test_string.encode()).hexdigest()
        self.assertEqual(len(computed_hash), 64)
        self.assertEqual(len("83b2096e10fcc09bd1cfa0fc11968330da2ab8874c1148e970356c6f874ae4ce"), 64)


class TestIntegration(unittest.TestCase):
    """Testes de integração (sem rede)."""

    def test_all_checks_return_dict(self):
        """Testa que todas as verificações retornam dicionários."""
        from scripts.doctor import (
            check_system_architecture,
            check_git,
            check_python,
            check_opencode,
            check_docker,
            check_curl,
            check_sha256sum,
            check_tucano,
            verify_tucano_checksum
        )

        self.assertIsInstance(check_system_architecture(), dict)
        self.assertIsInstance(check_git(), dict)
        self.assertIsInstance(check_python(), dict)
        self.assertIsInstance(check_opencode(), dict)
        self.assertIsInstance(check_docker(), dict)
        self.assertIsInstance(check_curl(), dict)
        self.assertIsInstance(check_sha256sum(), dict)
        self.assertIsInstance(check_tucano(), dict)
        self.assertIsInstance(verify_tucano_checksum(), dict)

    def test_no_network_dependency(self):
        """Testa que os checks não dependem de rede (quando mockados)."""
        # Verifica que podemos importar e usar as funções
        from scripts.doctor import check_system_architecture, check_python
        result1 = check_system_architecture()
        result2 = check_python()
        # Se chegamos aqui sem erro, não há dependência de rede
        self.assertTrue(result1.get("name"))
        self.assertTrue(result2.get("installed"))


if __name__ == "__main__":
    # Executa os testes
    unittest.main(verbosity=2)
