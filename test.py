import sunpy_soar
from sunpy.net import Fido

from sunpy.net.attrs import Instrument, Level, Time
from sunpy_soar.attrs import Identifier

instrument = Instrument('EUI')
time = Time('2021-02-01', '2021-02-02')
level = Level(1)
identifier = Identifier('EUI-FSI174-IMAGE')

res = Fido.search(instrument, time, level, identifier)
print(res)
