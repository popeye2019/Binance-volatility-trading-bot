import glob
import asyncio
import time
import sys
print(sys.argv)
nb_thread=5

tps1=time.time()

async def run(shell_command):
    p = await asyncio.create_subprocess_shell(shell_command)
    await p.communicate()


async def main(shell_commands):
    for f in asyncio.as_completed([run(c) for c in shell_commands]):
        await f



commands = ['python signalpop1.py -d 0 -f 5','python signalpop1.py -d 19 -f 24']


loop = asyncio.ProactorEventLoop()
loop.run_until_complete(main(commands))
loop.close()

tps2 = time.time()
print(tps2 - tps1)

