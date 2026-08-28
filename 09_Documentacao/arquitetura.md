# Arquitetura do Projeto

## Visão geral

O projeto possui duas camadas complementares:

1. **Oficina pedagógica:** planejamento, aulas, atividades, avaliações, materiais e projeto Meu Jogo.
2. **Registro digital:** arquivos, instrumentos de avaliação e sistemas desenvolvidos para apoiar o acompanhamento pedagógico.

## Estrutura sugerida do repositório

```text
Informatica_Educacional_MeuJogo/
├── 01_Projeto/
├── 02_Planejamento/
├── 03_Curriculo/
├── 04_Avaliacoes/
├── 05_Aulas/
├── 06_Recursos/
├── 07_Tecnologia/
├── 08_Seguranca/
├── 09_Documentacao/
├── README.md
└── CHANGELOG.md
```

## Organização de arquivos

Cada aula deve, quando necessário, possuir registros como:

- plano da aula;
- material de apoio;
- apresentação;
- exercício;
- recurso interativo;
- avaliação;
- observações do educador.

## Versionamento

O GitHub será utilizado como histórico do desenvolvimento do projeto. Alterações relevantes devem ser registradas com commits descritivos e mudanças pedagógicas importantes devem ser documentadas.

## Princípio de separação

O repositório público não deve conter dados pessoais identificáveis dos educandos, respostas individuais, credenciais, tokens, chaves de API ou outros dados institucionais/confidenciais.