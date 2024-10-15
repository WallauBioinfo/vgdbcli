## Comando ns

Ao rodar o vgdbcli, temos 2 comandos: `ns` e `seg`. O comando `ns` refere-se a rotinas de vírus não segmentados, como SARS-CoV-2, Denv, Chikv, Mpox, etc. Para rodar este comando, basta executar a linha:

```bash
vgdbcli ns --json-input input.json --metadados metadados.csv --unidade IAM --output teste.csv
```

Os argumentos são explicados com o parâmetro `--help` onde:

```
vgdbcli ns --help
Usage: vgdbcli ns [OPTIONS]

  Cria o arquivo .CSV com informações de sequenciamento completo para vírus
  não-segmentados.

Options:
  --json-input PATH  Arquivo Json no modelo de virus não segmentados. Modelo
                     na documentação.  [required]
  --metadados PATH   Arquivo CSV com metados das amostras. Opcional, conflita
                     com algum dos argumentos de metadados do gisaid. Modelo
                     na documentação. [required]
  --unidade TEXT     Código da Unidade. Exemplo: IAM, LVRS, FCE.  [required]
  --output TEXT      Nome do output com extensão .csv  [default:
                     vgdbcli_sequenciamento_completo.csv]
  --help             Show this message and exit.
```