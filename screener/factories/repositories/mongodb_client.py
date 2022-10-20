from pymongo import MongoClient
from screener.repositories.index import IndexRepository
from screener.repositories.institutional_investor import InstitutionalInvestorRepository
from screener.repositories.mongodb import AppMongoClient
from screener.repositories.sector import SectorRepository
from screener.repositories.stock import StockRepository

DATABASE_NAME = "transformed-data"


def _get_mongo_client():
    return MongoClient(host="localhost", port=27017)


def _get_app_mongodb_repository(collection_name: str) -> AppMongoClient:
    return AppMongoClient(
        database_name=DATABASE_NAME,
        collection_name=collection_name,
        mongo_client=_get_mongo_client()
    )


def get_stock_repository() -> StockRepository:
    client = _get_app_mongodb_repository(StockRepository.STOCK_DOCS_NAME)
    return StockRepository(client)


def get_index_repository() -> IndexRepository:
    repository = _get_app_mongodb_repository(IndexRepository.INDEX_DOCS_NAME)
    return IndexRepository(repository, get_stock_repository())


def get_sector_repository() -> SectorRepository:
    return SectorRepository(get_stock_repository())


def get_institutional_investor_repository() -> InstitutionalInvestorRepository:
    client = _get_app_mongodb_repository(InstitutionalInvestorRepository.INSTITUTIONAL_INVESTOR_NAME)
    return InstitutionalInvestorRepository(client)
