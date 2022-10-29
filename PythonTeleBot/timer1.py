
async def add_timer(name, time):
	await asyncio.sleep(time)
	print(f"Timer {name} has finished! in {time} seconds")

async def main(timers_):
	tasks = []
	for time in timers_:
		tasks.append(asyncio.create_task(add_timer(*time)))
	
	for task in tasks:
		await task



if __name__ == "__main__":

	timers = [
		["f", 10],
		["s", 11],
		["third", 3],
		["fourth", 5]
	]
	asyncio.run(main(timers))

