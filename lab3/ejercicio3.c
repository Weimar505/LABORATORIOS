#include <stdint.h>
#include <stdbool.h>
#include "inc/hw_memmap.h"
#include "driverlib/debug.h"
#include "driverlib/gpio.h"
#include "driverlib/sysctl.h"

#ifdef DEBUG
void
__error__(char *pcFilename, uint32_t ui32Line)
{
    while(1);
}
#endif
volatile uint32_t ui32Loop;
volatile uint32_t counter=0;
//*****************************************************************************
int main(void)
{
    SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ | SYSCTL_OSC_MAIN | SYSCTL_USE_PLL | SYSCTL_CFG_VCO_480),120000000);
    //
    // Enable the GPIO port that is used for the on-board LED.
    //
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPION);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOJ);
    //
    // Check if the peripheral access is enabled.
    //
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPION)|!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOF)|!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOJ))
    { 
    }
    //
    // Enable the GPIO pin for the LED (PN0).  Set the direction as output, and
    // enable the GPIO pin for digital function.
    //
    GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, GPIO_PIN_0);
    GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, GPIO_PIN_1);
    GPIOPinTypeGPIOOutput(GPIO_PORTF_BASE, GPIO_PIN_4);
    GPIOPinTypeGPIOOutput(GPIO_PORTF_BASE, GPIO_PIN_0);
    //
    GPIOPinTypeGPIOInput(GPIO_PORTJ_BASE, GPIO_PIN_0);
    GPIOPadConfigSet(GPIO_PORTJ_BASE, GPIO_PIN_0, GPIO_STRENGTH_2MA, GPIO_PIN_TYPE_STD_WPU);
    //
    GPIOPinTypeGPIOInput(GPIO_PORTJ_BASE, GPIO_PIN_1);
    GPIOPadConfigSet(GPIO_PORTJ_BASE, GPIO_PIN_1, GPIO_STRENGTH_2MA, GPIO_PIN_TYPE_STD_WPU);
    //
    // Loop forever.
    //
    while(1)
    {
    	if (GPIOPinRead(GPIO_PORTJ_BASE, GPIO_PIN_1)==0){
    		counter++;
    		while (GPIOPinRead(GPIO_PORTJ_BASE, GPIO_PIN_1) == 0) {
                // Espera activa
            	}
            	// Esperar un pequeño tiempo para evitar rebotes del botón
            	SysCtlDelay(1000000);
            	 if (counter >= 15){
            		counter =15;
            	}
    	}
    	else if (GPIOPinRead(GPIO_PORTJ_BASE, GPIO_PIN_0)==0){
    		counter--;
    		while (GPIOPinRead(GPIO_PORTJ_BASE, GPIO_PIN_0) == 0) {
                // Espera activa
            	}
            	// Esperar un pequeño tiempo para evitar rebotes del botón
            	SysCtlDelay(1000000);
            	if (counter == -1){
            		counter =0;
            	}
    	}
    	if (counter == 1){
    		GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, GPIO_PIN_1);
    		GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, 0x0);
    		GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, 0x0);
    		GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, 0x0);
    	}
    	else if (counter == 2){
    		GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, 0x0);
    		GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, GPIO_PIN_0);
    		GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, 0x0);
    		GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, 0x0);
    	}
    	else if (counter == 3){
    		GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, GPIO_PIN_1);
    		GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, GPIO_PIN_0);
    		GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, 0x0);
    		GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, 0x0);
    	}
    	else if (counter == 4){
    		GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, 0x0);
    		GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, 0x0);
    		GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, GPIO_PIN_4);
    		GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, 0x0);
    	}
    	
    	else if (counter == 5){
    		GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, 0x0);
    		GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, GPIO_PIN_1);
    		GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, GPIO_PIN_4);
    		GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, 0x0);
    	}
    	else if (counter == 6){
    		GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, GPIO_PIN_0);
    		GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, 0x0);
    		GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, GPIO_PIN_4);
    		GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, 0x0);
    	}
    	else if (counter == 7){
    		GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, GPIO_PIN_0);
    		GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, GPIO_PIN_1);
    		GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, GPIO_PIN_4);
    		GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, 0x0);
    	}
    	else if (counter == 8){
    		GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, 0x0);
    		GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, 0x0);
    		GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, 0x0);
    		GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, GPIO_PIN_0);
    	}
    	else if (counter == 9){
    		GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, 0x0);
    		GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, GPIO_PIN_1);
    		GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, 0x0);
    		GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, GPIO_PIN_0);
    	}
    	else if (counter == 10){
    		GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, GPIO_PIN_0);
    		GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, 0x0);
    		GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, 0x0);
    		GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, GPIO_PIN_0);
    	}
    	else if (counter == 11){
    		GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, GPIO_PIN_0);
    		GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, GPIO_PIN_1);
    		GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, 0x0);
    		GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, GPIO_PIN_0);
    	}
    	else if (counter == 12){
    		GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, 0x0);
    		GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, 0x0);
    		GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, GPIO_PIN_4);
    		GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, GPIO_PIN_0);
    	}
    	else if (counter == 13){
    		GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, 0x0);
    		GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, GPIO_PIN_1);
    		GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, GPIO_PIN_4);
    		GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, GPIO_PIN_0);
    	}
    	else if (counter == 14){
    		GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, GPIO_PIN_0);
    		GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, 0x0);
    		GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, GPIO_PIN_4);
    		GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, GPIO_PIN_0);
    	}
    	else if (counter == 15){
    		GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, GPIO_PIN_0);
    		GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, GPIO_PIN_1);
    		GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, GPIO_PIN_4);
    		GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, GPIO_PIN_0);
    	}
    	else if (counter == 0){
    		GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_0, 0x0);
    		GPIOPinWrite(GPIO_PORTN_BASE, GPIO_PIN_1, 0x0);
    		GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, 0x0);
    		GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_0, 0x0);
    	}
    }
}

