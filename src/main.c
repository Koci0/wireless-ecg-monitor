#include <stdlib.h>
#include <signal.h>
#include <stdio.h>

#include "ADS1263.h"

// External AVDD and AVSS(Default), or internal 2.5V
#define REF 5.08

void exit_handler(int signo) {
    printf("\nExit with signo: %d\n", signo);
    DEV_Module_Exit();
    exit(0);
}

int main() {
    UWORD i;
    unsigned int result;

    signal(SIGINT, exit_handler);

    printf("Dev module init...\n");
    result = DEV_Module_Init();
    if (result == 1) {
        printf("Dev module init failed!\n");
        exit(1);
    }
    printf("Dev module init finished.\n");

    // 0 is singleChannel, 1 is diffChannel
    ADS1263_SetMode(0);

    // The faster the rate, the worse the stability
    // and the need to choose a suitable digital filter(REG_MODE1)
    printf("ADS1263 init ADC1...\n");
    result = ADS1263_init_ADC1(ADS1263_400SPS);
    if (result == 1) {
        printf("ADS1263 init ADC1 failed!\n");
        DEV_Module_Exit();
        exit(1);
    }
    printf("ADS1263 init ADC1 finished.\n");

#define channel_number 10
    UBYTE channel_list[channel_number] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};

    UDOUBLE value[channel_number] = {0};
    while (1) {
        ADS1263_GetAll(channel_list, value, channel_number);
        for (i = 0; i < channel_number; i++) {
            if ((value[i] >> 31) == 1) {
                printf("IN%d is -%lf \r\n", channel_list[i], REF * 2 - value[i] / 2147483648.0 * REF);
            } else {
                printf("IN%d is %lf \r\n", channel_list[i], value[i] / 2147483647.0 * REF);
            }
            fflush(stdout);
        }
        for (i = 0; i < channel_number; i++) {
            printf("\33[1A");   // Move the cursor up
        }
        fflush(stdout);
    }

    return 0;
}
