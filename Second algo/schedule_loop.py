import schedule
import time

import algo_decisions as ad


schedule.every(ad.buy_sell_frequency).seconds.do(ad.algo_decision)

while True:
    schedule.run_pending()
    time.sleep(1)


# algo decisions uncomment is_open() and remove the fake one