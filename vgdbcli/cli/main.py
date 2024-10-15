#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
import sys
from vgdbcli import __version__
from vgdbcli.vgdbcli import ModoNaoSegmentado, ModoSegmentado
from vgdbcli.vgdbcli import (
    MENSAGEM_ERRO_JSON,
    MENSAGEM_ERRO_METADADOS,
    MENSAGEM_ERRO_VIRALFLOW,
    MENSAGEM_ERRO_VGDBCLI,
)


@click.version_option(__version__)
@click.group()
def cli():
    """
    Essa ferramenta engloba uma série de funcionalidades para envio de dados
    a plataforma Virus Genome DataBase (VGDB).
    """
    pass


def argumentos_padrao(help_json: str):
    def wrapper(argumentos):
        argumentos = click.option(
            "--json-input",
            help=f"{help_json}. Modelo na documentação.",
            type=click.Path(exists=True),
            required=True,
        )(argumentos)
        argumentos = click.option(
            "--metadados",
            help="Arquivo CSV com metadados das amostras. Modelo na documentação.",
            type=click.Path(exists=True),
            required=True,
        )(argumentos)
        argumentos = click.option(
            "--unidade",
            type=str,
            help="Código da Unidade. Exemplo: IAM, LVRS, FCE.",
            required=True,
        )(argumentos)
        argumentos = click.option(
            "--output",
            default="vgdbcli_sequenciamento_completo.csv",
            show_default=True,
            type=str,
            help="Nome do output com extensão .csv",
        )(argumentos)
        return argumentos

    return wrapper


@cli.command()
@argumentos_padrao(help_json="Arquivo json com dados de vírus não segmentados")
def ns(json_input, metadados, unidade, output):
    """
    Cria o arquivo .CSV para vírus não segmentados.
    """
    modo_ns = ModoNaoSegmentado()
    try:
        rotinas = modo_ns.get_rotinas(json_path=json_input)
    except Exception as err:
        click.secho(
            MENSAGEM_ERRO_JSON.format(err),
            err=True,
            fg="red",
        )
        sys.exit(1)
    try:
        resultados_viralflow_df = modo_ns.get_resultados_viralflow_df(
            rotinas_ns=rotinas
        )
    except Exception as err:
        click.secho(
            MENSAGEM_ERRO_VIRALFLOW.format(err),
            err=True,
            fg="red",
        )
        sys.exit(1)
    try:
        metadados_df = modo_ns.get_metadados_df(metadados_path=metadados)
    except Exception as err:
        click.secho(
            MENSAGEM_ERRO_METADADOS.format(err),
            err=True,
            fg="red",
        )
        sys.exit(1)
    try:
        modo_ns.create_ns_vgdbcli_input(
            resultados_viralflow_df=resultados_viralflow_df,
            metadados_df=metadados_df,
            unidade=unidade,
            arquivo_output=output,
        )
        click.secho(
            f"Pronto! O arquivo {output} foi criado e pode ser enviado ao VGDB.",
            fg="green",
        )
    except Exception as err:
        click.secho(
            MENSAGEM_ERRO_VGDBCLI.format(err),
            err=True,
            fg="red",
        )
        sys.exit(1)

@cli.command()
@argumentos_padrao(help_json="Arquivo json com dados de vírus segmentados")
def seg(json_input, metadados, unidade, output):
    """
    Cria o arquivo .CSV para vírus segmentados.
    """
    modo_seg = ModoSegmentado()
    try:
        rotinas = modo_seg.get_rotinas(json_path=json_input)
    except Exception as err:
        click.secho(
            MENSAGEM_ERRO_JSON.format(err),
            err=True,
            fg="red",
        )
        sys.exit(1)
    try:
        resultados_viralflow_df = modo_seg.get_resultados_viralflow_df(
            rotinas_ns=rotinas
        )
    except Exception as err:
        click.secho(
            MENSAGEM_ERRO_VIRALFLOW.format(err),
            err=True,
            fg="red",
        )
        sys.exit(1)
    try:
        metadados_df = modo_seg.get_metadados_df(metadados_path=metadados)
    except Exception as err:
        click.secho(
            MENSAGEM_ERRO_METADADOS.format(err),
            err=True,
            fg="red",
        )
        sys.exit(1)
    try:
        modo_seg.create_seg_vgdbcli_input(
            resultados_viralflow_df=resultados_viralflow_df,
            metadados_df=metadados_df,
            unidade=unidade,
            arquivo_output=output,
        )
        click.secho(
            f"Pronto! O arquivo {output} foi criado e pode ser enviado ao VGDB.",
            fg="green",
        )
    except Exception as err:
        click.secho(
            MENSAGEM_ERRO_VGDBCLI.format(err),
            err=True,
            fg="red",
        )
        sys.exit(1)