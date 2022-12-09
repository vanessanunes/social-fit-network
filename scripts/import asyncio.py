import asyncio
import os
import factory.random
import random
from datetime import datetime, timedelta
from typing import List
from unittest.mock import AsyncMock

from sqlalchemy.exc import InternalError, OperationalError
from sqlalchemy import select
from sqlalchemy.sql.ddl import CreateTable

from src.clubbi.common.mysql import with_sql_engine
from src.clubbi.data.external_data_definition import (
    metadata,
    table_clubbi_product,
    table_category_volume,
    table_supplier,
    table_merchants,
    table_region,
    table_partnership_prices,
)
from src.clubbi.data.merchants_repository import MerchantsRepository
from src.clubbi.data.order_repository import OrderRepository
from src.clubbi.data.protocols import Engine
from src.clubbi.data.region_repository import RegionRepository
from src.clubbi.data.supplier_repository import SupplierRepository
from src.clubbi.data.product_repository import ProductLogisticInfoRepository
from src.clubbi.data.shopper_plan_repository import ShopperPlanRepository
from src.clubbi.data.store_repository import StoreRepository
from src.clubbi.domain.shopper_plan import GenerateShopperPlanOptions, ShopperPlanCommandHandler
from src.clubbi.mocks.region import regions
from src.test.factories.merchant_factory import MerchantFactory
from src.test.factories.order_factory import OrderFactory


__MERCHANTS_IDS = ["QTKAU", "AXUOW"]


def random_datetime():
    return datetime.now() - timedelta(
        days=randint(0, 31),
        hours=randint(0, 23),
        minutes=randint(0, 59),
        seconds=randint(0, 59),
    )


async def create_clubbi_schema(engine: Engine):
    print("Creating schema (if not exists)")
    async with engine.connect() as conn:
        await conn.exec_driver_sql("CREATE SCHEMA IF NOT EXISTS clubbi;")


async def create_tables(engine: Engine):
    print("Creating tables (if not exists)")
    metadata.bind = engine
    tables = [
        table_merchants,
        table_supplier,
        table_clubbi_product,
        table_category_volume,
        table_region,
        table_partnership_prices,
    ]
    stmts = [CreateTable(table) for table in tables]
    for stmt in stmts:
        try:
            async with engine.connect() as conn:
                await conn.execute(stmt)
        except (InternalError, OperationalError) as e:
            print(f"{str(e)=}")
            if "1050" in str(e):  # 1050 = table already exists
                pass
            else:
                raise e


async def create_regions(engine: Engine):
    print("Creating regions (if not exists)")
    async with engine.connect() as conn:
        get_existing_ids = select([table_region.c.id]).select_from(table_region)
        proxy = await conn.execute(get_existing_ids)
        result = proxy.fetchall()
        existing_ids = [row[0] for row in result]
        for region in regions:
            if region.get("id") not in existing_ids:
                stmt = table_region.insert().values(**region)
                await conn.execute(stmt)


async def create_merchants(engine: Engine) -> None:
    print("Upserting merchants")
    merchants = [MerchantFactory(client_site_code=merchant_id) for merchant_id in __MERCHANTS_IDS]
    async with engine.connect() as conn:
        get_existing_ids = select([table_merchants.c.id]).select_from(table_merchants)
        proxy = await conn.execute(get_existing_ids)
        result = proxy.fetchall()
        existing_ids = [row[0] for row in result]
        for merchant in merchants:
            if merchant.id in existing_ids:
                await conn.execute(
                    table_merchants.update().where(table_merchants.c.id == merchant.id).values(merchant.to_db_model())
                )
                continue
            await conn.execute(table_merchants.insert().values(merchant.to_db_model()))


async def create_orders(engine: Engine) -> List[int]:
    print("Creating orders")
    orders = [
        OrderFactory(already_saved=False, region_id=1, customer_id=__MERCHANTS_IDS[i % len(__MERCHANTS_IDS)])
        for i in range(10)
    ]

    for order in orders:
        order_repo = OrderRepository(engine)
        await order_repo.save(order)

    return [i.id or 0 for i in orders]


async def generate_plans(orders_ids: List[int], engine: Engine) -> None:
    handler = ShopperPlanCommandHandler(
        order_repository=OrderRepository(engine),
        shopper_plan_repository=ShopperPlanRepository(engine),
        store_repository=StoreRepository(),
        publisher=AsyncMock(),
        product_repository=ProductLogisticInfoRepository(engine),
        merchant_repository=MerchantsRepository(engine),
        supplier_repository=SupplierRepository(engine),
        region_repository=RegionRepository(engine),
        number_of_workers=1,
    )
    await handler.calculate_plans(
        options=GenerateShopperPlanOptions(
            order_ids=orders_ids[0:1],
            region_id=1,
            status=None,
            split_version=3,
        )
    )


@with_sql_engine
async def _main(engine: Engine):
    assert os.environ.get("MYSQL_HOST") == "localhost"

    factory.random.reseed_random(42)
    random.seed(42)

    await create_clubbi_schema(engine)
    await create_tables(engine)
    await create_regions(engine)
    await create_merchants(engine)
    order_ids = await create_orders(engine)
    await generate_plans(order_ids, engine)


def main():
    asyncio.run(_main())


if __name__ == "__main__":
    main()
