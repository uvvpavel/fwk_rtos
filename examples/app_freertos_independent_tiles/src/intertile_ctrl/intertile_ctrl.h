// Copyright (c) 2020, XMOS Ltd, All rights reserved

#ifndef INTERTILE_CTRL_H_
#define INTERTILE_CTRL_H_

void intertile_ctrl_create_t0( UBaseType_t uxPriority );
void intertile_ctrl_create_t1( UBaseType_t uxPriority );

#include "intertile_driver.h"
INTERTILE_ISR_CALLBACK_FUNCTION_PROTO( intertile_dev_test0, device, buf, len, xReturnBufferToDMA );
INTERTILE_ISR_CALLBACK_FUNCTION_PROTO( intertile_dev_test1, device, buf, len, xReturnBufferToDMA );

void t0_test(void *arg);
void t1_test(void *arg);


#include "message_buffer.h"
#include "queue.h"
#include "soc.h"

typedef struct {
    MessageBufferHandle_t send_msg_buf;
    MessageBufferHandle_t recv_msg_buf;
    QueueHandle_t eventQueue;
    QueueHandle_t respQueue;
} intertile_msg_buffers_t;

int add(int a, int b);


#endif /* INTERTILE_CTRL_H_ */
