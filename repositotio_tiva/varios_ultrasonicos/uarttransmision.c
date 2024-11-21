#include <stdint.h>
#include <stdbool.h>
#include "inc/hw_memmap.h"
#include "inc/hw_ints.h"
#include "driverlib/sysctl.h"
#include "driverlib/gpio.h"
#include "driverlib/uart.h"
#include "driverlib/pin_map.h"
#include "utils/uartstdio.h"
#include "driverlib/timer.h"     
#include "driverlib/interrupt.h" 
#include "inc/hw_ints.h"         

#define MAX_BUFFER_SIZE 100       // Tamaño máximo del buffer para almacenar la frase
#define BAUDIOS 9600              // Velocidad de comunicación UART
#define TRIG_PIN GPIO_PIN_0       // Pin para Trig del sensor ultrasónico
#define ECHO_PIN GPIO_PIN_1       // Pin para Echo del sensor ultrasónico
#define TRIG_PORT GPIO_PORTL_BASE
#define ECHO_PORT GPIO_PORTL_BASE

uint32_t distance;
uint32_t startTime, endTime, duration;
uint32_t ui32SysClock;           
char uartBuffer[MAX_BUFFER_SIZE]; 
volatile uint8_t bufferIndex = 0; 

static void configureSysClock(void);  
static void configureUART0(void);     
static void config_timer(void);
static void config_timer1(void);
static void config_ultrasonico(void);
void medir_distancia(void);

int main(void) {
    configureSysClock();  
    configureUART0();     
    config_timer();
    config_timer1();
    config_ultrasonico();

    while (1) {
        medir_distancia();
    }
}

// Manejador de interrupciones del Timer1
void Timer1IntHandler(void) {
    TimerIntClear(TIMER1_BASE, TIMER_TIMA_TIMEOUT);
}

// Manejador de interrupciones del Timer0
void Timer0IntHandler(void) {
    TimerIntClear(TIMER0_BASE, TIMER_TIMA_TIMEOUT);
}

// Manejador de interrupciones de UART0 (cuando se recibe un dato)
void UART0IntHandler(void) {
    uint32_t ui32Status;
    char receivedChar;

    ui32Status = UARTIntStatus(UART0_BASE, true);
    UARTIntClear(UART0_BASE, ui32Status);

    while (UARTCharsAvail(UART0_BASE)) {
        receivedChar = UARTCharGetNonBlocking(UART0_BASE);

        if (receivedChar == '\r' || receivedChar == '\n') {
            uartBuffer[bufferIndex] = '\0'; 
            UARTprintf("Datos recibidos %s\r\n", uartBuffer);  
            bufferIndex = 0;
        }
        else {
            if (bufferIndex < MAX_BUFFER_SIZE - 1) {
                uartBuffer[bufferIndex++] = receivedChar;
            }
            else {
                UARTprintf("Buffer lleno, frase demasiado larga.\r\n");
                bufferIndex = 0;
            }
        }
    }
}

// Función para medir la distancia con el sensor ultrasónico
void medir_distancia(void){
    GPIOPinWrite(TRIG_PORT, TRIG_PIN, TRIG_PIN);
    SysCtlDelay(400);  

    GPIOPinWrite(TRIG_PORT, TRIG_PIN, 0);

    while (GPIOPinRead(ECHO_PORT, ECHO_PIN) == 0);
    startTime = TimerValueGet(TIMER1_BASE, TIMER_A);  

    while (GPIOPinRead(ECHO_PORT, ECHO_PIN) != 0);
    endTime = TimerValueGet(TIMER1_BASE, TIMER_A);  

    duration = startTime - endTime;  
    float time_us = (float)duration * 0.00833f;
    distance = time_us / 58.0f;

    UARTprintf("Distancia: %d cm\r\n", (int)distance);
    SysCtlDelay(120000000 * 0.1);
}

// Configuración del sensor ultrasónico
static void config_ultrasonico(void){
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOL);
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOL));

    GPIOPinTypeGPIOOutput(TRIG_PORT, TRIG_PIN);
    GPIOPinTypeGPIOInput(ECHO_PORT, ECHO_PIN);

    GPIOPinWrite(TRIG_PORT, TRIG_PIN, 0);
}

// Configuración del reloj del sistema a 120 MHz
static void configureSysClock(void) {
    ui32SysClock = SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ |
                                       SYSCTL_OSC_MAIN |
                                       SYSCTL_USE_PLL |
                                       SYSCTL_CFG_VCO_480), 120000000);
}

// Configuración del Timer0 para generar interrupciones periódicas
static void config_timer(void) {
    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER0);
    TimerConfigure(TIMER0_BASE, TIMER_CFG_A_PERIODIC | TIMER_CFG_B_ONE_SHOT);
    TimerLoadSet(TIMER0_BASE, TIMER_A, ui32SysClock - 1);

    IntEnable(INT_TIMER0A);
    TimerIntEnable(TIMER0_BASE, TIMER_TIMA_TIMEOUT);
    IntMasterEnable();
    TimerEnable(TIMER0_BASE, TIMER_A);
}

// Configuración del Timer1 para capturar el tiempo del pulso
static void config_timer1(void) {
    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER1);
    TimerConfigure(TIMER1_BASE, TIMER_CFG_A_PERIODIC | TIMER_CFG_B_ONE_SHOT);
    TimerLoadSet(TIMER1_BASE, TIMER_A, ui32SysClock - 1);

    IntEnable(INT_TIMER1A);
    TimerIntEnable(TIMER1_BASE, TIMER_TIMA_TIMEOUT);
    IntMasterEnable();
    TimerEnable(TIMER1_BASE, TIMER_A);
}

// Configuración de UART0
static void configureUART0(void) {
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOA);  
    SysCtlPeripheralEnable(SYSCTL_PERIPH_UART0);  
    
    GPIOPinConfigure(GPIO_PA0_U0RX);
    GPIOPinConfigure(GPIO_PA1_U0TX);
    GPIOPinTypeUART(GPIO_PORTA_BASE, GPIO_PIN_0 | GPIO_PIN_1);

    UARTConfigSetExpClk(UART0_BASE, ui32SysClock, BAUDIOS,
                        (UART_CONFIG_WLEN_8 |
                         UART_CONFIG_STOP_ONE |
                         UART_CONFIG_PAR_NONE));

    IntEnable(INT_UART0);                          
    UARTIntEnable(UART0_BASE, UART_INT_RX | UART_INT_RT);
    IntMasterEnable();                             
    UARTStdioConfig(0, BAUDIOS, ui32SysClock);
}
