import asyncio

from live_stream.theta_data.theta_opt_listener import ThetaOptionStreamListener
theta_option_stream_listener = ThetaOptionStreamListener()

async def main():
    # await theta_option_stream_handler.stop()
    await theta_option_stream_listener.connect()

if __name__ == "__main__":

    asyncio.get_event_loop().run_until_complete(main())