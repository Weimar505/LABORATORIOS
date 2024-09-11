#include <stdint.h>
#include <stdbool.h>
#include "inc/hw_memmap.h"
#include "driverlib/sysctl.h"
#include "driverlib/gpio.h"
#include "driverlib/pin_map.h"
#include "driverlib/uart.h"

uint32_t ui32SysClock;
int count = 0;

// Configurar el reloj del sistema
void configureSysClock(void)
{
    ui32SysClock = SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ |
                                       SYSCTL_OSC_MAIN |
                                       SYSCTL_USE_PLL |
                                       SYSCTL_CFG_VCO_240), 120000000);
}

// Configurar UART0 sin usar UARTStdio
void configureUART0(void)
{
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOA);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_UART0);
    
    // Configurar los pines PA0 (RX) y PA1 (TX) para UART0
    GPIOPinConfigure(GPIO_PA0_U0RX);
    GPIOPinConfigure(GPIO_PA1_U0TX);
    GPIOPinTypeUART(GPIO_PORTA_BASE, GPIO_PIN_0 | GPIO_PIN_1);

    // Configurar UART0 a 115200 baudios, 8 bits de datos, sin paridad, 1 bit de parada
    UARTConfigSetExpClk(UART0_BASE, ui32SysClock, 115200,
                        (UART_CONFIG_WLEN_8 | UART_CONFIG_STOP_ONE | UART_CONFIG_PAR_NONE));
}

// Función para enviar una cadena de caracteres a través de UART
void UARTSend(const char *pucBuffer)
{
    while (*pucBuffer)
    {
        UARTCharPut(UART0_BASE, *pucBuffer++);
    }
}

// Función para convertir un entero en cadena y enviarlo
void UARTSendInt(int num)
{
    char buffer[10];
    int i = 0;
    
    // Convierte el número a cadena
    if (num == 0) {
        buffer[i++] = '0';
    } else {
        while (num > 0) {
            buffer[i++] = (num % 10) + '0';
            num /= 10;
        }
    }
    
    // Enviar los caracteres en orden inverso
    while (i > 0) {
        UARTCharPut(UART0_BASE, buffer[--i]);
    }
    
    // Enviar salto de línea y retorno de carro
    UARTSend("\r\n");
}

int main(void)
{
    configureSysClock();  // Configura el sistema a 120 MHz
    configureUART0();     // Configura UART0
    
    // Enviar un mensaje inicial
    UARTSend("UART TRANSMISSION ONLY\r\n");

    // Bucle principal
    while(1)
    {
        UARTSend("Count: ");
        UARTSendInt(count);  // Envía el conteo a través de UART
        count++;
        
        // Delay para ralentizar el conteo (simple)
        SysCtlDelay(ui32SysClock / 3);  // Ajusta el valor de delay según sea necesario
    }
}
