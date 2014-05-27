CON
  _clkmode = xtal1 + pll16x                    ' Setup PLL       
  _xinfreq = 5_000_000                         ' Setup Clock

  SerialInBaud = serial#BAUD9600               ' Set USB Serial Baud rate 
  
  SerialLCDPin = 0                             ' Set Serial LCD pin
  SerialLCDBaud = serial#BAUD9600              ' Set Serial LCD Baud rate
  
OBJ
  serial  : "pcFullDuplexSerial4FC128"         ' Import Serial Object
VAR
  byte ClearLCD                                ' Declare Variable for Clear LCD Command 

PUB main|SerialCharacter
                                               ' Clear LCD Command, Serial LCD Controller Specific. Change as needed.           
  ClearLCD := string("?f")                     ' Clear LCD Command for Modern Device LCD117 Serial LCD Kit                      
                                               ' http://moderndevice.com/product/lcd117-serial-lcd-kit/                         
                                                                                                                                
  init_uarts                                   ' Setup both Serial ports                                                        
                                                                                                                                
  serial.str(1, ClearLCD)                      ' Send Clear Screen Command to LCD                                               
  waitcnt(clkfreq / 100 + cnt)                 ' Wait some time so we don't overload the buffer                                 
  serial.str(1, string("IRC2LCD"))             ' Send ID message to LCD                                                         
  waitcnt(clkfreq / 2 + cnt)                   ' Wait some time to display ID message                                           
  serial.str(1, ClearLCD)                      ' Send Clear Screen Command to LCD                                               
  waitcnt(clkfreq / 100 + cnt)                 ' Wait some time so we don't overload the buffer                                 
                                                                                                                                
 repeat                                                                                                                         
    SerialCharacter := serial.getc(0)          ' Get Character from USB serial port                                             
    if SerialCharacter == 13                   ' Look for \r (python style Carriage Return)                                     
      SerialCharacter := serial.rxtime(0, 5)   ' Wait for next Character                                                        
      if SerialCharacter == 9                  ' Look for \t (python style Tab Character)                                       
        serial.str(1, ClearLCD)                ' Send Clear Screen Command to LCD                                               
    serial.tx(1, SerialCharacter)              ' Send "SerialCharacter" to LCD                                                  
    waitcnt(clkfreq / 100 + cnt)               ' Wait some time so we don't overload the buffer                                 
    
PUB init_uarts
  serial.init                                  ' Initialize Serial object

  serial.AddPort(0,31,30,serial#PINNOTUSED,serial#PINNOTUSED,serial#DEFAULTTHRESHOLD,serial#NOMODE,SerialInBaud)                            ' Serial through USB to PC
  serial.AddPort(1,serial#PINNOTUSED,SerialLCDPin,serial#PINNOTUSED,serial#PINNOTUSED,serial#DEFAULTTHRESHOLD,serial#NOECHO,SerialLCDBaud)  ' Serial to Serial LCD       
                                                             
  serial.Start                                 ' Start Serial object
  waitcnt(clkfreq / 100 + cnt)                 ' Wait some time so we don't overload the buffer 