I2C_ADDRESS = 0x10
COMMAND_ALS = 0x04

STATUS_OK = 0
STATUS_ERROR = 0xff


class DigitalAmbiantLightSensor(object):
    """SEN0228 Gravity sensor driver.

    Attributes:
        lux (float): Value from sensor.
    """

    def __init__(self, i2c_client):
        self.__lux = 0.0
        self.__i2c_address = I2C_ADDRESS
        self.__i2c = i2c_client(I2C_ADDRESS)

    @property
    def lux(self):
        return self.__lux

    @property
    def i2c_address(self):
        return self.__i2c_address

    def get(self):
       self.__receive_data(COMMAND_ALS)
       #self.__scale_lux()

    def __receive_data(self, command):
        self.__i2c.begin_transmission(I2C_ADDRESS)
        if self.__i2c.write(command) != 1:
            return STATUS_ERROR
        if not self.__i2c.end_transmission:
            return STATUS_ERROR
        if self.__i2c.request_from(I2C_ADDRESS, 2) != 2:
            return STATUS_ERROR
        self.data = self.__i2c.read()
        self.data |= int(self.__i2c.read()) << 8
        return STATUS_OK

"""
scaleLux(uint32_t raw_counts, float& lux)
{
  als_gain_t gain;
  als_itime_t itime;
  getGain(gain);
  getIntegrationTime(itime);

  float factor1, factor2, result;
  static uint8_t x1=0, x2=1, d8=0;

  switch(gain & 0x3){
  case ALS_GAIN_x1:
    factor1 = 1.f;
    break;
  case ALS_GAIN_x2:
    factor1 = 0.5f;
    break;
  case ALS_GAIN_d8:
    factor1 = 8.f;
    break;
  case ALS_GAIN_d4:
    factor1 = 4.f;
    break;
  default:
    factor1 = 1.f;
    break;
  }

  switch(itime){
  case ALS_INTEGRATION_25ms:
    factor2 = 0.2304f;
    break;
  case ALS_INTEGRATION_50ms:
    factor2 = 0.1152f;
    break;
  case ALS_INTEGRATION_100ms:
    factor2 = 0.0576f;
    break;
  case ALS_INTEGRATION_200ms:
    factor2 = 0.0288f;
    break;
  case ALS_INTEGRATION_400ms:
    factor2 = 0.0144f;
    break;
  case ALS_INTEGRATION_800ms:
    factor2 = 0.0072f;
    break;
  default:
    factor2 = 0.2304f;
    break;
  }

  result = raw_counts * factor1 * factor2;
  if((result > 1880.00f) && (result < 3771.00f)){
	  if(x1 == 1){
		begin(ALS_GAIN_x1);
		x1 = 0; x2 = 1; d8 = 1;
	  }
  }else if(result>3770.00f){
	  if(d8 == 1){
		begin(ALS_GAIN_d8);
		x1 = 1; x2 = 1; d8 = 0;
	  }
  }else{
	  if(x2 == 1){
		begin();  
		x1 = 1; x2 = 0; d8 = 1;
	  }
  }
  lux = result;
  // apply correction from App. Note for all readings
  //   using Horner's method
  lux = lux * (1.0023f + lux * (8.1488e-5f + lux * (-9.3924e-9f + 
                                                    lux * 6.0135e-13f)));
}
"""
