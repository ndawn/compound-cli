import logging
from typing import Optional

from compound.action import Action
from compound.api import ApiService
from compound.handler import ActionHandler
from compound.db.models import Compound
from compound.logger import get_logger
from compound.misc import log_and_print

logger = get_logger(__name__)

handler = ActionHandler()


@handler.action('sync')
class SyncAction(Action):
    def act(self, arg: Optional[str]) -> None:
        try:
            compound_type = self._get_compound_enum_type(arg)
        except ValueError as exception:
            print(exception.args[0])
            return

        api = ApiService(self.config)
        compounds = api.list_compounds(compound_type)
        logger.debug(f'Retrieved {len(compounds)} entries from remote API')

        created_counter = 0

        for compound_data in compounds:
            compound, created = self.repository.get_or_create(
                type_=compound_type,
                name=compound_data.get('name'),
                formula=compound_data.get('formula'),
                inchi=compound_data.get('inchi'),
                inchi_key=compound_data.get('inchi_key'),
                smiles=compound_data.get('smiles'),
                cross_links_count=len(compound_data.get('cross_links', [])),
            )

            created_counter += created

        log_and_print(logger, f'Created {created_counter} new {arg} entries', logging.INFO)


@handler.action('show')
class ShowAction(Action):
    header_row = (
        'Name',
        'Type',
        'Formula',
        'InChI',
        'InChI key',
        'Smiles',
        'Cross links count',
    )

    def act(self, arg: Optional[str]) -> None:
        if arg is not None:
            try:
                compound_type = self._get_compound_enum_type(arg)
            except ValueError as exception:
                print(exception.args[0])
                return
        else:
            compound_type = None

        compounds = self.repository.get_many(compound_type)
        logger.debug(f'Retrieved {len(compounds)} from database')

        table = self._build_table(compounds)

        print(f'Total rows: {len(compounds)}')
        print(table)

    def _get_compound_as_row(self, compound: Compound) -> tuple[str, ...]:
        return tuple(
            self._trimmed(value)
            for value in (
                compound.name,
                compound.type.value,
                compound.formula,
                compound.inchi,
                compound.inchi_key,
                compound.smiles,
                str(compound.cross_links_count),
            )
        )

    def _trimmed(self, value: str) -> str:
        if len(value) > self.config.value_max_length + 3:
            return value[:self.config.value_max_length] + '...'
        return value

    def _build_table(self, compounds: list[Compound]) -> str:
        max_column_widths = dict.fromkeys(self.header_row, 0)

        rows = [self.header_row, *(self._get_compound_as_row(compound) for compound in compounds)]

        for i, column in enumerate(self.header_row):
            max_column_widths[column] = max(map(len, (row[i] for row in rows)))

        rows = [self._build_row(row, max_column_widths) for row in rows]
        row_separator = self._build_row_separator(max_column_widths)

        return f'{row_separator}\n' + f'\n{row_separator}\n'.join(rows) + f'\n{row_separator}'

    def _build_row(self, values: tuple[str, ...], column_widths: dict[str, int]) -> str:
        justified_columns = []

        for i, column in enumerate(self.header_row):
            justified_columns.append(f'{values[i].ljust(column_widths[column])}')

        return '| ' + ' | '.join(justified_columns) + ' |'

    def _build_row_separator(self, column_widths: dict[str, int]) -> str:
        return '+-' + '-+-'.join(['-' * (column_widths[column]) for column in self.header_row]) + '-+'
