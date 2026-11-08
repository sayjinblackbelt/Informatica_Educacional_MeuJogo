# 09 — Segurança e Privacidade

## Finalidade

Estabelecer princípios de segurança digital, privacidade e proteção das informações relacionadas ao projeto.

## 1. Segurança digital

Conteúdos trabalhados:

- senhas e autenticação;
- proteção de dados pessoais;
- links e sites suspeitos;
- downloads e arquivos desconhecidos;
- privacidade em serviços digitais;
- comunicação responsável;
- verificação de informações;
- reconhecimento de golpes e engenharia social.

## 2. Boas práticas para educandos

- não compartilhar senhas;
- utilizar senhas fortes e diferentes quando possível;
- não divulgar endereço, telefone ou outros dados pessoais sem necessidade;
- verificar o endereço do site antes de inserir informações;
- desconfiar de mensagens com urgência, ameaças ou promessas de prêmio;
- não abrir arquivos ou links desconhecidos sem orientação;
- pedir ajuda diante de uma situação suspeita;
- encerrar sessões em computadores compartilhados.

## 3. Privacidade dos educandos

A documentação pública do projeto **não deve conter**:

- nomes completos;
- contatos;
- documentos pessoais;
- credenciais;
- fotografias identificáveis;
- avaliações individuais;
- informações que permitam identificar desnecessariamente um educando.

Para atividades pedagógicas, utilizar identificadores sanitizados como `grupo_01` e, quando necessário, códigos internos que não revelem a identidade.

## 4. Princípio da minimização

Coletar somente os dados necessários para uma finalidade pedagógica ou administrativa definida. Não utilizar o repositório público como banco de dados de educandos.

## 5. Credenciais e secrets

Nunca armazenar no repositório:

- senhas;
- tokens;
- chaves de API;
- cookies de autenticação;
- arquivos de credenciais;
- links privados com acesso embutido.

Credenciais devem ser mantidas em mecanismos apropriados de gerenciamento de secrets. O GitHub recomenda não colocar secrets diretamente no código e utilizar recursos de armazenamento seguro. Consulte a [documentação sobre secret scanning](https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning) e [push protection](https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection).

## 6. Repositório público

Antes de publicar ou atualizar arquivos:

1. revisar nomes e identificadores;
2. verificar dados pessoais;
3. verificar credenciais e secrets;
4. revisar links privados;
5. conferir imagens e anexos;
6. verificar direitos de uso;
7. revisar histórico quando houver suspeita de exposição.

Para repositórios públicos, avalie os recursos de segurança disponíveis, como [Dependabot](https://docs.github.com/en/code-security/dependabot/dependabot-alerts/about-dependabot-alerts), [secret scanning](https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning), [push protection](https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection) e [code scanning](https://docs.github.com/en/code-security/code-scanning/introduction-to-code-scanning/about-code-scanning).

## 7. Resposta a incidentes

Se uma credencial for exposta:

1. considerar a credencial comprometida;
2. revogar ou rotacionar imediatamente;
3. verificar possíveis usos indevidos;
4. remover o conteúdo do estado atual do repositório;
5. avaliar a necessidade de remover o segredo do histórico;
6. documentar a correção sem registrar novamente a credencial.

A remoção de um segredo do arquivo atual não necessariamente elimina sua presença no histórico Git; por isso, credenciais expostas devem ser revogadas ou rotacionadas imediatamente.

## 8. Abordagem pedagógica

A segurança deve ser ensinada por exemplos e situações-problema.

O educando deve ser estimulado a:

**identificar o risco → explicar o problema → escolher uma atitude segura → justificar a escolha → refletir sobre as consequências.**

> **Princípio:** segurança digital é uma competência de autonomia, responsabilidade e pensamento crítico — não apenas uma lista de proibições.
