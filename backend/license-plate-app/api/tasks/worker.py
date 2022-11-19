# from core.celery import celery
# from app import startup_db_client
# from api.controllers.in_and_out import InAndOutController

# import asyncio

# loop = asyncio.get_event_loop()


# @celery.task()
# def save_realtime_in_or_out(
#     id_vehicle,
#     id_region,
#     time,
#     select
# ):
#     request = loop.run_until_complete(startup_db_client())
#     inAndOutCtrl = InAndOutController(request)
#     asyncio.run(
#         inAndOutCtrl.dotting_in_or_out(
#             id_vehicle,
#             id_region,
#             time,
#             select
#         )
#     )