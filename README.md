# AI Developer Bootstrap

Ambiente reproduzível de bootstrap para desenvolvimento multi-agent com Tucano e OpenCode.

## Visão Geral

- **Missão**: Construir um diagnóstico reproduzível e somente leitura do dev01 para avaliar prontidão para Tucano + OpenCode
- **Princípios**: Git é a fonte da verdade, Vertical Slice First, Complexity Must Earn Its Place, Evidence over Claims, Reuse Before Rebuild
- **Tucano**: Primeiro candidato para multi-agent DevEx (v0.2.7)
- **OpenCode**: Harness inicial de desenvolvimento

## Pré-requisitos

### Bloqueantes (Obrigatórios)

- [x] Python 3.x (com módulos: json, os, subprocess, platform, pathlib, argparse)
- [x] Git instalado
- [ ] Tucano v0.2.7 instalado (pendente de validação)
- [x] curl instalado
- [x] sha256sum instalado

### Opcionais

- [ ] Docker CLI e daemon
- [ ] OpenCode binário (pode ser instalado via pip ou download manual)

## Instalação

### Rápida (Manual)

```bash
# Clone o repositório
git clone <URL> /caminho/ai-developer-bootstrap
cd /caminho/ai-developer-bootstrap

# Execute o diagnóstico
python scripts/doctor.py

# Instale o Tucano (se necessário)
# Consulte docs/first-run.md para instruções detalhadas
```

### Via .deb (após download)

```bash
curl -LO "https://github.com/tucano-project/tucano/releases/download/v0.2.7/tucano_0.2.7_amd64.deb"
sha256sum -c tucano.sha256  # Verifique o hash
sudo dpkg -i tucano_0.2.7_amd64.deb
```

## Uso

### Diagnóstico do Ambiente

```bash
# Diagnóstico legível
python scripts/doctor.py

# Diagnóstico em JSON
python scripts/doctor.py --json
```

### Execução de Testes

```bash
# Execute todos os testes
python -m unittest discover -s tests -v

# Execute apenas testes de doctor
python -m unittest discover -s tests -p "test_doctor.py" -v
```

### Verificação de Tucano

```bash
# Verifica instalação
tucano --version

# Verifica checksum
python scripts/doctor.py --json | grep -A5 "tucano_checksum"
```

## Arquitetura

```
ai-developer-bootstrap/
├── AGENTS.md              # Instruções de engenharia
├── README.md              # Este arquivo
├── config/
│   └── tucano.json        # Versão e SHA256 do Tucano
├── docs/
│   └── first-run.md       # Guia de primeira execução
├── scripts/
│   └── doctor.py          # Script de diagnóstico
└── tests/
    └── test_doctor.py     # Testes automatizados
```

## Testes

### Rodar Todos os Testes

```bash
python -m unittest discover -s tests -v
```

### Testes Disponíveis

- `test_check_system_architecture` - Sistema e arquitetura
- `test_check_python_modules` - Módulos Python
- `test_check_git_installed` - Git instalado
- `test_check_git_not_installed` - Git não instalado
- `test_check_docker_cli` - Docker CLI
- `test_check_opencode_installed` - OpenCode instalado
- `test_check_opencode_not_installed` - OpenCode não instalado
- `test_check_sha256sum_installed` - sha256sum instalado
- `test_verify_tucano_checksum_valid` - Checksum válido
- `test_verify_tucano_checksum_invalid` - Checksum inválido
- `test_main_json_output` - Saída JSON
- `test_argument_parser` - Parser de argumentos
- `test_tucano_version_constant` - Versão constante
- `test_tucano_sha256_constant` - SHA256 constante
- `test_checksum_format` - Formato do checksum
- `test_all_checks_return_dict` - Todas as verificações retornam dict
- `test_no_network_dependency` - Sem dependência de rede

## Resultados Esperados

### Ambiente Pronto

```
RESULTADOS:
======================================================================

1. SISTEMA E ARQUITETURA
   Sistema: Linux 5.15.0-91-generic
   Versão:  #110~22.04.1-Ubuntu
   Máquina: x86_64
   Python:   CPython 3.11.0

2. GIT
   Instalado: Sim (git version 2.43.0)
   Status:    clean

3. PYTHON
   Versão: 3.11.0
   Módulos essenciais:
     - json: OK
     - os: OK
     - subprocess: OK
     - platform: OK
     - pathlib: OK
     - argparse: OK

4. OPENCODE
   Instalado: Não

5. DOCKER
   CLI instalado: True
   Versão: Docker version 24.0.0
   Daemon rodando: True

6. CURL
   Instalado: Sim (curl 8.4.0)

7. SHA256SUM
   Instalado: Sim (sha256sum (GNU coreutils) 8.32)

8. TUCANO
   Instalado: Sim
   Versão: Tucano v0.2.7
   Caminho: /home/kers-hugo/projects/ai-developer-bootstrap/tucano

9. TUCANO CHECKSUM
   Hash esperado: 83b2096e10fcc09bd1cfa0fc11968330da2ab8874c1148e970356c6f874ae4ce
   Hash atual:    83b2096e10fcc09bd1cfa0fc11968330da2ab8874c1148e970356c6f874ae4ce
   Status:        VALIDO

======================================================================

CLASSIFICAÇÃO:
   REQUISITOS BLOQUEANTES ATENDIDOS (7):
     - Python
     - Git
     - Docker CLI
     - curl
     - sha256sum
     - OpenCode
     - Tucano

======================================================================

✅ ATENÇÃO: AMBIENTE PREPARADO!
   Todos os requisitos bloqueantes estão atendidos.
```

### Ambiente Incompleto

```
⚠️ ATENÇÃO: REQUISITOS BLOQUEANTES NÃO ATENDIDOS!
   O ambiente precisa atender a 1 requisito(s) bloqueante(s).
   Bloqueantes: OpenCode
```

## Configuração

### Versão do Tucano

- **Versão**: v0.2.7
- **SHA256**: 83b2096e10fcc09bd1cfa0fc11968330da2ab8874c1148e970356c6f874ae4ce
- **Arquitetura**: amd64
- **URL**: https://github.com/tucano-project/tucano/releases/download/v0.2.7/tucano_0.2.7_amd64.deb

Verifique em `config/tucano.json`.

## Limitações

- Não usa sudo (exceto para instalação do .deb)
- Não muda o host
- Não acessa credenciais
- Não modifica outros repositórios
- Não faz push sem aprovação
- Não modifica upstream do Tucano
- Não usa Kubernetes, Terraform, Ansible, ai-jail, ai-memory sem necessidade
- Não constrói framework de plugins
- Runtime state e credentials permanecem fora do Git

## Desenvolvimento

### Ciclo de Desenvolvimento

Implement -> Validate -> Understand -> Experiment -> Consolidate

### Architecture Boundaries

- Bootstrap: Possui configuração e verificação desejadas
- Tucano: Possui candidate multi-agent user experience
- Harnesses: Interchangeáveis
- Runtime state e credentials: Fora do Git

### Engineering Principles

- Git é a fonte da verdade
- Vertical Slice First
- Complexity Must Earn Its Place
- Evidence over Claims
- Reuse Before Rebuild
- Prefer small, independently verifiable changes

## Contribuição

1. Inspeione o repositório antes de fazer mudanças
2. Explique a implementação escolhida brevemente
3. Implemente uma capacidade limitada por iteração
4. Adicione testes automatizados apropriados
5. Execute validações e relace evidências reais
6. Nunca fabrique evidências de execução
7. Nunca commit secrets, tokens ou bancos de dados locais
8. Nunca use sudo, comandos destrutivos ou instale software no host sem aprovação

## Licença

Este projeto segue os princípios de open source. Consulte `.gitignore` e `.gitattributes` para configuração de versão e exclusão de arquivos.

## Rodar Diagnóstico

```bash
# Diagnóstico completo
python scripts/doctor.py

# Diagnóstico em JSON
python scripts/doctor.py --json

# Executar testes
python -m unittest discover -s tests -v

# Verificar apenas Python
python scripts/doctor.py 2>&1 | grep -A20 "PYTHON"
```

## Comandos de Validação

```bash
# 1. Verificar Python
python --version
python -c "import json, os, subprocess, platform, pathlib, argparse; print('OK')"

# 2. Verificar Git
git --version

# 3. Verificar curl
curl --version

# 4. Verificar sha256sum
sha256sum --version

# 5. Verificar Tucano
tucano --version

# 6. Executar doctor
python scripts/doctor.py

# 7. Executar testes
python -m unittest discover -s tests -v

# 8. Verificar JSON
python scripts/doctor.py --json
```

## Suporte

Para problemas, consulte:

- `docs/first-run.md` - Guia de primeira execução
- `AGENTS.md` - Instruções de engenharia
- Testes em `tests/test_doctor.py`

## Histórico de Versões

- **v0.1.0** (2026-11-03): Primeira versão do bootstrap
  - Scripts/doctor.py com diagnóstico completo
  - Testes automatizados com unittest e mocks
  - Config/tucano.json com versão e SHA256
  - Docs/first-run.md com guia de instalação
  - README.md com documentação completa
