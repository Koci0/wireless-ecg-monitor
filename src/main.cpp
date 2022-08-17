
#include "ADS1263.h"

#include <stdio.h>
#include <iostream>
#include <chrono>
#include <signal.h>

const auto REF = 5.08;



void sigintHandler(int signal_number)
{
    std::cout << "\r\n END \r\n" << std::endl;
    DEV_Module_Exit();
    exit(0);
}

int main(int argc, char *argv[])
{
    using namespace std::literals;

    signal(SIGINT, sigintHandler);

    std::cout << "ADS1263 Demo" << std::endl;
    DEV_Module_Init();

    ADS1263_SetMode(0);
    if (ADS1263_init_ADC1(ADS1263_38400SPS) == 1)
    {
        std::cout << "END" << std::endl;
        DEV_Module_Exit();
        exit(0);
    }

    uint32_t ADC[10];
    while (true)
    {
        auto start_time = std::chrono::high_resolution_clock::now();
        ADS1263_GetAll(ADC); // Get ADC1 value
        for (auto i = 0; i < 10; i++)
        {
            if ((ADC[i] >> 31) == 1)
                std::cout << "IN" << i << " is -" << (REF * 2 - ADC[i] / 2147483648.0 * REF) << std::endl;
            else
                std::cout << "IN" << i << "is " << (ADC[i] / 2147483647.0 * REF) << std::endl;
        }
        auto duration = std::chrono::high_resolution_clock::now() - start_time;
        std::cout << "Done in " << std::chrono::duration_cast<std::chrono::microseconds>(duration).count() << "us" << std::endl;
        printf("\33[11A"); // Move the cursor up
    }

    return 0;
}
