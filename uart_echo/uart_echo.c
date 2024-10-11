//*****************************************************************************
//
// uart_echo.c - Example for reading data from and writing data to the UART in
//               an interrupt driven fashion.
//
// Copyright (c) 2013-2017 Texas Instruments Incorporated.  All rights reserved.
// Software License Agreement
// 
// Texas Instruments (TI) is supplying this software for use solely and
// exclusively on TI's microcontroller products. The software is owned by
// TI and/or its suppliers, and is protected under applicable copyright
// laws. You may not combine this software with "viral" open-source
// software in order to form a larger program.
// 
// THIS SOFTWARE IS PROVIDED "AS IS" AND WITH ALL FAULTS.
// NO WARRANTIES, WHETHER EXPRESS, IMPLIED OR STATUTORY, INCLUDING, BUT
// NOT LIMITED TO, IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
// A PARTICULAR PURPOSE APPLY TO THIS SOFTWARE. TI SHALL NOT, UNDER ANY
// CIRCUMSTANCES, BE LIABLE FOR SPECIAL, INCIDENTAL, OR CONSEQUENTIAL
// DAMAGES, FOR ANY REASON WHATSOEVER.
// 
// This is part of revision 2.1.4.178 of the EK-TM4C1294XL Firmware Package.
//
//*****************************************************************************

#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include "inc/hw_ints.h"
#include "inc/hw_memmap.h"
#include "driverlib/debug.h"
#include "driverlib/gpio.h"
#include "driverlib/interrupt.h"
#include "driverlib/pin_map.h"
#include "driverlib/rom.h"
#include "driverlib/rom_map.h"
#include "driverlib/sysctl.h"
#include "driverlib/uart.h"
#include "utils/uartstdio.h"   

//*****************************************************************************

#define MAX_BUFFER_SIZE 100  // Tamaño máximo del buffer para almacenar la frase
char uartBuffer[MAX_BUFFER_SIZE]; // Buffer para almacenar la frase recibida
volatile uint8_t bufferIndex = 0; // Índice del buffer
uint32_t g_ui32SysClock; // Frecuencia del sistema

//*****************************************************************************
//
// The error routine that is called if the driver library encounters an error.
//
//*****************************************************************************
#ifdef DEBUG
void
__error__(char *pcFilename, uint32_t ui32Line)
{
}
#endif

//*****************************************************************************
//
// Function Prototypes
//
//*****************************************************************************
void ConfigureUART(void);
void ConfigureGPIO(void);
void UARTIntHandler(void);
void ProcessReceivedChar(char receivedChar);
void BlinkLED(void);

//*****************************************************************************

//*****************************************************************************
//
// The UART interrupt handler.
//
//*****************************************************************************
void UARTIntHandler(void)
{
    uint32_t ui32Status;

    // Obtener y limpiar el estado de la interrupción
    ui32Status = UARTIntStatus(UART7_BASE, true);
    UARTIntClear(UART7_BASE, ui32Status);

    // Procesar los datos mientras haya en el FIFO
    while (UARTCharsAvail(UART7_BASE)) {
        char receivedChar = UARTCharGetNonBlocking(UART7_BASE); // Leer el carácter recibido
        ProcessReceivedChar(receivedChar); // Procesar el carácter recibido
    }
}

//*****************************************************************************
//
// Process received character
//
//*****************************************************************************
void ProcessReceivedChar(char receivedChar)
{
    if (receivedChar == '\r' || receivedChar == '\n') {
        uartBuffer[bufferIndex] = '\0'; // Terminar la cadena con el carácter nulo
        UARTprintf("Datos recibidos: %s\r\n", uartBuffer);  // Imprimir la frase recibida
        bufferIndex = 0; // Reiniciar el buffer para la siguiente frase
    } else {
        if (bufferIndex < MAX_BUFFER_SIZE - 1) {
            uartBuffer[bufferIndex++] = receivedChar; // Agregar el carácter al buffer
        } else {
            UARTprintf("Buffer lleno, frase demasiado larga.\r\n");
            bufferIndex = 0; // Reiniciar el buffer
        }
    }
    
    BlinkLED(); // Parpadear el LED para indicar la recepción de un carácter
}

//*****************************************************************************
//
// Blink the LED to indicate data transfer
//
//*****************************************************************************
void BlinkLED(void)
{
    GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, GPIO_PIN_0);
    SysCtlDelay(g_ui32SysClock / (1000 * 3)); // Delay for 1 millisecond
    GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, 0);
}

//*****************************************************************************
//
// Configure the UART for 115,200, 8-N-1 operation.
//
//*****************************************************************************
void ConfigureUART(void)
{
    // Configurar la UART para 115,200, 8-N-1
    ROM_UARTConfigSetExpClk(UART7_BASE, g_ui32SysClock, 115200,
                            (UART_CONFIG_WLEN_8 | UART_CONFIG_STOP_ONE |
                             UART_CONFIG_PAR_NONE));
    // Inicializar la UART estándar para printf
    UARTStdioConfig(0, 115200, g_ui32SysClock);
}

//*****************************************************************************
//
// Configure the GPIO for the LED and UART pins.
//
//*****************************************************************************
void ConfigureGPIO(void)
{
    // Habilitar el puerto GPIO para el LED
    ROM_SysCtlPeripheralEnable(SYSCTL_PERIPH_GPION);
    ROM_GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, GPIO_PIN_0);

    // Habilitar los periféricos utilizados por la UART
    ROM_SysCtlPeripheralEnable(SYSCTL_PERIPH_UART7);
    ROM_SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOC);

    // Configurar A0 y A1 como pines de UART
    GPIOPinConfigure(GPIO_PC4_U7RX);
    GPIOPinConfigure(GPIO_PC5_U7TX);
    ROM_GPIOPinTypeUART(GPIO_PORTC_BASE, GPIO_PIN_4 | GPIO_PIN_5);
}

//*****************************************************************************
//
// Main function to initialize the system and run the UART echo program.
//
//*****************************************************************************
int main(void)
{
    // Establecer la frecuencia del sistema a 120MHz
    g_ui32SysClock = MAP_SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ |
                                             SYSCTL_OSC_MAIN |
                                             SYSCTL_USE_PLL |
                                             SYSCTL_CFG_VCO_480), 120000000);

    // Configurar GPIO y UART
    ConfigureGPIO();
    ConfigureUART();

    // Habilitar interrupciones de UART
    ROM_IntMasterEnable();
    ROM_IntEnable(INT_UART7);
    ROM_UARTIntEnable(UART7_BASE, UART_INT_RX | UART_INT_RT);

    // Enviar un mensaje inicial
    UARTprintf("Ingrese texto: \r\n");

    // Bucle principal
    while (1)
    {
         UARTprintf("Hola... \r\n");
         SysCtlDelay(g_ui32SysClock*0.1);
    }
}
