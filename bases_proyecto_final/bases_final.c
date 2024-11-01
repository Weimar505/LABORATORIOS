#include <stdint.h>
#include <stdbool.h>
#include <string.h>  // Para usar strcmp()
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
#include "driverlib/pwm.h"       // Control del módulo PWM (configuración, generación de señales PWM)    
#define MAX_BUFFER_SIZE 100       // Tamaño máximo del buffer para almacenar la frase
#define BAUDIOS 9600              // Velocidad de comunicación UART
//---------------------SENSORES----------------------------------------------//
//Pines para los sensores ultrasonicos
#define TRIG_PIN GPIO_PIN_0      
#define ECHO_PIN GPIO_PIN_1       
#define TRIG_PIN2 GPIO_PIN_2      
#define ECHO_PIN2 GPIO_PIN_3    
#define TRIG_PIN2 GPIO_PIN_2     
#define ECHO_PIN2 GPIO_PIN_3       
#define TRIG_PIN3 GPIO_PIN_4     
#define ECHO_PIN3 GPIO_PIN_5 
#define TRIG_PIN4 GPIO_PIN_2    
#define ECHO_PIN4 GPIO_PIN_3 
//Puertos para los sensores
#define TRIG_PORT GPIO_PORTL_BASE
#define ECHO_PORT GPIO_PORTL_BASE
#define TRIG_PORT2 GPIO_PORTH_BASE
#define ECHO_PORT2 GPIO_PORTH_BASE
//variables para medir las distancias de los sensores
const int limite = 15;
const int limite2 = 25;
uint32_t distance,distance2,distance3,distance4;
uint32_t startTime, endTime, duration;
uint32_t startTime2, endTime2, duration2;
uint32_t startTime3, endTime3, duration3;
uint32_t startTime4, endTime4, duration4;
float time_us;
float time_us2;
float time_us3;
float time_us4;
//-------------------SYSTEM OF CLOCK-------------
//variable para el clock
uint32_t ui32SysClock;  
//----------------------UART---------------------------------------------------//
//variables para el envio de datos por UART         
char uartBuffer[MAX_BUFFER_SIZE]; 
volatile uint8_t bufferIndex = 0; 
//-----------------------PWM---------------------------------------------------//
#define BASE_PWM PWM0_BASE
#define PERF_PWM1 GPIO_PF1_M0PWM1
#define PERF_PWM2 GPIO_PF2_M0PWM2
#define PERF_PWM3 GPIO_PF3_M0PWM3
#define PIN_PWM1 GPIO_PIN_1 
#define PIN_PWM2 GPIO_PIN_2
#define PIN_PWM3 GPIO_PIN_3
#define PWM_PORT GPIO_PORTF_BASE
#define SALIDA_PWM1 PWM_OUT_1
#define SALIDA_PWM2 PWM_OUT_2
#define SALIDA_PWM3 PWM_OUT_3
uint32_t duty;
//-----------------------------MOTORES-----------------------------------------//
#define MOTOR1_DER_PIN GPIO_PIN_0
#define MOTOR1_IZQ_PIN GPIO_PIN_1
#define MOTOR2_DER_PIN GPIO_PIN_2
#define MOTOR2_IZQ_PIN GPIO_PIN_3
#define MOTORRES_PORT GPIO_PORTK_BASE
//-----------------------FUNCIONES DEL SISTEMA---------------------------------//
// Declaraciones de funciones
static void configureSysClock(void);  
static void configureUART0(void);     
static void config_timer(void);
static void config_timer1(void);
static void config_timer2(void);
static void config_ultrasonico(void);
static void config_pwm(void);    
static void config_motores(void);
//---------------------FUNCIONES A UTILIZAR------------------------------------//
void medir_distancia1(void);
void medir_distancia2(void);
void medir_distancia3(void);
void medir_distancia4(void);
//---------------------FUNCIONES DE LOS MOVIMINETOS----------------------------//
void giro_der(void);
void giro_izq(void);
void adelante(void);
void atras(void);
void apagado_motores(void);
//----------------------MAIN---------------------------------------------------//
int main(void) {
    configureSysClock();  
    configureUART0();     
    config_timer();
    config_timer1();
    config_timer2();
    config_pwm();
    config_ultrasonico();
    config_motores();
    while (1) {
        //PWMPulseWidthSet(BASE_PWM, SALIDA_PWM1, 255); // PF1 a 255
        //PWMPulseWidthSet(BASE_PWM, SALIDA_PWM2, 1); // PF2 a 128 (50%)
        //PWMPulseWidthSet(BASE_PWM, SALIDA_PWM3, 128);  // PF3 a 25
        //giro_der();
        //giro_izq();
    }
}
// Manejador de interrupciones del Timer2
void Timer2IntHandler(void) {
    TimerIntClear(TIMER2_BASE, TIMER_TIMA_TIMEOUT);
    medir_distancia1();
    medir_distancia2();
    medir_distancia3();
    medir_distancia4();
    UARTprintf("Distancia: %d cm ", (int)distance);
    UARTprintf("%d cm ", (int)distance2);
    UARTprintf("%d cm ", (int)distance3);
    UARTprintf("%d cm\r\n", (int)distance4);

        // Verificar el espacio frente al robot
    if (distance <= limite2) {
        // Caso donde hay un obstáculo en frente
        if (distance3 > distance2 && distance3 > limite) {
            // Gira a la derecha si tiene más espacio que el lado izquierdo
            giro_der();
        } else if (distance2 > distance3 && distance2 > limite) {
            // Gira a la izquierda si tiene más espacio que el lado derecho
            giro_izq();
        } else if (distance4 > limite) {
            // Si no hay espacio a los lados, pero sí atrás, retrocede
            atras();
        } else {
            // Si no hay espacio en ninguna dirección, se detiene
            apagado_motores();
        }
    }
    // Verificar si el obstáculo está muy cerca en la parte trasera
    else if (distance4 <= limite) {
        // Si está muy cerca detrás, intenta avanzar
        adelante();
    }
    // Verificar si hay un obstáculo muy cerca a la derecha
    else if (distance3 <= limite) {
        // Gira a la izquierda si el obstáculo está a la derecha
        giro_izq();
    }
    // Verificar si hay un obstáculo muy cerca a la izquierda
    else if (distance2 <= limite) {
        // Gira a la derecha si el obstáculo está a la izquierda
        giro_der();
    }
    else {
        // Si no hay obstáculos cerca, avanza
        adelante();
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
            UARTprintf("Datos recibidos: %s\r\n", uartBuffer);  
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
//Funcion para definir los moviminetos
void giro_der(void){
    GPIOPinWrite(MOTORRES_PORT, MOTOR2_DER_PIN, MOTOR2_DER_PIN);
    GPIOPinWrite(MOTORRES_PORT, MOTOR1_IZQ_PIN, MOTOR1_IZQ_PIN);
    GPIOPinWrite(MOTORRES_PORT, MOTOR2_IZQ_PIN, 0X00);
    GPIOPinWrite(MOTORRES_PORT, MOTOR1_DER_PIN, 0X00);
}
void giro_izq(void){
    GPIOPinWrite(MOTORRES_PORT, MOTOR1_DER_PIN, MOTOR1_DER_PIN);
    GPIOPinWrite(MOTORRES_PORT, MOTOR2_IZQ_PIN, MOTOR2_IZQ_PIN);
    GPIOPinWrite(MOTORRES_PORT, MOTOR1_IZQ_PIN, 0X00);
    GPIOPinWrite(MOTORRES_PORT, MOTOR2_DER_PIN, 0X00);
}
void adelante(void){
    GPIOPinWrite(MOTORRES_PORT, MOTOR1_DER_PIN, MOTOR1_DER_PIN);
    GPIOPinWrite(MOTORRES_PORT, MOTOR2_DER_PIN, MOTOR2_DER_PIN);
    GPIOPinWrite(MOTORRES_PORT, MOTOR1_IZQ_PIN, 0X00);
    GPIOPinWrite(MOTORRES_PORT, MOTOR2_IZQ_PIN, 0X00);
}
void atras(void){
    GPIOPinWrite(MOTORRES_PORT, MOTOR2_IZQ_PIN, MOTOR2_IZQ_PIN);
    GPIOPinWrite(MOTORRES_PORT, MOTOR1_IZQ_PIN, MOTOR1_IZQ_PIN);
    GPIOPinWrite(MOTORRES_PORT, MOTOR1_DER_PIN, 0X00);
    GPIOPinWrite(MOTORRES_PORT, MOTOR2_DER_PIN, 0X00);
}
void apagado_motores(void){
    GPIOPinWrite(MOTORRES_PORT, MOTOR2_IZQ_PIN, 0x00);
    GPIOPinWrite(MOTORRES_PORT, MOTOR1_IZQ_PIN, 0x00);
    GPIOPinWrite(MOTORRES_PORT, MOTOR1_DER_PIN, 0X00);
    GPIOPinWrite(MOTORRES_PORT, MOTOR2_DER_PIN, 0X00);
}
// Función para medir la distancia con el primer sensor ultrasónico
void medir_distancia1(void) {
    GPIOPinWrite(TRIG_PORT, TRIG_PIN, TRIG_PIN);
    SysCtlDelay(400);  
    GPIOPinWrite(TRIG_PORT, TRIG_PIN, 0);

    while (GPIOPinRead(ECHO_PORT, ECHO_PIN) == 0);
    startTime = TimerValueGet(TIMER1_BASE, TIMER_A);  

    while (GPIOPinRead(ECHO_PORT, ECHO_PIN) != 0);
    endTime = TimerValueGet(TIMER1_BASE, TIMER_A);  

    duration = startTime - endTime;  
    time_us = (float)duration * 0.00833f;
    distance = time_us / 58.0f;
}
// Función para medir la distancia con el segundo sensor ultrasónico
void medir_distancia2(void) {
    GPIOPinWrite(TRIG_PORT, TRIG_PIN2, TRIG_PIN2);
    SysCtlDelay(400);  
    GPIOPinWrite(TRIG_PORT, TRIG_PIN2, 0);

    while (GPIOPinRead(ECHO_PORT, ECHO_PIN2) == 0);
    startTime2 = TimerValueGet(TIMER1_BASE, TIMER_A);  

    while (GPIOPinRead(ECHO_PORT, ECHO_PIN2) != 0);
    endTime2 = TimerValueGet(TIMER1_BASE, TIMER_A);  

    duration2 = startTime2 - endTime2;  
    time_us2 = (float)duration2 * 0.00833f;
    distance2 = time_us2 / 58.0f;
}
// Función para medir la distancia con el tercer sensor ultrasónico
void medir_distancia3(void) {
    GPIOPinWrite(TRIG_PORT, TRIG_PIN3, TRIG_PIN3);
    SysCtlDelay(400);  
    GPIOPinWrite(TRIG_PORT, TRIG_PIN3, 0);

    while (GPIOPinRead(ECHO_PORT, ECHO_PIN3) == 0);
    startTime3 = TimerValueGet(TIMER0_BASE, TIMER_A);  

    while (GPIOPinRead(ECHO_PORT, ECHO_PIN3) != 0);
    endTime3 = TimerValueGet(TIMER0_BASE, TIMER_A);  

    duration3 = startTime3 - endTime3;  
    time_us3 = (float)duration3 * 0.00833f;
    distance3 = time_us3 / 58.0f;
}
// Función para medir la distancia con el tercer sensor ultrasónico
void medir_distancia4(void) {
    GPIOPinWrite(TRIG_PORT2, TRIG_PIN4, TRIG_PIN4);
    SysCtlDelay(400);  
    GPIOPinWrite(TRIG_PORT2, TRIG_PIN4, 0x00);

    while (GPIOPinRead(ECHO_PORT2, ECHO_PIN4) == 0);
    startTime4 = TimerValueGet(TIMER0_BASE, TIMER_A);  

    while (GPIOPinRead(ECHO_PORT2, ECHO_PIN4) != 0);
    endTime4 = TimerValueGet(TIMER0_BASE, TIMER_A);  

    duration4 = startTime4 - endTime4;  
    time_us4 = (float)duration4 * 0.00833f;
    distance4 = time_us4 / 58.0f;

}
// Configuración del sensor ultrasónico
static void config_ultrasonico(void){
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOL);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOH);
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOL));
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOH));

    GPIOPinTypeGPIOOutput(TRIG_PORT, TRIG_PIN);
    GPIOPinTypeGPIOInput(ECHO_PORT, ECHO_PIN);
    GPIOPinTypeGPIOOutput(TRIG_PORT, TRIG_PIN2);
    GPIOPinTypeGPIOInput(ECHO_PORT, ECHO_PIN2);
    GPIOPinTypeGPIOOutput(TRIG_PORT, TRIG_PIN3);
    GPIOPinTypeGPIOInput(ECHO_PORT, ECHO_PIN3);
    GPIOPinTypeGPIOOutput(TRIG_PORT2, TRIG_PIN4);
    GPIOPinTypeGPIOInput(ECHO_PORT2, ECHO_PIN4);
    GPIOPinWrite(TRIG_PORT, TRIG_PIN, 0x00);
    GPIOPinWrite(TRIG_PORT, TRIG_PIN2, 0x00);
    GPIOPinWrite(TRIG_PORT, TRIG_PIN3, 0x00);
    GPIOPinWrite(TRIG_PORT2, TRIG_PIN4, 0x00);
}
//Configuracion de los motores para las llantas
static void config_motores(void){
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOK);
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOK));
    GPIOPinTypeGPIOOutput(MOTORRES_PORT, MOTOR1_DER_PIN);
    GPIOPinTypeGPIOOutput(MOTORRES_PORT, MOTOR1_IZQ_PIN);
    GPIOPinTypeGPIOOutput(MOTORRES_PORT, MOTOR2_DER_PIN);
    GPIOPinTypeGPIOOutput(MOTORRES_PORT, MOTOR2_IZQ_PIN);
    GPIOPinWrite(MOTORRES_PORT, MOTOR1_DER_PIN, 0x00);
    GPIOPinWrite(MOTORRES_PORT, MOTOR1_IZQ_PIN, 0x00);
    GPIOPinWrite(MOTORRES_PORT, MOTOR2_DER_PIN, 0x00);
    GPIOPinWrite(MOTORRES_PORT, MOTOR2_IZQ_PIN, 0x00);


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
// Configuración del Timer2 para ejecutar secciones de constantes mediciones
static void config_timer2(void) {
    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER2);
    TimerConfigure(TIMER2_BASE, TIMER_CFG_A_PERIODIC | TIMER_CFG_B_ONE_SHOT);
    TimerLoadSet(TIMER2_BASE, TIMER_A, (ui32SysClock - 1)*0.1);

    IntEnable(INT_TIMER2A);
    TimerIntEnable(TIMER2_BASE, TIMER_TIMA_TIMEOUT);
    IntMasterEnable();
    TimerEnable(TIMER2_BASE, TIMER_A);
}
// Inicializar PWM
static void config_pwm(void) {
    // Habilitar los módulos PWM y GPIO
    SysCtlPeripheralEnable(SYSCTL_PERIPH_PWM0);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);

    // Esperar a que los periféricos estén listos
    while (!SysCtlPeripheralReady(SYSCTL_PERIPH_PWM0)) {}
    while (!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOF)) {}

    // Configurar PF1 como PWM1 (M0PWM1), PF2 como PWM2 (M0PWM2) y PF3 como PWM3 (M0PWM3)
    GPIOPinConfigure(PERF_PWM1);
    GPIOPinConfigure(PERF_PWM2);
    GPIOPinConfigure(PERF_PWM3);
    GPIOPinTypePWM(PWM_PORT, PIN_PWM1 | PIN_PWM2 | PIN_PWM3);

    // Configurar el reloj de PWM a SysClock/16
    PWMClockSet(BASE_PWM, PWM_SYSCLK_DIV_16);

    // Configurar el generador PWM para PF1 en PWM_GEN_0, PF2 en PWM_GEN_0 y PF3 en PWM_GEN_1
    PWMGenConfigure(BASE_PWM, PWM_GEN_0, PWM_GEN_MODE_DOWN | PWM_GEN_MODE_NO_SYNC);
    PWMGenConfigure(BASE_PWM, PWM_GEN_1, PWM_GEN_MODE_DOWN | PWM_GEN_MODE_NO_SYNC);

    // Establecer el período para ambos generadores
    duty = 255; // ARR
    PWMGenPeriodSet(BASE_PWM, PWM_GEN_0, duty); // PF1 y PF2
    PWMGenPeriodSet(BASE_PWM, PWM_GEN_1, duty); // PF3

    // Habilitar las salidas PWM en PF1 (M0PWM1), PF2 (M0PWM2) y PF3 (M0PWM3)
    PWMOutputState(BASE_PWM, PWM_OUT_1_BIT | PWM_OUT_2_BIT | PWM_OUT_3_BIT, true);

    // Habilitar los generadores PWM
    PWMGenEnable(BASE_PWM, PWM_GEN_0);
    PWMGenEnable(BASE_PWM, PWM_GEN_1);

    // Establecer el ciclo de trabajo inicial
    PWMPulseWidthSet(BASE_PWM, SALIDA_PWM1, 1);   // PF1
    PWMPulseWidthSet(BASE_PWM, SALIDA_PWM2, 1);   // PF2
    PWMPulseWidthSet(BASE_PWM, SALIDA_PWM3, 1);  // PF3
}
// Configuración del reloj del sistema a 120 MHz
static void configureSysClock(void) {
    ui32SysClock = SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ |
                                       SYSCTL_OSC_MAIN |
                                       SYSCTL_USE_PLL |
                                       SYSCTL_CFG_VCO_480), 120000000);
}