from flask import Flask
import click


def add_cmds(app: Flask):


    @app.cli.command('runscript')
    @click.argument('script')
    def runscript(script):
        f = open(script)
        exec(f.read())
        f.close()
