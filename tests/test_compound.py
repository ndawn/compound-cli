import re

import pytest

from compound.__main__ import main
from compound.db.models import Compound
from compound.db.models import CompoundType


def test_compound__invalid_command(capsys, db):
    main(['some_invalid_command', 'arg_value_doesnt_matter_here'])

    stdout, _ = capsys.readouterr()

    assert stdout.strip() == f'Unrecognized command: some_invalid_command. Available commands are: sync, show'


@pytest.mark.parametrize('arg', ['ATP', 'ADP', 'STI', '18W', '29P'])
def test_compound_sync__ok(capsys, db, arg):
    main(['sync', arg])

    stdout, _ = capsys.readouterr()
    stdout = stdout.strip()
    compounds = db.query(Compound).filter(Compound.type == CompoundType(arg)).all()

    # I use percent formatting here because I can't use raw string and f-string at the same time,
    # but my IDE was complaining to an invalid escape sequence (which is \d)
    match = re.match(r'Created (?P<count>\d+) new %s entries' % arg, stdout)

    assert match
    created_count = int(match.group('count'))
    assert created_count > 0
    assert len(compounds) == created_count


@pytest.mark.parametrize('command', ['sync', 'show'])
def test_compound__invalid_arg(capsys, command):
    main([command, 'some_invalid_arg'])

    stdout, _ = capsys.readouterr()

    # Here we check for uppercase arg value because it's being modified by the CLI tool
    assert stdout.strip() == f'Unsupported compound type: SOME_INVALID_ARG'


@pytest.mark.parametrize('type_', ['ATP', 'ADP', 'STI', '18W', '29P'])
def test_compound_show__ok(capsys, db, type_):
    db.add(
        Compound(
            name='test_name',
            type=CompoundType(type_),
            formula='test_formula',
            inchi='test_inchi',
            inchi_key='test_inchi_key',
            smiles='test_smiles',
            cross_links_count=123,
        )
    )
    db.flush()

    main(['show', type_])

    stdout, _ = capsys.readouterr()
    stdout = stdout.strip()

    assert stdout == (
        'Total rows: 1\n'
        '+-----------+------+--------------+------------+---------------+-------------+-------------------+\n'
        '| Name      | Type | Formula      | InChI      | InChI key     | Smiles      | Cross links count |\n'
        '+-----------+------+--------------+------------+---------------+-------------+-------------------+\n'
        f'| test_name | {type_}  | test_formula | test_inchi | test_inchi... | test_smiles | 123               |\n'
        '+-----------+------+--------------+------------+---------------+-------------+-------------------+'
    )
