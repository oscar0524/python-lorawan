
import struct
import json
import base64
from collections import OrderedDict
from .error import DecodeError, UnsupportedMethod

"""GWMP Identifiers"""
PUSH_DATA = 0
PUSH_ACK = 1
PULL_DATA = 2
PULL_RESP = 3
PULL_ACK = 4
TX_ACK = 5


class Stat(object):
    """A Gateway Stat (upstream) JSON object.

    The root JSON object shall contain zero or one stat
    objects. See Gateway to Server Interface Definition
    Section 6.2.1.

    Attributes:
        time (str): UTC time of the LoRa frame (us precision).
        lati (float): Gateway latitude in degress north of the equator.
        long (float): Gateway longitude in degress north of the equator.
        alti (int): Altitude of the gateway's position in metres above sea
                    level
        rxnb (int): Number of radio frames received since gateway start.
        rxok (int): Number of radio frames received with correct CRC since
                    gateway start.
        rwfw (int): Number of radio frames forwarded to the network server
                    since gateway start.
        ackr (int): Percentage of radio frames forwarded to the network
                    server, and acknowledged by the server since gateway
                    start.
        dwnb (int): Number of radio frames received from the network server
                    since gateway start.
        txnb (int): Number of radio frames transmitted since gateway start.

    """

    def __init__(self):
        """Stat initialisation method.

        """
        self.time = None
        self.lati = None
        self.long = None
        self.alti = None
        self.rxnb = None
        self.rxok = None
        self.rwfw = None
        self.ackr = None
        self.dwnb = None
        self.txnb = None

    @classmethod
    def decode(cls, stp):
        """Decode Stat JSON dictionary.

        Args:
            stp (dict): Dict representation of stat JSON object.

        Returns:
            Stat object.

        """

        skeys = stp.keys()
        s = Stat()

        # Set the attributes
        s.time = stp['time'] if 'time' in skeys else None
        s.lati = float(stp['lati']) if 'lati' in skeys else None
        s.long = float(stp['long']) if 'long' in skeys else None
        s.alti = int(stp['alti']) if 'alti' in skeys else None
        s.rxnb = int(stp['rxnb']) if 'rxnb' in skeys else None
        s.rxok = int(stp['rxok']) if 'rxok' in skeys else None
        s.rwfw = int(stp['rwfw']) if 'rwfw' in skeys else None
        s.ackr = int(stp['ackr']) if 'ackr' in skeys else None
        s.dwnb = int(stp['dwnb']) if 'dwnb' in skeys else None
        s.txnb = int(stp['txnb']) if 'txnb' in skeys else None
        return s


class Rxpk(object):
    """A Gateway Rxpk (upstream) JSON object.

    The root JSON object shall contain zero or more rxpk
    objects. See Gateway to Server Interface Definition
    Section 6.2.2.

    Attributes:
        tmst (int): value of the gateway time counter when the
                    frame was received (us precision).
        freq (float): Centre frequency of recieved signal (MHz).
        chan (int): Concentrator IF channel on which the frame
                    was received.
        rfch (int): Concentrator RF chain on which the frame
                    was received.
        stat (int): The result of the gateway's CRC test on the
                    frame - 1 = correct, -1 = incorrect, 0 = no test.
        modu (str): Modulation technique - "LORA" or "FSK".
        datr (str): Datarate identifier. For Lora, comprised of
                    "SFnBWm where n is the spreading factor and
                    m is the frame's bandwidth in kHz.
        codr (str): ECC code rate as "k/n" where k is carried
                    bits and n is total bits received.
        rssi (int): The measured received signal strength (dBm).
        lsnr (float): Measured signal to noise ratio (dB).
        data (str): Frame payload encoded in Base64.
        time (str): UTC time of the LoRa frame (us precision).
        size (int): Number of octects in the received frame.

    """

    def __init__(self, tmst=None, freq=None, chan=None, rfch=None,
                 stat=None, modu=None, datr=None, codr=None, rssi=None,
                 lsnr=None, data=None, time=None, size=None):
        """Rxpk initialisation method.

        """
        self.tmst = tmst
        self.freq = freq
        self.chan = chan
        self.rfch = rfch
        self.stat = stat
        self.modu = modu
        self.datr = datr
        self.codr = codr
        self.rssi = rssi
        self.lsnr = lsnr
        self.data = data
        self.time = time
        self.size = size

    @classmethod
    def decode(cls, rxp):
        """Decode Rxpk JSON dictionary.

        Args:
            rxp (dict): Dict representation of rxpk JSON object.

        Returns:
            Rxpk object if successful, None otherwise.

        """

        rkeys = rxp.keys()
        # Check mandatory fields exist
        mandatory = ('tmst', 'freq', 'chan', 'rfch',
                     'stat', 'modu', 'datr', 'codr',
                     'rssi', 'lsnr', 'data')
        if not all(rkeys for k in mandatory):
            return None
        # Mandatory attributes
        tmst = int(rxp['tmst'])
        freq = float(rxp['freq'])
        chan = int(rxp['chan'])
        rfch = int(rxp['rfch'])
        stat = int(rxp['stat'])
        modu = rxp['modu']
        datr = rxp['datr']
        codr = rxp['codr']
        rssi = int(rxp['rssi'])
        lsnr = float(rxp['lsnr'])
        data = base64.b64decode(rxp['data'])
        # Optional attributes
        time = rxp['time'] if 'time' in rkeys else None
        size = int(rxp['size']) if 'size' in rkeys else None
        return Rxpk(tmst=tmst, freq=freq, chan=chan, rfch=rfch, stat=stat,
                    modu=modu, datr=datr, codr=codr, rssi=rssi, lsnr=lsnr,
                    data=data, time=time, size=size)


class Txpk(object):
    """A Gateway Txpk (downstream) JSON object.

    The root JSON object shall contain zero or more txpk
    objects. See Gateway to Server Interface Definition
    Section 6.2.4.

    Attributes:
        imme (bool): If true, the gateway is commanded to
                     transmit the frame immediately 
        tmst (int): If "imme" is not true and "tmst" is present,
                    the gateway is commanded to transmit the frame
                    when its internal timestamp counter equals the
                    value of "tmst".
        time (str): UTC time. The precision is one microsecond. The
                    format is ISO 8601 compact format. If "imme" is
                    false or not present and "tmst" is not present,
                    the gateway is commanded to transmit the frame at
                    this time.
        freq (float): The centre frequency on when the frame is to
                    be transmitted in units of MHz.
        rfch (int): The antenna on which the gateway is commanded
                    to transmit the frame.
        powe (int): The output power which what the gateway is
                    commanded to transmit the frame.
        modu (str): Modulation technique - "LORA" or "FSK".
        datr (str): Datarate identifier. For Lora, comprised of
                    "SFnBWm where n is the spreading factor and
                    m is the frame's bandwidth in kHz.
        codr (str): ECC code rate as "k/n" where k is carried
                    bits and n is total bits received.
        ipol (bool): If true, commands gateway to invert the
                    polarity of the transmitted bits. LoRa Server sets
                    value to true when "modu" equals "LORA", otherwise
                    the value is omitted.
        size (int): Number of octets in the received frame.
        data (str): Frame payload encoded in Base64. Padding characters
                    shall not be not added
        ncrc (bool): If not false, disable physical layer CRC generation
                    by the transmitter.
    """

    def __init__(self, imme=None, tmst=None, time=None, freq=None,
                 rfch=None, powe=None, modu=None, datr=None, codr=None,
                 ipol=None, size=None, data=None, ncrc=None):
        """Txpk initialisation method.

        """
        self.imme = imme
        self.tmst = tmst
        self.time = time
        self.freq = freq
        self.rfch = rfch
        self.powe = powe
        self.modu = modu
        self.datr = datr
        self.codr = codr
        self.ipol = ipol
        self.size = size
        self.data = data
        self.ncrc = ncrc
        self.keys = ['imme', 'tmst', 'time', 'freq', 'rfch',
                     'powe', 'modu', 'datr', 'codr', 'ipol',
                     'size', 'data', 'ncrc']
        # Base64 encode data, no padding
        if self.data is not None:
            self.size = len(self.data)
            self.data = base64.b64encode(self.data)
            # Remove padding
            if self.data[-2:] == '==':
                self.data = self.data[:-2]
            elif self.data[-1:] == '=':
                self.data = self.data[:-1]
        else:
            self.size = 0

    def encode(self):
        """Create a JSON string from Txpk object

        """
        # Create dict from attributes. Maintain added order
        jd = {'txpk': OrderedDict()}
        for key in self.keys:
            val = getattr(self, key)
            if val is not None:
                jd['txpk'][key] = val
        return json.dumps(jd, separators=(',', ':'))


class GatewayMessage(object):
    """A Gateway Message.

    Messages sent between the LoRa gateway and the LoRa network
    server. The gateway message protocol operates over UDP and
    occupies the data area of a UDP packet. See Gateway to Server
    Interface Definition.

    Attributes:
        version (int): Protocol version - 0x01 or 0x02
        token (str): Arbitrary tracking value set by the gateway.
        id (int): Identifier - see GWMP Identifiers above.
        gatewayEUI (str): Gateway device identifier.
        payload (str): GWMP payload.
        remote (tuple): Gateway IP address and port.
        ptype (str): JSON protocol top-level object type.

    """

    def __init__(self, version=1, token=0, identifier=None,
                 gatewayEUI=None, txpk=None, remote=None,
                 ptype=None):
        """GatewayMessage initialisation method.

        Args:
            version (int): GWMP version.
            token (str): Message token.
            id: GWMP identifier.
            gatewayEUI: gateway device identifier.
            payload: GWMP payload.
            ptype (str): payload type
            remote: (host, port)

        Raises:
            TypeError: If payload argument is set to None.

        """
        self.version = version
        self.token = token
        self.id = identifier
        self.gatewayEUI = gatewayEUI
        self.payload = ''
        self.ptype = ptype
        self.remote = remote

        self.rxpk = None
        self.txpk = txpk
        self.stat = None

    @classmethod
    def decode(cls, data, remote):
        """Create a Message object from binary representation.

        Args:
            data (str): UDP packet data.
            remote (tuple): Gateway address and port.

        Returns:
            GatewayMessage object on success.

        """
        # Check length
        if len(data) < 4:
            raise DecodeError("Message too short.")
        # Decode header
        (version, token, identifer) = struct.unpack('<BHB', data[:4])
        m = GatewayMessage(version=version, token=token, identifier=identifer)
        m.remote = remote
        # Test versions (1 or 2) and supported message types
        if (m.version not in (1, 2) or
            m.version == 1 and m.id not in (PUSH_DATA, PULL_DATA) or
            m.version == 2 and m.id not in (PUSH_DATA, PULL_DATA, TX_ACK)
            ):
            raise UnsupportedMethod()

        # Decode gateway EUI and payload
        if m.id == PUSH_DATA:
            if len(data) < 12:
                raise DecodeError("PUSH_DATA message too short.")
            m.gatewayEUI = struct.unpack('<Q', data[4:12])[0]
            m.payload = data[12:]
        elif m.id == PULL_DATA:
            if len(data) < 12:
                raise DecodeError("PULL_DATA message too short.")
            m.gatewayEUI = struct.unpack('<Q', data[4:12])[0]
        elif m.id == TX_ACK:
            m.payload = data[4:]

        # Decode PUSH_DATA payload
        if m.id == PUSH_DATA:
            try:
                jdata = json.loads(m.payload)
            except ValueError:
                raise DecodeError("JSON payload decode error")
            m.ptype = jdata.keys()[0]
            # Rxpk payload - one or more.
            if m.ptype == 'rxpk':
                m.rxpk = []
                for r in jdata['rxpk']:
                    rx = Rxpk.decode(r)
                    if rx is not None:
                        m.rxpk.append(rx)
                if not m.rxpk:
                    raise DecodeError("Rxpk payload decode error")
            # Stat payload
            elif m.ptype == 'stat':
                m.stat = Stat.decode(jdata)
                if m.stat is None:
                    raise DecodeError("Stat payload decode error")
            # Unknown payload type
            else:
                raise DecodeError("Unknown payload type")
        return m

    def encode(self):
        """Create a binary representation of message from Message object.

        Returns:
            String of packed data.

        """
        data = ''
        if self.id == PUSH_ACK:
            data = struct.pack('<BHB', self.version, self.token, self.id)
        elif self.id == PULL_ACK:
            data = struct.pack('<BHBQ', self.version, self.token, self.id,
                               self.gatewayEUI)
        elif self.id == PULL_RESP:
            if self.version == 1:
                self.token = 0
            self.payload = self.txpk.encode()
            data = struct.pack('<BHB', self.version, self.token, self.id) + \
                self.payload
        return data
