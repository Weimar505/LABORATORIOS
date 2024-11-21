#include <stdbool.h>
#include <stdint.h>
#include "inc/hw_memmap.h"
#include "driverlib/gpio.h"
#include "driverlib/pin_map.h"
#include "driverlib/pwm.h"
#include "driverlib/sysctl.h"

// Variable para el reloj del sistema
uint32_t g_ui32SysClock;

// Función para configurar el reloj del sistema
void configureSystemClock(void) {
    g_ui32SysClock = SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ | SYSCTL_OSC_MAIN |
                                         SYSCTL_USE_PLL | SYSCTL_CFG_VCO_480), 120000000);
}

// Función para configurar el PWM
void configurePWM(void) {
    // Habilitar los módulos PWM y GPIO
    SysCtlPeripheralEnable(SYSCTL_PERIPH_PWM0);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);

    // Esperar a que los periféricos estén listos
    while (!SysCtlPeripheralReady(SYSCTL_PERIPH_PWM0)) {}
    while (!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOF)) {}

    // Configurar PF1 como PWM1 (M0PWM1), PF2 como PWM2 (M0PWM2) y PF3 como PWM3 (M0PWM3)
    GPIOPinConfigure(GPIO_PF1_M0PWM1);
    GPIOPinConfigure(GPIO_PF2_M0PWM2);
    GPIOPinConfigure(GPIO_PF3_M0PWM3);
    GPIOPinTypePWM(GPIO_PORTF_BASE, GPIO_PIN_1 | GPIO_PIN_2 | GPIO_PIN_3);

    // Configurar el reloj de PWM a SysClock/16
    PWMClockSet(PWM0_BASE, PWM_SYSCLK_DIV_16);

    // Configurar el generador PWM para PF1 en PWM_GEN_0, PF2 en PWM_GEN_0 y PF3 en PWM_GEN_1
    PWMGenConfigure(PWM0_BASE, PWM_GEN_0, PWM_GEN_MODE_DOWN | PWM_GEN_MODE_NO_SYNC);
    PWMGenConfigure(PWM0_BASE, PWM_GEN_1, PWM_GEN_MODE_DOWN | PWM_GEN_MODE_NO_SYNC);

    // Establecer el período para ambos generadores
    uint32_t duty = 255; // Frecuencia de 100 Hz
    PWMGenPeriodSet(PWM0_BASE, PWM_GEN_0, duty); // PF1 y PF2
    PWMGenPeriodSet(PWM0_BASE, PWM_GEN_1, duty); // PF3

    // Habilitar las salidas PWM en PF1 (M0PWM1), PF2 (M0PWM2) y PF3 (M0PWM3)
    PWMOutputState(PWM0_BASE, PWM_OUT_1_BIT | PWM_OUT_2_BIT | PWM_OUT_3_BIT, true);

    // Habilitar los generadores PWM
    PWMGenEnable(PWM0_BASE, PWM_GEN_0);
    PWMGenEnable(PWM0_BASE, PWM_GEN_1);

    // Establecer el ciclo de trabajo inicial
    PWMPulseWidthSet(PWM0_BASE, PWM_OUT_1, 2);   // PF1
    PWMPulseWidthSet(PWM0_BASE, PWM_OUT_2, 2);   // PF2
    PWMPulseWidthSet(PWM0_BASE, PWM_OUT_3, 2);  // PF3
}

int main(void) {
    // Llamar a las funciones para inicializar el sistema
    configureSystemClock();
    configurePWM();

    // Mantener el programa en un bucle infinito
    while (1) {
        // Ajustar el ciclo de trabajo en el bucle
        PWMPulseWidthSet(PWM0_BASE, PWM_OUT_1, 25); // PF1 a 255
        PWMPulseWidthSet(PWM0_BASE, PWM_OUT_2, 25); // PF2 a 128 (50%)
        PWMPulseWidthSet(PWM0_BASE, PWM_OUT_3, 25);  // PF3 a 25
    }
}
