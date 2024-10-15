# vgdbcli

Ferramenta para automação do envio de informações ao VGDB. Nesta primeira versão, a ferramenta concatena os resultados do ViralFlow juntamente com metadados que o usuário providencia, de forma a criar os inputs para o VGDB de forma padronizada, e em caso de erros, informando ao usuário as possíveis causas.

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

## Testando

No diretório `teste` constam os arquivos e instruções para teste dos dois módulos da ferramenta.

## Linhas de comando

Ambos os métodos possuem os mesmos argumentos:

```bash
vgdbcli ns --json-input <input.json> --metadados <metadados.csv> --unidade <unidade> --output <output.csv>
vgdbcli seg --json-input <input.json> --metadados <metadados.csv> --unidade <unidade> --output <output.csv>
```

## Input json

Ambos os módos recebem um arquivo json, com a seguinte informação:

### não segmentado

```json
{
    "ID-ROTINA-TESTE1": {
        "virus" : "SARS-CoV-2",
        "data_rotina": "2024-10-23",
        "primer": "CovidSeq_V3",
        "protocolo": "Padrão CovidSeq",
        "resultados_viralflow": "./ROTINA_TESTE_NS/RESULTS/COMPILED_OUTPUT/short_summary.csv"
    },
    "ID-ROTINA-TESTE2": {
        "virus" : "DENV-1",
        "data_rotina": "2023-10-23",
        "primer": "DENV1_G5_Naveca",
        "protocolo": "Protocolo DenV_OT",
        "resultados_viralflow": "./ROTINA_TESTE_2_NS/RESULTS/COMPILED_OUTPUT/short_summary.csv"
    }
}
```

### segmentado

```json
{
    "ID-ROTINA-TESTE": {
        "virus" : "OROPOUCHE",
        "data_rotina": "2024-10-23",
        "primer": "OrovSeq_V1",
        "protocolo": "Padrão Orov",
        "resultados_viralflow_segmentos": 
            {
                "L": "./ROTINA_TESTE_SEG/RESULTS_L/COMPILED_OUTPUT/short_summary.csv",
                "M": "./ROTINA_TESTE_SEG/RESULTS_M/COMPILED_OUTPUT/short_summary.csv",
                "S": "./ROTINA_TESTE_SEG/RESULTS_S/COMPILED_OUTPUT/short_summary.csv"
            }
    }
}
```

Ambos os tipos de input aceitam uma lista de rotinas, e possuem 4 campos em comum:
- virus
- data_rotina
- primer
- protocolo

O que difere de um método para outro é que:
- no método `ns` é passado o campo `resultados_viralflow` onde o usuário deve setar o path dos resultados compiltados `short_summary.csv` do ViralFlow.
- no método `seg` é passado o campo `resultados_viralflow_segmentos` onde o usuário deve setar um dicionário com a relação segmento e path dos resultados compilados `short_summary.csv` do ViralFlow para cada segmento.

Os valores aceitos para virus, primer, protocolo, podem ser [checados neste manual](https://docs.google.com/document/d/13Exnz0zlYgqtqcec9ulk-vRlzTJs5GRRP8H5a8yOzMs/edit?usp=sharing).

## Input de metadados

O arquivo de metadados deve ser um .CSV (separado por vírgula), com os seguintes campos:

| campo               | tipo             | obrigatório* | valores possíveis                                                                                          |
| ------------------- | ---------------- | ------------ | ---------------------------------------------------------------------------------------------------------- |
| cod_amostra         | string           | TRUE         | -                                                                                                          |
| uf                  | enum(string)     | TRUE         | AC, AL, AM, AP, BA, CE, DF, ES, GO, MA, MG, MS, MT, PA, PB, PE, PI, PR, RJ, RN, RO, RR, RS, SC, SE, SP, TO |
| municipio           | string           | FALSE        | -                                                                                                          |
| lab_origem          | enum(string)     | TRUE         | Checar manual                                                                                              |
| data_coleta         | data(YYYY-MM-DD) | TRUE         | -                                                                                                          |
| paciente_genero     | string           | FALSE        | M/F/Male/Female/Masculino/Feminino                                                                         |
| paciente_nascimento | data(YYYY-MM-DD) | FALSE        | -                                                                                                          |
| gal_fiocruz         | string           | FALSE        | -                                                                                                          |
| gal_lacen           | string           | FALSE        | -                                                                                                          |
| linhagem            | string           | TRUE         | -                                                                                                          |
| submetido           | booleano         | FALSE        | TRUE/FALSE                                                                                                 |
| banco_de_dados      | enum(string)     | FALSE        | Gisaid, EpiFlu,EpiCoV, EpiRSV, EpiPox, EpiArbo, NCBI, EBI, ENA                                             |
| gisaid_virus_name   | string           | FALSE        | Nome do vírus no arquivo fasta submetido                                                                   |

