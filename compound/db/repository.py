from typing import Optional

from compound.logger import get_logger
from compound.db.models import Compound
from compound.db.models import CompoundType
from compound.db.session import Session

from sqlalchemy import true

logger = get_logger(__name__)


class Repository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_many(self, type_: Optional[CompoundType] = None) -> list[Compound]:
        filter_expression = true()

        if type_ is not None:
            filter_expression &= Compound.type == type_

        query = self.session.query(Compound).filter(filter_expression).order_by(Compound.type)
        logger.debug(f'Querying database: {str(query)}')
        return query.all()

    def get_or_create(
        self,
        type_: CompoundType,
        name: str,
        formula: str,
        inchi: str,
        inchi_key: str,
        smiles: str,
        cross_links_count: int,
    ) -> tuple[Compound, bool]:
        query = self.session.query(Compound).filter(
            (Compound.type == type_)
            & (Compound.name == name)
            & (Compound.formula == formula)
            & (Compound.inchi == inchi)
            & (Compound.inchi_key == inchi_key)
            & (Compound.smiles == smiles)
            & (Compound.cross_links_count == cross_links_count)
        )

        logger.debug(f'Querying database: {str(query)}')

        compound = query.one_or_none()
        logger.debug(f'Retrieved compound: {compound}')

        if compound is not None:
            return compound, False

        compound = Compound(
            type=type_,
            name=name,
            formula=formula,
            inchi=inchi,
            inchi_key=inchi_key,
            smiles=smiles,
            cross_links_count=cross_links_count,
        )

        self.session.add(compound)
        self.session.flush()

        return compound, True
