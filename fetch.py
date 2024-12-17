from config import config

config.setPredictionDaySpan(3)
config.setMinimumApparentElevation(35)
config.setNoradId(config.NOAA15ID)

print("The Radio Passes URL is set as:")
print("%s"%config.buildUrl())
