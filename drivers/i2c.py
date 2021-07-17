

class I2CClient(object):

    def __init__(self):
        pass

    def begin_transmission(self, i2c_address):
        self.transmitting = 1
        self.txaddress = i2c_address
        self.txbufferindex = 0
        self.txbufferlength = 0

    def end_transmission(self):
        pass

    def request_from(self, i2c_address, arg):
        pass

    def write(self):
        pass

    def read(self):
        pass



receiveData(uint8_t command, uint32_t& data)
{
  Wire.beginTransmission(I2C_ADDRESS);
  if (Wire.write(command) != 1){
    return STATUS_ERROR;
  }
  if (Wire.endTransmission(false)){  // NB: don't send stop here
    return STATUS_ERROR;
  }
  if (Wire.requestFrom(uint8_t(I2C_ADDRESS), uint8_t(2)) != 2){
    return STATUS_ERROR;
  }
  data = Wire.read();
  data |= uint32_t(Wire.read()) << 8;
  return STATUS_OK;
}