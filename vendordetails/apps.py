from django.apps import AppConfig


class VendorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vendordetails'

    # def ready(self) -> None:
    #     try:
    #         import threading
    #         import asyncio
    #         from .consumer import kafka_order_consumer

    #         def run_background_task():
    #             print("Creating Daemon Thread ....... ")
    #             loop = asyncio.new_event_loop()
    #             asyncio.set_event_loop(loop)

    #             loop.create_task(kafka_order_consumer())
    #             loop.run_forever()

    #         thread1 = threading.Thread(target=run_background_task)
    #         thread1.daemon = True
    #         thread1.start()

    #     except Exception as e:
    #         print(e)
