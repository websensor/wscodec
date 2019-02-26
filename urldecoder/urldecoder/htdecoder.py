from .decoder import Decoder

class HTDecoder(Decoder):
    """
    Extracts samples containing 2 measurands (temperature and humidity) from the circular buffer.

    Parameters
    ----------
    encstr : str
        Circular buffer string containing samples encoded in base64.

    timestamped : bool
        Indicates whether or not to timestamp the returned samples.

    timeintminutes : int
        Time interval between samples in minutes.

    secretkey : str
        Secret key used to verify the source of the samples.

    """
    def __init__(self, encstr, timestamped, timeintminutes, secretkey):
        super().__init__(encstr, secretkey)

        decsmpls = list()

        for rawsmpl in self.rawsmpls:
            tempMsb = rawsmpl['tempMsb']
            rhMsb = rawsmpl['rhMsb']
            Lsb = rawsmpl['Lsb']

            tempLsb = (Lsb >> 4) & 0xF
            rhLsb = Lsb & 0xF
            temp = ((tempMsb << 4) | tempLsb)
            rh = ((rhMsb << 4) | rhLsb)

            temp = (temp * 165)/4096 - 40
            rh = (rh * 100)/4096

            decsmpl = {'temp':temp, 'rh':rh}
            decsmpls.append(decsmpl)

        self.smpls = self.applytimestamp(decsmpls, timeintminutes)
