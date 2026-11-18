# Primeiro Execução - Guia de Instalação Segura

Este documento descreve como instalar e configurar o AI Developer Bootstrap de forma segura em um ambiente Debian 13.

## Pré-requisitos

- Debian 13 (ou derivado compatível)
- Acesso de sudo (root)
- Conexão com a internet (apenas para download)

## 1. Download Seguro

```bash
# Download do .deb oficial
curl -LO "https://github.com/tucano-project/tucano/releases/download/v0.2.7/tucano_0.2.7_amd64.deb"

# Verificação de checksum SHA256
sha256sum -c tucano.sha256  # Arquivo com o hash esperado
```

## 2. Instalação Manual

```bash
# Instale o .deb (não use -y para revisar antes)
sudo dpkg -i tucano_0.2.7_amd64.deb

# Verifique se a instalação foi bem-sucedida
tucano --version
```

## 3. Configuração Inicial do OpenCode no Tucano

```bash
# Crie o diretório de trabalho
mkdir -p ~/opencode-workspace
cd ~/opencode-workspace

# Inicialize o repositório Git
git init
git config user.email "seu@email.com"
git config user.name "Seu Nome"

# Clone o repositório do AI Developer Bootstrap (opcional, se quiser usar os scripts)
git clone /home/kers-hugo/projects/ai-developer-bootstrap .
```

## 4. Teste em Repositório Descartável

```bash
# Crie um repositório de teste
git init
git config user.email "seu@email.com"
git config user.name "Seu Nome"

# Execute o doctor para verificar o ambiente
python scripts/doctor.py

# Verifique a saída - deve mostrar todos os requisitos bloqueantes atendidos
```

## 5. Execução do Diagnóstico

```bash
# Diagnóstico completo
python scripts/doctor.py

# Diagnóstico em formato JSON
python scripts/doctor.py --json

# Verifique se todos os requisitos bloqueantes estão atendidos
```

## 6. Verificação de Resultados Esperados

```bash
# O script doctor.py deve mostrar:
# - ✅ Python instalado e com módulos essenciais
# - ✅ Git instalado
# - ✅ Docker CLI instalado (opcional)
# - ✅ OpenCode instalado
# - ✅ Tucano instalado
# - ✅ Checksum do Tucano válido

# Se algum requisito estiver faltando, o script mostrará:
# ⚠️ ATENÇÃO: REQUISITOS BLOQUEANTES NÃO ATENDIDOS!
```

## 7. Próximos Passos

Após a instalação e verificação:

1. Execute `python scripts/doctor.py` para confirmar o ambiente
2. Revise a saída JSON com `python scripts/doctor.py --json`
3. Valide que todos os requisitos bloqueantes estão atendidos
4. Comece a usar Tucano e OpenCode para seus projetos

## 8. Solução de Problemas

### Erro: "tucano: command not found"

```bash
# Verifique se o .deb foi instalado
dpkg -l | grep tucano

# Se estiver instalado, adicione ao PATH
export PATH="$PATH:/usr/local/bin"
source ~/.bashrc

# Ou verifique a instalação no diretório atual
./tucano --version
```

### Erro: checksum inválido

```bash
# Baixe novamente
curl -LO "https://github.com/tucano-project/tucano/releases/download/v0.2.7/tucano_0.2.7_amd64.deb"

# Verifique o hash
sha256sum tucano_0.2.7_amd64.deb
# Deve ser: 83b2096e10fcc09bd1cfa0fc11968330da2ab8874c1148e970356c6f874ae4ce
```

### Erro: Python sem módulos essenciais

```bash
# Instale os módulos via pip (se necessário)
pip install json os subprocess platform pathlib argparse
# (estes já vêm com o Python padrão, mas pode precisar de upgrade)
```

## 9. Limitações

- Este bootstrap não inclui frameworks de plugins
- Não modifica upstream do Tucano
- Não usa Kubernetes, Terraform, Ansible, ai-jail ou ai-memory sem necessidade demonstrada
- Runtime state e credentials devem permanecer fora do Git

## 10. Conclusão

Após seguir este guia, você terá:

- ✅ Tucano v0.2.7 instalado e verificado
- ✅ OpenCode configurado
- ✅ Ambiente pronto para desenvolvimento multi-agent
- ✅ Scripts de diagnóstico funcionando
- ✅ Testes automatizados rodando

Boa sorte com o AI Developer Bootstrap!
