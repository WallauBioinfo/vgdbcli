## Comando seg

Ao rodar o vgdbcli, temos 2 comandos: `ns` e `seg`. O comando `seg` refere-se a rotinas de  segmentados, como Oropouche e Influenza. Para rodar este comando, basta executar a linha:

```bash
vgdbcli seg --json-input input.json --metadados metadados.csv --unidade IAM --output teste.csv
```

Os argumentos são explicados com o parâmetro `--help` onde:

```
vgdbcli seg --help
Usage: vgdbcli seg [OPTIONS]

  Cria o arquivo .CSV para vírus segmentados.

Options:
  --output TEXT      Nome do output com extensão .csv  [default:
                     vgdbcli_sequenciamento_completo.csv]
  --unidade TEXT     Código da Unidade. Exemplo: IAM, LVRS, FCE.  [required]
  --metadados PATH   Arquivo CSV com metadados das amostras. Modelo na
                     documentação.  [required]
  --json-input PATH  Arquivo json com dados de vírus segmentados. Modelo na
                     documentação.  [required]
  --help             Show this message and exit.
```