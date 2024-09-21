#include <stdint.h>           // Incluir definiciones de tipos enteros estándar
#include <stdbool.h>          // Incluir definiciones de tipo booleano
#include "inc/hw_memmap.h"    // Incluir definiciones de mapeo de memoria de hardware
#include "driverlib/sysctl.h" // Incluir funciones de control del sistema
#include "driverlib/gpio.h"   // Incluir funciones para manejar GPIO
#include "driverlib/pin_map.h" // Incluir mapeo de pines
#include "driverlib/uart.h"   // Incluir funciones para manejar UART
#include "driverlib/adc.h"    // Incluir funciones para manejar ADC
#include "utils/uartstdio.c"   // Incluir utilidades para la comunicación UART (asegúrate de que este archivo esté disponible)

uint32_t ui32SysClock;        // Variable para almacenar la frecuencia del reloj del sistema

// Configurar el reloj del sistema
void configureSysClock(void) {
    // Establecer la frecuencia del reloj del sistema a 120 MHz usando el PLL
    ui32SysClock = SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ | // Oscilador externo de 25 MHz
                                       SYSCTL_OSC_MAIN |   // Usar el oscilador principal
                                       SYSCTL_USE_PLL |    // Usar el PLL
                                       SYSCTL_CFG_VCO_240), // Configurar VCO a 240 MHz
                                       120000000);         // Frecuencia de salida deseada
}

// Configurar UART0
void configureUART0(void) {
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOA); // Habilitar el reloj para el puerto GPIO A
    SysCtlPeripheralEnable(SYSCTL_PERIPH_UART0);  // Habilitar el reloj para UART0
    
    // Configurar los pines PA0 (RX) y PA1 (TX) para UART0
    GPIOPinConfigure(GPIO_PA0_U0RX); // Configurar PA0 como entrada RX
    GPIOPinConfigure(GPIO_PA1_U0TX); // Configurar PA1 como salida TX
    GPIOPinTypeUART(GPIO_PORTA_BASE, GPIO_PIN_0 | GPIO_PIN_1); // Configurar los pines como UART

    // Configurar UART0 a 115200 baudios, 8 bits de datos, sin paridad, 1 bit de parada
    UARTConfigSetExpClk(UART0_BASE, ui32SysClock, 115200,
                        (UART_CONFIG_WLEN_8 |  // Longitud de palabra de 8 bits
                         UART_CONFIG_STOP_ONE | // 1 bit de parada
                         UART_CONFIG_PAR_NONE)); // Sin paridad
    
    // Inicializar la UART estándar para printf
    UARTStdioConfig(0, 115200, ui32SysClock);
}

// Inicializar ADC
void InitADC(void) {
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOE); // Habilitar el reloj para el puerto GPIO E (donde está PE3)
    SysCtlPeripheralEnable(SYSCTL_PERIPH_ADC0); // Habilitar el reloj para el módulo ADC0

    // Configurar el pin PE3 como entrada analógica para el ADC
    GPIOPinTypeADC(GPIO_PORTE_BASE, GPIO_PIN_3); // Configurar el pin como entrada de ADC

    // Esperar a que el módulo ADC esté listo
    while (!SysCtlPeripheralReady(SYSCTL_PERIPH_ADC0)) {}

    // Configurar el secuenciador 3 para el ADC
    ADCSequenceConfigure(ADC0_BASE, 3, ADC_TRIGGER_PROCESSOR, 0); // Configurar secuenciador 3
    ADCSequenceStepConfigure(ADC0_BASE, 3, 0, ADC_CTL_CH0 | ADC_CTL_IE | ADC_CTL_END); // Configurar paso 0
    ADCSequenceEnable(ADC0_BASE, 3); // Habilitar el secuenciador 3
    ADCIntClear(ADC0_BASE, 3); // Limpiar interrupciones del secuenciador 3
}

// Inicializar los LEDs
void InitLEDs(void) {
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPION); // Habilitar el reloj para el puerto GPIO F

    // Configurar los pines PF1 y PF2 como salidas para los LEDs
    GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, GPIO_PIN_1 | GPIO_PIN_0);
}

// Leer valor del ADC
uint32_t ReadADC(void) {
    uint32_t adcValue; // Variable para almacenar el valor leído del ADC

    // Disparar el ADC
    ADCProcessorTrigger(ADC0_BASE, 3);

    // Esperar a que la conversión esté completa
    while (!ADCIntStatus(ADC0_BASE, 3, false)) {}

    // Leer el valor del ADC
    ADCSequenceDataGet(ADC0_BASE, 3, &adcValue);

    // Limpiar la bandera de interrupción
    ADCIntClear(ADC0_BASE, 3);

    return adcValue; // Retornar el valor leído del ADC
}

int main(void) {
    configureSysClock();  // Configura el sistema a 120 MHz
    configureUART0();     // Configura UART0
    InitADC();            // Inicializa el ADC
    InitLEDs();           // Inicializa los LEDs
    
    // Enviar un mensaje inicial a través de UART
    UARTprintf("ADC READINGS\r\n");

    // Bucle principal
    while(1) {
        // Leer el valor del ADC y enviarlo
        uint32_t adcValue = ReadADC(); // Llamar a la función para leer el ADC
        UARTprintf("ADC Value: %d\r\n", adcValue); // Enviar el valor del ADC

        // Encender o apagar los LEDs según el valor del ADC
        if (adcValue > 2048) {
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1 | GPIO_PIN_0, GPIO_PIN_1 | GPIO_PIN_0); // Encender ambos LEDs
        } else {
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1 | GPIO_PIN_0, 0x00); // Apagar ambos LEDs
        }

        // Delay para ralentizar la lectura (aproximadamente 1 segundo)
        SysCtlDelay(ui32SysClock / 12); // Ajustar el valor de delay según sea necesario
    }
}
