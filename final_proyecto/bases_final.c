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
#define ciclo 150 //100%255
#define ciclo2 178 // aprox el 70%
#define ciclo3 150 // aprox el 70%
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
uint32_t distance,distance2,distance3,distance4;
uint32_t startTime, endTime, duration;
uint32_t startTime2, endTime2, duration2;
uint32_t startTime3, endTime3, duration3;
uint32_t startTime4, endTime4, duration4;
uint32_t estado1,estado2;
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
static void configureUART3(void);     
static void config_timer(void);
static void config_timer1(void);
static void config_timer2(void);
static void config_timer3(void);
static void config_ultrasonico(void);
static void config_pwm(void);    
static void config_motores(void);
static void uartprintf(const char *str);
//---------------------FUNCIONES A UTILIZAR------------------------------------//
void medir_distancia1(void);
//void medir_distancia2(void);
//void medir_distancia3(void);
//void medir_distancia4(void);
//Funciones para manipular las fases de los moviminetos
void fase_1(void);
void fase_2(void);
void obj_detect(void);
//Variables que se utlizaran en las fases del movimineto
bool bandera;
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
    configureUART3();  
    config_timer();
    config_timer1();
    config_timer2();
    config_timer3();
    config_pwm();
    config_ultrasonico();
    config_motores();
    bandera = false;
    estado1 =0;
    estado2 =0;
    while (1) {
        //PWMPulseWidthSet(BASE_PWM, SALIDA_PWM1, 255); // PF1 a 255
        //PWMPulseWidthSet(BASE_PWM, SALIDA_PWM2, 1); // PF2 a 128 (50%)
        //PWMPulseWidthSet(BASE_PWM, SALIDA_PWM3, 128);  // PF3 a 25
        //giro_der();
        //giro_izq();
        
        if (bandera == false){
            fase_1();
        }
        else if(bandera == true){
            fase_2();
        }
        else{
            adelante();
        }

    }
}
// Manejador de interrupciones del Timer2
void Timer3IntHandler(void) {
    TimerIntClear(TIMER3_BASE, TIMER_TIMA_TIMEOUT); 
    estado1 ++;
    if (estado1 >1){
        estado1=0;
    }

}
// Manejador de interrupciones del Timer2
void Timer2IntHandler(void) {
    TimerIntClear(TIMER2_BASE, TIMER_TIMA_TIMEOUT);
    medir_distancia1();
    //medir_distancia2();
    //medir_distancia3();
    //medir_distancia4();
    //UARTprintf("Distancia: %d cm \r\n", (int)distance);
    //UARTprintf("%d cm ", (int)distance2);
    //UARTprintf("%d cm ", (int)distance3);
    //UARTprintf("%d cm\r\n", (int)distance4);
    if((int)distance <=15){
        bandera= true;
        //UARTprintf("ENCENDIDO\r\n");

    }
    else{
        //UARTprintf("APAGADO\r\n");
        bandera= false;
    }
}
// Manejador de interrupciones del Timer1
void Timer1IntHandler(void) {
    TimerIntClear(TIMER1_BASE, TIMER_TIMA_TIMEOUT);
}
// Manejador de interrupciones del Timer0
void Timer0IntHandler(void) {
    TimerIntClear(TIMER0_BASE, TIMER_TIMA_TIMEOUT);
    estado2 ++;
    if (estado2 >2){
        estado2=0;
    }
}
// Manejador de la interrupción de UART3 (cuando se recibe un dato)
void UART3IntHandler(void) {
    uint32_t ui32Status;
    char receivedChar;

    // Obtener y limpiar el estado de la interrupción
    ui32Status = UARTIntStatus(UART3_BASE, true);
    UARTIntClear(UART3_BASE, ui32Status);

    // Procesar los datos mientras haya en el FIFO
    while (UARTCharsAvail(UART3_BASE)) {
        // Leer el carácter recibido
        receivedChar = UARTCharGetNonBlocking(UART3_BASE);

        // Si es un retorno de carro o salto de línea, la frase está completa
        if (receivedChar == '\r' || receivedChar == '\n') {
            uartBuffer[bufferIndex] = '\0';  // Terminar la cadena con el carácter nulo
            //para imprimir en el UART3
            //uartprintf("Datos recibidos UART0: ");
            //uartprintf(uartBuffer);  // Enviar la frase recibida a través del UART3
            //uartprintf("\r\n");
            //para imprimir en el UART0
            UARTprintf("Datos recibidos UART3: ");
            UARTprintf(uartBuffer);  // Enviar la frase recibida a través del UART3
            UARTprintf("\r\n");
            //------------
            bufferIndex = 0;  // Reiniciar el buffer para la siguiente frase
        }
        else {
            if (bufferIndex < MAX_BUFFER_SIZE - 1) {
                uartBuffer[bufferIndex++] = receivedChar;  // Agregar el carácter al buffer
            }
            else {
                UARTprintf("Buffer lleno, frase demasiado larga.\r\n");
                bufferIndex = 0;  // Reiniciar el buffer
            }
        }
        obj_detect();
    }
}
// Manejador de interrupciones de UART0 (cuando se recibe un dato)
void UART0IntHandler(void) {
    uint32_t ui32Status;
    char receivedChar;

    // Obtener y limpiar el estado de la interrupción
    ui32Status = UARTIntStatus(UART0_BASE, true);
    UARTIntClear(UART0_BASE, ui32Status);

    // Procesar los datos mientras haya en el FIFO
    while (UARTCharsAvail(UART0_BASE)) {
        // Leer el carácter recibido
        receivedChar = UARTCharGetNonBlocking(UART0_BASE);

        // Si es un retorno de carro o salto de línea, la frase está completa
        if (receivedChar == '\r' || receivedChar == '\n') {
            uartBuffer[bufferIndex] = '\0';  // Terminar la cadena con el carácter nulo
            //para imprimir en el UART3
            uartprintf("Datos recibidos UART0: ");
            uartprintf(uartBuffer);  // Enviar la frase recibida a través del UART3
            uartprintf("\r\n");
            //--------------------------
            bufferIndex = 0;  // Reiniciar el buffer para la siguiente frase
        }
        else {
            if (bufferIndex < MAX_BUFFER_SIZE - 1) {
                uartBuffer[bufferIndex++] = receivedChar;  // Agregar el carácter al buffer
            }
            else {
                uartprintf("Buffer lleno, frase demasiado larga.\r\n");
                bufferIndex = 0;  // Reiniciar el buffer
            }
        }
        obj_detect();
    }
}
// uartprintf para el uart3 
// Función para enviar una cadena por UART
static void uartprintf(const char *str) {
    while (*str) {
        UARTCharPut(UART3_BASE, *str++);  
    }
}
// funciones de las fases
void obj_detect(void){
    if (strcmp(uartBuffer, "derobj") == 0) {
        UARTprintf("holaa\n");
    }
    else  if (strcmp(uartBuffer, "izqobj") == 0) {
        UARTprintf("adios\n");
    }
}
void fase_1(void){
    if (estado1 == 0){
        adelante();
    }
    else if (estado1 == 1){
        giro_izq();
    }
}
void fase_2(void){
    if (estado2 == 0){
        atras();
    }
    else if (estado2 == 1){
        giro_der();
    }
    else if(estado2 == 2){
        bandera = false;
    }

}
//Funcion para definir los moviminetos
void giro_der(void){
    GPIOPinWrite(MOTORRES_PORT, MOTOR2_DER_PIN, MOTOR2_DER_PIN);
    GPIOPinWrite(MOTORRES_PORT, MOTOR1_IZQ_PIN, MOTOR1_IZQ_PIN);
    GPIOPinWrite(MOTORRES_PORT, MOTOR2_IZQ_PIN, 0X00);
    GPIOPinWrite(MOTORRES_PORT, MOTOR1_DER_PIN, 0X00);
    PWMPulseWidthSet(BASE_PWM, SALIDA_PWM1, ciclo2);
    PWMPulseWidthSet(BASE_PWM, SALIDA_PWM2, ciclo2);
}
void giro_izq(void){
    GPIOPinWrite(MOTORRES_PORT, MOTOR1_DER_PIN, MOTOR1_DER_PIN);
    GPIOPinWrite(MOTORRES_PORT, MOTOR2_IZQ_PIN, MOTOR2_IZQ_PIN);
    GPIOPinWrite(MOTORRES_PORT, MOTOR1_IZQ_PIN, 0X00);
    GPIOPinWrite(MOTORRES_PORT, MOTOR2_DER_PIN, 0X00);
    PWMPulseWidthSet(BASE_PWM, SALIDA_PWM1, ciclo3);
    PWMPulseWidthSet(BASE_PWM, SALIDA_PWM2, ciclo3);
}
void adelante(void){
    GPIOPinWrite(MOTORRES_PORT, MOTOR2_IZQ_PIN, MOTOR2_IZQ_PIN);
    GPIOPinWrite(MOTORRES_PORT, MOTOR1_IZQ_PIN, MOTOR1_IZQ_PIN);
    GPIOPinWrite(MOTORRES_PORT, MOTOR1_DER_PIN, 0X00);
    GPIOPinWrite(MOTORRES_PORT, MOTOR2_DER_PIN, 0X00);
    PWMPulseWidthSet(BASE_PWM, SALIDA_PWM1, ciclo);
    PWMPulseWidthSet(BASE_PWM, SALIDA_PWM2, ciclo);
}
void atras(void){
    GPIOPinWrite(MOTORRES_PORT, MOTOR1_DER_PIN, MOTOR1_DER_PIN);
    GPIOPinWrite(MOTORRES_PORT, MOTOR2_DER_PIN, MOTOR2_DER_PIN);
    GPIOPinWrite(MOTORRES_PORT, MOTOR1_IZQ_PIN, 0X00);
    GPIOPinWrite(MOTORRES_PORT, MOTOR2_IZQ_PIN, 0X00);
    PWMPulseWidthSet(BASE_PWM, SALIDA_PWM1, ciclo);
    PWMPulseWidthSet(BASE_PWM, SALIDA_PWM2, ciclo);
}
void apagado_motores(void){
    GPIOPinWrite(MOTORRES_PORT, MOTOR2_IZQ_PIN, 0x00);
    GPIOPinWrite(MOTORRES_PORT, MOTOR1_IZQ_PIN, 0x00);
    GPIOPinWrite(MOTORRES_PORT, MOTOR1_DER_PIN, 0X00);
    GPIOPinWrite(MOTORRES_PORT, MOTOR2_DER_PIN, 0X00);
    PWMPulseWidthSet(BASE_PWM, SALIDA_PWM1, 0);
    PWMPulseWidthSet(BASE_PWM, SALIDA_PWM2, 0);
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
//void medir_distancia2(void) {
   // GPIOPinWrite(TRIG_PORT, TRIG_PIN2, TRIG_PIN2);
   // SysCtlDelay(400);  
   // GPIOPinWrite(TRIG_PORT, TRIG_PIN2, 0);

   // while (GPIOPinRead(ECHO_PORT, ECHO_PIN2) == 0);
    //startTime2 = TimerValueGet(TIMER1_BASE, TIMER_A);  

   // while (GPIOPinRead(ECHO_PORT, ECHO_PIN2) != 0);
   // endTime2 = TimerValueGet(TIMER1_BASE, TIMER_A);  

   // duration2 = startTime2 - endTime2;  
    //time_us2 = (float)duration2 * 0.00833f;
    //distance2 = time_us2 / 58.0f;
//}//
// Función para medir la distancia con el tercer sensor ultrasónico
/*void medir_distancia3(void) {
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
}*/
// Función para medir la distancia con el tercer sensor ultrasónico
/*void medir_distancia4(void) {
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

}*/
// Configuración del sensor ultrasónico
static void config_ultrasonico(void){
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOL);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOH);
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOL));
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOH));

    GPIOPinTypeGPIOOutput(TRIG_PORT, TRIG_PIN);
    GPIOPinTypeGPIOInput(ECHO_PORT, ECHO_PIN);
    //GPIOPinTypeGPIOOutput(TRIG_PORT, TRIG_PIN2);
    //GPIOPinTypeGPIOInput(ECHO_PORT, ECHO_PIN2);
    //GPIOPinTypeGPIOOutput(TRIG_PORT, TRIG_PIN3);
    //GPIOPinTypeGPIOInput(ECHO_PORT, ECHO_PIN3);
    //GPIOPinTypeGPIOOutput(TRIG_PORT2, TRIG_PIN4);
    //GPIOPinTypeGPIOInput(ECHO_PORT2, ECHO_PIN4);
    GPIOPinWrite(TRIG_PORT, TRIG_PIN, 0x00);
    //GPIOPinWrite(TRIG_PORT, TRIG_PIN2, 0x00);
    //GPIOPinWrite(TRIG_PORT, TRIG_PIN3, 0x00);
    //GPIOPinWrite(TRIG_PORT2, TRIG_PIN4, 0x00);
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
// Configurar UART3
static void configureUART3(void) {
    // Habilitar los periféricos necesarios
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOA);  // Habilitar el reloj para el puerto GPIO A
    SysCtlPeripheralEnable(SYSCTL_PERIPH_UART3);  // Habilitar el reloj para UART3
    
    // Configurar los pines PA4 (RX) y PA5 (TX) para UART3
    GPIOPinConfigure(GPIO_PA4_U3RX);  // Configura PA4 como RX de UART3
    GPIOPinConfigure(GPIO_PA5_U3TX);  // Configura PA5 como TX de UART3
    GPIOPinTypeUART(GPIO_PORTA_BASE, GPIO_PIN_4 | GPIO_PIN_5);  // Configura los pines como UART

    // Configurar UART3: 9600 baudios, 8 bits de datos, sin paridad, 1 bit de parada
    UARTConfigSetExpClk(UART3_BASE, ui32SysClock, BAUDIOS,
                        (UART_CONFIG_WLEN_8 |
                         UART_CONFIG_STOP_ONE |
                         UART_CONFIG_PAR_NONE));

    // Habilitar interrupciones de recepción en UART3
    IntEnable(INT_UART3);  // Habilitar la interrupción en el procesador
    UARTIntEnable(UART3_BASE, UART_INT_RX | UART_INT_RT);  // Habilitar interrupciones RX y de timeout
    UARTStdioConfig(3, BAUDIOS, ui32SysClock);  // Configuración de UART3 para printf
}
// Configuración de UART0
static void configureUART0(void) {
    // Habilitar los periféricos necesarios
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOA);  // Habilitar el reloj para el puerto GPIO A
    SysCtlPeripheralEnable(SYSCTL_PERIPH_UART0);  // Habilitar el reloj para UART0
    
    // Configurar los pines PA0 (RX) y PA1 (TX) para UART0
    GPIOPinConfigure(GPIO_PA0_U0RX);  // Configura PA0 como RX de UART0
    GPIOPinConfigure(GPIO_PA1_U0TX);  // Configura PA1 como TX de UART0
    GPIOPinTypeUART(GPIO_PORTA_BASE, GPIO_PIN_0 | GPIO_PIN_1);  // Configura los pines como UART

    // Configurar UART0: 9600 baudios, 8 bits de datos, sin paridad, 1 bit de parada
    UARTConfigSetExpClk(UART0_BASE, ui32SysClock, BAUDIOS,
                        (UART_CONFIG_WLEN_8 |
                         UART_CONFIG_STOP_ONE |
                         UART_CONFIG_PAR_NONE));

    // Habilitar interrupciones de recepción en UART0
    IntEnable(INT_UART0);  // Habilitar la interrupción en el procesador
    UARTIntEnable(UART0_BASE, UART_INT_RX | UART_INT_RT);  // Habilitar interrupciones RX y de timeout
    IntMasterEnable();     // Habilitar interrupciones globales
        // Inicializar la UART estándar para printf
}
// Configuración del Timer0 para generar interrupciones periódicas
static void config_timer(void) {
    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER0);
    TimerConfigure(TIMER0_BASE, TIMER_CFG_A_PERIODIC | TIMER_CFG_B_ONE_SHOT);
    TimerLoadSet(TIMER0_BASE, TIMER_A, ((ui32SysClock - 1)/3)*5);

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
// Configuración del Timer2 para ejecutar secciones de constantes mediciones
static void config_timer3(void) {
    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER3);
    TimerConfigure(TIMER3_BASE, TIMER_CFG_A_PERIODIC | TIMER_CFG_B_ONE_SHOT);
    TimerLoadSet(TIMER3_BASE, TIMER_A, ((ui32SysClock - 1)/3)*3);

    IntEnable(INT_TIMER3A);
    TimerIntEnable(TIMER3_BASE, TIMER_TIMA_TIMEOUT);
    IntMasterEnable();
    TimerEnable(TIMER3_BASE, TIMER_A);
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