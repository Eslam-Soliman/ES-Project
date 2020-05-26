**Project Description:**

Real-time ECG plotter for AD8232 sensor, using the STM32F103C8T6 microcontroller (black pill)

**Project Features:**

- The ability to collect and plot1 min worth of ECG data

- The ability to set the sampling rate from 4 values (25, 50, 100, 200) Hz, with the possibility of adding new values

- The ability to ask for calculating and displaying the BPM (beats per minute)

**Project Architecture:**

**![](https://lh4.googleusercontent.com/uSem3_r5AdF0mnwaVuIvEHhCco8BdfZKmQjlJfvmsQ1VoYF6gMLpb0FMf_Vaz92Zi_aOO99LV3dznOhWpvNL0KAwtCJOzxacsmzK5PN_V-CrfOXFVGFLrkhn7Tb02UBiWxabyXU2d0k)

The project consists of two main components:

- C++ driver for the MCU and the ECG sensor, its main functionalities:

- Analogs-to-Digital conversion of the sensor output

- Transmitting Digital Data to PC using serial communication (UART)

- Setting sampling rate for the ADC conversion

- Python GUI PC application for plotting transmitted data and convenient user interaction, main application functionalities:

- Receiving and plotting data from the MCU through serial communication

- Transmitting two kinds of commands to the MCU, request to send data, and setting the sampling rate

- Moderating commands issuing synchronization

**Communication Encoding:**

Communication is based on UART with a baud rate of 115200bit/s

MCU-to-PC:

- Data are sent to PC via UART as 2-byte unsigned integers, in the range [0, 4,095], this range represent voltage output in the range [0, 3.3] volt.

PC-to-MCU:

- Commands are sent to the MCU as an 1-byte ASCII characters

&#39;0&#39;: Request to send 1-minute worth of ECG data

&#39;1&#39;: Set the sampling rate to 25Hz

&#39;2&#39;: Set the sampling rate to 50Hz

&#39;4&#39;: Set the sampling rate to 100Hz

&#39;8&#39;: Set the sampling rate to 200Hz

**Decisions / Assumptions:**

- ECG plot shows last 500 ECG readings, the x-axis is not time based.

- As a result of code latency, plot refreshing/updating rate is less than sampling rate, as a result, to display 1-minute worth of data in high sampling rates \&gt;=50, the plot will take more than one minute. Plotting time increases linearly with the chosen sampling rate

- Beats per minutes (BPM) value is calculated using the most recent 1-minute set of data, to be able to calculate and get the bpm, plotting data request has to be issued first.

- All buttons are disabled while receiving ECG data, the user is not able to request new group of data, change the sampling rate, neither request calculating bmp.

- Beats per minute threshold (BPM) is 2300 in digital output, or 1.85V in analog. This limit is chosen based on several runs with testing and observation, while comparing with expected results.

- Available sampling rates are (25, 50, 100, 200). No higher sampling rates are supported as higher frequencies are not popular for regular use ECGs. Also, higher sampling rates will lead to an inconvenience in waiting for \&gt;= 10 minutes to collect results

**MCU Driver Implementation Details (Program Flow):**

- In case MCU is transmitting data, timer interrupt gets fired regularly, parametrized via the sampling rate chosen by the user.

- Timer interrupts triggers ADC start of conversion.

- ADC conversion complete callback function transmits conversion output (non-blocking) to PC via UART.

- MCU continuously listen for PC commands, commands sent from PC are either requests for sending data of requests for changing sampling rate

**Desktop App Implementation Details:**

- Application consists of two main threads:

- Main thread for handling GUI events; user interaction and screen refreshing, checks for data updates, and updates the plot.

- Listening thread that receives data from the MCU and pushes them to updates queue.

- Plot refresh rate depends on run-time performance; data are being displayed in the plot as-soon-as it is possible. As a result, 1 min worth of data could take more than 1 minute to be plotted in the case of high sampling rates

- BPM is calculated on the desktop app side via checking if signal passes certain threshold, in out case it is 1.85V.

**System configuration (MCU):**

- System clock is set to 8MHz

- Timer clock is set to 8MHz

- Timer prescalar is set to 799

- ADC clock is set to 4MHz

- UART baud rate = 115200bits/s

 **CubeMX timer configurations:**

**![](https://lh6.googleusercontent.com/4MyuwPFjYwnINnVG5e7I-mScgv-HTP9sSk3_FdtA7RCLbB0omPvZVox52v-xMC2VRyjVS2IT1lvZ5rAUevEGubIzi3eHY-_1Kj-z-c-cSuIDZtwi3D2FvqzuEptFpRS-85SYzRnIyUw)

**Limitations:**

- Python latency made it impossible for the plot to be refreshed in the same frequency as the sampling rate. As a result, displaying time will be more in 1 minute for high sampling rates. However, 1-minute worth of data is still being transmitted and displayed without any loss.

**Possible Future Increments:**

- Pass the sensor signal through a low-pass filter to eliminate the high frequency noise.

- Transform the x-axis to be time based

- Add compatibility for multiple ports

- Add functionality to change the baud rate

**ECG Plot Screenshots:**

Sampling frequency set to 25 samples per second

![](https://lh4.googleusercontent.com/YSXq26SROKNLnBF1gbO768leBw0jSRXiWPHzflLXIeDeRHsq-U_Rj2W_HVC_ojUn6ww6ZeuKLZ2nct3psF3Qf-dd1vtM4HdhfuFwkxnB-DwufeeCKcKLIrL112TccefY6Y_zLYN9LtY)

Sampling frequency set to 100 samples per second

![](https://lh5.googleusercontent.com/NBrD4R1J4PnHlgEGmtZfjEjZGym3fHgiEvUdBSNrTMtSCwLYpyS7LjDyq9qwRWHp_d4YlpqmKXiJanjBgJQvrKqi5ZnuVCtB4bzJEfDNHkYzIQG0mWqVst1nVYfnfNpIktMYZV1Sw_Q)