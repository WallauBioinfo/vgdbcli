# vgdbcli
Ferramenta para automação do envio de informações ao VGDB.

## Instalação

Para instalar e usar a ferramenta, você vai precisar de:
- git
- python3
- pip

```bash
git clone https://github.com/WallauBioinfo/vgdbcli
cd vgdbcli
pip install .
```

### Checando a instalação

```bash
vgdbcli --version
    vgdbcli, version 1.0.0
```

## Comandos

A ferramenta vgdbcli conta, até o momento, com 2 comandos:
- `ns`: Cria o input para o VGDB de vírus não segmentados.
- `seg`: Cria o input para o VGDB de vírus segmentados.

Para acessar as informações da ferramenta, basta digitar `vgdbcli --help`.

```bash
vgdbcli --help
    Usage: vgdbcli [OPTIONS] COMMAND [ARGS]...

    Essa ferramenta engloba uma série de funcionalidades para envio de dados a
    plataforma Virus Genome DataBase (VGDB).

    Options:
    --version  Show the version and exit.
    --help     Show this message and exit.

    Commands:
    ns   Cria o arquivo .CSV para vírus não segmentados.
    seg  Cria o arquivo .CSV para vírus segmentados.
```
