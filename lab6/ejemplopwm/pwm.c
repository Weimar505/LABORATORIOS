#include <stdint.h>
#include <stdbool.h>
#include "inc/hw_memmap.h"
#include "driverlib/sysctl.h"
#include "driverlib/gpio.h"
#include "driverlib/pwm.h"
#include "driverlib/pin_map.h"
#include "driverlib/uart.h"
#include "utils/uartstdio.c"
#define duty 400 // ciclo de trabajo maximo del pwm 
uint32_t ui32SysClock; // Variable para almacenar la frecuencia del reloj del sistema
uint32_t width;        // Variable para almacenar el ancho del pulso de PWM
static void configureSysClock(void); // Configurar el sistema a 120 MHz
static void configureUART0(void);    // Configurar UART0
static void InitPWM(void);           // Inicializar PWM
static void config_gpio(void);      //Configuracion GPIOs
int main(void) {
    configureSysClock(); // Configurar el sistema a 120 MHz
    configureUART0();    // Configurar UART0
    InitPWM();           // Inicializar PWM
    config_gpio();      // inicializar GPIO
    width = 50;         //porcentaje de pwm segun la variable duty
    UARTprintf("PWM Control Example\r\n");

    while (1) {
        PWMPulseWidthSet(PWM0_BASE, PWM_OUT_1, width);
        GPIOPinWrite(GPIO_PORTN_BASE,GPIO_PIN_2, GPIO_PIN_2);

    }
}

// Configurar UART0
static void configureUART0(void) {
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOA); // Habilitar el reloj para GPIO A
    SysCtlPeripheralEnable(SYSCTL_PERIPH_UART0);  // Habilitar el reloj para UART0

    // Configurar los pines para UART0
    GPIOPinConfigure(GPIO_PA0_U0RX); // Configurar PA0 como RX
    GPIOPinConfigure(GPIO_PA1_U0TX); // Configurar PA1 como TX
    GPIOPinTypeUART(GPIO_PORTA_BASE, GPIO_PIN_0 | GPIO_PIN_1); // Configurar como UART

    // Configurar UART0 a 115200 baudios, 8 bits de datos, sin paridad, 1 bit de parada
    UARTConfigSetExpClk(UART0_BASE, ui32SysClock, 115200,
                        (UART_CONFIG_WLEN_8 |
                         UART_CONFIG_STOP_ONE |
                         UART_CONFIG_PAR_NONE));
    
    // Inicializar la UART estándar para printf
    UARTStdioConfig(0, 115200, ui32SysClock);
}

// Inicializar PWM
 static void InitPWM(void) {
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF); // Habilitar el reloj para GPIO F
    SysCtlPeripheralEnable(SYSCTL_PERIPH_PWM0);   // Habilitar el reloj para el módulo PWM0

    // Configurar PF1 como salida de PWM
    GPIOPinConfigure(GPIO_PF1_M0PWM1); 
    GPIOPinTypePWM(GPIO_PORTF_BASE, GPIO_PIN_1); // Configurar PF1 como PWM

    // Configurar el generador PWM0
    PWMGenConfigure(PWM0_BASE, PWM_GEN_0, PWM_GEN_MODE_DOWN | PWM_GEN_MODE_NO_SYNC);
    PWMGenPeriodSet(PWM0_BASE, PWM_GEN_0, duty); // Establecer el período del PWM (frecuencia de 250 Hz)

    PWMPulseWidthSet(PWM0_BASE, PWM_OUT_1, 0); // Establecer el ciclo de trabajo inicial
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_PWM0))
    {

    }
    PWMGenEnable(PWM0_BASE, PWM_GEN_0); // Habilitar el generador PWM
    PWMOutputState(PWM0_BASE, PWM_OUT_1_BIT, true); // Habilitar la salida PWM
}
static void config_gpio(void){
    //todo los perifericos que tienen gpio
    //habilitacion de perifericos
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOA);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOB); 
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOC);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOD);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOE);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOG);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOH);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOJ);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOK);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOL);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOM);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPION);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOP);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOQ);
    //
    GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, GPIO_PIN_2);
}
// Configurar el reloj del sistema
static void configureSysClock(void) {
    // Configurar el sistema para usar el PLL y establecer la frecuencia a 120 MHz
    ui32SysClock = SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ |
                                       SYSCTL_OSC_MAIN |
                                       SYSCTL_USE_PLL |
                                       SYSCTL_CFG_VCO_240),
                                       120000000);
}