#include <stdint.h>
#include <stdbool.h>
#include "inc/hw_memmap.h"
#include "driverlib/debug.h"
#include "driverlib/gpio.h"
#include "driverlib/sysctl.h"

#ifdef DEBUG
void
_error_(char *pcFilename, uint32_t ui32Line)
{
    while(1);
}
#endif
volatile uint32_t ui32Loop;
volatile uint32_t counter=0;

//***************************
int main(void)
{
    SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ | SYSCTL_OSC_MAIN | SYSCTL_USE_PLL | SYSCTL_CFG_VCO_480), 120000000);
    
    // Habilitar los puertos GPIO utilizados
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPION);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOJ);
    
    // Comprobar si el periférico está listo
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPION) | !SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOF) | !SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOJ)) 
    {
    }

    // Configurar botones como entradas con resistencia pull-up
    GPIOPinTypeGPIOInput(GPIO_PORTJ_BASE, GPIO_PIN_0);  // Botón 1
    GPIOPadConfigSet(GPIO_PORTJ_BASE, GPIO_PIN_0, GPIO_STRENGTH_2MA, GPIO_PIN_TYPE_STD_WPU);
    
    GPIOPinTypeGPIOInput(GPIO_PORTJ_BASE, GPIO_PIN_1);  // Botón 2
    GPIOPadConfigSet(GPIO_PORTJ_BASE, GPIO_PIN_1, GPIO_STRENGTH_2MA, GPIO_PIN_TYPE_STD_WPU);

    // Configurar dos botones externos adicionales en PORTF
    GPIOPinTypeGPIOInput(GPIO_PORTF_BASE, GPIO_PIN_0);  // Botón 3 externo
    GPIOPadConfigSet(GPIO_PORTF_BASE, GPIO_PIN_0, GPIO_STRENGTH_2MA, GPIO_PIN_TYPE_STD_WPU);
    
    GPIOPinTypeGPIOInput(GPIO_PORTF_BASE, GPIO_PIN_4);  // Botón 4 externo
    GPIOPadConfigSet(GPIO_PORTF_BASE, GPIO_PIN_4, GPIO_STRENGTH_2MA, GPIO_PIN_TYPE_STD_WPU);

    // Bucle principal
    while(1)
    {
        // Botón 1
        if (GPIOPinRead(GPIO_PORTJ_BASE, GPIO_PIN_1) == 0) {
            counter++;
            while (GPIOPinRead(GPIO_PORTJ_BASE, GPIO_PIN_1) == 0) {
                // Espera activa para evitar rebotes
            }
            SysCtlDelay(1000000);  // Delay para evitar rebotes del botón
            if (counter >= 15) {
                counter = 15;
            }
        }

        // Botón 2
        else if (GPIOPinRead(GPIO_PORTJ_BASE, GPIO_PIN_0) == 0) {
            counter--;
            while (GPIOPinRead(GPIO_PORTJ_BASE, GPIO_PIN_0) == 0) {
                // Espera activa para evitar rebotes
            }
            SysCtlDelay(1000000);  // Delay para evitar rebotes del botón
            if (counter == -1) {
                counter = 0;
            }
        }

        // Botón 3 (externo) en GPIO_PORTF_PIN_0
        else if (GPIOPinRead(GPIO_PORTF_BASE, GPIO_PIN_0) == 0) {
            counter += 2;  // Incrementar en 2 con este botón
            while (GPIOPinRead(GPIO_PORTF_BASE, GPIO_PIN_0) == 0) {
                // Espera activa
            }
            SysCtlDelay(1000000);  // Delay para evitar rebotes del botón
            if (counter > 15) {
                counter = 15;
            }
        }

        // Botón 4 (externo) en GPIO_PORTF_PIN_4
        else if (GPIOPinRead(GPIO_PORTF_BASE, GPIO_PIN_4) == 0) {
            counter -= 2;  // Decrementar en 2 con este botón
            while (GPIOPinRead(GPIO_PORTF_BASE, GPIO_PIN_4) == 0) {
                // Espera activa
            }
            SysCtlDelay(1000000);  // Delay para evitar rebotes del botón
            if (counter < 0) {
                counter = 0;
            }
        }

        // Continuar con la lógica de control del LED basado en el valor de counter
        if (counter == 1) {
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, GPIO_PIN_1);
            GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, 0x0);
            GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, 0x0);
            GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, 0x0);
        }
        // El resto del código permanece igual
        // ...
    }
}
