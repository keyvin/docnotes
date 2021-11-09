from machine import Pin
from rp2 import PIO, StateMachine, asm_pio

#PICO WIRING - see https://datasheets.raspberrypi.com/pico/Pico-R3-A4-Pinout.pdf
#There is a difference between physical and GPIO. pins in this sketch reference gpio pin numbering

#Basic Operation
#Though the sketch operates fast enough that extra IO wait is not necessary, when the pico keeps a wait line held low
#The chip select is ORed (74hct32) with this wait line, causing the z80 cpu to wait until the pico raises it's wait line
#high. The Pico then waits for it to be deselected, bringing it's wait line low again. 

#I am using a 74HCT154 to decode four address lines, a 74hct32 for address selection and generation of the wait signal
#and two 74lvc125s as logic level shifters

#The chip select is used to enable/disable the 74lvc125, ensuring that the pico is disconneced from the data bus
#after the IO. It has 3.3v on the low side (pico) and 5v on the high side. It is powered from the 3.3v side.
#my z80 is capable of reading the 3.3v during reads properly. Your mileage may vary.

#The write signal from the CPU is used to set the direction of the data bus 74lvc125. It is also used in the state machine. 

#Signals like c/s, write, read, and the lower address lines are passed through the second 74lvc125. It's direction is 
#always B to A. This is to protect the pico. 

#D0-8 connects to GPIOs 19-21. C/S (active low as written, but you can change that in the PIO SM) to GP13, 
#WAIT to GP12 (via ORed cs at 74hct32) and read (from z80, could revers to use write in PIO SM). 

#TL/DR - I am using the c/s for the pico ORed GPIO pin to assert WAIT. When CS is asserted, the data bus is enabled. 
#74lvc125 has it's direction controlled by WRITE. PIO State machine branches based on READ. 


WAIT_PIN = Pin(12, Pin.OUT, )
DATA_BUS_BASE = Pin(14, Pin.OUT)
CS_PIN = Pin(13, Pin.IN)
WRITE_PIN = Pin(11)
    
WAIT_PIN.value(1) #disable blocking on iorequest until ready. 

#PIO - See https://www.raspberrypi.com/news/what-is-pio/
#https://docs.micropython.org/en/latest/library/rp2.html
#https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf

#To change the direction of more than 5 pins at a time, you must
#use out. You can generate all ones with mov osr ~null or zeros with ~1
#all side sets control the wait pin. 
#some of these WILL block (freezing the z80 due to WAIT) or not block. See python documentation
#to change behavior
#we either write output or read input based on WRITE/READ


#Side Sets have no time cost - they occur alongside instruction
#I did briefly test this without the wait pin. At full PICO speed
#Things got missed. At 100mhz PIO, 7Mhz z80 it seemd to work.
#Since PIO operations take one CLOCK CYCLE(!!!!) it may work
#With Steve Curtis's sb130 that does not break out WAIT.

@asm_pio(sideset_init=PIO.OUT_LOW,  autopull=True, pull_thresh=8, out_shiftdir = PIO.SHIFT_RIGHT, out_init=(PIO.OUT_HIGH,PIO.OUT_HIGH,PIO.OUT_HIGH,PIO.OUT_HIGH,PIO.OUT_HIGH,PIO.OUT_HIGH,PIO.OUT_HIGH,PIO.OUT_HIGH))
def z80_io():
    nop().side(0)        
    wait(0,gpio,13)
    jmp(pin,"rcv") #NOTE THE DIFFERENCE ON JMP BETWEEN PIN and PINS - you want pin.           
    mov(osr,invert(null))
    out(pindirs,8)
    pull()    
    out(pins,8)   
    mov(osr,null)
    out(pindirs,8)
    jmp("exit")
    label("rcv")
    mov(osr,invert(null))
    out(pindirs,8)    
    in_(pins, 8)
    push()   
    label("exit")
    nop().side(1)      #de-assert wait
    wait(1,gpio,13)    #Wait for z80 to finish
  
    

sm2 = StateMachine(
        0,
        globals()["z80_io"],   
        freq = 50000000,             #50mhz seems fast enough for 7mhz 780
        out_base=DATA_BUS_BASE,
        in_base=DATA_BUS_BASE,
        set_base=DATA_BUS_BASE,
        sideset_base=WAIT_PIN,
        jmp_pin=WRITE_PIN  #READ/WRITE...
)    

print ("start")    
sm2.active(1) #enable state machine
sm2.put(55) #write an initial value to FIFO
WAIT_PIN.value(0) # enable blocking

j = 1
while True:
    j=j+1    
    sm2.put(j)    
    if sm2.rx_fifo()>0:
        print(sm2.get()) 
    
    